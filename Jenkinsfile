pipeline {
    agent any

    environment {
        GITHUB_TOKEN = credentials('github-token') // Make sure this exists
        GITHUB_REPO = 'qillbel/scrap1_q-wmo'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.COMMIT_SHA = sh(script: "git rev-parse HEAD", returnStdout: true).trim()
                }
            }
        }

        stage('Lint') {
            steps {
                sh 'npm install'
                sh 'npm run lint'
            }
        }

        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
    }

    post {
        success {
            script {
                node('') {  // Specify your agent label or keep empty if agent any works
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
                }
            }
        }
        failure {
            script {
                node('') {  // Specify your agent label or keep empty if agent any works
                    def statusJson = """
                    {
                        "state": "failure",
                        "context": "continuous-integration/jenkins/pr-merge",
                        "description": "Merged build failed",
                        "target_url": "${env.BUILD_URL}"
                    }
                    """
                    sh """
                    curl -s -X POST -H "Authorization: token ${env.GITHUB_TOKEN}" \\
                         -d '${statusJson}' \\
                         https://api.github.com/repos/${env.GITHUB_REPO}/statuses/${env.COMMIT_SHA}
                    """
                }
            }
        }
    }
}
