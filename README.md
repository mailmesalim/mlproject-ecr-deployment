
 1. Clone the existing project
git clone https://github.com/mailmesalim/mlproject.git mlproject-ecr-deployment

 2. Go into the new folder
cd  mlproject-ecr-deployment

 3. Remove the link to the original repo
git remote remove origin

 4. Add your new repo as the remote
git remote add origin https://github.com/mailmesalim/mlproject-ecr-deployment.git

5. Create repository manually on GitHub

 6. Push to your new repo
git push -u origin main
