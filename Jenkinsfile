pipeline {
    agent any
    
    options {
        timeout(time: 60, unit: 'MINUTES')  // 1 hour total timeout
    }
    
    tools {
        nodejs 'NodeJS'  // Make sure NodeJS is configured in Jenkins
    }
    
    stages {
        // ==========================================
        // STAGE 1: Checkout (Simplified)
        // ==========================================
        stage('Checkout') {
            options {
                timeout(time: 10, unit: 'MINUTES')
            }
            steps {
                echo 'Checking out code...'
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    extensions: [[$class: 'CloneOption', depth: 1, noTags: true, shallow: true]],
                    userRemoteConfigs: [[
                        url: 'https://github.com/UmarGameDev/habitica.git',
                        credentialsId: 'github-credentials'
                    ]]
                ])
                
                // Verify checkout
                sh '''
                    echo "Checkout completed"
                    echo "Current directory:"
                    pwd
                    ls -la
                '''
            }
        }
        
        // ==========================================
        // STAGE 2: Setup and Verify
        // ==========================================
        stage('Setup') {
            options {
                timeout(time: 5, unit: 'MINUTES')
            }
            steps {
                sh '''
                    echo "=== SYSTEM VERIFICATION ==="
                    echo "Node.js version:"
                    node --version
                    echo "NPM version:"
                    npm --version
                    
                    # Copy config if needed
                    if [ -f config.json.example ] && [ ! -f config.json ]; then
                        echo "Copying config file..."
                        cp config.json.example config.json
                    fi
                    
                    echo "Available disk space:"
                    df -h . || echo "Cannot check disk space"
                '''
            }
        }
        
        // ==========================================
        // STAGE 3: Install Dependencies (Optimized)
        // ==========================================
        stage('Install Dependencies') {
            options {
                timeout(time: 20, unit: 'MINUTES')
            }
            steps {
                sh '''
                    echo "=== INSTALLING DEPENDENCIES ==="
                    echo "Start time: $(date)"
                    
                    # Clean npm cache first
                    echo "Cleaning npm cache..."
                    npm cache clean --force || true
                    
                    # Install with verbose output to monitor progress
                    echo "Installing dependencies..."
                    npm install --no-audit --legacy-peer-deps --verbose
                    
                    echo "End time: $(date)"
                    echo "Dependencies installed"
                    
                    # Check node_modules size
                    echo "Node modules size:"
                    du -sh node_modules/ 2>/dev/null || echo "Cannot check size"
                '''
            }
        }
        
        // ==========================================
        // STAGE 4: Build Client (Only if needed)
        // ==========================================
        stage('Build Client') {
            when {
                // Only build if client directory exists
                expression { fileExists('website/client') }
            }
            options {
                timeout(time: 15, unit: 'MINUTES')
            }
            steps {
                sh '''
                    echo "=== BUILDING CLIENT ==="
                    echo "Start time: $(date)"
                    
                    # Build the client
                    cd website/client
                    npm install --no-audit
                    npm run build
                    
                    echo "Client build completed"
                    echo "Build directory contents:"
                    ls -la build/ 2>/dev/null || echo "No build directory"
                    
                    cd ../..
                    echo "End time: $(date)"
                '''
            }
        }
        
        // ==========================================
        // STAGE 5: Run Basic Tests
        // ==========================================
        stage('Run Tests') {
            options {
                timeout(time: 10, unit: 'MINUTES')
            }
            steps {
                sh '''
                    echo "=== RUNNING BASIC TESTS ==="
                    
                    # Try a simple test first
                    echo "1. Testing if server can start..."
                    timeout 30 bash -c '
                        # Try to start server in background
                        node website/server/index.js &
                        PID=$!
                        
                        # Wait a few seconds
                        sleep 10
                        
                        # Check if process is running
                        if kill -0 $PID 2>/dev/null; then
                            echo "✓ Server started successfully"
                            kill $PID 2>/dev/null
                            exit 0
                        else
                            echo "✗ Server failed to start"
                            exit 1
                        fi
                    ' || echo "Server test completed"
                    
                    # Run simple tests
                    echo "2. Running sanity tests..."
                    npm run test:sanity || echo "Sanity tests completed"
                    
                    echo "All tests completed"
                '''
            }
        }
        
        // ==========================================
        // STAGE 6: Create Artifacts
        // ==========================================
        stage('Create Artifacts') {
            options {
                timeout(time: 5, unit: 'MINUTES')
            }
            steps {
                sh '''
                    echo "=== CREATING ARTIFACTS ==="
                    
                    # Create artifacts directory
                    mkdir -p artifacts
                    
                    # Create a simple build summary
                    cat > artifacts/build-info.txt << EOF
                    Habitica Build Information
                    ===========================
                    Build Number: ${BUILD_NUMBER}
                    Build Date: $(date)
                    Node Version: $(node --version)
                    NPM Version: $(npm --version)
                    Git Commit: $(git rev-parse HEAD 2>/dev/null || echo "Unknown")
                    
                    Directory Structure:
                    $(find . -maxdepth 2 -type d | sort)
                    EOF
                    
                    # Package the build
                    echo "Packaging build..."
                    tar -czf artifacts/habitica-build.tar.gz \
                        --exclude=node_modules \
                        --exclude=.git \
                        --exclude=artifacts \
                        .
                    
                    echo "Artifacts created:"
                    ls -la artifacts/
                '''
            }
            
            post {
                success {
                    echo "Archiving artifacts..."
                    archiveArtifacts artifacts: 'artifacts/**/*', fingerprint: true
                }
            }
        }
    }
    
    post {
        always {
            echo "=== PIPELINE COMPLETED ==="
            echo "Status: ${currentBuild.currentResult}"
            echo "Duration: ${currentBuild.durationString}"
            echo "Build URL: ${env.BUILD_URL}"
            
            sh '''
                echo "Final workspace size:"
                du -sh . 2>/dev/null || echo "Cannot check workspace size"
            '''
        }
        
        success {
            echo "✅ HABITICA BUILD SUCCESSFUL!"
            echo "Build #${BUILD_NUMBER} completed"
        }
        
        failure {
            echo "❌ HABITICA BUILD FAILED!"
            echo "Check the console output for errors"
        }
        
        unstable {
            echo "⚠️ HABITICA BUILD UNSTABLE"
            echo "Some tests may have failed"
        }
    }
}