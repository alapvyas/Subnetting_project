pipeline {
    agent any

    environment {
        // Define environment variables
        FLASK_ENV = 'production'
        DOCKERHUB_USERNAME = 'your_dockerhub_username'
        DOCKERHUB_PASSWORD = 'your_dockerhub_password'
        DOCKER_IMAGE = 'my-flask-app:latest'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building the application...'
                sh 'docker build -t ${DOCKER_IMAGE} .'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                // Test commands here
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerHubCredentials', usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_PASSWORD')]) {
                    echo 'Pushing Docker image to Docker Hub...'
                    sh 'docker login -u ${DOCKERHUB_USERNAME} -p ${DOCKERHUB_PASSWORD}'
                    sh 'docker tag ${DOCKER_IMAGE} ${DOCKERHUB_USERNAME}/${DOCKER_IMAGE}'
                    sh 'docker push ${DOCKERHUB_USERNAME}/${DOCKER_IMAGE}'
                    sh 'docker logout'
                }
            }
        }

        stage('Run Docker Image') {
            steps {
                echo 'Running Docker image...'
                sh "docker run -d -p 5000:5000 ${DOCKER_IMAGE}"
            }
        }

        stage('Deploy to Fly.io') {
            steps {
                script {
                    // Generate a random alphanumeric string for the app name
                    def appName = "app-${UUID.randomUUID().toString().take(8)}"
                    echo "Deploying to Fly.io with app name: ${appName}"
                    // Deploy using the fly CLI
                    sh "fly launch --name ${appName} --image ${DOCKERHUB_USERNAME}/${DOCKER_IMAGE} -y"
                }
            }
        }
    }
}
