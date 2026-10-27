pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        PATH = "/opt/homebrew/bin:/Users/suhailsuffli/.docker/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install -r requirements-dev.txt
                    .venv/bin/python -m compileall -q src
                '''
            }
        }

        stage('Test') {
            steps {
                sh '.venv/bin/python -m pytest -v --junitxml=test-results.xml'
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build \
                      -t devops-calculator:build-${BUILD_NUMBER} .
                    docker image inspect \
                      devops-calculator:build-${BUILD_NUMBER} \
                      --format '{{.Id}}'
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'test-results.xml',
                             allowEmptyArchive: true
        }
    }
}
