pipeline {
    agent any

    environment {
        GITHUB_TOKEN = credentials('github-token')
        GITHUB_REPO = 'qillbel/scrap1_q-wmo'
        PR_ID = '11' // <-- set this dynamically or manually for now
        BASE_BRANCH = 'main'
    }

    stages {
        stage('Prepare Merged Commit') {
            steps {
                sh '''
                    git config --global user.email "jenkins@dummy.com"
                    git config --global user.name "jenkins bot"
                    git remote set-url origin https://github.com/${GITHUB_REPO}.git

                    # Fetch base branch
                    git fetch origin ${BASE_BRANCH}

                    # Fetch merged PR commit from GitHub's special ref
                    git fetch origin pull/${PR_ID}/merge:pr-${PR_ID}-merge

                    # Checkout the merged commit
                    git checkout pr-${PR_ID}-merge

                    # Save commit SHA for GitHub status API
                    COMMIT_SHA=$(git rev-parse HEAD)
                    echo "COMMIT_SHA=${COMMIT_SHA}" > env.properties
                '''
            }
        }

        stage('Load Commit SHA') {
            steps {
                script {
                    def props = readProperties file: 'env.properties'
                    env.COMMIT_SHA = props['COMMIT_SHA']
                }
            }
        }

        stage('Build') {
            steps {
                echo "Running build on merged commit: ${env.COMMIT_SHA}"
                sh 'npm install'
            }
        }

        stage('Lint') {
            steps {
                echo 'Running linter...'
                sh 'npm run lint || true'
            }
        }

        stage('Unit Tests') {
            steps {
                echo 'Running unit tests...'
                sh 'npm run test:unit'
            }
        }

        stage('Integration Tests') {
            steps {
                echo 'Running integration tests...'
                sh 'npm run test:integration'
            }
        }
    }

    post {
        success {
            echo "✅ CI Pipeline passed"
            sh '''
                curl -s -X POST -H "Authorization: token ${GITHUB_TOKEN}" \
                -d '{"state": "success", "context": "continuous-integration/jenkins/pr-merge", "description": "Merged build passed", "target_url": "'"${BUILD_URL}"'"}' \
                https://api.github.com/repos/${GITHUB_REPO}/statuses/${COMMIT_SHA}
            '''
        }

        failure {
            echo "❌ CI Pipeline failed"
            sh '''
                curl -s -X POST -H "Authorization: token ${GITHUB_TOKEN}" \
                -d '{"state": "failure", "context": "continuous-integration/jenkins/pr-merge", "description": "Merged build failed", "target_url": "'"${BUILD_URL}"'"}' \
                https://api.github.com/repos/${GITHUB_REPO}/statuses/${COMMIT_SHA}
            '''
        }
    }
}
