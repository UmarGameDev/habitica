pipeline {
    agent any
    
    options {
        timeout(time: 1, unit: 'HOURS')   // Timeout on whole pipeline job
    }
    
    tools {
        nodejs 'node21'  // Configure Node.js in Jenkins
    }
    
    stages {
        stage('Checkout') {
            options {
                timeout(time: 30, unit: 'MINUTES')   // Timeout on checkout stage
            }
            steps {
                echo 'Checking out code with shallow clone...'
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    extensions: [
                        [$class: 'CloneOption', 
                         depth: 1, 
                         shallow: true,
                         noTags: true,
                         timeout: 30]
                    ],
                    userRemoteConfigs: [[
                        url: 'https://github.com/UmarGameDev/habitica.git',
                        credentialsId: ''
                    ]]
                ])
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
            // Clean up workspace to save disk space
            cleanWs()
        }
        success {
            echo '✅ BUILD STAGE SUCCESS: Code compiled and artifacts created'
        }
        failure {
            echo '❌ BUILD STAGE FAILED: Check console for errors'
        }
    }
}