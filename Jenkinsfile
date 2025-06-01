pipeline {
    agent any

    environment {
        GITHUB_TOKEN = credentials('github-token')
        GITHUB_REPO = 'qillbel/scrap1_q-wmo'
        PR_ID = '11'  // or inject dynamically
        BASE_BRANCH = 'main'
    }

    stages {
        stage('Prepare merged commit') {
            steps {
                sh '''
                  git config --global user.email "jenkins@dummy.com"
                  git config --global user.name "jenkins bot"
                  git remote set-url origin https://github.com/${GITHUB_REPO}.git

                  git fetch origin pull/${PR_ID}/merge:pr-${PR_ID}-merge
                  git checkout pr-${PR_ID}-merge

                  COMMIT_SHA=$(git rev-parse HEAD)
                  echo "COMMIT_SHA=${COMMIT_SHA}" > env.properties
                '''
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
                curl -s -X POST -H "Authorization: token ${GITHUB_TOKEN}" -H "Content-Type: application/json" \
                    -d '{"state":"success","context":"continuous-integration/jenkins/pr-merge","description":"Merged build passed","target_url":"${env.BUILD_URL}"}' \
                    https://api.github.com/repos/${GITHUB_REPO}/statuses/${COMMIT_SHA}
                """
            }
        }
        failure {
            script {
                sh """
                curl -s -X POST -H "Authorization: token ${GITHUB_TOKEN}" -H "Content-Type: application/json" \
                    -d '{"state":"failure","context":"continuous-integration/jenkins/pr-merge","description":"Merged build failed","target_url":"${env.BUILD_URL}"}' \
                    https://api.github.com/repos/${GITHUB_REPO}/statuses/${COMMIT_SHA}
                """
            }
        }
    }
}
