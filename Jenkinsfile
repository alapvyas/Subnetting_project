pipeline {
    agent any

    environment {
        // Define environment variables here
        FLASK_ENV = 'production'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building the application...'

                sh 'docker build -t my-flask-app:latest .'

                echo 'Cleaning up...'
            }
        }

        stage('Test') {
            steps {
                echo 'Hey, if we don\'t test, the number of cases don\'t go up! :)'
            }
        }

        stage('Push') {
            steps {
                echo 'Placeholder for pushing to Docker Hub'
            }
        }

        stage('Run') {
            steps {
                sh 'docker run -itd -p 5000:5000 my-flask-app:latest'
            }
        }
    }
}
