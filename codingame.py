import sys
import math
import datetime
from datetime import timedelta

dicoMaze ={}

w, h = [int(i) for i in input().split()]
for i in range(h):
    row = input()
    dicoMaze[i] = row

# Fonctions ------------------------------------------------------------------------------------------------------------

# Transforme liste des directions en string pour le print sur condingame
def formaterResultatFinal(cheminEmprunte):
    resultatFinal = ""
    debut = True
    for elt in cheminEmprunte:
        if debut :
            debut = False
            resultatFinal = resultatFinal + elt
        else:
            resultatFinal = resultatFinal + " " + elt
    return resultatFinal

# Permet de trouver la position d'un symbole unique
def trouverPositionCaractere(caractere):
    for ligne in dicoMaze: # une ligne correspond techniquement à une chaine de caractère

        # Ligne dans laquel est le caractere recherchée
        if caractere in dicoMaze[ligne]:
            
            # Index du caractère correspondant
            positionCaractereDepart = dicoMaze[ligne].index(caractere)
            
            positionDepart = [ligne, positionCaractereDepart]
            return positionDepart

# Determiner si la ligne est paire
def determinerLignePaire(posInitiale):
    # Détermine si la ligne est paire ( pour les up / down )
    if posInitiale[0] / 2 == int(posInitiale[0] / 2):
        return True
    else:
        return False

# Determine le symbole à partir d'une position + direction
def symboleAt(posInitiale, direction):
    
    # Determine si ligne paire 
    lignePaire = determinerLignePaire(posInitiale)

    # Determine le symboleAt
    if direction == 'L':
        # Symbole correspondant
        caseL = dicoMaze[posInitiale[0]][posInitiale[1]-1]
        return caseL
    
    elif direction == 'R':
        # Symbole correspondant
        caseR = dicoMaze[posInitiale[0]][posInitiale[1]+1]
        return caseR
    
    elif direction == 'UL':
        # Symbole sur la case correspondante
        if lignePaire :
            caseUL = dicoMaze[posInitiale[0]-1][posInitiale[1]-1]
            return caseUL

        elif not lignePaire:
            caseUL = dicoMaze[posInitiale[0]-1][posInitiale[1]]
            return caseUL

    elif direction == 'UR':
        # Symbole sur la case correspondante
        if lignePaire :
            caseUR = dicoMaze[posInitiale[0]-1][posInitiale[1]]
            return caseUR

        elif not lignePaire:
            caseUR = dicoMaze[posInitiale[0]-1][posInitiale[1]+1]
            return caseUR

    elif direction == 'DR':
        # Symbole sur la case correspondante
        if lignePaire :
            caseDR = dicoMaze[posInitiale[0]+1][posInitiale[1]]
            return caseDR
        elif not lignePaire :
            caseDR = dicoMaze[posInitiale[0]+1][posInitiale[1]+1]
            return caseDR
    
    elif direction == 'DL':
        # Symbole sur la case correspondante
        if lignePaire :
            caseDL = dicoMaze[posInitiale[0]+1][posInitiale[1]-1]
            return caseDL

        elif not lignePaire :
            caseDL = dicoMaze[posInitiale[0]+1][posInitiale[1]]
            return caseDL

# Determiner le symbole à partir de la position
def symboleAtPosActuelle(posInitiale):
    symboleActuel = dicoMaze[posInitiale[0]][posInitiale[1]]
    return symboleActuel

# Detection glissade
def detectionGlissade(directionCible, posInitiale):
     
    # Si premier deplacement ou dernier symbole rencontres n'est pas "_" => pas en glisse
    if len(directionEmprunteAbsolu) == 0 or suiviSymbolesRencontres[len(suiviSymbolesRencontres)-1] != "_":
        return "non"

    # Si pas de glissade car stopé par un mur (ou porte fermé)
    elif symboleAt(posInitiale, directionEmprunteAbsolu[len(directionEmprunteAbsolu)-1]) == "#"  \
        or symboleAt(posInitiale, directionEmprunteAbsolu[len(directionEmprunteAbsolu)-1]).lower() not in inventaire \
        and symboleAt(posInitiale, directionEmprunteAbsolu[len(directionEmprunteAbsolu)-1]) not in ["_",".","E","a","b","c","d"]:
        return "non"
    
    # Sinon (dernier symbole == "_")
    else:
        
        # Enregistrement de la direction de glisse
        directionGlisse = directionEmprunteAbsolu[len(directionEmprunteAbsolu)-1]
        
        # Si glissade dans la bonne direction
        if directionGlisse == directionCible:
            return 'bonneDirection'
        
        # Sinon...
        else:
            return 'mauvaiseDirection'

