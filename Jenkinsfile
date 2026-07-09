/*
Edit History:
| Person | Date | Comment |
| --- | --- | --- |
| Shiladitya | 07/10/2026 | Created |
*/

pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.12'
        IMAGE_NAME = 'fastapi-ecommerce'
        REGISTRY_URL = 'docker.io'
        REGISTRY_NAMESPACE = 'exampleorg'
        REGISTRY_CREDENTIALS_ID = 'docker-registry-credentials'
        IMAGE_TAG = 'local'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Image Metadata') {
            steps {
                script {
                    env.GIT_SHORT_COMMIT = sh(
                        script: 'git rev-parse --short=7 HEAD',
                        returnStdout: true
                    ).trim()
                    env.IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_SHORT_COMMIT}"
                }
            }
        }

        stage('Set Up Python') {
            steps {
                sh '''
                    if command -v python${PYTHON_VERSION} >/dev/null 2>&1; then
                      PYTHON_BIN=python${PYTHON_VERSION}
                    else
                      PYTHON_BIN=python3
                    fi

                    ${PYTHON_BIN} -m venv .venv
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
                    pytest --junitxml=test-results/pytest.xml
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
                      -t ${REGISTRY_URL}/${REGISTRY_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG} \
                      -t ${REGISTRY_URL}/${REGISTRY_NAMESPACE}/${IMAGE_NAME}:latest \
                      .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: "${REGISTRY_CREDENTIALS_ID}",
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "${DOCKER_PASSWORD}" | docker login "${REGISTRY_URL}" \
                          --username "${DOCKER_USERNAME}" \
                          --password-stdin

                        docker push ${REGISTRY_URL}/${REGISTRY_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${REGISTRY_URL}/${REGISTRY_NAMESPACE}/${IMAGE_NAME}:latest
                        docker logout "${REGISTRY_URL}"
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs(
                deleteDirs: true,
                disableDeferredWipeout: true,
                notFailBuild: true
            )
        }
        success {
            echo "CI completed. Published ${REGISTRY_URL}/${REGISTRY_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}"
        }
    }
}
