/*
Edit History:
| Person | Date | Comment |
| --- | --- | --- |
| Shiladitya | 07/11/2026 | Modified the Jenkinsfile |
| Shiladitya | 07/10/2026 | Created |
*/

pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.12'
        IMAGE_REPOSITORY = "shiladitya997/python_fastapi_project"
        IMAGE_NAME = 'python_fastapi_project'
        REGISTRY_URL = 'https://hub.docker.com/repository/shiladitya997/python_fastapi_project'
        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE_NAME = "${IMAGE_REPOSITORY}:${IMAGE_TAG}"
        LATEST_IMAGE = "${IMAGE_REPOSITORY}:latest"
        REGISTRY_CREDENTIALS = "DOCKERHUB_REPO_SHILADITYA"
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }   

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set Up Python/Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt -r requirements-dev.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    mkdir -p test-results
                    # pytest --junitxml=test-results/pytest.xml
                    pytest -v
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results/*.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                      -t ${IMAGE_NAME}:${IMAGE_TAG} \
                      -t ${IMAGE_NAME}:latest \
                      .
                '''
            }
        }

        stage('Scan Docker Image') {
            steps {
                sh '''
                    trivy image \
                        --exit-code 1 \
                        --severity HIGH,CRITICAL \
                        --ignore-unfixed \
                        ${IMAGE_NAME}
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: "${REGISTRY_CREDENTIALS}",
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "${DOCKER_PASSWORD}" | docker login "${REGISTRY_URL}" \
                          --username "${DOCKER_USERNAME}" \
                          --password-stdin

                        docker push ${IMAGE_NAME}
                        docker push ${LATEST_IMAGE}
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "CI completed successfully."
            echo "Published ${IMAGE_NAME}:${IMAGE_TAG} and ${IMAGE_NAME}:latest"
        }
        failure {
            echo "Pipeline failed. Please check the logs for details."
        }
        always {
            sh '''
                docker image rm ${IMAGE_NAME} || true
                docker image rm ${LATEST_IMAGE} || true
                rm -rf .venv
            '''
            cleanWs(
                deleteDirs: true,
                disableDeferredWipeout: true,
                notFailBuild: true
            )
        }
    }
}
