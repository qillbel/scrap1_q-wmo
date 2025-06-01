pipeline {
    agent any

    environment {
        BASE_BRANCH = "main"
        GITHUB_REPO = "qillbel/scrap1_q-wmo"
        GITHUB_API = "https://api.github.com"
        COMMIT_SHA = "" // will be set dynamically
    }

    stages {
        stage('Prepare Merge') {
            steps {
                echo "Fetching PR branch and base branch to test merge"
                sh '''
                    git config --global user.email "jenkins@dummy.com"
                    git config --global user.name "jenkins bot"

                    git remote set-url origin https://github.com/${GITHUB_REPO}.git
                    git fetch origin

                    git fetch origin ${BASE_BRANCH}
                    git fetch origin ${BRANCH_NAME}

                    git checkout -b test-merge origin/${BASE_BRANCH}
                    git merge origin/${BRANCH_NAME} --no-edit

                    export COMMIT_SHA=$(git rev-parse HEAD)
                    echo "COMMIT_SHA=${COMMIT_SHA}" >> env.properties
                '''
                script {
                    def props = readProperties file: 'env.properties'
                    env.COMMIT_SHA = props.COMMIT_SHA
                }
            }
        }

        stage('Build') {
            steps {
                echo "Building..."
                sh 'npm install'
            }
        }

        stage('Lint') {
            steps {
                sh 'npm run lint || true'
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'npm run test:unit'
            }
        }

        stage('Integration Tests') {
            steps {
                sh 'npm run test:integration'
            }
        }
    }

    post {
        success {
            echo "✅ CI passed on merged result"
            withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'TOKEN')]) {
                sh '''
                    curl -s -X POST -H "Authorization: token $TOKEN" \
                    -H "Content-Type: application/json" \
                    -d '{
                        "state": "success",
                        "context": "continuous-integration/jenkins/pr-merge",
                        "description": "Build succeeded",
                        "target_url": "'"$BUILD_URL"'"
                    }' \
                    ${GITHUB_API}/repos/${GITHUB_REPO}/statuses/${COMMIT_SHA}
                '''
            }
        }

        failure {
            echo "❌ CI failed on merged result"
            withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'TOKEN')]) {
                sh '''
                    curl -s -X POST -H "Authorization: token $TOKEN" \
                    -H "Content-Type: application/json" \
                    -d '{
                        "state": "failure",
                        "context": "continuous-integration/jenkins/pr-merge",
                        "description": "Build failed",
                        "target_url": "'"$BUILD_URL"'"
                    }' \
                    ${GITHUB_API}/repos/${GITHUB_REPO}/statuses/${COMMIT_SHA}
                '''
            }
        }
    }
}
