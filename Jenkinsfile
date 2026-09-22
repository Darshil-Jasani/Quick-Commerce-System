pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Code successfully retrieved from GitHub.'
            }
        }

        stage('Build Docker Images') {
            steps {
                bat 'docker compose build'
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                bat 'docker compose up -d'
            }
        }

        stage('Smoke Test') {
            steps {
                echo 'System deployed successfully. Checking service endpoints...'
                bat 'curl -s http://localhost:8001/docs'
                bat 'curl -s http://localhost:8002/docs'
                bat 'curl -s http://localhost:8003/docs'
            }
        }
    }

    post {
        always {
            echo 'Pipeline run completed.'
        }
    }
}
