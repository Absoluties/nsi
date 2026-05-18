# coding: utf-8


# Chez Fleury & Bott
def fleury_bott(somme_a_rendre):
    '''
    Entrée (entier) : une somme d'argent à rendre
    Sortie (string) : phrases indiquant les billets à utiliser

    Cette fonction prend une somme à rendre en entrée, calcule le rendu de
    monnaie optimal avec des billets de 500, 200, 100, 50, 20, 10, 5, 2 et 1
    puis renvoie une chaîne de caractères indiquant les billets à utiliser
    pour rembourser la somme à l'aide de phrases.
    '''

    # Si la somme à rendre est 0, on ne rend rien
    if not somme_a_rendre:
        return "\nPour 0€ de trop, il n'y a rien à rendre !\n"

    if somme_a_rendre < 0:
        return f"\nHarry doit encore {somme_a_rendre * -1}€ au libraire !\n"

    # On initialise la liste des billets disponibles et la chaîne de
    # caractères de sortie indiquant les billets à rendre
    BILLETS_DISPO = (500, 200, 100, 50, 20, 10, 5, 2, 1)
    rendu = f'\nPour {somme_a_rendre}€ :\n'

    # On crée une boucle while qui calcule les billets à rendre
    # et les indiques dans la chaîne de caractères <rendu>
    i = 0
    while somme_a_rendre:
        # On initialise une variable <billets> qui contient le nombre
        # de billets de valeur <BILLETS_DISPO[i]> à rendre pour éviter
        # des redondances
        billets = somme_a_rendre // BILLETS_DISPO[i]

        # Si on peut utiliser des billets de valeur <BILLETS_DISPO[i]>
        # Dire combien de ces billets il faut utiliser et
        # ajuster la somme à rendre
        if billets:
            rendu = f"{rendu}Il faut rendre {billets}"\
                    f" billet(s) de {BILLETS_DISPO[i]}€\n"

            # On retranche les billets utillisés du total à rendre
            somme_a_rendre -= BILLETS_DISPO[i] * billets

        # On passe aux billets d'une valeur inférieure
        i += 1

    # On renvoie les instructions indiquant les billets à utiliser pour
    # rendre l'argent
    return rendu


# Chez Mme Guipure
def mme_guipure(somme_a_rendre):
    '''
    Entrée (entier) : une somme d'argent à rendre
    Sortie (string) : phrases indiquant les billets à utiliser

    Cette fonction prend une somme à rendre en entrée, calcule le rendu de
    monnaie optimal avec des billets de 500, 200, 100, 50, 20, 10, 5, 2 et 1
    avec un nombre limité de billets puis renvoie une chaîne de caractères
    indiquant les billets à utiliser pour rembourser la somme à l'aide de phrases.
    Si le remboursement n'est pas total, la commerçante remboursera du mieux
    qu'elle peut, quitte à donner trop.

    '''
    if not somme_a_rendre:
        return "\nPour 0€ de trop, il n'y a rien à rendre !\n"

    if somme_a_rendre < 0:
        return f"\nHarry doit encore {somme_a_rendre * -1}€ au magasin !\n"

    # Liste qui contient les billets disponibles sous forme de tuples.
    # La première valeur est la valeur du billet et la seconde sa quantité.
    BILLETS_DISPO = ((200, 1), (100, 3), (50, 1), (20, 1), (10, 1), (2, 5))

    # Listes contenant les billets mis de côté au premier tour.
    # Bonus
    billets_non_utilises = []

    caisse_vide = True  # Bonus

    rendu = f'\nPour {somme_a_rendre}€ :\n'

    i = 0
    while somme_a_rendre and i < len(BILLETS_DISPO):
        # On initialise cette variable pour éviter les redondances.
        billets_necessaires = somme_a_rendre // BILLETS_DISPO[i][0]
        if billets_necessaires:
            if billets_necessaires > BILLETS_DISPO[i][1]:
                rendu = f"{rendu}Il faut rendre {BILLETS_DISPO[i][1]}"\
                        f" billet(s) de {BILLETS_DISPO[i][0]}€\n"
                somme_a_rendre -= BILLETS_DISPO[i][0] * BILLETS_DISPO[i][1]
                billets_non_utilises.append(0)  # Bonus
            else:
                rendu = f"{rendu}Il faut rendre {billets_necessaires}"\
                        f" billet(s) de {BILLETS_DISPO[i][0]}€\n"
                somme_a_rendre -= BILLETS_DISPO[i][0] * (billets_necessaires)

                billets_non_utilises.append(
                    BILLETS_DISPO[i][1] - billets_necessaires
                )  # Bonus
                # Bonus
                if caisse_vide and BILLETS_DISPO[i][1] - billets_necessaires:
                    caisse_vide = False

        i += 1

    # Bonus
    if somme_a_rendre:
        if not caisse_vide:
            rendu = f"{rendu}\nIl reste {somme_a_rendre}€ à rendre et la caisse n'est pas vide. Mme Guipure va rembourser Harry du mieux qu'elle peut :\n"\
                    f"(État des billets : {billets_non_utilises})\n"

            for index, nb_billets in enumerate(billets_non_utilises[::-1]):
                if somme_a_rendre <= 0:
                    break
                index = -1 - index
                if nb_billets:
                    x = somme_a_rendre // (BILLETS_DISPO[index][0] * nb_billets) + 1

                    if x <= nb_billets:
                        somme_a_rendre -= x * BILLETS_DISPO[index][0]
                        rendu = f"{rendu}Mme Guipure rend {x} billet(s) de {BILLETS_DISPO[index][0]}€ de plus à Harry"
                    else:
                        somme_a_rendre -= BILLETS_DISPO[index][0] * nb_billets
                        rendu = f"{rendu}Mme Guipure rend {nb_billets} billet(s) de {BILLETS_DISPO[index][0]}€ de plus à Harry"

            if somme_a_rendre < 0:
                return f"{rendu}\nElle rend donc {-1 * somme_a_rendre}€ de trop\n"

        return f"{rendu}\nIl reste malheureusement {somme_a_rendre}€ à rendre et la caisse est vide"
    # Fin du Bonus

    return rendu


