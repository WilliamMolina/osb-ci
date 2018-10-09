node {

    stage('Initialize'){
        def mavenHome  = tool 'myMaven'
        env.Path = "${mavenHome}/bin:${env.Path}"
    }

    stage('Checkout') {
        checkout scm
    }

    stage('Build'){
        bat "mvn clean install"
    }

}