pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout code from your repository
                git branch: 'main', url: 'https://github.com/VineetKurapati/Text-Summeriser_CloudComputing.git'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                // Install required dependencies
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Flask App') {
            steps {
                // Run Flask application
                sh 'python app1.py &'
            }
        }

        stage('Test') {
            steps {
                // Perform any testing if needed
                // This could include running automated tests against the running Flask app
                sh 'python test_script.py' // Replace 'test_script.py' with your actual test script
            }
        }
    }

    post {
        always {
            // Clean up after the pipeline run
            sh 'pkill -f app1.py' // Kill the Flask app process after testing
        }
    }
}
