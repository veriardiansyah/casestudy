pipeline {
  agent any

  environment {
     DOCKERHUB_CREDENTIALS = credentials('docker-hub')
  }

  stages {
    stage('Checkout Source Code') {
      steps {
        git url: 'https://github.com/veriardiansyah/casestudy.git', branch: 'master'
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          echo "🛠️ Building image ${IMAGE}:${TAG}..."
          def builtImage = docker.build("${IMAGE}:${TAG}")
        }
      }
    }

    stage('Push Docker Image') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: "docker-hub",
          usernameVariable: 'USER',
          passwordVariable: 'PASS'
        )]) {
          script {
            echo "📦 Pushing image to DockerHub..."
            sh """
              echo "$PASS" | docker login -u "$USER" --password-stdin
              docker push ${IMAGE}:${TAG}
            """
          }
        }
      }
    }

     stage('Deploy to Minikube') {
            steps {
                sh 'helm upgrade --install flask-app ./helm-chart --set image.repository=$DOCKERHUB_CREDENTIALS_USR/demo-app --set image.tag=latest'
  }

  post {
    success {
      echo "✅ Pipeline Sukses: Aplikasi berhasil dideploy ke Kubernetes"
    }
    failure {
      echo "❌ Pipeline Gagal: Cek log untuk mengetahui error"
    }
  }
}
