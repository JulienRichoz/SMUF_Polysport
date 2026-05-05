# Générateur de Tournoi Automatisé (SMUF Polysport)

Bienvenue dans le générateur d'emplois du temps du SMUF Polysport ! 
Ce projet contient des scripts Python permettant de créer des plannings complexes pour des tournois sportifs comprenant des dizaines d'équipes et plusieurs sports simultanés, puis de vérifier mathématiquement que le résultat est parfait et équitable.

## 1. Prérequis (À faire une seule fois)

Pour faire tourner le script, vous avez besoin de deux outils sur votre ordinateur :

### A. Une licence Gurobi (Le Solveur)
Le script utilise **Gurobi**, l'un des solveurs mathématiques les plus puissants au monde, pour calculer le planning. 
- Il nécessite une licence académique gratuite.
- **[Obtenez votre licence académique Gurobi ici](https://www.gurobi.com/academia/academic-program-and-licenses/)** et suivez leurs instructions d'installation.

### B. Le gestionnaire de paquets `uv`
Au lieu des méthodes Python traditionnelles complexes, ce projet utilise **`uv`**, un gestionnaire de projet ultra-rapide et simple qui s'occupe de tout (environnement virtuel, installation des dépendances, etc.) en arrière-plan.
- **[Installez uv en suivant ce lien](https://docs.astral.sh/uv/#installation)**.

## 2. Installation du projet

Une fois Gurobi et `uv` installés, ouvrez votre terminal (ou invite de commande) et naviguez jusqu'au dossier où vous avez téléchargé ce projet :

```bash
cd chemin/vers/le/dossier/SMUF_Polysport/scheduler
```

Ensuite, demandez à `uv` de préparer le projet et de télécharger les librairies mathématiques nécessaires (pandas, cvxpy, etc.) avec cette simple commande :

```bash
uv sync
```

## 3. Utilisation des scripts

### Étape 1 : Générer le calendrier du tournoi
Ouvrez le fichier `tournament_scheduler.py` et modifiez tout en bas le nombre d'équipes (`N`) et la répartition des terrains (`sports`). 

*PS: Une règle générale est d'avoir au maximum 4x le nombre d'équipes que de terrains disponibles (si 20 terrains, alors 20*4 = 80 équipes). Si le nombre d'équipe dépasse ce nombre, il faudra alors augmenter le nombre de timeslots avec des plannings plus complexes.*

Ensuite, lancez le script avec la commande :

```bash
uv run tournament_scheduler.py
```
> **Patience !** Le calcul d'un tournoi (par exemple 80 équipes) est un problème complexe. Cela peut prendre 2 à 3 minutes pendant lesquelles le terminal va afficher des calculs. Une fois terminé, le script génèrera un fichier CSV (ex: `tournament_schedule_80.csv`).

### Étape 2 : Vérifier que le calendrier est parfait
Pour être sûr à 100% que le planning est équitable (pas de matchs en double pour une équipe sur un même créneau, nombre de matchs identique pour tous), utilisez le script de vérification :

1. Ouvrez `verify_scheduler.py` et vérifiez que le nom du fichier ciblé tout en bas correspond bien au `.csv` que vous venez de générer.
2. Lancez la vérification :

```bash
uv run verify_scheduler.py
```

Si le terminal affiche **"SUCCÈS : Le calendrier est parfait !"**, votre tournoi est prêt !
