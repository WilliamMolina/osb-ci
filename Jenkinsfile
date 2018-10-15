pipeline {
    agent any
    tools {
        maven 'localMaven'
    }
    stages {        
        stage('Checkout') {
            steps {
                checkout scm
            }            
        }
        stage ('Test') {
            steps {
                bat 'java --version' 
            }
            post {
                always {
                    junit "results/*.xml"
                }
            }
        }
    }
}