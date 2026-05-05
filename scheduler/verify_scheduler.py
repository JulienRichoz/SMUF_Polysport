"""
=============================================================================
SMUF Polysport - Vérificateur de Calendrier (Scheduler Verifier)
=============================================================================
Ce script analyse un fichier CSV contenant un planning généré pour s'assurer 
de sa validité mathématique et de son équité.

Vérifications effectuées :
1. Ubiquité : Aucune équipe ne joue deux matchs sur le même créneau horaire.
2. Équité du temps de jeu : Chaque équipe joue exactement le même nombre de matchs.
3. Diversité : Chaque équipe joue au moins une fois à tous les sports disponibles.
=============================================================================
"""

import pandas as pd
import re

def verify_schedule(filename):
    print(f"--- Vérification du calendrier : {filename} ---")
    
    # 1. Chargement du fichier CSV
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"❌ ERREUR : Le fichier {filename} est introuvable.")
        return

    # 2. Calcul des constantes globales attendues
    total_timeslots = len(df)
    expected_games = total_timeslots // 2  # Une équipe joue 1 match sur 2 (ou repose 1 fois sur 2)

    # Récupération des colonnes contenant les matchs (exclusion de la colonne temps)
    raw_columns = [col for col in df.columns if col.lower() != 'time slot']
    
    # Extraction dynamique de la liste de tous les sports (ex: 'sport1_stadium1' -> 'sport1')
    all_sports = set()
    for col in raw_columns:
        sport_generic_name = col.split('_')[0].strip()
        all_sports.add(sport_generic_name)

    # Dictionnaire principal de suivi des données par équipe
    # Structure : { numero_equipe: {'matchs_joues': int, 'sports_joues': set()} }
    teams_data = {}
    errors_found = False

    # 3. Analyse détaillée du planning (Ligne par Ligne)
    for index, row in df.iterrows():
        timeslot = row.get('time slot', f"Ligne {index}")
        teams_in_current_slot = set()  # Permet de vérifier l'ubiquité sur le timeslot actuel
        
        # Parcours de chaque terrain (colonne)
        for col in raw_columns:
            val = str(row[col])
            
            # Si la cellule contient un match (présence du mot 'vs')
            if 'vs' in val.lower(): 
                # Extraction sécurisée des numéros d'équipes (ex: "Equipe 12 vs 14" -> [12, 14])
                teams = re.findall(r'\d+', val)
                
                # Identification du sport pour la colonne actuelle
                sport_name = col.split('_')[0].strip()
                
                for t in teams:
                    team_num = int(t)
                    
                    # Initialisation des statistiques de l'équipe si c'est sa première apparition
                    if team_num not in teams_data:
                        teams_data[team_num] = {'matchs_joues': 0, 'sports_joues': set()}
                    
                    # RÈGLE 1 : Vérification de l'ubiquité (pas de double match en simultané)
                    if team_num in teams_in_current_slot:
                        print(f"❌ ERREUR UBIQUITÉ : L'équipe {team_num} est programmée plusieurs fois lors du timeslot {timeslot} !")
                        errors_found = True
                    
                    teams_in_current_slot.add(team_num)
                    
                    # Mise à jour des compteurs de l'équipe
                    teams_data[team_num]['matchs_joues'] += 1
                    teams_data[team_num]['sports_joues'].add(sport_name)

    # 4. Bilan Global et Vérification des règles de fin de tournoi
    if not teams_data:
        print("❌ ERREUR : Aucune équipe valide n'a été détectée dans le fichier CSV.")
        return
        
    # Le numéro d'équipe le plus élevé définit le nombre total d'équipes attendues
    total_teams = max(teams_data.keys())
    
    print(f"Nombre d'équipes détectées : {total_teams}")
    print(f"Nombre total de timeslots : {total_timeslots}")
    print(f"Chaque équipe doit jouer exactement : {expected_games} matchs")
    print(f"Catégories de sports détectées ({len(all_sports)}) : {', '.join(all_sports)}\n")

    # Parcours séquentiel de l'équipe 1 à N pour garantir qu'aucune équipe ne manque à l'appel
    for team_num in range(1, total_teams + 1):
        # Vérification si l'équipe a été totalement "oubliée" par le scheduler
        if team_num not in teams_data:
            print(f"❌ ERREUR CRITIQUE : L'équipe {team_num} n'a AUCUN match programmé dans tout le tournoi !")
            errors_found = True
            continue
            
        data = teams_data[team_num]
        played = data['matchs_joues']
        sports_played = data['sports_joues']
        
        # RÈGLE 2 : Équité parfaite du nombre total de matchs
        if played != expected_games:
            print(f"❌ ERREUR ÉQUITÉ : L'équipe {team_num} a joué {played} matchs au lieu de {expected_games} !")
            errors_found = True
            
        # RÈGLE 3 : Diversité des sports (Soustraction des ensembles pour trouver les sports manquants)
        missing_sports = all_sports - sports_played
        if missing_sports:
            print(f"❌ ERREUR DIVERSITÉ : L'équipe {team_num} n'a pas joué aux sports suivants : {', '.join(missing_sports)}")
            errors_found = True

    # 5. Rendu Final
    print("-" * 50)
    if not errors_found:
        print("✅ SUCCÈS : Le calendrier est parfait ! Aucune anomalie détectée.")
        print("  - L'ubiquité est respectée (Aucun doublon simultané).")
        print("  - L'équité est respectée (Temps de jeu strictement identique).")
        print("  - La rotation est respectée (Chaque sport est joué au moins une fois).")
    else:
        print("⚠️ ÉCHEC : Le calendrier est invalide. Veuillez corriger les erreurs ci-dessus.")

if __name__ == "__main__":
    # Nom du fichier généré par le scheduler à analyser
    nom_du_fichier = 'PolysportGames_Matches_2026 - IMPORT_Planning.csv'
    verify_schedule(nom_du_fichier)
