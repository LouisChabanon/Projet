import random
from Plantes import Plantes


class Parcelle:
    def __init__(self, coordonees: tuple, plantes: list, insectes: list, humidite: float, has_engrais: bool, has_insecticide: bool):
        self._coordonees = tuple(coordonees)
        self._humidite = float(humidite)
        self._has_engrais = bool(has_engrais)
        self._has_insecticide = bool(has_insecticide)
        self._plantes = list(plantes)
        self._insectes = list(insectes)

    def get_coordonees(self):
        return self._coordonees

    def get_plantes(self):
        return self._plantes

    def get_insects(self):
        return self._insectes

    def add_insect(self, insecte):
        self._insectes.append(insecte)

    def add_plante(self, plante):
        self._plantes.append(plante)

    def choose_partenaire(self, insecte):
        '''
        Methode choisisant un partenaire pour la reproduction d'un insecte
        '''
        for i in self._insectes:
            if i.get_time_since_last_reproduction() >= i.get_tps_reproduction() and i.get_sexe() != insecte.get_sexe() and i.get_espece() == insecte.get_espece():
                return i
        return None

    def get_voisin_aleatoire(self, potager):
        matrice = potager.get_matrice()
        voisins = [[matrice[i][j]
                    if i >= 0 and i < len(matrice) and j >= 0 and j < len(matrice[0]) else 0
                    for j in range(self._coordonees[1]-1, self._coordonees[1]+1)]
                   for i in range(self._coordonees[0]-1, self._coordonees[0] + 1)]

        return random.choice(voisins)

    def update(self, potager):
        for i in self._plantes:
            i.developper(self)

        for i in self._insectes:
            i.manger(self)
            i.bouger(self)
            i.reproduire(self)
