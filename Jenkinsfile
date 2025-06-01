pipeline {
    agent any

    environment {
        BRANCH_NAME = "${env.BRANCH_NAME}"
    }

    stages {
        stage('Checkout Merged PR') {
            when {
                expression { return env.CHANGE_ID != null }
            }
            steps {
                script {
                    echo "Checking out and merging PR #${env.CHANGE_ID} into target branch ${env.CHANGE_TARGET}"
                    sh '''
                        git fetch origin ${CHANGE_TARGET}
                        git fetch origin pull/${CHANGE_ID}/head:pr-${CHANGE_ID}
                        git checkout -b merge-${CHANGE_ID} origin/${CHANGE_TARGET}
                        git merge pr-${CHANGE_ID}
                        ls -lah
                        cat package.json || echo "No package.json found"
                    '''
                }
            }
        }

        stage('Checkout Branch') {
            when {
                expression { return env.CHANGE_ID == null }
            }
            steps {
                checkout scm
                sh 'ls -lah'
                sh 'cat package.json || echo "No package.json found"'
            }
        }

        stage('Build') {
            steps {
                echo "Running build on branch: ${env.BRANCH_NAME}"
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