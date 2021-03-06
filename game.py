# -*- coding: utf-8 -*-
from copy import deepcopy
# plateau: List[List[nat]]
# liste de listes (lignes du plateau) d'entiers correspondant aux contenus des cases du plateau de jeu

# coup: Pair[nat nat]
# Numero de ligne et numero de colonne de la case correspondante a un coup d'un joueur

# Jeu
# jeu:N-UPLET[plateau nat List[coup] List[coup] Pair[nat nat]]
# Structure de jeu comportant :
#           - le plateau de jeu
#           - Le joueur a qui c'est le tour de jouer (1 ou 2)
#           - La liste des coups possibles pour le joueur a qui c'est le tour de jouer
#           - La liste des coups joues jusqu'a present dans le jeu
#           - Une paire de scores correspondant au score du joueur 1 et du score du joueur 2

game=None #Contient le module du jeu specifique: awele ou othello
joueur1=None #Contient le module du joueur 1
joueur2=None #Contient le module du joueur 2

#Fonctions minimales 

def getCopieJeu(jeu):
    """ jeu->jeu
        Retourne une copie du jeu passe en parametre
        Quand on copie un jeu on en calcule forcement les coups valides avant
    """
    jeu[2] = getCoupsValides(jeu)
    return deepcopy(jeu)

def finJeu(jeu):
    """ jeu -> bool
        Retourne vrai si c'est la fin du jeu
    """
    return game.finJeu(jeu)

def coupValide(jeu, c):
    return c in jeu[2]

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
        On suppose que la fonction n'est appelee que si il y a au moins un coup valide possible
        et qu'elle retourne obligatoirement un coup valide
    """
    j = getJoueur(jeu)
    if j == 1:
        j = joueur1
    else:
        j = joueur2
        
    c = j.saisieCoup(getCopieJeu(jeu))

    while (not coupValide(jeu, c)):
        print "Coup n'est pas valide, recommencez"
        c = j.saisieCoup(getCopieJeu(jeu))
    return c

def joueCoup(jeu,coup):
    """ jeu*coup->void
        Joue un coup a l'aide de la fonction joueCoup defini dans le module game
        Hypothese:le coup est valide
        Met tous les champs de jeu à jour (sauf coups valides qui est fixee à None)
    """
    game.joueCoup(jeu, coup)

def initialiseJeu():
    """ void -> jeu
        Initialise le jeu (nouveau plateau, liste des coups joues vide, liste des coups valides None et joueur = 1)
    """
    return [game.initplateau(), 1, None, [], game.initscore()]
    
def getGagnant(jeu):
    """jeu->nat
    Retourne le numero du joueur gagnant apres avoir finalise la partie. Retourne 0 si match nul
    """
    if (finJeu(jeu)):
        if (jeu[-1][0] > jeu[-1][1]):
            return 1
        elif (jeu[-1][1] > jeu[-1][0]):
            return 2
        else:
            return 0
    else:
        print "Jeu non termine"

def tirets(s):
    
    res = ""
    for i in range(len(s)):
        if (s[i] == '\t'):
            res += "-------"
        else:
            res += "-"
    return res

def affiche(jeu):
    """ jeu->void
        Affiche l'etat du jeu de la maniere suivante :
                 Coup joue = <dernier coup>
                 Scores = <score 1>, <score 2>
                 Plateau :

                         |       0     |     1       |      2     |      ...
                    ------------------------------------------------
                      0  | <Case 0,0>  | <Case 0,1>  | <Case 0,2> |      ...
                    ------------------------------------------------
                      1  | <Case 1,0>  | <Case 1,1>  | <Case 1,2> |      ...
                    ------------------------------------------------
                    ...       ...          ...            ...
                 Joueur <joueur>, a vous de jouer
                    
         Hypothese : le contenu de chaque case ne depasse pas 5 caracteres
    """
    if (jeu [3] != []): print "Coup joue = ", jeu[3][-1]
    print "Scores = ", jeu[4][0], jeu[4][1]
    print "Plateau : "
    
    s = "\t \t|"
    for i in range(len(jeu[0][0])):
        s += "\t%d\t|" % i
    print s
    print tirets(s)
    for i in range(len(jeu[0])):
        s = "\t%d\t|" % i
        for j in range(len(jeu[0][i])):
            s += "\t%d\t|" % jeu[0][i][j]
        print s
        print tirets(s)
        
    
    
# Fonctions utiles

def getPlateau(jeu):
    """ jeu  -> plateau
        Retourne le plateau du jeu passe en parametre
    """
    return jeu[0]

def addCoupJoue(jeu, coup):
    jeu[3].append(coup)

def getCoupsJoues(jeu):
    """ jeu  -> List[coup]
        Retourne la liste des coups joues dans le jeu passe en parametre
    """
    return jeu[3]

def resetCoupsValides(jeu):
    """ Jeu -> None
    Remet à none la liste des coups valides
    """
    jeu[2] = None

def getCoupsValides(jeu):
    """ jeu  -> List[coup]
        Retourne la liste des coups valides dans le jeu passe en parametre
        Si None, alors on met à jour la liste des coups valides
    """
    if jeu[2] == None:
        jeu[2] = game.getCoupsValides(jeu)
    return jeu[2]
    
def getScores(jeu):
    """ jeu  -> Pair[nat nat]
        Retourne les scores du jeu passe en parametre
    """
    return jeu[4]

def getJoueur(jeu):
    """ jeu  -> nat
        Retourne le joueur a qui c'est le tour de jouer dans le jeu passe en parametre
    """
    return jeu[1]

def changeJoueur(jeu):
    """ jeu  -> void
        Change le joueur a qui c'est le tour de jouer dans le jeu passe en parametre (1 ou 2)
    """
    jeu[1] = 2 if jeu[1] == 1 else 1

def getScore(jeu,joueur):
    """ jeu*nat->int
        Retourne le score du joueur
        Hypothese: le joueur est 1 ou 2
    """
    return jeu[4][joueur - 1]

def setCaseVal(jeu, ligne, colonne, val):
    jeu[0][ligne][colonne] = val

def getCaseVal(jeu, ligne, colonne):
    """ jeu*nat*nat -> nat
        Retourne le contenu de la case ligne,colonne du jeu
        Hypothese: les numeros de ligne et colonne appartiennent bien au plateau  : ligne<=getNbLignes(jeu) and colonne<=getNbColonnes(jeu)
    """
    return jeu[0][ligne][colonne]
    