# Chez Ollivander
def ollivander(gallions, mornilles, noises):
    '''
    Entrée (3 entiers) : une somme d'argent à rendre
    Sortie (string) : phrases indiquant les pièces à utiliser

    Cette fonction prend une somme à rendre en entrée, calcule le rendu de
    monnaie optimal avec des pièces (gallions, mornilles, noises),
    puis renvoie une chaîne de caractères indiquant les pièces à utiliser
    pour rembourser la somme à l'aide de phrases.

    PS: 1 gallion = 17 mornilles ; 1 mornille = 29 noises
    '''

    if not (gallions + mornilles + noises):
        return "\nIl n'y a rien à rendre !\n"

    if (gallions + mornilles + noises) < 0:
        return f"\nHarry doit encore de l'argent à Ollivander !\n"

    # On convertit les noises de trop en mornilles
    mornilles += noises // 29
    noises = noises % 29

    # On convertit les mornilles de trop en gallions
    gallions += gallions + mornilles // 17
    mornilles = mornilles % 17

    return f'\nIl faut nous rendre {gallions} gallions, {mornilles} mornilles et {noises} noises.\n'


def carte():
    '''
    Cette fonction sert de menu. Elle sert à guider Harry au cours ses
    emplettes dans le chemin de Traverse.
    '''
    deja_vu = False

    while True:
        if deja_vu:
            print('\n\nDésormais, ', end='')
        else:
            print('\n Bienvenue au chemin de traverse. La meilleure rue commerçante du monde magique !\n'
                  'Harry doit acheter ses fournitures scolaires. Pour commencer, ', end='')
            deja_vu = True

        x = input("chez qui va Harry ? : (Fleury | Guipure | Ollivander | Partir)\n").lower()

        if x == 'fleury':
            x = input("Si vous voulez entrer une valeur de test personnalisée"
                      ", entrez-là, sinon le test s'effectuera avec des"
                      " valeurs prédéfinies (si la valeur est incorrecte, elle"
                      " ne sera pas prise en compte): ")
                      
            if x and x.isdigit():
                print(fleury_bott(int(x)))

            else:
                ECHANTILLON = (0, 60, 63, 231, 899)

                for test in ECHANTILLON:
                    print(fleury_bott(test))

        elif x == 'guipure':
            x = input("Si vous voulez entrer une valeur de test personnalisée"
                      ", entrez-là, sinon le test s'effectuera avec des"
                      " valeurs prédéfinies (si la valeur est incorrecte, elle"
                      " ne sera pas prise en compte): ")
            if x and x.isdigit():
                print(mme_guipure(int(x)))

            else:
                ECHANTILLON = (0, 8, 62, 231, 497, 942)

                for test in ECHANTILLON:
                    print(mme_guipure(test))

        elif x == 'ollivander':
            if input("Voulez-vous voulez entrer des valeurs de test personnalisées ? (Oui | Non) ").lower() == 'oui':
                try:
                    gallions = int(input('Nombre de gallions : '))
                    mornilles = int(input('Nombre de mornilles : '))
                    noises = int(input('Nombre de noises : '))
                    print(ollivander(gallions, mornilles, noises))
                    continue
                except:
                    print("Une valeur incorrecte a été donnée, le s'effectuera avec les valeurs"
                          "prédéfinies")

            ECHANTILLON = ((0, 0, 0), (0, 0, 654), (0, 23, 78), (2, 11, 9), (7, 531, 451))
            for test_gallions, test_mornilles, test_noises in ECHANTILLON:
                print(ollivander(test_gallions, test_mornilles, test_noises))

        elif x == 'partir':
            print('Harry a quitté le chemin de traverse et rentre chez lui.')
            return

        else:
            print('Harry ne connaît pas cette boutique.')

carte()
