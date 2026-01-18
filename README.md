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

## 4. Deployment

Once everything is set up, every push to the `main` branch will trigger the GitHub Action workflow which will:
1. Build the Docker image.
2. Push the image to AWS ECR.
3. Pull the image on your EC2 instance.
4. Run the application on port 8080.

## Verified Steps
1. [x] Docker Build
2. [x] Github Workflow
3. [x] IAM User in AWS
