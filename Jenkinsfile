pipeline {
    agent any
    tools {
        maven 'myMaven'
    }
    stages {        
        stage('Checkout') {
            steps {
                checkout scm
            }            
        }
        stage ('Build') {
            steps {
                bat 'mvn clean install' 
            }
        }
    }
}