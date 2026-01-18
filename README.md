# End-to-End Machine Learning Project with Deployment

This project demonstrates a complete machine learning pipeline, deployed using Docker, AWS ECR, and AWS EC2 via GitHub Actions.

## 1. Git Repository Setup

If you are setting this up for the first time:

```bash
# 1. Clone the existing project
git clone https://github.com/mailmesalim/mlproject.git mlproject-ecr-deployment

# 2. Go into the new folder
cd mlproject-ecr-deployment

# 3. Remove the link to the original repo
git remote remove origin

# 4. Add your new repo as the remote
git remote add origin https://github.com/mailmesalim/mlproject-ecr-deployment.git

# 5. Create repository manually on GitHub (name: mlproject-ecr-deployment)

# 6. Push to your new repo
git push -u origin main
```

## 2. AWS Setup

### IAM User
Create an IAM User in AWS with the following permissions:
- `AmazonEC2ContainerRegistryFullAccess`
- `AmazonEC2FullAccess`

### Elastic Container Registry (ECR)
Create a repository in ECR to store your Docker images.

```bash
aws ecr create-repository --repository-name simple-app --region us-east-1
```
*Note: Save the repository URI (e.g., `566373416292.dkr.ecr.us-east-1.amazonaws.com/simple-app`).*

### EC2 Instance (Self-Hosted Runner)
Launch an Ubuntu EC2 instance (t2.micro is sufficient for testing, t2.small/medium recommended for prod).

**Connect to your EC2 instance and run the following commands to install Docker:**

```bash
# Optional: Update and Upgrade
sudo apt-get update -y
sudo apt-get upgrade

# Required: Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add ubuntu user to docker group
sudo usermod -aG docker ubuntu
newgrp docker
```

## 3. GitHub Actions Configuration

### Configure Self-Hosted Runner
1. Go to your GitHub Repository -> **Settings** -> **Actions** -> **Runners**.
2. Click **New self-hosted runner**.
3. Choose **Linux**.
4. Run the provided commands on your EC2 instance to register the runner.

### Configure Secrets
Go to **Settings** -> **Secrets and variables** -> **Actions** -> **New repository secret**. Add the following secrets:

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `AWS_ACCESS_KEY_ID` | IAM User Access Key | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | IAM User Secret Key | `wJalr...` |
| `AWS_REGION` | AWS Region | `us-east-1` |
| `AWS_ECR_LOGIN_URI` | ECR Registry URL (without repo name) | `566373416292.dkr.ecr.us-east-1.amazonaws.com` |
| `ECR_REPOSITORY_NAME` | ECR Repository Name | `simple-app` |

## 4. Azure Deployment

### 1. Azure Container Registry (ACR) Setup
Create an Azure Container Registry to store your Docker images.

```bash
# Create a Resource Group
az group create --name mlproject-rg --location eastus

# Create ACR
az acr create --resource-group mlproject-rg --name <your-acr-name> --sku Basic --admin-enabled true

# Login to ACR (Local)
az acr login --name <your-acr-name>
```

### 2. Azure Web App Setup
Create an App Service Plan and Web App for Containers.

```bash
# Create App Service Plan
az appservice plan create --name mlproject-plan --resource-group mlproject-rg --sku B1 --is-linux

# Create Web App
az webapp create --resource-group mlproject-rg --plan mlproject-plan --name <your-webapp-name> --deployment-container-image-name <your-acr-name>.azurecr.io/<your-webapp-name>:latest
```

### 3. Configure Secrets in GitHub
Run the following command to generate credentials for the `AZURE_CREDENTIALS` secret:

```bash
az ad sp create-for-rbac --name "mlproject-cicd" --role contributor --scopes /subscriptions/<subscription-id>/resourceGroups/mlproject-rg --sdk-auth
```
*Copy the entire JSON output.*

Add the following secrets to your GitHub Repository:

| Secret Name | Description | Source |
|-------------|-------------|--------|
| `AZURE_CREDENTIALS` | Service Principal JSON | Output of verifying `az ad sp ...` command above |
| `ACR_LOGIN_SERVER` | ACR Login Server | `<your-acr-name>.azurecr.io` |
| `ACR_USERNAME` | ACR Admin Username | `az acr credential show -n <your-acr-name> --query "username" -o tsv` |
| `ACR_PASSWORD` | ACR Admin Password | `az acr credential show -n <your-acr-name> --query "passwords[0].value" -o tsv` |
| `AZURE_WEBAPP_NAME` | Name of your Web App | `<your-webapp-name>` |

## 5. Deployment

Once everything is set up, every push to the `main` branch will trigger the GitHub Action workflow which will:
1. Build the Docker image.
2. Push the image to AWS ECR / Azure ACR.
3. Pull the image on your EC2 instance / Deploy to Azure Web App.
4. Run the application on port 8080 (AWS) or 80/5000 (Azure).

### Important Note on Ports
- **Dockerfile**: Ensure your app exposes the correct port (e.g., `EXPOSE 5000`).
- **AWS**: Ensure EC2 Security Group allows traffic on the application port (e.g., 8080 or 5000).
- **Azure**: Add an Application Setting `WEBSITES_PORT=5000` if your app does not listen on port 80.

## Verified Steps
1. [x] Docker Build
2. [x] Github Workflow
3. [x] IAM User in AWS
4. [ ] Azure Deployment

