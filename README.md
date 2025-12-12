# 📘 **README — Version Académique / Universitaire**

````markdown
# 🥖 BoulangeGame  
### Simulation numérique d’apprentissage professionnel en boulangerie  
**Projet universitaire — Python / Pygame**

---

## 1. Présentation générale du projet

**BoulangeGame** est un module de simulation numérique destiné à soutenir l’apprentissage des fondamentaux du métier de boulanger.  
Il a été développé dans le cadre d’un enseignement consacré aux **jeux et simulations en formation professionnelle**.  
L’objectif principal est de transposer un processus artisanal réel — la fabrication du pain — dans un environnement interactif permettant d’explorer, de manipuler et de comprendre les relations entre variables techniques et résultats obtenus.

Le projet s’inscrit dans une démarche de modélisation pédagogique visant à rendre visibles des mécanismes professionnels souvent implicites, tout en offrant un espace sécurisé d’expérimentation pour des apprenants novices.

---

## 2. Finalités pédagogiques

Le module poursuit plusieurs finalités :

### ● **Compréhension des relations causales**
Permettre à l’apprenant de saisir comment la variation de la température, du temps de cuisson ou des ingrédients influence directement le résultat final.

### ● **Apprentissage par essai-erreur**
Proposer un environnement dans lequel l’apprenant peut tester des choix, observer les conséquences et ajuster ses décisions.

### ● **Régulation des apprentissages par feedback**
Fournir des rétroactions immédiates et différenciées (pain réussi, insuffisamment cuit, brûlé, erreur d’ingrédient, etc.).

### ● **Découverte guidée**
Encadrer l’exploration à travers une structure simplifiée, conformément aux travaux de De Jong & Van Joolingen (1998).

### ● **Approche béhavioriste et ouverture constructiviste**
Le module repose initialement sur des mécaniques béhavioristes (répétitions, ajustements, renforcement), tout en ménageant des perspectives d’enrichissement vers une démarche plus constructiviste.

Ce dispositif peut être mobilisé en collège, en CAP boulangerie ou dans des formations initiales aux métiers de l’alimentation.

---

## 3. Fonctionnalités du simulateur

- Interface interactive développée avec **Pygame**
- Sélection d’une recette (pain, viennoiserie, etc.)
- Choix des ingrédients de base
- Réglage des paramètres de cuisson (température, durée)
- Évaluation automatique du résultat en fonction des écarts aux paramètres attendus
- Navigation entre plusieurs écrans : accueil, sélection, cuisson, résultats
- Modularité permettant l’extension du jeu (nouvelles recettes, nouveaux niveaux, mode enseignant)

---

## 4. Installation du projet

### 4.1. Clonage du dépôt
```bash
git clone https://github.com/diather/BoulangeGame.git
cd BoulangeGame
````

### 4.2. Création d’un environnement virtuel (recommandé)

```bash
python3 -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

### 4.3. Installation des dépendances

```bash
pip install -r requirements.txt
```

---

## 5. Exécution du simulateur

Lancer le programme principal :

```bash
python3 main.py
```

Le simulateur démarre alors en affichant l’écran d’accueil, donnant accès à la sélection des recettes puis aux étapes interactives du jeu.

---

## 6. Organisation du code

```
BoulangeGame/
│── main.py                 # Point d'entrée
│── game.py                 # Logique générale du jeu
│── recipes.py              # Paramètres de cuisson et règles métiers
│── ui_components.py        # Boutons, compteurs et éléments d'interface
│── screens/                # Ensembles d’écrans du simulateur
│── images/                 # Ressources visuelles (ingrédients, résultats)
│── requirements.txt        # Bibliothèques nécessaires
│── README.md               # Document académique de présentation
```

Cette structure permet une maintenance facilitée, une extension progressive et une meilleure lisibilité du code pour des étudiants ou chercheurs.

---

## 7. Perspectives d’amélioration

Plusieurs évolutions sont envisagées :

* Intégration d’un **mode enseignant** (suivi des essais, statistiques, erreurs fréquentes)
* Augmentation de la **fidélité graphique et sonore**
* Création de **niveaux de difficulté progressifs**
* Mise en place d’un **système d’hypothèses** (approche constructiviste)
* Exportation vers une **version web jouable** via PyGBAG
* Ajout d’un système de **guidage adaptatif** basé sur les erreurs récurrentes

---

## 8. Cadre théorique mobilisé

Le projet s’appuie notamment sur :

* **De Jong, T. & Van Joolingen, W. (1998).** *Discovery Learning in Computer Simulations.*
  → Importance du guidage dans les environnements de simulation.

* **Hattie, J. & Timperley, H. (2007).** *The Power of Feedback.*
  → Rôle structurant du feedback dans la régulation des apprentissages.

* Théories de l’**apprentissage béhavioriste** : renforcement, répétition, ajustements progressifs.

Ce cadre permet d’associer rigueur pédagogique et jouabilité.

---

## 9. Auteur du projet

**Bassir Diallo (Diather)**
Étudiant en **Sciences de l’Éducation et de la Formation (UGA)**
et en **Administration d’Infrastructures Sécurisées (ETNA)**.
Projet réalisé dans le cadre de l’UE *Jeux & Simulations en Formation Professionnelle*.

---

## 10. Licence

Projet mis à disposition pour un usage pédagogique et scientifique.
L’ajout d’une licence libre (MIT ou Creative Commons) est recommandé selon les besoins.

```


```
