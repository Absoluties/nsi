from random import choice

# On initialise le dictionnaire qui va contenir les personnages et leur score
classement = {}


# Fonction principale et exécutée en première
def main(jouer):

    """
    Entrée : booléen, indique si on fait immédiatement jouer les personnages

    Cette fonction fait jouer les personnages du fichier CSV si l'utilisateur
    le souhaite sauf si le paramètre <jouer> est True, auquel cas la fonction
    s'exécute en entier immédiatement.
    Elle permet de contrôler l'execution du programme.
    """

    # Si on ne sait pas si l'utilisateur veut faire jouer les personnages
    if not jouer:
        # Tant qu'on n'obtient pas de réponse valide
        while True:
            # On utilise la méthode lower() pour n'obtenir que des minuscules
            x = input(
                "\n\nVoulez-vous faire jouer 140 personnages "
                "issus de la saga Harry Potter ? (Y/N)\n→ "
            ).lower()

            if x == "y":
                break
            elif x == "n":
                print("Bonne journée")
                input("\n\nAppuyez sur une touche pour sortir...")
                return
            else:
                print("Réponse incorrecte")

    print("Importation des personnages...\nPrgression du tournoi...")

    # On ouvre le fichier csv et on fait jouer chaque personnage 10 parties
    with open("Characters.csv", mode='r', encoding="utf-8") as f:
        next(f)  # On passe l'en-tête
        # Pour chaque ligne dans le fichier
        for ligne in f:
            score = 0  # Initialisation du score.
            start = ligne.index(";") + 1  # Index du début du nom
            end = ligne.index(";", start + 1)  # Index + 1 de la fin du nom

            # On met le score à jour après chacune des 10 parties
            for _ in range(10):
                score += jouer_partie()

            # On ajoute le joueur dans le classement
            classement[ligne[start:end]] = score

    # Tant qu'on n'obtient pas de réponse valide
    while True:
        # On utilise la méthode lower() pour n'obtenir que des minuscules
        x = input("\n\nVoulez-vous afficher le classement ? (Y/N)\n→ ").lower()

        if x == "y":
            resultats()
            return
        elif x == "n":
            rejouer()
            return
        else:
            print("Réponse incorrecte")


def jouer_partie():

    """
    Sortie : le score du joueur 1

    Cette fonction sert à jouer une partie de morpion entre deux joueurs.
    Les coups sont aléatoire.
    Le joueur 1 est considéré comme un challenger jouant contre l'ordinateur.
    """

    # Initialisation des variables nécessaires au fonctionnement de la partie
    victoire = False
    compteur = 0
    grille = [["•" for colonne in range(3)] for ligne in range(3)]
    score = 2  # Le score est par défaut celui d'une égalité
    cases_libres = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # Les cases sont numérotées
    suivi_de_partie = '\n'
    printed = False

    # Tant que la partie n'est pas terminée
    while (not victoire) and cases_libres:

        # On choisit la case sur laquelle le joueur va jouer
        x = choice(cases_libres)

        # On détermine qui joue et donc quel symbole il faut utiliser
        # On détermine la case choisie et on y met le symbole du joueur
        if compteur % 2 == 0:
            grille[x // 3][x % 3] = "X"
        else:
            grille[x // 3][x % 3] = "O"

        # On indique la case jouée comme occupée
        cases_libres.pop(
            cases_libres.index(x)
        )

        # Optionnel (augmente ENORMEMENT le temps d'exécution)
        # On affiche la grille actuelle :
        # Pour ce faire on affiche chaque ligne, colonne par colonne.
        suivi_de_partie = f"{suivi_de_partie}{grille[0][0]:^3}"\
            f"{grille[0][1]:^3}{grille[0][2]:^3}\n{grille[1][0]:^3}"\
            f"{grille[1][1]:^3}{grille[1][2]:^3}\n{grille[2][0]:^3}"\
            f"{grille[2][1]:^3}{grille[2][2]:^3}\n\n"

        # On regarde si une ligne est gagnante
        for i in range(len(grille)):
            if grille[i][0] == grille[i][1] == grille[i][2] != "•":
                print(f"{suivi_de_partie}La ligne {i + 1} est gagnante")
                printed = True
                victoire = True

        # On regarde si une colonne est gagnante
        for i in range(len(grille)):
            if grille[0][i] == grille[1][i] == grille[2][i] != "•":
                if not printed:
                    print(suivi_de_partie)
                    printed = True
                print(f"La colonne {i + 1} est gagnante")  # Optionnel
                victoire = True

        # On regarde si une diagonale est gagnante
        if (grille[0][0] == grille[1][1] == grille[2][2] != "•") or (
            grille[0][2] == grille[1][1] == grille[2][0] != "•"
        ):
            if not printed:
                    print(suivi_de_partie)
            print("Une diagonale est gagnante")  # Optionnel
            victoire = True

        # On incrémente le compteur de tour pour changer de joueur
        compteur += 1

    # Ici la partie est finie

    # On détermine le joueur gagnant et on met à jour le score
    if victoire:
        # On détermine quel joueur a joué en dernier et on l'affiche
        if (compteur - 1) % 2 == 0:
            print("Le joueur remporte la partie !")  # Optionnel
            score = 5
        else:
            print("L'ordinateur remporte la partie !")  # Optionnel
            score = 0
    # Optionnel
    else:
        print(f"{suivi_de_partie}Il y a égalité")

    # On renvoie le score du joueur 1
    return score


def resultats():

    """
    Cette fonction affiche les personnages et leur score après les avoir trié.
    Elle affiche ensuite la moyenne du score des personnages.
    """

    print("Tournoi terminé ! "
          f"Voici les résultats des {len(classement)} candidats :\n")

    # On affiche le classement trié
    for i, j in sorted(
        classement.items(), key=lambda item: item[1], reverse=True
    ):
        print(f"{i:^40} {j:^5}")

    # On affiche la moyenne de tous les scores
    print("\nLa moyenne des score est de "
          f"{sum(classement.values())/len(classement):.2f}")

    rejouer()


def rejouer():

    """
    Cette fonction demande à l'utilisateur s'il veut rejouer.
    Si oui, une nouvelle série de parties se lance. Si non, le programme
    s'arrête.
    """

    # Tant qu'on n'obtient pas de réponse valide
    while True:
        # On utilise la méthode lower() pour n'obtenir que des minuscules
        x = input("\n\nVoulez-vous rejouer ? (Y/N)\n→ ").lower()
        if x == "y":
            main(True)
            return
        elif x == "n":
            print("Bonne journée")
            input("\n\nAppuyer sur une touche pour sortir...")
            return
        else:
            print("Réponse incorrecte")


main(False)