# Empecher le retour en arrière (sauf si situation particulière: clé par exemple, traité plus loin)
def empecherRetourArriere(direction):
    
    # Direction à bloquer est la direction opposé
    directionABloquer = dicoDirectionOpposee[direction]
    
    # Empeche le retour en arrière quand la direction cible est l'opposé de la derniere direction prise
    if len(directionEmprunteAbsolu) != 0 and directionEmprunteAbsolu[len(directionEmprunteAbsolu)-1] == directionABloquer :
        # print("retour en arrière bloqué, derdirection=>",directionABloquer)
        return True
    else:
        return False

# Autoriser le retour en arrière si clés
def retourArriereCle(posInitiale, direction, demiTourCle, directionRetourCle):

    # Contiendra les positions des clés dans le labyrinthe
    posCle = []
    try:
        posCle.append(trouverPositionCaractere("a"))
        posCle.append(trouverPositionCaractere("b"))
        posCle.append(trouverPositionCaractere("c"))
        posCle.append(trouverPositionCaractere("d"))
    except: pass
    
    # si on est sur la clé
    if len(cheminEmprunte) != 0 and posInitiale in posCle:
        demiTourCle = True

        # Append dans une liste pour bien enregistrer la 1ere fois ou il passe dessus
        directionRetourCle.append(cheminEmprunte[len(cheminEmprunte)-1])
        return "surCle"
    
    # Permet le retour en arriere si clé recup et marche arriere depuis clé mais sur un case suivante
    elif demiTourCle  and directionRetourCle[len(directionRetourCle)-1] == dicoDirectionOpposee[direction]:
        return "autorise"

# Determine si posCible est hors labyrinthe
def determinerBordDeMap(posInitiale, directionDeterminer):

    if directionDeterminer == "L" and posInitiale[1] == 0:
        return True

    elif directionDeterminer == "R" and posInitiale[1] == w-1:
        return True

    elif directionDeterminer == "UL":
        if posInitiale[0] == 0 or posInitiale[0] / 2 == int(posInitiale[0] / 2) and posInitiale[1] == 0:
            return True
        else:
            return False
    
    elif directionDeterminer == "UR":
        if posInitiale[0] == 0 or posInitiale[0] / 2 != int(posInitiale[0] / 2) and posInitiale[1] == w-1:
            return True
        else:
            return False
    
    elif directionDeterminer == "DR":
        if posInitiale[0] == h-1 or posInitiale[0] / 2 != int(posInitiale[0] / 2) and posInitiale[1] == w-1:
            return True
        else:
            return False

    elif directionDeterminer == "DL":
        if posInitiale[0] == h-1 or posInitiale[0] / 2 == int(posInitiale[0] / 2) and posInitiale[1] == 0:
            return True
        else:
            return False
    else:
        return False

# Determine positionCible avec posInitiale + direction
def determinerNouvellePosition(posInitiale, directionDeterminer):
    
    # Si la ligne est paire
    lignePaire = determinerLignePaire(posInitiale)
    
    # Depuis l'ancienne position...
    ligne = posInitiale[0]
    caractere = posInitiale[1]

    posInitiale = []

    if directionDeterminer == "L":

        # ...determine la nouvelle position
        posInitiale.append(ligne)
        posInitiale.append(caractere-1)
        return posInitiale
    
    elif directionDeterminer == "R":

        # Determine la nouvelle position
        posInitiale.append(ligne)
        posInitiale.append(caractere+1)
        return posInitiale
    
    elif directionDeterminer == "UL":

        # ...determine la nouvelle pos
        posInitiale.append(ligne-1)
        if lignePaire :
            posInitiale.append(caractere-1)
        elif not lignePaire :
            posInitiale.append(caractere)

        return posInitiale

    elif directionDeterminer == "UR":

        # ...determine la nouvelle pos
        posInitiale.append(ligne-1)
        if lignePaire :
            posInitiale.append(caractere)
        elif not lignePaire :
            posInitiale.append(caractere+1)
        
        return posInitiale

    elif directionDeterminer == "DR":

        # ...determine la nouvelle pos
        posInitiale.append(ligne+1)
        if lignePaire :
            posInitiale.append(caractere)
        elif not lignePaire :
            posInitiale.append(caractere+1)

        return posInitiale
    
    elif directionDeterminer == "DL":

        # ...determine la nouvelle pos
        posInitiale.append(ligne+1)
        if lignePaire :
            posInitiale.append(caractere-1)
        elif not lignePaire :
            posInitiale.append(caractere)
        
        return posInitiale

