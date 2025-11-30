pipeline {
    agent any
    
    options {
        timeout(time: 2, unit: 'HOURS')   // Increased overall timeout
    }
    
    tools {
        nodejs 'NodeJS'
    }
    
    stages {
        stage('Checkout') {
            options {
                timeout(time: 60, unit: 'MINUTES')   // Increased to 60 minutes for checkout
            }
            steps {
                echo 'Checking out code with optimized shallow clone...'
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    extensions: [
                        [$class: 'CloneOption', 
                         depth: 1, 
                         shallow: true,
                         noTags: true,
                         honorRefspec: true,
                         timeout: 60],  // Increased timeout to 60 minutes
                        [$class: 'DisableRemotePoll']  // Disable remote polling to speed up
                    ],
                    userRemoteConfigs: [[
                        url: 'https://github.com/UmarGameDev/habitica.git',
                        credentialsId: '',
                        timeout: 60  // Increased timeout for remote operations
                    ]]
                ])
                
                // Verify Node.js is available
                sh 'node --version'
                sh 'npm --version'
            }
        }
        
        stage('Build - Install Dependencies') {
            options {
                timeout(time: 30, unit: 'MINUTES')
            }
            steps {
                echo 'Installing system dependencies...'
                sh '''
                    apt-get update
                    apt-get install -y libkrb5-dev
                '''
                
                echo 'Installing npm dependencies...'
                sh 'cp config.json.example config.json'
                sh 'npm ci'
            }
        }
        
        stage('Build - Compile Code') {
            options {
                timeout(time: 30, unit: 'MINUTES')
            }
            steps {
                echo 'Compiling application code...'
                sh 'npm run postinstall'  // This runs gulp build and client build
            }
        }
        
        stage('Build - Create Artifacts') {
            options {
                timeout(time: 15, unit: 'MINUTES')
            }
            steps {
                echo 'Creating build artifacts...'
                
                // Create directory for artifacts
                sh 'mkdir -p build-artifacts'
                
                // Archive build outputs
                sh '''
                    cp -r website/ build-artifacts/
                    cp package.json build-artifacts/
                    cp package-lock.json build-artifacts/
                    cp config.json build-artifacts/
                    ls -la build-artifacts/
                '''
            }
            
            post {
                success {
                    // Archive the build artifacts in Jenkins
                    archiveArtifacts artifacts: 'build-artifacts/**/*', fingerprint: true
                    echo 'Build artifacts archived successfully'
                }
            }
        }
        
        stage('Build - Verify') {
            options {
                timeout(time: 10, unit: 'MINUTES')
            }
            steps {
                echo 'Verifying build output...'
                sh '''
                    echo "=== Checking build outputs ==="
                    ls -la website/client/dist/ || echo "Client dist directory"
                    ls -la website/server/ || echo "Server directory"
                '''
                
                // Run basic sanity test
                sh 'npm run test:sanity'
            }
        }
    }
    
    post {
        always {
            echo 'Build Stage completed - check console for details'
            script {
                // Only clean workspace if we're inside a node context
                if (env.NODE_NAME) {
                    cleanWs()
                }
            }
        }
        success {
            echo '✅ BUILD STAGE SUCCESS: Code compiled and artifacts created'
        }
        failure {
            echo '❌ BUILD STAGE FAILED: Check console for errors'
        }
    }
}