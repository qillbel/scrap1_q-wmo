pipeline {
    agent any

    environment {
        GITHUB_TOKEN = credentials('GITHUB_TOKEN')  // Jenkins secret text credential ID
        GITHUB_REPO = 'qillbel/scrap1_q-wmo'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
                script {
                    env.COMMIT_SHA = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
                    echo "Commit SHA: ${env.COMMIT_SHA}"
                }
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
                echo 'Running lint...'
                sh 'npm run lint'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                sh 'npm test'
            }
        }
    }

    post {
        success {
            script {
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
        failure {
            script {
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
