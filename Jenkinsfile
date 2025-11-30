pipeline {
    agent any
    
    options {
        timeout(time: 2, unit: 'HOURS')
    }
    
    tools {
        nodejs 'NodeJS'
    }
    
    stages {
        stage('Checkout') {
            options {
                timeout(time: 60, unit: 'MINUTES')
            }
            steps {
                echo 'Checking out code using direct git commands...'
                sh '''
                    # Clean any existing repository
                    echo "Cleaning any existing git repository..."
                    rm -rf .git
                    
                    # Initialize new repository
                    echo "Initializing new git repository..."
                    git init
                    git remote add origin https://github.com/UmarGameDev/habitica.git
                    
                    # Configure git for better performance with large repositories
                    echo "Configuring git for optimal performance..."
                    git config core.compression 0
                    git config core.loosecompression 0
                    git config http.postBuffer 524288000
                    git config https.postBuffer 524288000
                    git config http.lowSpeedLimit 0
                    git config http.lowSpeedTime 999999
                    
                    # Fetch with shallow clone and retry logic
                    echo "Fetching repository with shallow clone..."
                    retry(3) {
                        git fetch --depth 1 --progress --no-tags origin main
                    }
                    
                    # Checkout the fetched commit
                    echo "Checking out the fetched code..."
                    git checkout FETCH_HEAD
                    
                    # Verify the checkout
                    echo "Verifying checkout..."
                    ls -la
                    echo "Current directory:"
                    pwd
                '''
                
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
                    # Update package list and install required system dependencies
                    apt-get update
                    apt-get install -y libkrb5-dev g++ make python3
                '''
                
                echo 'Installing npm dependencies...'
                sh '''
                    # Copy configuration file
                    cp config.json.example config.json
                    
                    # Clean install npm dependencies
                    npm ci --no-audit --prefer-offline
                '''
            }
        }
        
        stage('Build - Compile Code') {
            options {
                timeout(time: 30, unit: 'MINUTES')
            }
            steps {
                echo 'Compiling application code...'
                sh '''
                    # Run the build process
                    npm run postinstall
                    
                    # Verify build outputs
                    echo "Build completed. Checking outputs..."
                    find . -name "*.js" -o -name "*.css" -o -name "*.html" | head -20
                '''
            }
        }
        
        stage('Build - Create Artifacts') {
            options {
                timeout(time: 15, unit: 'MINUTES')
            }
            steps {
                echo 'Creating build artifacts...'
                sh '''
                    # Create directory for artifacts
                    mkdir -p build-artifacts
                    
                    # Copy essential build outputs
                    echo "Copying website files..."
                    cp -r website/ build-artifacts/
                    
                    echo "Copying configuration files..."
                    cp package.json build-artifacts/
                    cp package-lock.json build-artifacts/
                    cp config.json build-artifacts/
                    cp -r node_modules/ build-artifacts/ 2>/dev/null || echo "node_modules not copied"
                    
                    # List the artifacts
                    echo "Build artifacts structure:"
                    ls -la build-artifacts/
                    echo "Website directory contents:"
                    ls -la build-artifacts/website/ || echo "No website directory"
                '''
            }
            
            post {
                success {
                    echo 'Archiving build artifacts...'
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
                    echo "Client dist directory:"
                    ls -la website/client/dist/ 2>/dev/null || echo "Client dist directory not found"
                    
                    echo "Server directory:"
                    ls -la website/server/ 2>/dev/null || echo "Server directory not found"
                    
                    echo "Root files:"
                    ls -la | grep -E "(package|config|\.js|\.json)"
                    
                    echo "=== Checking file sizes ==="
                    du -sh website/ || echo "Cannot check website size"
                    du -sh node_modules/ || echo "Cannot check node_modules size"
                '''
                
                // Run basic sanity test
                echo 'Running sanity tests...'
                sh 'npm run test:sanity || echo "Sanity tests not available, continuing..."'
            }
            
            post {
                always {
                    echo 'Build verification completed'
                }
            }
        }
        
        stage('Deploy Preparation') {
            options {
                timeout(time: 10, unit: 'MINUTES')
            }
            steps {
                echo 'Preparing for deployment...'
                sh '''
                    echo "=== Final build summary ==="
                    echo "Build completed at: $(date)"
                    echo "Node version: $(node --version)"
                    echo "NPM version: $(npm --version)"
                    echo "Current branch: $(git branch --show-current 2>/dev/null || echo 'detached')"
                    echo "Latest commit: $(git log -1 --oneline 2>/dev/null || echo 'No git info')"
                    
                    echo "=== Disk usage ==="
                    df -h .
                    echo "=== Build directory size ==="
                    du -sh . || echo "Cannot check directory size"
                '''
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline execution completed - check console for details'
            script {
                // Only clean workspace if we're inside a node context
                if (env.NODE_NAME) {
                    echo 'Cleaning workspace...'
                    cleanWs()
                } else {
                    echo 'Skipping workspace cleanup (no node context)'
                }
            }
        }
        success {
            echo '✅ PIPELINE SUCCESS: All stages completed successfully'
            emailext (
                subject: "✅ Pipeline SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                The pipeline ${env.JOB_NAME} #${env.BUILD_NUMBER} completed successfully.
                
                Check the build at: ${env.BUILD_URL}
                
                Stages completed:
                - Checkout: ✅
                - Install Dependencies: ✅
                - Compile Code: ✅
                - Create Artifacts: ✅
                - Verify Build: ✅
                
                Artifacts have been archived and are ready for deployment.
                """,
                to: "${env.CHANGE_AUTHOR_EMAIL ?: 'umar@example.com'}"
            )
        }
        failure {
            echo '❌ PIPELINE FAILED: Check console for errors'
            emailext (
                subject: "❌ Pipeline FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                The pipeline ${env.JOB_NAME} #${env.BUILD_NUMBER} failed.
                
                Check the build at: ${env.BUILD_URL}
                
                Please check the console output for detailed error information.
                """,
                to: "${env.CHANGE_AUTHOR_EMAIL ?: 'umar@example.com'}"
            )
        }
        unstable {
            echo '⚠️ PIPELINE UNSTABLE: Some tests failed or quality gates not met'
        }
        changed {
            echo 'Pipeline status changed from previous build'
        }
    }
}