pipeline {
    agent any

    environment {
        // Define environment variables here
        FLASK_ENV = 'production'
    }

    stages {
        stage('Initialize') {
            steps {
                echo 'Initializing...'
                sh 'echo "Starting Jenkins Pipeline"'
            }
        }

        stage('Build') {
            steps {
                echo 'Building...'

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
                sh 'docker run -itd -t my-flask-app:latest -p 5000:5000 '
            }
        }
    }
}
