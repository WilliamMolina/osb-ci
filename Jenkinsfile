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
        stage ('Deploy for testing') {
            steps {
                bat '''
                mvn pre-integration-test -DoracleServerUrl=\"http://localhost:7101\" -DoracleUsername=\"weblogic\" -DoraclePassword=\"welcome1\" -DoracleHome=\"D:/jdev/\"
                '''
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