pipeline {
    agent any
    environment {
        IMAGE = "bolt391/demo-app"
        TAG = "latest"
        DOCKER_CRED = "docker-hub"
        KUBECONFIG_CRED = "kubeconfig-dev"
        NAMESPACE = "default"
        HELM_RELEASE = "casestudy"
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
                    def buildResult = docker.build("${IMAGE}:${TAG}")
                    builtImage = buildResult.image
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withDockerRegistry(credentialsId: DOCKER_CRED) {
                    script {
                        echo "📦 Pushing image to DockerHub..."
                        docker.withRegistry(builtImage) {
                            docker.push("${IMAGE}:${TAG}")
                        }
                    }
                }
            }
        }

        stage('Deploy to Kubernetes (Helm)') {
            steps {
                withCredentials([kubernetesCredentials(credentialsId: KUBECONFIG_CRED, variable: 'KUBECONFIG')]) {
                    script {
                        echo "🚀 Deploying to Kubernetes via Helm..."
                        sh '''
                            export KUBECONFIG=$KUBECONFIG
                            helm upgrade --install $HELM_RELEASE ./helm \
                              --set image.repository=$IMAGE \
                              --set image.tag=$TAG \
                              --namespace $NAMESPACE --create-namespace
                        '''
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
