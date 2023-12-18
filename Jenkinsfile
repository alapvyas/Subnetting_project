pipeline {
    agent any

    environment {
        // Define environment variables
        FLASK_ENV = 'production'
        DOCKERHUB_USERNAME = 'your_dockerhub_username' // 
        DOCKERHUB_PASSWORD = 'your_dockerhub_password' // 
        DOCKER_IMAGE = 'my-flask-app:latest' // 
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
                //
            }
        }

        stage('Push to Docker Hub')
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerHubCredentials', usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_PASSWORD')]) {
                    // Generate a unique tag for the image, e.g., using the build number
                    def uniqueTag = "build-${env.BUILD_NUMBER}"
                    echo 'Pushing Docker image to Docker Hub with tag: ' + uniqueTag
                    sh 'docker login -u ${DOCKERHUB_USERNAME} -p ${DOCKERHUB_PASSWORD}'
                    sh "docker tag ${DOCKER_IMAGE} ${DOCKERHUB_USERNAME}/${DOCKER_IMAGE}:${uniqueTag}"
                    sh "docker push ${DOCKERHUB_USERNAME}/${DOCKER_IMAGE}:${uniqueTag}"
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
    }
}
