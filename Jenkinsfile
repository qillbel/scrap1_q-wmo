pipeline {
    agent any

    environment {
        GITHUB_TOKEN = credentials('github-token') // Ensure this exists in Jenkins Credentials
        GITHUB_REPO = 'qillbel/scrap1_q-wmo'
        PR_ID = '11' // Replace or dynamically assign if needed
        BASE_BRANCH = 'main'
    }

    stages {
        stage('Prepare Merged Commit') {
            steps {
                sh '''
                    git config --global user.email "jenkins@dummy.com"
                    git config --global user.name "jenkins bot"
                    git remote set-url origin https://github.com/${GITHUB_REPO}.git

                    git fetch origin ${BASE_BRANCH}
                    git fetch origin pull/${PR_ID}/merge:pr-${PR_ID}-merge
                    git checkout pr-${PR_ID}-merge

                    COMMIT_SHA=$(git rev-parse HEAD)
                    echo "COMMIT_SHA=${COMMIT_SHA}" > env.properties
                '''
            }
        }

        stage('Load SHA') {
            steps {
                script {
                    def props = readProperties file: 'env.properties'
                    env.COMMIT_SHA = props.COMMIT_SHA
                }
            }
        }

        stage('Build & Test') {
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
                def statusPayload = """
                {
                  "state": "success",
                  "context": "continuous-integration/jenkins/pr-merge",
                  "description": "Merged build passed",
                  "target_url": "${env.BUILD_URL}"
                }
                """

                sh """#!/bin/bash
                curl -s -X POST \
                  -H "Authorization: token ${GITHUB_TOKEN}" \
                  -H "Content-Type: application/json" \
                  -d '${statusPayload}' \
                  https://api.github.com/repos/${GITHUB_REPO}/statuses/${COMMIT_SHA}
                """
            }
        }

        failure {
            script {
                def statusPayload = """
                {
                  "state": "failure",
                  "context": "continuous-integration/jenkins/pr-merge",
                  "description": "Merged build failed",
                  "target_url": "${env.BUILD_URL}"
                }
                """

                sh """#!/bin/bash
                curl -s -X POST \
                  -H "Authorization: token ${GITHUB_TOKEN}" \
                  -H "Content-Type: application/json" \
                  -d '${statusPayload}' \
                  https://api.github.com/repos/${GITHUB_REPO}/statuses/${COMMIT_SHA}
                """
            }
        }
    }
}
