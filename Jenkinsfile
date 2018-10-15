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
                bat 'mvn com.smartbear.soapui:soapui-maven-plugin:5.4.0:test' 
            }
            post {
                always {
                    junit "results/*.xml"
                }
            }
        }
    }
}