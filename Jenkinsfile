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
                // Using the absolute path to docker on Windows to bypass environment variables
                bat '"C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker" compose build'
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                bat '"C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker" compose up -d'
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
