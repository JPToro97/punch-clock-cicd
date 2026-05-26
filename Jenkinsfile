pipeline {
    agent any

    environment {
        IMAGE_NAME = "punch-clock-app"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:${env.BUILD_NUMBER} ."
                }
            }
        }

        stage('Run Automated Tests') {
            steps {
                script {
                    // Running tests inside a temporary container
                    sh "docker run --rm ${IMAGE_NAME}:${env.BUILD_NUMBER} pytest tests/"
                }
            }
        }
    }

    post {
        always {
            sh "docker rmi ${IMAGE_NAME}:${env.BUILD_NUMBER}"
        }
        success {
            echo "Pipeline completed successfully: All tests passed."
        }
        failure {
            echo "Pipeline failed: Please check the test logs for details."
        }
    }
}