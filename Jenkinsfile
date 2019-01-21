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
        stage ('Configure') {
            steps {
                sh '''
                D:\\jdev\\oracle_common\\common\\bin\\wlst.cmd .\\config\\datasource.py .\\config\\datasources
                '''
                }
        }
        stage ('Deploy for testing') {
            steps {
                sh '''
                mvn pre-integration-test -DoracleServerUrl=\"http://192.168.11.7:7101\" -DoracleUsername=\"weblogic\" -DoraclePassword=\"welcome1\" -DoracleHome=\"D:/jdev/\"
                '''
                }
        }
        stage ('Test') {
            steps {
                sh 'mvn com.smartbear.soapui:soapui-maven-plugin:5.4.0:test -U' 
            }
            post {
                always {
                    junit "results/*.xml"
                }
            }
        }
    }
}