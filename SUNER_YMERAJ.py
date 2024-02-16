from collections import deque
import heapq
import math
import matplotlib.pyplot as plt
import random
import time
import numpy as np

profondeur = 500
heuri = {"heuri_accessibilite": True, "heuri_distance": False, "heuri_score": True, "heuri_borne": False}


def trace(coord_x, coord_y, coord_but, chemin_size, cout):
    plt.plot(coord_x, coord_y, marker='o', linestyle='-', color='b', label='Trajectoire')
    plt.plot(*coord_but, marker='o', markersize=8, color='r', label='But')
    #plt.text(coord_but[0]-20, coord_but[1], , ha='right')
    plt.title('Trace des coordonnées dans le plan Z²\n' + f'Taille du chemin: {chemin_size-1}' + f', Cout: {cout}')
    plt.xlabel('Coordonnée X')
    plt.ylabel('Coordonnée Y')

    # truc pour grille entier
    #plt.xticks(range(min(coord_x), max(coord_x) + 1, 1))
    #plt.yticks(range(min(coord_y), max(coord_y) + 1, 1))


    plt.legend()
    plt.grid(True)
    plt.show()

def afficherPointsEtBut(zone, but, dimensions=2):
    if dimensions == 2:
        coord_x = [point[0] for point in zone]
        coord_y = [point[1] for point in zone]

        plt.scatter(coord_x, coord_y, color='blue', label='Points dans la zone')
        plt.scatter(but[0], but[1], color='red', label='But')

        # truc pour grille entier
        plt.xticks(range(min(coord_x), max(coord_x) + 1, 1))
        plt.yticks(range(min(coord_y), max(coord_y) + 1, 1))

        plt.legend()
        plt.grid(True)
        plt.show()

def successeurs(etat, action):
    add = []
    sub = []
    for i in range(len(etat)):
        add.append(etat[i] + action[i])
        sub.append(etat[i] - action[i])
    return add, sub

def testBut(etat, but):
    for i in range(len(etat)):
        if etat[i] != but[i]:
            return False
    return True

def vecteur_gen(nb_Vecteur, dim, min_val=None, max_val=None):
    if min_val is None:
        min_val = -2**31
    if max_val is None:
        max_val = 2 ** 31

    return [list(np.random.randint(min_val, max_val, dim)) for _ in range(nb_Vecteur)]

def but_gen(dim, min_val=None, max_val=None):
    if min_val is None:
        min_val = -2**31
    if max_val is None:
        max_val = 2 ** 31

    return list(np.random.randint(min_val, max_val, dim))

def distance(etat, but):
    somme = 0
    for i in range(len(etat)):
        somme += (but[i] - etat[i]) ** 2
    return math.sqrt(somme)


def cadran(etat, but):
    for i in range(len(etat)):
        if (etat[i] >= 0) != (but[i] >= 0):
            return False
    return True

def generer_zone(but, nmax):
    demi_cote = int(nmax / 2)
    x, y = but

    sommet1 = (x - demi_cote, y - demi_cote)
    sommet2 = (x + demi_cote, y - demi_cote)
    sommet3 = (x + demi_cote, y + demi_cote)
    sommet4 = (x - demi_cote, y + demi_cote)

    return [sommet1, sommet2, sommet3, sommet4]


def est_dans_zone(successeur, zone):
    x_vals = [sommet[0] for sommet in zone]
    y_vals = [sommet[1] for sommet in zone]

    x_min, x_max = min(x_vals), max(x_vals)
    y_min, y_max = min(y_vals), max(y_vals)

    x, y = successeur
    return x_min <= x <= x_max and y_min <= y <= y_max

def densite(actions, but, zone, nmax):
    points_zone = []

    file = deque()
    file.append(but)

    while file:
        etat = file.popleft()
        for action in actions:
            for successeur in successeurs(etat, action):
                if est_dans_zone(successeur, zone) and successeur not in points_zone:
                    points_zone.append(successeur)
                    file.append(successeur)
    nb_points_zone = len(points_zone)
    densite_zone = nb_points_zone/((nmax+1)**2)
    #print(nb_points_zone, (nmax+1)**2, densite_zone)
    #print(points_zone)
    afficherPointsEtBut(points_zone, but)
    return nb_points_zone, densite_zone