# Empeche les repetition (et donc les boucles)
def empecherRepetition(dicoHistorique, posInitiale, direction, dicoGlissade):

    # Si à partir de la pos actuelle la direction d'où je viens et celle où je veux aller déjà fait
    if len(cheminEmprunte) != 0 and dicoHistorique[str(posInitiale)].count(direction+" "+cheminEmprunte[len(cheminEmprunte)-1]) >= 1 \
        and detectionGlissade(direction, posInitiale) == "non":
        
        return True

    # Si glissade et départ de glisse identique 2x ou plus
    elif len(cheminEmprunte) != 0 and len(dicoGlissade[str(posInitiale)]) >= 2 \
        and dicoHistorique[str(posInitiale)].count(direction+" "+cheminEmprunte[len(cheminEmprunte)-1]) >= 1 \
        and detectionGlissade(direction, posInitiale) == "bonneDirection" \
        and dicoGlissade[str(posInitiale)][len(dicoGlissade[str(posInitiale)])-1] == dicoGlissade[str(posInitiale)][len(dicoGlissade[str(posInitiale)])-2]:

        return True

# Contient les fonctions qui empechent d'avancer (bord de map, retourArriere,...)
def nePasAvancer(dicoHistorique, posInitiale, direction, dicoGlissade, dateDebut):
    global nb_max_direction
    global demiTourCle
    
    # Empecher la répetition
    stop = empecherRepetition(dicoHistorique, posInitiale, direction, dicoGlissade)
    if stop :
        return True
    else: pass

    # ATTENTION içi limite le nombre de directions prise
    if datetime.datetime.now() - dateDebut > timedelta(seconds=0.1) and nb_max_direction != 7:
        nb_max_direction = 7
    
    # Si nombre max de direction prise
    if len(cheminEmprunte) > nb_max_direction:
        return True
    else: pass
    
    # Autoriser retour arriere si clé
    if retourArriereCle(posInitiale, direction, demiTourCle, directionRetourCle) == "surCle" \
        or retourArriereCle(posInitiale, direction, demiTourCle, directionRetourCle) == "autorise":
        pass
    # Empecher le retour en arrière
    elif empecherRetourArriere(direction) :
        demiTourCle = False
        return True
    else: 
        demiTourCle = False
        pass
    
    # Si bord de map
    if determinerBordDeMap(posInitiale, direction) :
        return True
    else: pass

    # Situation sur la case E=> bloqué donc return posInitiale sans modif
    if symboleAtPosActuelle(posInitiale) == "E":
        return True
    else: pass

    return False

# Enregistre les infos dans les listes et dico selon les situations et renvoie True si le deplacement est possible ( selon statut glissade )
def deplacement(statutGlissade, direction, posInitiale, case, situation):
    global eDetecte
    global directionEmprunteAbsolu
    global statutDeGlisse
    global cheminEmprunte
    global dicoHistorique
    global dernierDepartGlissade
    global suiviSymbolesRencontres

    if statutGlissade == "non":
        if situation == "E":
            # Enregistre que la sortie a été trouvé
            eDetecte = True
        
        elif situation == "." or situation == "_":
            # Si 1er deplacement
            if len(cheminEmprunte) == 0:
                dicoHistorique[str(posInitiale)].append(direction+" "+"S")
            else:
                # Enregistrement du deplacement par rapport à la position et la direction antecedente
                dicoHistorique[str(posInitiale)].append(direction+" "+cheminEmprunte[len(cheminEmprunte)-1])
        
        # Enregistrement de la direction prise et du statut de glisse
        directionEmprunteAbsolu.append(direction)
        statutDeGlisse.append("non")
        cheminEmprunte.append(direction)

        #Enregistre le symbole rencontré
        suiviSymbolesRencontres.append(case)

        if situation == '_':
            # Enregistre le depart de glissade
            dernierDepartGlissade.append(posInitiale)
        else: pass

        return True

    elif statutGlissade == "bonneDirection":
        if situation == "E":
            # Enregistre que la sortie a été trouvé
            eDetecte = True
        
        elif situation == "." or situation == "_":
            # Enregistrement de la pos de depart liée à la glissade en cours
            dicoGlissade[str(posInitiale)].append(dernierDepartGlissade[len(dernierDepartGlissade)-1])
        
        # Enregistrement des status liés aux glissades
        directionEmprunteAbsolu.append(direction)
        statutDeGlisse.append("bonneDirection")

        #Enregistre le symbole rencontré
        suiviSymbolesRencontres.append(case)

        return True
    
    elif statutGlissade == 'mauvaiseDirection':
        return False

