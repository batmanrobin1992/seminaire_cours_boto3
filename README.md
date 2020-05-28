# Séminaire sur Boto3

## Installation

### Installation sur Ubuntu 18.04 LTS

#### Installation de PyCharm

    1- Aller à la page suivante : https://www.jetbrains.com/pycharm/download/#section=linux
    2- Cliquer sur Download sous la section Professional
    3- Ouvrir un Terminal
    4- sudo tar -xvf LE_NOM_TARBALL.tar.gz -C /opt (Extraire .tar.gz vers opt pour supporter l’exécution du dossier)
    5- cd /opt/ LE_NOM_TARBALL (Aller à l'emplacement du Tarball)
    6- ./jetbrains-toolbox (Ouvrir le JetBrains ToolBox faire la commande suivante)
    7- Laisser par défaut les options jusqu’à License Activation
        7.1- Choisir Activate PyCharm
        7.2- Dans Get License from choisir JB Account
        7.3- Entrer les informations relatives à votre compte IntelliJ dans Licence Activation 
        (Important de vérifier que vous avez un compte sur IntelliJ : https://account.jetbrains.com/login)
        7.4- Cliquer sur Activate

#### Installation de Python 3.7.7
    1- cd ~
    2- cd /tmp
    3- wget https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz
    4- tar –xvf Python-3.7.7.tgz
    5- python3 --version (Vérifier la version de Python)
    6- Si vous ne voyez pas Python 3.7.7, lors le dernière commande
       6.1- sudo update-alternatives --config python
       6.2- sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 7
       6.3- python3 –version

#### Créer un nouveau projet
    1- Cliquer sur New Project
       1.1- Choisir Pure Python
       1.2- Choisir pour Base interpreter le chemin vers l’interpreter Python 3.7.7
            exemple: usr/bin/python3.7
    2- Dans location, lui donner le nom : seminaire_cours_boto3
    3- Cliquer en bas sur Terminal > Écrire la commande suivant :  pip --version (Vérifier, si pip est installé)
    4- Si pip n'est pas installé
       5.1- Cliquer en bas sur Terminal > Écrire la commande suivant : sudo apt install python3-pip
       5.2- Refaire étape 4
       
#### Installer Boto3
    1- Aller dans PyCharm
    2- Cliquer en bas sur Terminal > Écrire la commande suivant : pip3 install boto3

#### Configuration du AWS CLI
    *Access Key ID et Secret Key ID vous seront donnés, lors du séminaire sur Boto3*
    1- Cliquer en bas sur Terminal
    2- sudo apt-get update
    3- sudo apt-get install awscli
    4- aws --version (Vérifier que AWS CLI est installé)
    5- aws configure (Configurer les variables d'environnement pour configurer l’AWS CLI)
       5.1- Entrer Access Key ID
       5.2- Entrer Secret Key ID
       5.3- Dans Region entrer: ca-central-1
       5.4- Dans Format entrer: json
       5.5- cat ~/.aws/config (Vérification de la région et du format)
       5.6- cat ~/.aws/credentials (Vérification du Access Key ID et du Secret Key ID)
       
#### Tester, si tout fonctionne
    1- Suivre les étapes dans le Wiki - Test Boto3
       
### Installation sur Windows 10

#### Installation de PyCharm
    1- Aller à la page suivante : https://www.jetbrains.com/pycharm/download/#section=windows
    2- Cliquer sur Download sous la section Professional
    3- Exécuter l’installeur
       3.1- Cliquer Next jusqu'à Installation Options
       3.2- Cocher dans Installation Options 64-bit launcher (Optionnel - Met de créer un raccourci sur votre Bureau)
       3.3- Choisir dans Choose Start Menu Folder: JetBrains
       3.4- Cliquer Install

    . 
#### Installation de Python 3.7.7
    1- Aller https://www.python.org/downloads/windows/
    2- Cliquer dans la section Python 3.7.7 sur Windows x86-64 executable installer
    3- Exécuter l’installeur
    4- Cocher Add Python 3.7 to PATH
    5- Choissait Install Now
    6- Ouvrir un Command Prompt
       6.1- Écrire python --version (Vérifier la version de Python)
       6.2- Écrire pip --version (Vérifier, si pip est installé)
    
#### Installation de pip (S’il n’est pas présent dans votre projet PyCharm)
    1- Aller télécharger pip http://bootstrap.pypa.io/get-pip.py
    2- Enregistrer le script sous C:\Program Files\Python37\Script
    3- Ouvrir un Command Prompt
       3.1- cd C:\Program Files\Python37\Script
       3.2- python get-pip.py (Installer pip)
       3.3- pip --version (Vérifier, si pip est installé maintenant)
       
#### Créer un nouveau projet
    1- Cliquer sur New Project
       1.1- Choisir Pure Python
       1.2- Choisir pour Python interpreter le chemin vers l’interpreter Python 3.7.7
            exemple: usr/bin/python3.7
    2- Dans location, lui donner le nom : seminaire_cours_boto3
        
#### Installer Boto3
    1- Aller dans Pycharm
    2- Cliquer en bas sur Terminal > Écrire la commande suivant: pip3 install boto3
    
#### Installation de AWS CLI
    *Access Key ID et Secret Key ID vous seront donnés, lors du séminaire sur Boto3*
    1- Aller à https://aws.amazon.com/fr/cli/
    2- Cliquer à gauche sur Téléchargez et exécutez l'installateur Windows
    3- Double cliquer pour le fichier pour l’installer
    4- Ouvrir un Command Prompt
       4.1- aws configure (Configurer les variables d'environnement pour configurer l’AWS CLI)
       4.2- Entrer Access Key ID
       4.3- Entrer Secret Key ID
       4.4- Dans Region entrer: ca-central-1
       4.5- Dans Format entrer: JSON
  
       
#### Tester, si tout fonctionne
    1- Suivre les étapes dans le Wiki - Test Boto3

