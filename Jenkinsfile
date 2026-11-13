pipeline {
  agent any
  triggers { pollSCM('* * * * *') } // check the repo for new commits every minute
  environment {
    IMAGE = 'localhost:5001/app'
    TAG = "${env.GIT_COMMIT.take(7)}" // one immutable image tag per commit
  }
  stages {
    stage('Test') {
      steps {
        sh 'python3 -m coverage run --source=app -m unittest discover tests && python3 -m coverage xml'
      }
    }
    stage('SonarQube') {
      steps {
        withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
          // qualitygate.wait makes the scanner exit non-zero when the gate fails, which fails the build
          sh 'sonar-scanner -Dsonar.host.url=http://sonarqube:9000 -Dsonar.qualitygate.wait=true'
        }
      }
    }
    stage('Build & Push') {
      steps {
        sh 'docker build -t $IMAGE:$TAG . && docker push $IMAGE:$TAG'
      }
    }
    stage('Deploy') {
      steps {
        sh 'helm upgrade --install app chart --set image.tag=$TAG --wait --rollback-on-failure --timeout 2m'
      }
    }
    stage('Smoke test') {
      steps {
        // the kind node's NodePort, reached over the shared docker network; must serve this commit
        sh 'curl -fsS http://cicd-control-plane:30080/ | grep "version $TAG"'
      }
    }
  }
}
