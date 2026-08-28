pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'python3 --version'
                sh 'python3 -m pip install --user pytest'
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m pytest'
            }
        }

        stage('Result') {
            steps {
                echo 'Build and tests completed successfully.'
            }
        }
    }
}
