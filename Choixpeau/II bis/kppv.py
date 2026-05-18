# encoding utf-8
def get_characters(file_characters, file_stats):
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
    with open(file_characters, mode="r", encoding="utf_8") as characters_file:
        houses = {
            line.split(";", 2)[-2]: line.split(";", 5)[-2]
            for line in characters_file.readlines()[1:]
        }

    # On obtient l'en-tête du fichier CSV et on passe la première ligne.
    with open(
        file_stats, mode="r", encoding="utf_8"
    ) as characteristics_file:
        characteristics = characteristics_file.readline()[:-1].split(";")[1:]

        # On remplit la liste des profils sans oublier de convertir les chaînes de caratères en entiers.
        # Il est important de savoir que le fichier "Characters.csv" contient tous les profils du fichier "Caracteristiques_des_persos"
        # (l'inverse est faux) et c'est pourquoi on peut utiliser un dictionnaire avec le nom de chaque profil comme clé.
        for line in characteristics_file:
            characters.append(
                (
                    line[:line.index(";")],
                    {
                        characteristics[index]: int(value)
                        for index, value in enumerate(line[:-1].split(";")[1:])
                    },
                    houses[line[: line.index(";")]],
                )
            )

    return characters

def get_most_occurrence(houses_list):
    '''
    Renvoie la maison avec la plus réccurente. Si il y a égalité c'est la première qui est renvoyée.
    Par conséquent le profil avec la distance la plus petite prévaut. 
    '''

    occurrences = {}

    for item in houses_list:
        if item in occurrences:
            occurrences[item] += 1
        else:
            occurrences[item] = 1

    most_occurrence = 0
    choice = ''

    for house in occurrences:
        if occurrences[house] > most_occurrence:
            most_occurrence = occurrences[house]
            choice = house

    return choice

def k_neighbors(test, k, characters_file, stats_file):
    """
    Entrées :
        - test : dictionnaire décrivant le profil à tester
        - k : entier indiquant le nombre de voisins à retourner
        - sample : liste contenant les profils de référence

    Sortie : tuple contenant les k plus prochse voisins et leur maison majoritaire
    """

    # Initialisation de la liste qui contiendra les profils proches.
    neighbors = []

    sample = get_characters(characters_file, stats_file)

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
        return (neighbors[:k], get_most_occurrence([i[2] for i in neighbors[:k]]))

    return False
