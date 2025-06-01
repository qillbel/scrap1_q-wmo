pipeline {
    agent any

    environment {
        GITHUB_TOKEN = credentials('jenkins-ci-token')
        GITHUB_REPO = 'qillbel/scrap1_q-wmo'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.COMMIT_SHA = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                    echo "Commit SHA: ${env.COMMIT_SHA}"
                }
            }
        }

        stage('Lint and Test') {
            steps {
                sh 'npm install'
                sh 'npm run lint'
                sh 'npm test'
            }
        }
    }

    post {
        success {
            script {
                if (env.GITHUB_TOKEN && env.GITHUB_REPO && env.COMMIT_SHA) {
                    def statusJson = """
                    {
                      "state": "success",
                      "context": "continuous-integration/jenkins/pr-merge",
                      "description": "Build succeeded",
                      "target_url": "${env.BUILD_URL}"
                    }
                    """
                    sh """
                    curl -s -X POST -H "Authorization: token ${env.GITHUB_TOKEN}" \\
                         -d '${statusJson}' \\
                         https://api.github.com/repos/${env.GITHUB_REPO}/statuses/${env.COMMIT_SHA}
                    """
                } else {
                    echo "Missing GITHUB_TOKEN, GITHUB_REPO or COMMIT_SHA, skipping status update"
                }
            }
        }
        failure {
            script {
                if (env.GITHUB_TOKEN && env.GITHUB_REPO && env.COMMIT_SHA) {
                    def statusJson = """
                    {
                      "state": "failure",
                      "context": "continuous-integration/jenkins/pr-merge",
                      "description": "Build failed",
                      "target_url": "${env.BUILD_URL}"
                    }
                    """
                    sh """
                    curl -s -X POST -H "Authorization: token ${env.GITHUB_TOKEN}" \\
                         -d '${statusJson}' \\
                         https://api.github.com/repos/${env.GITHUB_REPO}/statuses/${env.COMMIT_SHA}
                    """
                } else {
                    echo "Missing GITHUB_TOKEN, GITHUB_REPO or COMMIT_SHA, skipping status update"
                }
            }
        }
    }
}
