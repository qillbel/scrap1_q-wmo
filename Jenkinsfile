pipeline {
    agent any

    environment {
        // Jenkins credential ID containing your GitHub PAT
        GITHUB_TOKEN = credentials('jenkins-ci-token')
        // GitHub repo slug (owner/repo)
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

        stage('Test') {
            steps {
                // Make sure you have a "test" script in package.json, else change this line
                sh 'npm test'
            }
        }
    }

    post {
        success {
            script {
                notifyGitHubStatus('success', 'Build succeeded')
            }
        }
        failure {
            script {
                notifyGitHubStatus('failure', 'Build failed')
            }
        }
    }
}

def notifyGitHubStatus(String state, String description) {
    def commitSha = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
    def buildUrl = env.BUILD_URL

    def payload = """
    {
        "state": "${state}",
        "context": "continuous-integration/jenkins/pr-merge",
        "description": "${description}",
        "target_url": "${buildUrl}"
    }
    """

    sh """
    curl -s -X POST -H "Authorization: token ${env.GITHUB_TOKEN}" -d '${payload}' \
    https://api.github.com/repos/${env.GITHUB_REPO}/statuses/${commitSha}
    """
}
