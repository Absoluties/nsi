from browser import document
from browser.html import BUTTON, DIV, TABLE, H1, TH, TR, H3
import kppv

with open('qcm.csv') as f:
    questions_reponses = [
        [question_answer for question_answer in line[:-2].split(';')] for line in f.readlines()[1:]]

profile = {'Intelligence': 0, 'Courage': 0, 'Ambition': 0, 'Good': 0}


def click(ev):
    global compteur
    trait = questions_reponses[compteur - 1][int(ev.currentTarget.id)][-1]

    for letter in trait:
        if letter == 'I':
            profile['Intelligence'] += 1
        if letter == 'C':
            profile['Courage'] += 1
        if letter == 'G':
            profile['Good'] += 1
        if letter == 'A':
            profile['Ambition'] += 1

    if compteur < len(questions_reponses):
        compteur += 1
        document['compteur'].textContent = str(compteur)

        document['question_div'].textContent = questions_reponses[compteur - 1][0]
        for id in '1234':
            document[id].textContent = questions_reponses[compteur -
                                                         1][int(id)][:questions_reponses[compteur - 1][int(id)].index('.') + 1]
    else:
        for element in document.body:
            element.parentNode.removeChild(element)

        for key in profile:
            profile[key] = int(10 * profile[key] / len(questions_reponses)) + 3

        neighbors = kppv.k_neighbors(
            profile, 15, "Characters.csv", "Caracteristiques_des_persos.csv")

        document.body <= H1(f'→ {neighbors[1]} ←', id='results_house')

        table = TABLE(id='results_table')
        table <= TR(TH('Nom') + TH('Distance') + TH('Maison'))
        for neighbor in neighbors[0]:
            table <= TR(TH(neighbor[0]) +
                        TH(f'{neighbor[1]:.3}') + TH(neighbor[2]))
        document.body <= table

        document.body <= BUTTON('RECOMMENCER', id='restart_button')
        document['restart_button'].bind('click', main)


def main(_):
    # Reset everything
    for element in document.body:
        element.parentNode.removeChild(element)
    global compteur
    compteur = 1
    for key in profile:
        profile[key] = 0

    document.body <= DIV(questions_reponses[0][0], id="question_div")
    document.body <= DIV(id="buttons_div")
    for id in '1234':
        document["buttons_div"] <= BUTTON(questions_reponses[0][int(
            id)][:questions_reponses[0][int(id)].index('.') + 1], id=id, Class="answer_button")
        document[id].bind("click", click)

    document.body <= H3('QUESTION')
    document.body <= H3('1', id='compteur')


if __name__ == '__main__':
    main(False)
