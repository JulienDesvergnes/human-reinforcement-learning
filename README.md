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