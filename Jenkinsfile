pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
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
                bat 'docker compose down'
                bat 'docker compose up -d'
            }
        }

        stage('Smoke Test') {
            steps {
                bat 'ping -n 11 127.0.0.1 > NUL'
                bat 'curl -f http://localhost:8001/ || exit 1'
                bat 'curl -f http://localhost:8002/ || exit 1'
                bat 'curl -f http://localhost:8003/ || exit 1'
            }
        }
    }

    post {
        success {
            echo 'Build, deploy, and smoke test all succeeded!'
        }
        failure {
            echo 'Pipeline failed — check the stage logs above.'
        }
        always {
            bat 'docker compose down'
        }
    }
}