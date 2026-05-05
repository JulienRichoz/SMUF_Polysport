# 🏆 Polysport - Système de Gestion & Planning (Édition 2026)

Ce projet gère l'entièreté du tournoi Polysport : de la génération du planning des matchs à l'affichage en direct pour les joueurs et l'interface de gestion pour le staff.

## 🏗️ 1. Architecture du Projet

Le système est découpé en 3 parties distinctes :

1. **⚙️ Générateur de tournoi (Python)** : [Scheduler](https://github.com/JulienRichoz/SMUF_Polysport/tree/main/scheduler)
   * *Rôle :* Génère la grille des matchs équilibrée en fonction du nombre d'équipes et de terrains.
2. **🗄️ Database (Google Sheets)** : *[Lien privé vers le Google Sheet]*
   * *Rôle :* Base de données centrale. Contient les plannings, les équipes, le staff et les configurations.
3. **📱 UI & Web App (Google Apps Script)** : [Google Apps Script](https://github.com/JulienRichoz/SMUF_Polysport/tree/main/google-apps-script)
   * *Rôle :* L'application web finale (Frontend public + Frontend Staff sécurisé par PIN) qui lit les données du Google Sheet.

---

## 🚀 2. Workflow / Mode d'emploi (Comment lancer le tournoi)

Voici les étapes à suivre pour configurer une nouvelle édition :

1. **Configuration (Python)** : Définir le nombre d'équipes et de terrains dans l'outil *Python Scheduler* et lancer la génération.
2. **Import (Google Sheets)** : Copier/Coller le résultat du planning généré dans l'onglet `IMPORT_PLANNING` (ou directement construire la grille dans `AFFICHAGE_FINAL`).
3. **Inscriptions & Staffing (Google Sheets)** : 
   * Centraliser les contacts et effectifs des joueurs dans l'onglet `REF_Equipes`.
   * Gérer les sports et terrains dans `REF_Sports`.
   * Assigner les rôles des bénévoles dans `REF_Benevoles`.
   * Remplir le `PLANNING_GENERAL` pour la timeline de la journée.
4. **Diffusion (App Script)** : Déployer une nouvelle version de l'App Web via Google Apps Script et partager le lien public / QR Code aux participants.

---

## 🛠️ 3. État du projet (Bilan 2026)

**✅ Ce qui fonctionne très bien :**
* **Application "Single Page"** : Les données sont chargées une seule fois à l'ouverture, ce qui rend l'application extrêmement rapide sur mobile, même avec une mauvaise connexion.
* **Sécurité Staff** : Le portail Admin est protégé par un code PIN (`2526`).
* **Intelligence de la Fiche Bénévole** : Le code déduit tout seul le rôle du bénévole (Joueur, Arbitre, Pause) en fonction de l'heure actuelle.
* **Redirection Rapide** : Les boutons intégrés permettent aux arbitres de sauter directement sur la page de leur terrain, et aux joueurs de voir les détails de leur équipe.

**⚠️ Les "Bricolages" actuels (Dette technique) :**
* *Base de données* : Trop de bidouillages de dernière minute avec la feuille Benevole. Alléger et rendre plus compréhensible la DB. 
* *Inscriptions des joueurs et bénévoles* : Nécessite de copier/coller. Il faut automatiser et lier les inscriptions google form à la google sheet en ajoutant des étapes de vérification manuelles (validation paiement et équipe)

---

## 🎯 4. Roadmap & Améliorations pour l'année prochaine

Pour la prochaine édition, voici les chantiers prioritaires pour fluidifier l'organisation :

### A. Refonte de la Base de Données (Google Sheets)
* **Créer un onglet `CONFIG` :** Au lieu de cacher des variables dans l'onglet `PLANNING_GENERAL` ou dans l'en-tête de `REF_Benevoles`, créer un onglet dédié contenant les heures globales (Début du tournoi, Basculement des shifts, Heure de Rangement, Date du tournoi). Le code ira lire ces infos proprement.
* **Supprimer les feuilles inutiles :** Nettoyer le fichier Excel pour ne garder que les onglets strictement lus par l'application (`REF_Equipes`, `REF_Benevoles`, `REF_Sports`, `PLANNING_GENERAL`, `AFFICHAGE_FINAL`).

### B. Automatisation des Inscriptions
* **Lier Google Forms à Google Sheets :** Actuellement, les données des joueurs et bénévoles sont copiées/collées. Il faut lier le formulaire d'inscription directement au fichier du tournoi.
* * **Publipostage :** Une fois les équipes validées, faire un bouton de publipostage pour envoyer par mail les info à toutes les équipes. 

* *Avantage :* Plus de problème d'espaces fantômes ou de fautes de frappe qui "cassent" le lien entre le nom de l'équipe et le planning.

### C. Améliorations du Code (App Script)
* **Dynamiser les équipes "Staff" :** Remplacer le code en dur (`if (staff.shift1.includes("SMUF 1"))`) par une variable lisant une liste d'équipes configurées dans le Google Sheet (ex: Colonne "Équipes Staff" dans l'onglet `CONFIG`).
* **Vue Globale Interactive :** Coder une vraie vue globale du Staff en HTML/JS (au lieu d'une image Excel), générée à partir des données de `REF_Benevoles` pour savoir en temps réel s'il manque un arbitre à un poste.

### D. Le pont Python -> Google Sheets
* Créer un script (Google Apps Script / Python API) qui permet de transférer *automatiquement* la matrice générée par le Scheduler Python vers la feuille `AFFICHAGE_FINAL` sans avoir à faire de la mise en forme manuelle (gestion des sauts de ligne "Équipe A \n VS \n Équipe B").

---
*Document généré à l'issue de l'édition 2026. GLHF pour la prochaine édition !*