def est_dans_bande(etat_initial, but, successeur, nmax, premier=False):
    xi, yi = etat_initial
    xb, yb = but
    xs, ys = successeur

    borne_min = -nmax if yb >= 0 else nmax  # borne horizontale min
    borne_max = yb + nmax if yb >= 0 else yb - nmax # borne horizontale max

    if xb == xi:  # cas si divise par zero
        if premier:
            x = np.linspace(xi - nmax, xi + nmax, 400)
            #plt.axvline(x=xi, label='Droite principale', color='blue')
            plt.axvline(x=xi + nmax, label='Bande supérieure', linestyle='--', color='green')
            plt.axvline(x=xi - nmax, label='Bande inférieure', linestyle='--', color='green')

            plt.axhline(y=borne_min, label='Borne min', color='orange', linestyle='--')
            plt.axhline(y=borne_max, label='Borne max', color='orange', linestyle='--')

            plt.xlabel('x')
            plt.ylabel('y')
            plt.axhline(0, color='black', linewidth=0.5)
            plt.axvline(0, color='black', linewidth=0.5)
            plt.grid(True)
            #plt.legend()
            plt.title('Tracé des droites avec bande')

        return xi - nmax <= ys <= xi + nmax and (ys <= borne_max if yb >= 0 else ys >= borne_max) and (ys <= borne_min if yb >= 0 else ys >= borne_min)

    else:
        a = (yb - yi) / (xb - xi)
        b = yi - a * xi

        d = nmax / math.sqrt(1 + a**2)  # distance perpendiculairement a la droite, bande de recherche

        g = lambda x: a * x + (b + d)  # fonction definie localement
        h = lambda x: a * x + (b - d)
        #print("h(xs) = ", h(xs), " ys", ys, " g(xs) = ", g(xs))
        #print("ys: ", ys, " born min: ", borne_min, " borne max ", borne_max, " nmax= ", nmax)
        #print(h(xs) <= ys <= g(xs) and (ys <= borne_max if yb >= 0 else ys >= borne_max) and (ys <= borne_min if yb >= 0 else ys >= borne_min))
        #print(h(xs) <= ys <= g(xs))
        #print((ys <= borne_max if yb >= 0 else ys >= borne_max))
        #print((ys >= borne_min if yb >= 0 else ys <= borne_min))
        if premier:
            x = np.linspace(min(xi, xb) - nmax, max(xi, xb) + nmax, 400)
            plt.plot(x, g(x), label='Bande supérieure', linestyle='--', color='green')
            plt.plot(x, h(x), label='Bande inférieure', linestyle='--', color='green')

            plt.axhline(y=borne_min, label='Borne min', color='orange', linestyle='--')
            plt.axhline(y=borne_max, label='Borne max', color='orange', linestyle='--')

            plt.scatter([xi, xb], [yi, yb], color='black')
            plt.text(xi, yi, 'État initial', horizontalalignment='right')
            plt.text(xb, yb, 'But', horizontalalignment='left')

            plt.xlabel('x')
            plt.ylabel('y')
            plt.axhline(0, color='black', linewidth=0.5)
            plt.axvline(0, color='black', linewidth=0.5)
            plt.grid(True)
            #plt.legend()
            plt.title('Tracé des droites avec bande')
        #time.sleep(20)

        return h(xs) <= ys <= g(xs) and (ys <= borne_max if yb >= 0 else ys >= borne_max) and (ys >= borne_min if yb >= 0 else ys <= borne_min)



