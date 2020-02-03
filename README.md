# human-reinforcement-learning
Projet long - Apprentissage par renforcement humain

Je vous donne ici quelques liens supplémentaires de documentation sur le renforcement classique:
1. https://www.lebigdata.fr/reinforcement-learning-definition
2. https://fr.wikipedia.org/wiki/Apprentissage_par_renforcement

Une série de vidéo qui résume le fonctionnement d'un réseau de neurones :
1. https://www.youtube.com/watch?v=aircAruvnKk
2. https://www.youtube.com/watch?v=IHZwWFHWa-w
3. https://www.youtube.com/watch?v=Ilg3gGewQ5U
4. https://www.youtube.com/watch?v=tIeHLnjs5U8

## Configuration de l'environnement python

Ce processus d'installation ne fonctionne que pour un os de type windows.
Il faut dans un premier temps installer Anaconda pour avoir accès au terminal Anaconda Prompt : https://www.anaconda.com/distribution/
Une fois l'installation d'Anaconda terminée, ouvrir Anaconda prompt et installer les dépendances suivantes dans un nouvel environnement :
1. conda create -n tensorflow_cpu pip python=3.6
2. activate tensorflow_cpu 
3. pip install --ignore-installed --upgrade tensorflow==2.0
4. pip install keras
5. pip install numpy
6. pip install matplotlib
7. pip install keras-gym

## Quelques documents sur le renforcement humain

1. https://www.ijcai.org/Proceedings/2019/0884.pdf
2. https://web.stanford.edu/class/psych209/Readings/MnihEtAlHassibis15NatureControlDeepRL.pdf
3. https://arxiv.org/pdf/1706.03741.pdf
4. https://arxiv.org/pdf/1810.11748.pdf
5. https://grail.cs.washington.edu/projects/stateselection/stateselection.pdf
6. https://arxiv.org/pdf/1709.10163.pdf

## Gym de OpenAI

Le lien vers le pack de gym de OpenAI : - https://gym.openai.com/envs/#toy_text

## Tuto Git

Voici quelques commandes pour récupérer le dépôt git et faire des ajouts :

1. Créer un compte git et me transmettre l'adresse mail avec laquelle vous l'avez créé ou le nom d'utilisateur
2. Dans un terminal : git clone https://github.com/JulienDesvergnes/human-reinforcement-learning.git (récupère les données sur le serveur distant.)
3. En cas d'ajout de fichier :
	1. TOUJOURS FAIRE UN PULL AVANT D'AJOUTER DES MODIFICATIONS : git pull
	2. S'assurer d'avoir fait un git pull et d'avoir résolu les conflits en local
	3. git add mon_fichier.txt (ajout au local du fichier au prochain commit.)
	4. git commit -m "Mon message personnalisé qui décrit bien ce que j'ajoute"
	5. git push (propage les commits locaux sur le serveur distant.)
4. Commande utile : git status (résume l'état du dépôt local.)

