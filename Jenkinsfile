pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker build -t quick-commerce-user-service ./user-service'
                sh 'docker build -t quick-commerce-product-service ./product-service'
                sh 'docker build -t quick-commerce-order-service ./order-service'
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh 'docker compose down || true'
                sh 'docker compose up -d --build'
            }
        }

        stage('Smoke Test') {
            steps {
                sh 'sleep 10'
                sh 'curl -f http://localhost:8001/ || exit 1'
                sh 'curl -f http://localhost:8002/ || exit 1'
                sh 'curl -f http://localhost:8003/ || exit 1'
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
            sh 'docker compose down || true'
        }
    }
}