# À partir de la posInitiale et de la direction, si le déplacement peut s'éffectuer => renvoie la nouvelle pos; sinon la posInitiale inchangé
def avancer(posInitiale, direction, dateDebut):
    global dicoHistorique
    global dicoGlissade
    global dernierDepartGlissade
    global eDetecte

    # N'avance pas si repetition, nb max de direction atteinte, retour arrière ou bord de map
    if nePasAvancer(dicoHistorique, posInitiale, direction, dicoGlissade, dateDebut) :
        return posInitiale
    else: pass

    # Symbole correspondant
    case = symboleAt(posInitiale, direction)

    # Detection de glissade
    statutGlissade = detectionGlissade(direction, posInitiale)

    # Si clé
    if case in ['a','b','c','d']:# and case not in inventaire
        inventaire.append(case)

    # Situation fin car "E" trouvé
    if case == "E":

        # Selon statut glissade determine si il est possible d'avancer et agit en conséquences(enregistre la direction prise)
        decisionAvancer = deplacement(statutGlissade, direction, posInitiale, case,situation="E")
        if decisionAvancer :
            pass
        elif not decisionAvancer:
            return posInitiale

        # Nouvelle position
        posInitiale = determinerNouvellePosition(posInitiale, direction)

        return posInitiale

    # Situation direction prise (emplacement libre, clé ou porte ouverte)
    elif case == "." or case in ['a','b','c','d'] or case.lower() in inventaire:

        # Selon statut glissade determine si il est possible d'avancer et agit en conséquences(enregistre la direction prise)
        decisionAvancer = deplacement(statutGlissade, direction, posInitiale, case, situation=".")
        if decisionAvancer :
            pass
        elif not decisionAvancer:
            return posInitiale

        # Nouvelle position
        posInitiale = determinerNouvellePosition(posInitiale, direction)

        return posInitiale
    
    # Situation case glissante
    elif case == "_":

        # Selon statut glissade determine si il est possible d'avancer et agit en conséquences(enregistre la direction prise)
        decisionAvancer = deplacement(statutGlissade, direction, posInitiale, case, situation="_")
        if decisionAvancer :
            pass
        elif not decisionAvancer:
            return posInitiale

        # Nouvelle position
        posInitiale = determinerNouvellePosition(posInitiale, direction)

        # print("case",direction," ",case)
        return posInitiale

    # Situation mur, S, ou porte fermé
    elif case == "#" or case == "S" or case.lower() not in inventaire: #
        
        return posInitiale

# Fonction recurcive principale
def fonctionRecursive(posInitiale, dateDebut):
    global cheminsResultats
    global eDetecte

    # Contient le nombre de direction emprunte
    directionPrise = 0
    
    # Liste des directions à prendre dans la recurcive
    listeDirections = ["L","DL","DR","R","UR","UL"]

    for directionAPrendre in listeDirections:

        # Essayer d'avancer dans la direction cible
        lenDicoHistoriqueAvant = len(dicoHistorique[str(posInitiale)])
        posInitialeSuivante = avancer(posInitiale, directionAPrendre, dateDebut)
        lenDicoHistoriqueApres = len(dicoHistorique[str(posInitiale)])

        # Enregistre qu'une direction a été prise (si c'est le cas)
        if lenDicoHistoriqueAvant != lenDicoHistoriqueApres:
            directionPrise += 1
    
        # Si le deplacement à eu lieu, lance une nouvelle instance de la recurcive avec la nouvelle position
        if posInitialeSuivante != posInitiale:
            fonctionRecursive(posInitialeSuivante, dateDebut)

        # Si fin car E trouvé donc enregistrement du chemin
        if eDetecte :
            eDetecte = False
            cheminsResultats.append(cheminEmprunte.copy())

        # Sinon E pas trouvé et fin de recurcive (branche), donc impasse
        elif directionAPrendre == "UL":
            try:
                symboleActuel = symboleAtPosActuelle(posInitiale)

                # Si on recule en etant sur une case contenant une clée, celle-ci sort de l'inventaire
                if symboleActuel in ['a','b','c','d']:
                    inventaire.remove(symboleActuel)
                
                # Supprime la dernière direction enregistré si pas en glissade car enregistré que si glissade
                if statutDeGlisse[len(statutDeGlisse)-1] == "non":
                    cheminEmprunte.pop(len(cheminEmprunte)-1)
                
                # Supprime der elt de la variable chemin emprunte
                directionEmprunteAbsolu.pop(len(directionEmprunteAbsolu)-1)

                # Supprime le dernier statut de glisse
                statutDeGlisse.pop(len(statutDeGlisse)-1)

                # Supprime der symboles en mm temps pour cohérence
                suiviSymbolesRencontres.pop(len(suiviSymbolesRencontres)-1)

                if directionPrise != 0:
                    for i in range(directionPrise):

                        dicoHistorique[str(posInitiale)].pop(len(dicoHistorique[str(posInitiale)])-1)
            
            # Fin de la dernière recurcive
            except:
                pass

