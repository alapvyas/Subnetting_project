pipeline {
    agent any

    environment {
        // Define environment variables
        FLASK_ENV = 'production'
        DOCKERHUB_USERNAME = 'alapv'
        DOCKERHUB_PASSWORD = 'Mistborn@9574'
        DOCKER_IMAGE = 'my-flask-app:latest'
        AWS_ACCESS_KEY_ID = 'AKIAUZKPZNTTPY3PQMB2'
        AWS_SECRET_ACCESS_KEY = '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'
        S3_BUCKET = 'subnettingapp'
        CLOUDFRONT_DISTRIBUTION_ID = 'E1WO4DBOAH8F2I'
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
                // Add your test commands here
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

        stage('Generate Static Files') {
            steps {
                echo 'Generating static files from Docker container...'
                sh 'docker run --rm -v $(pwd)/static_output:/output ${DOCKER_IMAGE}'
                // Ensure your Docker container copies static files to the /output directory
            }
        }

        stage('Deploy to S3') {
            steps {
                withAWS(credentials: 'awsCredentials') {
                    echo 'Deploying static files to S3...'
                    sh 'aws s3 sync static_output/ s3://${S3_BUCKET} --delete'
                }
            }
        }

        stage('Update CloudFront') {
            steps {
                withAWS(credentials: 'awsCredentials') {
                    echo 'Invalidating CloudFront distribution...'
                    sh 'aws cloudfront create-invalidation --distribution-id ${CLOUDFRONT_DISTRIBUTION_ID} --paths "/*"'
                }
            }
        }
    }
}
