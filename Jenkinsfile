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
                bat '''
                D:\\jdev\\oracle_common\\common\\bin\\wlst.cmd .\\config\\datasource.py .\\config\\datasources
                '''
                }
        }
        stage ('Deploy for testing') {
            steps {
                bat '''
                mvn pre-integration-test -DoracleServerUrl=\"http://localhost:7101\" -DoracleUsername=\"weblogic\" -DoraclePassword=\"welcome1\" -DoracleHome=\"D:/jdev/\"
                '''
                }
        }
    }
}