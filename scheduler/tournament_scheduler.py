import csv
import cvxpy as cp
import numpy as np
import math

def solve_pool(N_pool, stadiums_per_sport):
    S = len(stadiums_per_sport)
    M = S  # 1 match par sport
    max_concurrent = sum(stadiums_per_sport) * 2
    
    # Calcul dynamique du nombre de time slots minimum pour ce pool
    T = math.ceil((N_pool * M) / max_concurrent)
    
    # Vérification que la capacité par sport est suffisante
    for s in range(S):
        if (N_pool / 2) > (T * stadiums_per_sport[s]):
            T = math.ceil((N_pool / 2) / stadiums_per_sport[s])
            
    print(f"--- Résolution pour un Pool de {N_pool} équipes sur {T} timeslots ---")
    
    x = cp.Variable((N_pool, N_pool, T, S), boolean=True)
    constraints = []

    # 1. Pas de match contre soi-même
    for i in range(N_pool):
        constraints.append(x[i, i, :, :] == 0)

    # 2. Symétrie
    for i in range(N_pool):
        for j in range(i+1, N_pool):
            constraints.append(x[i, j, :, :] == x[j, i, :, :])

    # 3. Chaque équipe joue AU PLUS UN match par timeslot (permet des pauses dynamiques)
    for i in range(N_pool):
        for t in range(T):
            constraints.append(cp.sum(x[i, :, t, :]) <= 1)

    # 4 & 5. Chaque équipe joue EXACTEMENT 1 match par sport (soit 10 matchs au total)
    for i in range(N_pool):
        for s in range(S):
            constraints.append(cp.sum(x[i, :, :, s]) == 1)

    # 6. Pas de match en double contre la même équipe
    for i in range(N_pool):
        for j in range(i+1, N_pool):
            constraints.append(cp.sum(x[i, j, :, :]) <= 1)

    # 7. Limite de stades par sport et par timeslot
    for s in range(S):
        for t in range(T):
            constraints.append(cp.sum(x[:, :, t, s]) / 2 <= stadiums_per_sport[s])

    # Résolution (l'objectif est 0 car on cherche juste une solution faisable, ce qui accélère Gurobi)
    prob = cp.Problem(cp.Minimize(0), constraints)
    prob.solve(solver=cp.GUROBI, verbose=True, Threads=8)

    if prob.status in ["optimal", "feasible"]:
        return np.round(x.value).astype(int), T
    else:
        return None, T

def export_interleaved_csv(sched_A, sched_B, N_A, N_B, filename, stadiums_per_sport):
    S = len(stadiums_per_sport)
    T_A = sched_A.shape[2]
    T_B = sched_B.shape[2]
    
    column_headers = ["time slot"]
    for s in range(S):
        for st in range(stadiums_per_sport[s]):
            column_headers.append(f"sport{s+1}_stadium{st+1}")
            
    rows = []
    t_a, t_b = 0, 0
    current_timeslot = 1
    
    # Intercalage automatique des deux pools
    while t_a < T_A or t_b < T_B:
        if t_a < T_A:
            rows.append(build_row(sched_A, t_a, current_timeslot, S, stadiums_per_sport, offset=0))
            current_timeslot += 1
            t_a += 1
            
        if t_b < T_B:
            # L'offset N_A permet aux équipes du Pool B de commencer à N_A + 1 (ex: team47)
            rows.append(build_row(sched_B, t_b, current_timeslot, S, stadiums_per_sport, offset=N_A))
            current_timeslot += 1
            t_b += 1
            
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(column_headers)
        writer.writerows(rows)
    print(f"\n✅ Fichier généré : {filename} avec {current_timeslot - 1} timeslots.")

def build_row(schedule, t, timeslot_label, S, stadiums_per_sport, offset):
    N = schedule.shape[0]
    slots = {f"sport{s+1}": ["" for _ in range(stadiums_per_sport[s])] for s in range(S)}
    stadium_usage = {s: 0 for s in range(S)}
    
    for i in range(N):
        for j in range(i+1, N):
            for s in range(S):
                if schedule[i, j, t, s] == 1:
                    c_slot = stadium_usage[s]
                    if c_slot < stadiums_per_sport[s]:
                        slots[f"sport{s+1}"][c_slot] = f"team{i+1+offset} vs team{j+1+offset}"
                        stadium_usage[s] += 1
    row = [timeslot_label]
    for s in range(S):
        row.extend(slots[f"sport{s+1}"])
    return row

def generate_tournament(N_total, stadiums_per_sport):
    if N_total % 2 != 0:
        print("❌ ERREUR: Le nombre d'équipes (N) doit être un chiffre pair.")
        return

    # Séparation en deux Pools, en s'assurant que chaque pool est PAIR
    N_A = N_total // 2
    if N_A % 2 != 0:
        N_A += 1
    N_B = N_total - N_A

    print(f"🔄 Équipes totales : {N_total}. Division en Pool A ({N_A}) et Pool B ({N_B})")
    
    sched_A, T_A = solve_pool(N_A, stadiums_per_sport)
    if sched_A is None:
        print("❌ Échec de la génération pour le Pool A")
        return
        
    sched_B, T_B = solve_pool(N_B, stadiums_per_sport)
    if sched_B is None:
        print("❌ Échec de la génération pour le Pool B")
        return
        
    export_interleaved_csv(sched_A, sched_B, N_A, N_B, f"tournament_schedule_{N_total}.csv", stadiums_per_sport)

if __name__ == '__main__':
    N = 80  # Nombre de terrains, doit être pair (au preferable N = 4* nbTerrains)
    sports = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2] # 10 sports, 2 terrains
    generate_tournament(N, sports)