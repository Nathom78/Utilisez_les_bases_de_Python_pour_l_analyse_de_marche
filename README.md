# Utilisez les bases de Python pour l'analyse de marche
## P2 - Formation Développeur Python

Objectif: 
http://books.toscrape.com/

Vous pouvez retrouver en pdf [les objectifs complets ici](http://course.oc-static.com/projects/Python+FR/P2+-+Utilisez+les+bases+de+Python+pour+l'analyse+de+march%C3%A9/Python_P2_FR_Requirements.pdf)
### Prérequis
* Python est bien installé sur votre ordinateur
* Git installé (conseillé)

# INSTALLATION ( pour windows )

Créer un dossier vide. Il contiendra le code complet du projet, ainsi que les données du site aspiré.

## 1. Installation du logicel

Ouvrez un terminal:

Depuis le dossier précédemment créé, clonez le repository du programme avec la commande :

<pre><code>git clone https://github.com/Nathom78/Utilisez_les_bases_de_Python_pour_l_analyse_de_marche.git</code></pre>

Ou utiliser [ce repository](https://github.com/Nathom78/Utilisez_les_bases_de_Python_pour_l_analyse_de_marche.git)
<br>
## 2. Créer et activer l'environnement virtuel

Dans le terminal, toujours à la **racine du projet** :<br>
Tapez la commande suivante, afin de créer un environnement dans le repertoire env:
<pre><code> python -m venv env </code></pre>
Et la commande suivante, pour activer l'environnement:
<pre><code> source env/bin/activate</code></pre>
Résultat:
<pre> (env) "chemin de votre répertoire crée"> </pre>

## 3. Installer les paquets nécessaires aux projets 

Normalement une fois le clonage du projet réalisé, il y a un fichier *requirement.txt* à la racine.<br>
Taper la commande suivante :
<pre> pip install -r requirements.txt </pre>
Pour vérifier, taper cette commande :
<pre><code>pip list</code></pre>
Et vous devriez avoir :
>><pre><code>beautifulsoup4     4.11.1
>>certifi            2022.9.24
>>charset-normalizer 2.1.1
>>idna               3.4
>>pip                22.2.2
>>requests           2.28.1
>>setuptools         65.3.0
>>soupsieve          2.3.2.post1
>>urllib3            1.26.12</code></pre>
## 4. Execution du logiciel

Il ne reste plus qu'à lancer le programme books.toscrape.py, toujours depuis le terminal, grâce à la commande suivante :

<pre> py books.toscrape.py </pre>


## Technologies
[![My Skills](https://skillicons.dev/icons?i=python,html,git,github&theme=dark)](https://skillicons.dev)