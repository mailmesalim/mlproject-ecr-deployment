##I can build my ML project as package can install and can upload to pypi
from setuptools import find_packages,setup
from typing import List

##This function will return the list of requirements
##If -e . is present, it will remove it and is required 
## so when requirements.txt(-e . to connect setup.py) will run it will call setup.py
HYPEN_E_DOT='-e .'
def get_requirements(file_path)->List[str]:
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements
        
    



setup(
name='mlproject',
version='0.0.1',
author='Salim Khan',
author_email='mailme.salim@gmail.com',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')
)