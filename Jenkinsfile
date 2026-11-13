// Runs for the branches develop, uat and prod (see infra/jenkins/casc.yaml).
// The branch name is also the environment: its namespace and its chart/values-<branch>.yaml.
pipeline {
  agent any
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
        sh 'helm upgrade --install app chart --namespace $BRANCH_NAME --create-namespace -f chart/values-$BRANCH_NAME.yaml --set image.tag=$TAG --wait --rollback-on-failure --timeout 2m'
      }
    }
    stage('Smoke test') {
      steps {
        // this environment's NodePort, reached over the shared docker network; must serve this commit
        sh '''
          PORT=$(awk '/^nodePort:/ {print $2}' chart/values-$BRANCH_NAME.yaml)
          curl -fsS http://cicd-control-plane:$PORT/ | grep "version $TAG"
        '''
      }
    }
  }
}
