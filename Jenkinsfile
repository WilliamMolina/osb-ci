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
        stage ('Build') {
            steps {
                bat 'mvn clean package -U -gs C:\Users\williammolina\.m2\settings.xml' 
            }
        }
    }
}