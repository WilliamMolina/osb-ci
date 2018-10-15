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
                bat 'mvn --version' 
            }
            post {
                always {
                    junit "results/*.xml"
                }
            }
        }
    }
}