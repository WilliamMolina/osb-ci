pipeline {
    agent any
    tools {
        maven 'myMaven'
    }
    stages {        
        stage('Checkout') {
            checkout scm
        }
        stage ('Build') {
            steps {
                bat 'mvn clean install' 
            }
        }
    }
}