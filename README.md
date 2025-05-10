<h1 align=center>
    <p>Trash & Splash</p>
</h1>

<p align=center>
    <strong>Sauver les poissons de la pollution et restaurer l'équilibre écologique. </strong>
</p>

![demo](https://i.imgur.com/APnqbvf.png)

# 📖 Presentation Générale

**Contributeurs :**

- Paolo Giometti : 25% du travail
- Lili-Rose Lauret : 25% du travail
- Anaelle Perilloux : 25% du travail
- Youssef Ghedammsi : 25% du travail
- Asma : 0% du travail

__*Sujet :*__ Ce projet a pour but de sauver les poissons de la pollution et restaurer l'équilibre écologique.

__*Problématique :*__ Comment sensibiliser les joueurs à la pollution marine tout en proposant une expérience de jeu à
la fois compétitive et ludique ?

__*Description :*__ Deux joueurs s'affrontent dans une pêche compétitive. L'objectif ? Sauver les poissons des déchets
humains. Comment ? En marquant le maximum de points en attrapant les déchets, tout en évitant les poissons qui doivent
demeurer dans leur habitat.

## 🛠️ Technologies utilisées

- **Langage :** Python
- **Bibliothèques :** Pygame, opencv, math, random, json, time
- **Outils de développement :**
    - **PyCharm :** environnement de développement
    - **GitHub :** gestion de versions et collaboration
    - **Notion :** gestion de projet et répartition des tâches
    - **Filmora :** montage vidéo pour les présentations
    - **Figma :** design et maquettes

## 🚀 Installation et lancement

1. Assurez-vous d'avoir Python installé (version 3.8 ou supérieure recommandée)
2. Clonez ce dépôt : `git clone https://github.com/Liliroselrt/Projet-Transverse`
3. Installez les dépendances : `pip install pygame opencv-python`
4. Lancez le jeu : `python main.py`

## 🎮 Comment jouer

1. Lancez le jeu et sélectionnez "JOUER" dans le menu principal
2. Configurez le nombre de joueurs et entrez les prénoms
3. Utilisez les commandes pour diriger votre canne à pêche
4. Attrapez les déchets (+points) et évitez les poissons (-points)
5. Le joueur avec le plus grand nombre de points à la fin remporte la partie

## 📝 Documentation Technique

**Fonctionnalités principales :**

- Menu interactif avec options de jeu, règles et sortie
- Configuration des joueurs (1 ou 2 joueurs)
- Système de points différenciés (déchets vs poissons)
- Historique des scores et classement
- Animation de la canne à pêche avec équations physiques

**Structure du projet :**

- `main.py` : point d'entrée du jeu
- `components/` : modules du jeu (menu, joueur, physique, etc.)
- `resources/` : ressources graphiques et sonores

# 📆 Journal de Bord

### **Chronologie du Projet :**

- __*A chercher*__ : Recherche de l'idée du jeu, mise en place des outils
- __*3 mars :*__ Répartition des tâches, suites des recherches
- __*17 mars :*__ Avancé de la mise en page : menu principal, mise en place des éléments principaux.
- __*24 mars :*__ Partie physique et avancée de la canne à pêche
- __*25 mars :*__ Modification du temps et des points, transitions dans la courbe et création de l'angle de lancement.
- __*7 avril :*__ Easter Egg, animation, continue code partie Lili-Rose et Youssef.
- __*1 mai :*__ Mise en place de l'animation au début du jeux 
- __*7 mai :*__ Réglage des derniers détails

### 📚**Répartition des Tâches :**

- **ReadMe** : Lili-Rose
- **main** : Paolo 
- **Anaelle :**
  - équation physique,
  - mouvement des joueurs, 
  - mise en scéne du début du jeu,
  - choix d'une musique de fond,
  - design 
- **Paolo :**
  - mouvement des poissons,
  - affichage du temps,
  - défini les touches de déplacement, 
  - lie le design au code,
  - lie le travail au chacun au code principal
- **Lili-Rose :**
  - compteur entre les poissons et les déchets,
  - menu de départ,
  - affichage des points,
  - affichage de fin de jeu, 
  - rentrer le nom des joueurs,
  - faire le menu des touches
- **Youssef :**
  - historique des joueurs,
  - 1v1, ajout du 2e joueur

## ✅ Tests et Validation (NON-IMPLEMENTE)

**Stratégie de test :** chaque module est testé individuellement puis intégré à l'ensemble pour validation globale.

**Points à valider :**

- Interface utilisateur intuitive
- Détection des collisions
- Calcul des scores
- Enregistrement des résultats
