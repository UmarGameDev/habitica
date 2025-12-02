pipeline {
    agent any
    
    stages {
        stage('Diagnose Git') {
            steps {
                bat '''
                    echo "=== GIT DIAGNOSIS ==="
                    echo "Trying to find git.exe..."
                    
                    echo "1. Checking PATH..."
                    where git.exe
                    
                    echo "2. Common locations:"
                    dir "C:\\Program Files\\Git\\bin\\git.exe" 2>nul || echo "Not in Program Files"
                    dir "C:\\Program Files (x86)\\Git\\bin\\git.exe" 2>nul || echo "Not in Program Files (x86)"
                    dir "C:\\Git\\bin\\git.exe" 2>nul || echo "Not in C:\\Git"
                    
                    echo "3. Trying to run git..."
                    git --version 2>nul && echo "Git works!" || echo "Git command failed"
                    
                    echo "=== END DIAGNOSIS ==="
                '''
            }
        }
    }
}