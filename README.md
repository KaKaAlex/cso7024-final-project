# Northwind Logistics Delivery Tracking Service

This repository contains the Northwind Logistics delivery-tracking application and the DevOps workflow developed for the CSO7024 final project.

The solution integrates:

- Git and GitHub pull-request workflow
- Automated testing with pytest
- GitHub Actions CI/CD
- Ansible environment automation
- Docker containerisation
- Kubernetes orchestration with Minikube

## Application endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Service information |
| GET | `/health` | Health status |
| GET | `/deliveries` | All delivery records |
| GET | `/deliveries/{id}` | A specific delivery or HTTP 404 |

The application stores its data in memory and has no external database.

## Architecture

```text
Developer
   |
   | Git feature branch and pull request
   v
GitHub Repository
   |
   | GitHub Actions
   v
Install dependencies -> Compile -> Test -> Build Docker image
   |
   | Push on main
   v
GitHub Container Registry
   |
   | Local image loaded into Minikube
   v
Kubernetes Deployment (2 Pods) -> NodePort Service -> Host
```

## Project structure

```text
.github/workflows/ci.yml   CI/CD pipeline
ansible/                   Ansible inventory and playbook
app/                       Python application
kubernetes/                Deployment and Service manifests
tests/                     Automated test suite
.dockerignore              Docker build exclusions
Dockerfile                 Container image definition
requirements.txt           Pinned testing dependency
run.py                     Local application entry point
```

## Prerequisites

- Python 3.10 or newer
- Git
- Docker Desktop
- kubectl
- Minikube
- WSL with Ansible

## Run locally

```powershell
python -m app
```

The service listens on port `8000`.

Test it from a second terminal:

```powershell
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/deliveries
Invoke-RestMethod http://localhost:8000/deliveries/NL-1002
```

## Automated testing

Install the pinned testing dependency:

```powershell
python -m pip install -r requirements.txt
```

Run all tests:

```powershell
python -m pytest -v
```

The suite contains unit tests for the in-memory data functions and integration tests for the HTTP API.

## Git workflow

Changes are developed on short-lived feature branches:

```powershell
git switch -c feature/example
git add .
git commit -m "Describe the change"
git push -u origin feature/example
```

Each feature branch is reviewed through a GitHub pull request before being merged into `main`.

## CI/CD pipeline

The GitHub Actions workflow runs on:

- Pull requests targeting `main`
- Pushes to `main`

The workflow:

1. Checks out the repository
2. Configures Python 3.11
3. Installs dependencies
4. Compiles the Python source
5. Runs all automated tests
6. Builds the Docker image
7. Publishes the image to GitHub Container Registry after a successful push to `main`

Published image:

```text
ghcr.io/kakaalex/cso7024-final-project:latest
```

## Ansible automation

The Ansible playbook creates a reproducible local environment in WSL. It:

- Creates the deployment directory
- Copies the application
- Creates a Python virtual environment
- Installs pinned dependencies
- Configures port `8000`
- Verifies the deployed application

Check the syntax:

```powershell
wsl ansible-playbook -i ansible/inventory.ini ansible/playbook.yml --syntax-check
```

Run the playbook:

```powershell
wsl ansible-playbook -i ansible/inventory.ini ansible/playbook.yml
```

Running the playbook again should report `changed=0` and `failed=0`, demonstrating idempotency.

## Docker deployment

Build the image:

```powershell
docker build -t northwind-delivery:1.0 .
```

Run it:

```powershell
docker run --rm -p 8000:8000 northwind-delivery:1.0
```

Test it from a second terminal:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

The container runs as a numeric non-root user and includes a Docker health check.

## Kubernetes deployment

Start Minikube:

```powershell
minikube start --driver=docker
```

Build and load the local image:

```powershell
docker build -t northwind-delivery:1.0 .
minikube image load northwind-delivery:1.0 --overwrite=true
```

Validate the manifests:

```powershell
kubectl apply --dry-run=client -f kubernetes/
```

Deploy:

```powershell
kubectl apply -f kubernetes/
kubectl rollout status deployment/northwind-delivery
```

Check the resources:

```powershell
kubectl get pods
kubectl get service northwind-delivery
```

The Deployment runs two replicas with:

- Readiness and liveness probes
- CPU and memory controls
- Non-root execution
- Disabled privilege escalation
- Dropped Linux capabilities

Access the service:

```powershell
kubectl port-forward service/northwind-delivery 8080:80
```

From a second terminal:

```powershell
Invoke-RestMethod http://localhost:8080/health
Invoke-RestMethod http://localhost:8080/deliveries/NL-1002
```

Stop the port forward with `Ctrl + C`.

## Cleanup

Remove the Kubernetes resources:

```powershell
kubectl delete -f kubernetes/
```

Stop Minikube:

```powershell
minikube stop
```

## Limitations

- Delivery data is held in memory and is not persistent.
- The Kubernetes deployment uses a local Minikube cluster.
- The CI runner publishes the image but cannot directly access the local Minikube cluster.
- The solution does not include production TLS, authentication or monitoring.
