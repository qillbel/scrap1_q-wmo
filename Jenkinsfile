pipeline {
    agent any

    environment {
        GITHUB_REPO = 'qillbel/scrap1_q-wmo'  // your repo here
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

    withCredentials([string(credentialsId: 'jenkins-ci-token', variable: 'GITHUB_TOKEN')]) {
        // Use a here-doc to avoid Groovy string interpolation issues and expose token safely
        sh """
        curl -s -X POST -H "Authorization: token \$GITHUB_TOKEN" -d @- \
        https://api.github.com/repos/${env.GITHUB_REPO}/statuses/${commitSha} <<EOF
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
