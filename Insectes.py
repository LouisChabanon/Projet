from Plantes import Plante
import random

# TODO:
# - Implementer les mutations


class Insecte():
    '''
    Classe Insectes definissant le comportement des insectes dans la simulation
    '''

    def __init__(self, espece: str, sexe: str, max_health: int, health: int, mobilite: float, resistance: int, tps_reproduction: int, taille_max_portee: int) -> None:
        self._espece = str(espece)
        self._sexe = str(sexe)
        self._max_health = int(max_health)
        self._health = int(health)
        self._mobilite = float(mobilite)
        self._resistance = int(resistance)
        self._tps_reproduction = int(tps_reproduction)
        self._taille_max_portee = int(taille_max_portee)

        self._time_since_last_reproduction = 0
        self._eat_combo = 0

    # Getters et Setters

    def get_espece(self) -> str:
        return self._espece

    def get_sexe(self) -> str:
        return self._sexe

    def get_max_health(self) -> int:
        return self._max_health

    def get_health(self) -> int:
        return self._health

    def get_mobilite(self) -> float:
        return self._mobilite

    def get_resistance(self) -> int:
        return self._resistance

    def get_tps_reproduction(self) -> int:
        return self._tps_reproduction

    def get_time_since_last_reproduction(self) -> int:
        return self._time_since_last_reproduction

    def get_taille_max_portee(self) -> int:
        return self._taille_max_portee

    def set_health(self, new_health: int) -> None:
        self._health = new_health

    def manger(self, parcelle) -> None:
        '''
        Methode permettant de faire manger un insecte
        L'insecte essaye de se nouriur de la plante dans la parcelle, si elle n'est pas presente, il perd de la vie.
        Si elle est presente, il gagne de la vie et un combo est incremente.
        '''
        if not Plante in parcelle.get_occupants():
            self._health -= 1
            if self._eat_combo != 0:
                self._eat_combo = 0
            else:
                self._eat_combo -= 1
        else:
            self._eat_combo += 1
            if self._eat_combo >= 3:
                self._health += 1

    def se_reproduire(self, parcelle) -> None:
        '''
        Methode permettant de faire se reproduire un insecte,
        L'insecte essaye de se reproduire avec un partenaire de la meme espece et de sexe oppose.
        Si il y a un partenaire, et que les deux insectes ont un combo de nourriture positif, ils se reproduisent.
        '''
        if self._time_since_last_reproduction >= self._tps_reproduction:
            partenaire = parcelle.choose_partenaire(self)
            if partenaire == None:
                return None
            if self._espece == partenaire.get_espece():
                if self._sexe != partenaire.get_sexe():
                    if self._eat_combo > 0 and partenaire.get_eat_combo() > 0:
                        self._time_since_last_reproduction = 0
                        partenaire.set_time_since_last_reproduction(0)
                        if self._sexe == "F":
                            taille_portee = self.taille_portee()
                        else:
                            taille_portee = partenaire.taille_portee()
                        for i in range(taille_portee):
                            attribus = self.__dict__
                            mutation = False
                            parite = False
                            for j in attribus.keys():
                                if random.random() >= 0.5:
                                    parite = True
                                    attribus[j] = partenaire.__dict__[j]
                            if not parite:
                                k = random.randint(0, len(attribus.keys())-1)
                                attribus[list(attribus.keys())[k]] = partenaire.__dict__[
                                    k]
                            parcelle.add_occupant(Insecte(attribus["espece"], attribus["sexe"], attribus["max_health"], attribus["max_health"]/2,
                                                          self._mobilite, self._resistance, self._tps_reproduction, self._taille_max_portee))

    def taille_portee(self) -> int:
        '''
        Methode permettant de calculer la taille de la portee d'un insecte
        '''
        return random.randint(1, self._taille_max_portee)

    def bouger(self, parcelle) -> None:
        proba = self._mobilite
        if self._eat_combo <= -3:
            proba = 2*proba
        if self._health <= 20:
            proba = proba/2
        if random.random() <= proba:
            parcelle.remove_occupant(self)
            parcelle.get_voisin_aleatoire().add_occupant(self)

    def mourir(self):
        del self
