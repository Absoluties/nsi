# encoding utf-8


def get_characters():
    """
    Sortie : liste contenant des profils de référence sous forme de
             dictonnaire et leur maison attitrée dans un tuple.

    Cette fonction extrait des profils de deux fichiers CSV
    (l'un contient la maison et l'autre le portrait moral d'un élève)
    si un élève est présent dans chacun des deux fichiers.
    """
    # Initialisation qui contiendra la liste des profils extraits.
    characters = []

    # On crée un dictionnaire contenant les maisons de chaque profil de reference
    # dans un dictionnaire avec le nom des personnages comme clés.
    with open("Characters.csv", mode="r", encoding="utf_8") as characters_file:
        houses = {
            line.split(";", 2)[-2]: line.split(";", 5)[-2]
            for line in characters_file.readlines()[1:]
        }

    # On obtient l'en-tête du fichier CSV et on passe la première ligne.
    with open(
        "Caracteristiques_des_persos.csv", mode="r", encoding="utf_8"
    ) as characteristics_file:
        characteristics = characteristics_file.readline()[:-1].split(";")[1:]

        # On remplit la liste des profils sans oublier de convertir les chaînes de caratères en entiers.
        # Il est important de savoir que le fichier "Characters.csv" contient tous les profils du fichier "Caracteristiques_des_persos"
        # (l'inverse est faux) et c'est pourquoi on peut utiliser un dictionnaire avec le nom de chaque profil comme clé.
        for line in characteristics_file:
            characters.append(
                (
                    line[: line.index(";")],
                    {
                        characteristics[index]: int(value)
                        for index, value in enumerate(line[:-1].split(";")[1:])
                    },
                    houses[line[: line.index(";")]],
                )
            )

    return characters


def k_neighbors(test, k, sample):
    """
    Entrées :
        - test : dictionnaire décrivant le profil à tester
        - k : entier indiquant le nombre de voisins à retourner
        - sample : liste contenant les profils de référence

    Sortie : tuple contenant les k plus prochse voisins et leur maison majoritaire
    """
    # Initialisation de la liste qui contiendra les profils proches.
    neighbors = []

    for reference in sample:
        # On calcule la distance euclidienne entre le profile de test et ceux de référence
        # puis on ajoute la maison du profil à <neighbors> si la distance est inférieure à <k>.
        # √x = x**0.5
        neighbors.append(
            (
                reference[0],
                sum(
                    [
                        (value - reference[1][trait]) ** 2
                        for trait, value in test.items()
                    ]
                ) ** 0.5,
                reference[2],
            )
        )

    # Si le profil de test a des voisins on peut renvoyer la maison choisie
    # sinon on renvoie <False>.
    if neighbors:
        neighbors.sort(key=lambda x: x[1])
        houses = [i[2] for i in neighbors[:k]]
        # On ne considère que les k plus proches voisins et on n'a pas besoin
        # d'associer les noms aux maisons
        return ((i[0] for i in neighbors[:k]), max(set(houses), key=houses.count))

    return False


# Affichage des tests
def display(profiles):
    """
    Entrée : liste ou tuple contenant des profils sous forme de dictionnaire

    Cette fonction affiche les résultats obtenu après utilisation de l'algorithme
    des k plus proches voisins sur un ou plusieurs profils (voisins + maison)
    """
    for profile in profiles:
        choixpeau = k_neighbors(profile, 10, get_characters())

        print(f"\n{'Voici le profil examiné :':^80}")
        for trait, value in profile.items():
            print(f' {trait:>8}:', f'{value:<9}', end='')

        if choixpeau:
            print(f"\n{'Voici les profils semblables au profil de test :':^80}")
            for i in choixpeau[0]:
                print(f"{i:^80}")
            print(f"{'''Ce profil devait être celui d'un élève de...''':^80}\n→{choixpeau[1]:^75}←\n")
        else:
            print("Cet élève est hors-normes et ne correspond à aucun autre !")


def hmi():
    """
    Cette fonction qui ne prend pas d'entrée et ne renvoie rien a pour but
    d'assister l'utilisateur dans l'utilisation du programme. Elle permet
    d'exécuter les autres fonctions et crée un profil personnalisé.
    """

    print("Bienvenue à Poudlard, où le Choipeau va décider à quelle maison vous allez appartenir.\n"
          "Pour commencer, vous avez la possibilité de déterminer la maison de choix d'un profil "
          "personnalisé ou bien de profils préétablis.")

    # On considère que l'utilisateur sait taper des nombres entre 0 et 10
    while True:
        try:
            choice = int(input("\nUtiliser un profil personnalisé ou des profils préétablis (1|2) : "))

            if choice == 1:
                print("Bienvenue dans l'utilitaire de création de profil d'élève.")

                # Il nous faut un itérable contenant des profils donc on place le dictionnaire
                # dans une liste d'un élément puisque un tuple d'un seul élément est interprété
                # comme l'élément compris dans le tuple par python
                profile = [{
                    "Courage": int(input("En premier lieu, choississez la valeur courage du profil : ")),
                    "Ambition": int(input("Maintenant, choississez la valeur ambition du profil : ")),
                    "Intelligence": int(input("Désormais, choississez la valeur intelligence du profil : ")),
                    "Good": int(input("Enfin, choississez la valeur good du profil : "))
                }]

                display(profile)
                break

            elif choice == 2:
                profiles = (
                            {"Courage": 9, "Ambition": 2, "Intelligence": 8, "Good": 9},
                            {"Courage": 6, "Ambition": 7, "Intelligence": 9, "Good": 7},
                            {"Courage": 3, "Ambition": 8, "Intelligence": 6, "Good": 3},
                            {"Courage": 2, "Ambition": 3, "Intelligence": 7, "Good": 8},
                            {"Courage": 3, "Ambition": 4, "Intelligence": 8, "Good": 8},
                            {"Courage": 2, "Ambition": 2, "Intelligence": 1, "Good": 10},
                )

                display(profiles)
                break

        except Exception as e:
            print(e)

        # Si une valeur invalide est entrée quelque part
        print("Désolé je n'ai pas compris, veuillez réessayer.")

# Début du programme + bonne pratique
if __name__ == '__main__':
    hmi()
