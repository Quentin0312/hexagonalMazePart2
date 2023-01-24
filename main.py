import functions
import datetime

# Permet d'enregistrer le temps d'éxecution
dateDebut = datetime.datetime.now()

# Trouver le point de départ
positionDepartTrouvee = functions.trouverPositionCaractere("S")

# "S" se transforme en "_" pour lab 10 et 11
functions.dicoMaze[positionDepartTrouvee[0]] = functions.dicoMaze[positionDepartTrouvee[0]].replace("S", "_")

# À partir de la pos initiale
posInitiale = positionDepartTrouvee

# Fonction recurcive principale
fin = functions.fonctionRecursive(posInitiale, dateDebut)

# Contient la liste des longeurs de chemins de sorties
listeLen = []

# Remplit listeLen
for elt in functions.cheminsResultats:
    listeLen.append(len(elt))

# Range dans l'ordre
sortListeLen = listeLen.copy()
sortListeLen.sort()

# Récupère l'index de la valeur correspondant au chemin le plus court
indexResultatFinal = listeLen.index(sortListeLen[0])
resultatFinal = functions.cheminsResultats[indexResultatFinal]

# Affiche le message resultat
messageResultat = functions.determinerMessageResultat(functions.formaterResultatFinal(resultatFinal))
print(messageResultat)

# Affiche le chemin resultat
print(functions.formaterResultatFinal(resultatFinal))

# Affiche le temps d'éxecution
dateFin = datetime.datetime.now()
print("Temps d'éxecution",dateFin-dateDebut)
