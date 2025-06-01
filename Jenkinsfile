pipeline {
    agent any

    environment {
        GITHUB_REPO = 'qillbel/scrap1_q-wmo'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'npm install'
            }
        }

        stage('Lint') {
            steps {
                sh 'npm run lint'
            }
        }
    }

    post {
        success {
            script {
                updateGitHubStatus('success', 'Build succeeded')
            }
        }
        failure {
            script {
                updateGitHubStatus('failure', 'Build failed')
            }
        }
    }
}

def updateGitHubStatus(String state, String description) {
    def commitSha = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
    def buildUrl = env.BUILD_URL

    withCredentials([usernamePassword(credentialsId: 'jenkins-ci-token', usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
        sh """
            curl -s -u "\$GITHUB_USER:\$GITHUB_TOKEN" -X POST -d @- https://api.github.com/repos/${env.GITHUB_REPO}/statuses/${commitSha} <<EOF
            {
                "state": "${state}",
                "context": "continuous-integration/jenkins/pr-merge",
                "description": "${description}",
                "target_url": "${buildUrl}"
            }
EOF
        """
    }
}
