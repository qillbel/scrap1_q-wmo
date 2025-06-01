pipeline {
    agent any

    environment {
        BRANCH_NAME = "${env.BRANCH_NAME}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
				sh 'ls -lah'
				sh 'cat package.json || echo "No package.json found"'
            }
        }

        stage('Build') {
            steps {
                echo "Running build on branch: ${env.BRANCH_NAME}"
                // Example: Install dependencies
                sh 'npm install'
            }
        }

        stage('Lint') {
            steps {
                echo 'Running linter...'
                sh 'npm run lint || true' // Don’t fail build on lint
            }
        }

        stage('Unit Tests') {
            steps {
                echo 'Running unit tests...'
                sh 'npm run test:unit'
            }
        }

        stage('Integration Tests') {
            steps {
                echo 'Running integration tests...'
                sh 'npm run test:integration'
            }
        }
    }

    post {
        success {
            echo "✅ CI Pipeline passed"
        }
        failure {
            echo "❌ CI Pipeline failed"
        }
    }
}
