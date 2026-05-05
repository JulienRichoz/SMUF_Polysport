import pandas as pd
import re

def verify_schedule(filename):
    print(f"--- Vérification du calendrier : {filename} ---")
    
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"❌ ERREUR : Le fichier {filename} est introuvable.")
        return

    # Calcul des attentes
    total_timeslots = len(df)
    expected_games = total_timeslots // 2
    
    print(f"Nombre total de timeslots : {total_timeslots}")
    print(f"Chaque équipe doit jouer exactement : {expected_games} matchs\n")

    # Initialisation du compteur de matchs pour les équipes 1 à 80
    games_per_team = {i: 0 for i in range(1, 81)}
    errors_found = False

    # Parcours de chaque ligne (time slot)
    for index, row in df.iterrows():
        timeslot = row['time slot']
        teams_in_current_slot = set()
        
        # Parcours de chaque colonne (stade/match)
        for col in df.columns:
            if col != 'time slot':
                val = str(row[col])
                if 'vs' in val:
                    # Extraction des numéros des équipes
                    teams = re.findall(r'\d+', val)
                    
                    for t in teams:
                        team_num = int(t)
                        
                        # Règle 1 : Ne pas jouer deux fois dans le même timeslot
                        if team_num in teams_in_current_slot:
                            print(f"❌ ERREUR : L'équipe {team_num} est programmée plusieurs fois lors du timeslot {timeslot} !")
                            errors_found = True
                        
                        teams_in_current_slot.add(team_num)
                        
                        # Ajout au compteur total de l'équipe
                        if team_num in games_per_team:
                            games_per_team[team_num] += 1
                        else:
                            games_per_team[team_num] = 1 # Si par hasard une équipe > 80 existe

    # Règle 2 : Vérifier que chaque équipe (1 à 80) joue exactement expected_games fois
    for team_num in range(1, 81):
        played = games_per_team.get(team_num, 0)
        if played != expected_games:
            print(f"❌ ERREUR : L'équipe {team_num} a joué {played} matchs au lieu de {expected_games} !")
            errors_found = True

    # Bilan final
    print("-" * 40)
    if not errors_found:
        print("✅ SUCCÈS : Le calendrier est parfait ! Aucune erreur détectée.")
        print("- Aucune équipe ne joue en double sur un time slot.")
        print("- Toutes les équipes ont un nombre parfaitement équitable de matchs.")
    else:
        print("⚠️ ÉCHEC : Le calendrier contient des erreurs (voir ci-dessus).")

if __name__ == "__main__":
    # Nom du fichier généré précédemment à vérifier
    nom_du_fichier = 'tournament_schedule_80.csv'
    verify_schedule(nom_du_fichier)