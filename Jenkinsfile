pipeline {
  agent any
  stages {
    stage('prepare') {
      steps {
        git branch: 'master',
        url: 'https://github.com/biohazardvos/birthday_bot.git'
        sh 'pip3 install -r requirements.txt'
      }
    }
    stage('test') {
      steps {
        sh 'python3 test_birthdaybot.py'
      }
      post {
        always {
          junit 'test-reports/*.xml'
        }
      }
    }
    stage('build') {
      steps {
        sh 'docker-compose up -d --build'
      }
    }
  }
}