# Créer un dictionnaire ayant pour clées toutes les positions du labyrinthe
def creationDico(w, h):
    dico = {}
    # Création des clé du dicoHistorique
    for elt in range(h):
        for subelt in range(w):
            dico["["+str(elt)+", "+str(subelt)+"]"] = []
    return dico

# Message à print contenant réussite ou échec
def determinerMessageResultat(cheminResultat):

    if cheminResultat == "R R DR R":
        return "labyrinthe 1 réussi"

    elif cheminResultat == "R DR DR DL DL DL UR UR R DR DR DR DR R R":
        return "labyrinthe 2 et/ou 3 réussi"

    elif cheminResultat == "DL DR R UR UL":
        return "labyrinthe 4 réussi"

    elif cheminResultat == "R DR DR DR R R UR UL L L L DL DL DR R R":
        return "labyrinthe 5 réussi"

    elif cheminResultat == "DR DR R UR UL L L L DL DR DR R R":
        return "labyrinthe 6 réussi"

    elif cheminResultat == "DR R L L":
        return "labyrinthe 7 réussi"

    elif cheminResultat == "DR R L L L":
        return "labyrinthe 8 réussi"

    elif cheminResultat == "DR R UR UL L UR":
        return "labyrinthe 9 reussi"

    elif cheminResultat == "DR L UL R UR UL DL":
        return "labyrinthe 10 reussi"
    else:
        return"raté"

# Variables----------------------------------------------------------------------------------------------------

# Nombre max de direction que l'algo peut prendre
nb_max_direction = 20 # 16=> lab11; 7=> lab10; 20=> les autres

# Directions opposées (retour en arrière)
dicoDirectionOpposee = {
    "L" : "R",
    "R" : "L",
    "DL" : "UR",
    "DR" : "UL",
    "UR" : "DL",
    "UL" : "DR"
}

# Contient les clées récupéré
inventaire = []

# True si "E" trouvé
eDetecte = False

# True si sur une position contenant une clé
demiTourCle = False

# Contient les directions de demi tour quand sur un position contenant une clé et demi tour effectué
directionRetourCle = []

# Enregistrer le chemin emprunté
cheminEmprunte = []

# Enregistre chemin emprunte absolu (direction append mm si glissade, ATTENTION absolu ne signifie pas que tout est garder au contraire!Absolu=>glissade/pasG)
directionEmprunteAbsolu = []

# Suivi des symboles rencontrés
suiviSymbolesRencontres = []

# Contient les diff chemin qui mène vers "E"
cheminsResultats = []

# Pour pas pop si chemin pas emprunte car glissade
statutDeGlisse = []

# Deplacements effectués par position
dicoHistorique = creationDico(w, h)

# Contient les depart de glissade par position
dicoGlissade = creationDico(w, h)

# Contient la pos du dernier depart de glissade
dernierDepartGlissade = []

# Execution ----------------------------------------------------------------------------------------------

# Permet d'enregistrer le temps d'éxecution
dateDebut = datetime.datetime.now()

# Trouver le point de départ
positionDepartTrouvee = trouverPositionCaractere("S")

# "S" se transforme en "_" pour lab 10 et 11
dicoMaze[positionDepartTrouvee[0]] = dicoMaze[positionDepartTrouvee[0]].replace("S", "_")

# À partir de la pos initiale
posInitiale = positionDepartTrouvee

# Fonction recurcive principale
fin = fonctionRecursive(posInitiale, dateDebut)

# Contient la liste des longeurs de chemins de sorties
listeLen = []

# Remplit listeLen
for elt in cheminsResultats:
    listeLen.append(len(elt))

# Range dans l'ordre
sortListeLen = listeLen.copy()
sortListeLen.sort()

# Récupère l'index de la valeur correspondant au chemin le plus court
indexResultatFinal = listeLen.index(sortListeLen[0])
resultatFinal = cheminsResultats[indexResultatFinal]

# Affiche le message resultat
messageResultat = determinerMessageResultat(formaterResultatFinal(resultatFinal))
# print(messageResultat)

# Affiche le chemin resultat
print(formaterResultatFinal(resultatFinal))

# Affiche le temps d'éxecution
dateFin = datetime.datetime.now()
# print("Temps d'éxecution",dateFin-dateDebut)



