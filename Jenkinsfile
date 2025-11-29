pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub with shallow clone...'
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    extensions: [
                        [$class: 'CloneOption', 
                         depth: 1, 
                         shallow: true,
                         timeout: 60]
                    ],
                    userRemoteConfigs: [[url: 'https://github.com/UmarGameDev/habitica.git']]
                ])
            }
        }
        
        stage('Setup') {
            steps {
                echo 'Setting up environment...'
                sh 'cp config.json.example config.json'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing npm dependencies...'
                sh 'npm install'
            }
        }
        
        stage('Lint') {
            steps {
                echo 'Running linting...'
                sh 'npm run lint-no-fix'
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed - check console for details'
        }
    }
}