def accessible(etat_initial, but, actions):
    global profondeur
    cout = 0
    explorer = []
    profondeur_actuelle = 0
    if heuri.get("heuri_score") or heuri.get("heuri_distance"):
        score = 0
        etat = (score, etat_initial, profondeur_actuelle, cout)
        structure = []
        heapq.heappush(structure, (score, etat))
        ei = 1
        prof = 2
        co = 3

    else:
        etat = (etat_initial, profondeur_actuelle, cout)
        structure = deque()
        structure.append(etat)
        ei = 0
        prof = 1
        co = 2

    if heuri.get("heuri_borne") and len(but) == 2:
        norme = [distance(etat_initial, action) for action in actions]
        nmax = 2 * math.ceil(sum(norme))  # taille d'un arete de la zone qui encadre but
        zone = generer_zone(but, nmax)
        densite_zone = densite(actions, but, zone, nmax)[1] * 100
        print("la densite engendre par les vecteur dans le plan est de ", densite_zone, "%")
        if densite_zone == 1.0:
            return True

    while structure:
        if heuri.get("heuri_score") or heuri.get("heuri_distance"):  # on utilise une pile tq sur le sommet les etat les plus proche du but
            score, etat = heapq.heappop(structure)
            if etat[prof] > profondeur:
                continue
        else:
            etat = structure.popleft()
        cout = etat[co]

        if etat[ei] not in explorer:
            explorer.append(etat[ei])

        if testBut(etat[ei], but):
            profondeur = etat[prof]
            print("profondeur max", profondeur)
            return True, cout

        #print(etat)
        #print(structure)
        for action in actions:
            for successeur in successeurs(etat[ei], action):
                cout += 1
                if successeur not in explorer:
                    profondeur_suivante = etat[prof] + 1
                    if heuri.get("heuri_borne"):
                        if est_dans_bande(etat_initial, but, successeur, nmax):
                            if heuri.get("heuri_distance") :
                                score = distance(successeur, but)
                                etat_successeur = (score, successeur, profondeur_suivante, cout)
                                heapq.heappush(structure, (score, etat_successeur))
                            elif heuri.get("heuri_score") :
                                score = distance(successeur, but)/profondeur_suivante
                                etat_successeur = (score, successeur, profondeur_suivante,cout)
                                heapq.heappush(structure, (score, etat_successeur))
                            else:
                                etat_successeur = (successeur, profondeur_suivante, cout)
                                structure.append(etat_successeur)
                    else:
                        if heuri.get("heuri_distance"):
                            score = distance(successeur, but)
                            etat_successeur = (score, successeur, profondeur_suivante, cout)
                            heapq.heappush(structure, (score, etat_successeur))
                        elif heuri.get("heuri_score"):
                            score = distance(successeur, but) / profondeur_suivante
                            etat_successeur = (score, successeur, profondeur_suivante, cout)
                            heapq.heappush(structure, (score, etat_successeur))
                        else:
                            etat_successeur = (successeur, profondeur_suivante, cout)
                            structure.append(etat_successeur)

    return False, cout


