pipeline {
    agent any

    environment {
        GITHUB_TOKEN = credentials('github-token')
        GITHUB_REPO = 'qillbel/scrap1_q-wmo'
        PR_ID = '' // will be passed as parameter or parsed from webhook payload
        BASE_BRANCH = 'main'
        BRANCH_NAME = '' // PR branch name, must be passed in or detected
    }

    parameters {
        string(name: 'PR_ID', defaultValue: '', description: 'GitHub PR Number')
        string(name: 'BRANCH_NAME', defaultValue: '', description: 'PR branch name (e.g., qillbel-patch-1)')
    }

    stages {
        stage('Checkout & Merge') {
            steps {
                script {
                    sh """
                    git config --global user.email "jenkins@dummy.com"
                    git config --global user.name "jenkins bot"
                    git remote set-url origin https://github.com/${GITHUB_REPO}.git

                    git fetch origin ${BASE_BRANCH}
                    git fetch origin ${BRANCH_NAME}

                    git checkout -b merged-branch origin/${BASE_BRANCH}
                    git merge origin/${BRANCH_NAME} --no-edit

                    COMMIT_SHA=\$(git rev-parse HEAD)
                    echo "COMMIT_SHA=\$COMMIT_SHA" > env.properties
                    """
                }
            }
        }

        stage('Load Commit SHA') {
            steps {
                script {
                    def props = readProperties file: 'env.properties'
                    env.COMMIT_SHA = props.COMMIT_SHA
                }
            }
        }

        stage('Build and Test') {
            steps {
                sh 'npm install'
                sh 'npm run lint || true'
                sh 'npm run test:unit'
                sh 'npm run test:integration'
            }
        }
    }

    post {
        success {
            script {
                sh """
                curl -s -X POST -H "Authorization: token ${GITHUB_TOKEN}" -H "Content-Type: application/json" \\
                    -d '{"state":"success","context":"continuous-integration/jenkins/pr-merge","description":"Merged build passed","target_url":"${env.BUILD_URL}"}' \\
                    https://api.github.com/repos/${GITHUB_REPO}/statuses/${COMMIT_SHA}
                """
            }
        }
        failure {
            script {
                sh """
                curl -s -X POST -H "Authorization: token ${GITHUB_TOKEN}" -H "Content-Type: application/json" \\
                    -d '{"state":"failure","context":"continuous-integration/jenkins/pr-merge","description":"Merged build failed","target_url":"${env.BUILD_URL}"}' \\
                    https://api.github.com/repos/${GITHUB_REPO}/statuses/${COMMIT_SHA}
                """
            }
        }
    }
}
