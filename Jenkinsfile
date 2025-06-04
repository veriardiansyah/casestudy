pipeline {
  agent any

  environment {
    IMAGE = "bolt391/demo-app"
    TAG = "latest"
    DOCKER_CRED = "docker-hub"
    KUBECONFIG_CRED = "kubeconfig-dev"
    NAMESPACE = "default"
    HELM_RELEASE = "casestudy"
    HELM_BIN = "${env.WORKSPACE}/linux-amd64/helm"
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
          docker.build("${IMAGE}:${TAG}")
        }
      }
    }

    stage('Push Docker Image') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: "${DOCKER_CRED}",
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

    stage('Install Helm') {
      steps {
        sh '''
          curl -LO https://get.helm.sh/helm-v3.18.2-linux-amd64.tar.gz
          tar -zxvf helm-v3.18.2-linux-amd64.tar.gz
        '''
        sh "${HELM_BIN} version"
      }
    }

    stage('Deploy to Kubernetes (Helm)') {
      steps {
        withCredentials([file(credentialsId: "${KUBECONFIG_CRED}", variable: 'KUBE_FILE')]) {
          script {
            echo "🚀 Deploying to Kubernetes via Helm..."
            sh """
              export KUBECONFIG=$KUBE_FILE
              ${HELM_BIN} upgrade --install ${HELM_RELEASE} ./helm \
                --set image.repository=${IMAGE} \
                --set image.tag=${TAG} \
                --namespace ${NAMESPACE} --create-namespace
            """
          }
        }
      }
    }
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