def chemin(etat_initial, but, actions):
    premier = True
    global profondeur
    cout = 0
    profondeur_suivante = 0

    if testBut(etat_initial, but):
        return [etat_initial], cout
    etat = etat_initial

    chemin_initial = []
    if heuri.get("heuri_score") or heuri.get("heuri_distance"):
        score = 0
        chemin_etat = (score, etat, profondeur_suivante, chemin_initial, cout)
        structure = []
        heapq.heappush(structure, (score, chemin_etat))
        ei = 1
        prof = 2
        ch = 3
        co = 4
    else:
        chemin_etat = (etat, profondeur_suivante, chemin_initial, cout)
        structure = deque()
        structure.append(chemin_etat)
        ei = 0
        prof = 1
        ch = 2
        co = 3

    if heuri.get("heuri_borne") and len(but) == 2:
        norme = [distance(etat_initial, action) for action in actions]
        nmax = 2 * math.ceil(sum(norme))  # taille d'un arete de la zone qui encadre but
        #print(nmax)
    while structure:
        if heuri.get("heuri_score") or heuri.get("heuri_distance"):  # on utilise une pile tq sur le sommet les etat les plus proche du but
            score, chemin_etat = heapq.heappop(structure)
        else:
            chemin_etat = structure.popleft()
        cout = chemin_etat[co]
        etat = chemin_etat[ei]
        chemin_actuel = chemin_etat[ch]
        chemin_actuel.append(etat)
        profondeur_suivante = chemin_etat[prof] + 1

        if profondeur_suivante > profondeur:
            continue

        print(chemin_etat)
        #print(structure)
        #time.sleep(0.5)
        for action in actions: # a chaque tour on initialise une liste des etat suivant issue de chaque action
            for successeur in successeurs(etat, action): # pour chacun des nouveau etat calculer precedement
                cout += 1
                coupe = False
                chemin_suivant = chemin_actuel.copy()
                if successeur not in chemin_suivant:
                    for r in structure: # evite les boucle
                        if heuri.get("heuri_score") or heuri.get("heuri_distance"):
                            if r[1][ei] == successeur or successeur in r[1][ch]:
                                coupe = True
                                break
                        else:
                            if successeur in r[ch]:
                                coupe = True
                                break
                    if coupe:
                        continue
                    if heuri.get("heuri_borne"):
                        if est_dans_bande(etat_initial, but, successeur, nmax, premier):
                            premier = False
                            if testBut(successeur, but):
                                chemin_suivant.append(successeur)
                                return chemin_suivant, cout
                            elif heuri.get("heuri_distance"):
                                score = distance(successeur, but)
                                chemin_etat = (score, successeur, profondeur_suivante, chemin_suivant, cout)
                                heapq.heappush(structure, (score, chemin_etat))
                            elif heuri.get("heuri_score"):
                                score = distance(successeur, but) / profondeur_suivante
                                chemin_etat = (score, successeur, profondeur_suivante, chemin_suivant, cout)
                                heapq.heappush(structure, (score, chemin_etat))
                            else:
                                chemin_etat = (successeur, profondeur_suivante, chemin_suivant, cout)
                                structure.append(chemin_etat)
                    else:
                        if testBut(successeur, but):
                            chemin_suivant.append(successeur)
                            return chemin_suivant, cout
                        elif heuri.get("heuri_distance"):
                            score = distance(successeur, but)
                            chemin_etat = (score, successeur, profondeur_suivante, chemin_suivant, cout)
                            heapq.heappush(structure, (score, chemin_etat))
                        elif heuri.get("heuri_score"):
                            score = distance(successeur, but) / profondeur_suivante
                            chemin_etat = (score, successeur, profondeur_suivante, chemin_suivant, cout)
                            heapq.heappush(structure, (score, chemin_etat))
                        else:
                            chemin_etat = (successeur, profondeur_suivante, chemin_suivant, cout)
                            structure.append(chemin_etat)

    return [], cout

def main():
    etat_initial = [0,0]
    #actions = vecteur_gen(10, 2, -5, 5)
    #but = but_gen(2, 500, 1000)
    #actions = [[1, 0], [0, 1]]
    #but = [5, 5]
    #but = [7, 7]
    actions = [[2,3],[3,1],[5,5]]
    #but = [10,9]
    but = [63, 72]
    #etat_initial = [0,0,0,0]
    #actions = [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]
    #but = [10,10,10,10]
    print("Configuration:")
    print("Etat de depart: ", etat_initial)
    print("Etat but: ", but)
    print("Liste des action (Vecteur)", actions)
    print("profondeur de recherche max:", profondeur)
    if heuri.get("heuri_accessibilite"):
        temps_debut = time.time()
        acc, cout_acc = accessible(etat_initial, but, actions)
        temps_fin = time.time()
        temps_ecoule = temps_fin - temps_debut
        print("temps de la recherche d'accessibiliter: ", temps_ecoule)
        if not acc:
            print("Dans cette configuration le but n'est pas accessible")
            return -1
        print("Dans cette configuration le but est accessible")
        print("Cout de la recherche d'accessibilite: ", cout_acc)
    temps_debut = time.time()
    ch, cout_ch = chemin(etat_initial, but, actions)
    temps_fin = time.time()
    temps_ecoule = temps_fin - temps_debut
    print("temps de la recherche d'un chemin: ", temps_ecoule)
    if ch:
        print("Chemin trouvé :", ch)
        print("Cout de la recherche du chemin: ", cout_ch)
        if len(etat_initial) == 2:
            x = [c[0] for c in ch]
            y = [c[1] for c in ch]
            trace(x, y, but, len(y), cout_ch)
    else:
        print("pas de solution")



main()

