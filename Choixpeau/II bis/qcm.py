from browser import document
from browser.html import BUTTON, DIV, IMG, INPUT, P, TABLE, TH, TR
import kppv


def clear_body():
    '''
    Cette fonction supprime tous les éléments présents dans
    le corps de la page HTML.
    '''
    for element in document.body:
        element.parentNode.removeChild(element)

def show_results(k):
    '''
    Entrée : entier cindiquant le nombre de voisins à prendre en compte

    Cette fonction permet d'afficher les résultats du QCM. Ces derniers
    comprennent :
        - une indication de la maison choisie
        - le tableau contenant les voisins
        - le blason de la maison choisie
        - un bouton pour recommencer le QCM
        - un slider pour décider du nombre de voisins pris en compte
    '''
    # On supprime l'affichage précédent
    clear_body()

    # On calcule les distances pour déterminer les voisins et la maison
    neighbors = kppv.k_neighbors(
        profile,
        k,
        "csv/Characters.csv",
        "csv/Caracteristiques_des_persos.csv"
    )

    if neighbors:
        # Slider pour décider du nombre de voisins
        document.body <= P('Nombre de voisins', style="font-size: 20; margin-bottom: 15px")
        document.body <= DIV(
            INPUT(type="range", min="1", max="15", value=k, id="k_slider"),
            id="slider_div"
        )
        document["slider_div"] <= P(document["k_slider"].value)
        document["k_slider"].bind("change", lambda x: show_results(int(x.currentTarget.value)))

        # Affichage du blason de la maison choisie
        document.body <= IMG(src=f'img/{neighbors[1]}.png', id='left_results_crest')
        document.body <= IMG(src=f'img/{neighbors[1]}.png', id='right_results_crest')

        # Affichage de la maison choisie
        document.body <= P(
            f'Vous êtes exactement comme un élève de {neighbors[1]} !',
            id="results_house"
        )

        # Création du tableau affichant les voisins
        neighbors_table = TABLE(id='results_table')
        # Ajout des en-têtes des 3 colonnes
        neighbors_table <= TR(TH('Nom') + TH('Distance') + TH('Maison'))
        # Ajout du des informations sur les voisins
        for neighbor in neighbors[0]:
            neighbors_table <= TR(TH(neighbor[0]) +
                                  TH(f'{neighbor[1]:.3}') +
                                  TH(neighbor[2]), id="results_table_text")
        # Ajout du tableau à la page
        document.body <= neighbors_table

        # Création du bouton pour recommencer le quiz
        document.body <= BUTTON('RECOMMENCER', id='restart_button')
        document['restart_button'].bind('click', new_qcm)
    else:
        # On ne peut pas arriver ici car il n'y a pas de distance minimum
        document.body <= P(
            'Woah, vous avez un sacré caractère ! Vous ne correspondez à aucune maison.',
            id='results_house')

def answer_button_clicked(event):
    '''
    Entrée : évènement indiquant quel bouton a été utilisé

    Cette fonction est appelée à chaque fois que l'utilisateur
    répond à une question du QCM. Elle permet de mettre à jour
    le profil en fonction de la réponse.
    '''
    compteur = int(document["compteur"].textContent)

    # On regarde s'il reste des questions
    if compteur < len(questions_answers):
        # On récupère les caractéristiques morales associées à la réponse,
        # indiquées après le "." de cette dernière.
        answer = questions_answers[compteur - 1][int(
                event.currentTarget.id[-1]
        )]
        characteristics = answer[answer.index('.') + 1:]

        sign = 1  # Cela permet de gérer les décrémentations des caractéristques
        for letter in characteristics:
            if letter == '-':
                sign = -1
                continue  # On passe la partie qui remet <sign> à 1
            if letter == 'I':
                profile['Intelligence'] += sign
            if letter == 'C':
                profile['Courage'] += sign
            if letter == 'G':
                profile['Good'] += sign
            if letter == 'A':
                profile['Ambition'] += sign

            sign = 1

        update_qcm()
    else:
        # Par défaut, on affiche 3 voisins
        show_results(3)

def update_qcm():
    '''
    Cette fonction met à jour les questions, le compteur de questions et
    les boutons de réponses du QCM.
    '''
    compteur = int(document["compteur"].textContent)

    document["question"].textContent = questions_answers[compteur][0]

    for id in '1234':
        answer = questions_answers[compteur][int(id)]
        document[f"answer_button_{id}"].textContent = answer[:answer.index(
            '.') + 1:]

    document["compteur"].textContent = str(compteur + 1)

# Il y a un paramètre car la méthode <bind> appelle les fonctions
# avec un évènement en paramètre
def new_qcm(_=None):
    '''
    Entrée : paramètre obligatoire à cause de la méthode <bind> qui appelle
             une fonction avec un évènement comment paramètre. Inutilisé.

    Cette fonction initialise le QCM en ajoutant images, boutons,
    le compteur de questions et le conteneur de la question.
    '''

    # On supprime tous les éventuels résidus sur la page
    clear_body()

    # On crée un nouveau profil
    global profile
    profile = {'Intelligence': 0, 'Courage': 0, 'Ambition': 0, 'Good': 0}

    # Numéro de la question
    document.body <= P(0, id="compteur")

    # Création de la question
    document.body <= P(id="question")

    # Création des boutons
    document.body <= DIV(id="buttons_container")
    for i in range(2):
        document["buttons_container"] <= DIV(
            id=f"buttons_group_{i}", Class="buttons_group")
        document[f"buttons_group_{i}"] <= BUTTON(
            id=f"answer_button_{2*i+1}", Class="answer_button").bind("click", answer_button_clicked)
        document[f"buttons_group_{i}"] <= BUTTON(
            id=f"answer_button_{2*i+2}", Class="answer_button").bind("click", answer_button_clicked)

    # Affichage des blasons des 4 maisons
    document.body <= DIV(
        IMG(src="img/Slytherin.png", Class="house_crest") +
        IMG(src="img/Gryffindor.png", Class="house_crest") +
        IMG(src="img/Ravenclaw.png", Class="house_crest") +
        IMG(src="img/Hufflepuff.png", Class="house_crest")
    )

    update_qcm()

# Il y a un paramètre car la méthode <bind> appelle les fonctions
# avec un évènement en paramètre
def new_intro(_=None):
    '''
    Cette fonction
    '''
    # On supprime tous les éventuels résidus sur la page
    clear_body()

    document.body <= IMG(src="img/Choixpeau.png", style="width: 30%; height: 30%")

    document.body <= DIV(
        P("Le choixpeaux magique est un conseiller d'orientation pour les nouveaux élève de l'école de sorcellerie Poudlard.") +
        P("Aujourd'hui il te propose d'étudier ta personnalité à l'aide d'un questionnaire pour décider quelle maison te correspond le mieux."),
        id='question',
        style="position: absolute; top: 65%"
    )

    document.body <= BUTTON('COMMENCER', id='restart_button').bind('click', new_qcm)

if __name__ == '__main__':
    with open('csv/qcm.csv') as f:
        questions_answers = [
            [question_answer for question_answer in line[:-2].split(';')]
            for line in f.readlines()[1:]
        ]

    new_intro()
