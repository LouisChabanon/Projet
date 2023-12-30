
import random
import numpy as np


# TODO:
# - Implementer les mutations


class Insecte():
    '''
    Classe Insectes definissant le comportement des insectes dans la simulation
    '''

    def __init__(self, espece: str, sexe: str, max_health: int, life_time: int, mobilite: float, resistance: int, tps_reproduction: int, taille_max_portee: int, logger) -> None:
        self._espece = str(espece)
        self._sexe = str(sexe)
        self._max_health = int(max_health)
        self._health = int(max_health)
        self._life_time = int(life_time)
        self._mobilite = float(mobilite)
        self._resistance = int(resistance)
        self._tps_reproduction = int(tps_reproduction)
        self._taille_max_portee = int(taille_max_portee)

        self._time_since_last_reproduction = 0
        self._eat_combo = 0

        self._logger = logger

    # Getters et Setters

    def get_espece(self) -> str:
        return self._espece

    def get_sexe(self) -> str:
        return self._sexe

    def get_health(self) -> int:
        return self._health

    def set_health(self, new_health: int) -> None:
        self._health = new_health

    def get_mobilite(self) -> float:
        return self._mobilite

    def get_resistance(self) -> int:
        return self._resistance

    def get_tps_reproduction(self) -> int:
        return self._tps_reproduction

    def get_time_since_last_reproduction(self) -> int:
        return self._time_since_last_reproduction

    def set_time_since_last_reproduction(self, new_time: int) -> None:
        self._time_since_last_reproduction = new_time

    def get_taille_max_portee(self) -> int:
        return self._taille_max_portee

    def set_health(self, new_health: int) -> None:
        self._health = new_health

    def get_eat_combo(self) -> int:
        return self._eat_combo

    def get_life_time(self) -> int:
        return self._life_time

    life_time = property(get_life_time)
    health = property(get_health, set_health)
    resistance = property(get_resistance)
    tps_reproduction = property(get_tps_reproduction)
    mobilite = property(get_mobilite)
    sexe = property(get_sexe)
    espece = property(get_espece)

    def manger(self, parcelle) -> None:
        '''
        Methode permettant de faire manger un insecte
        L'insecte essaye de se nouriur de la plante dans la parcelle, si elle n'est pas presente, il perd de la vie.
        Si elle est presente, il gagne de la vie et un combo est incremente.
        '''
        if len(parcelle.get_plantes()) == 0:
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
                self._logger.info("Pas de partenaire trouve")
                return None
            if self._eat_combo > 0 and partenaire.get_eat_combo() > 0:
                self._time_since_last_reproduction = 0
                partenaire.set_time_since_last_reproduction(0)

                if self._sexe == "F":
                    taille_portee = self.taille_portee()
                else:
                    taille_portee = partenaire.taille_portee()

                for i in range(taille_portee):
                    attribus = self.__dict__
                    pas_mutable = ["_espece", "_sexe", "_logger"]
                    entiers = ["_max_health", "_life_time", "_resistance",
                               "_tps_reproduction", "_taille_max_portee"]
                    mutation = False
                    parite = False  # True si au moins un attribut a ete herite du partenaire
                    for j in attribus.keys():
                        if random.random() >= 0.5:
                            parite = True
                            attribus[j] = partenaire.__dict__[j]
                        if random.random() <= 0.05 and mutation == False and j not in pas_mutable:
                            mutation = True
                            attribus[j] = np.random.normal(
                                attribus[j], 0.05 * attribus[j])
                            if j in entiers:
                                attribus[j] = round(attribus[j])

                    if not parite:
                        # -2 pour ne pas prendre en compte le logger
                        k = random.randint(0, len(attribus.keys())-2)
                        attribus[list(attribus.keys())[k]] = partenaire.__dict__[
                            list(attribus.keys())[k]]

                    enfant = Insecte(attribus["_espece"], attribus["_sexe"], attribus["_max_health"], attribus["_life_time"],
                                     self._mobilite, self._resistance, self._tps_reproduction, self._taille_max_portee, self._logger)
                    enfant.health = int(enfant.health/2)
                    parcelle.add_insect(enfant)
                    self._logger.info(
                        f"Reproduction de l'insecte {self._espece} dans la parcelle {parcelle.coordonnes}")
        else:
            self._time_since_last_reproduction += 1

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
            parcelle.remove_insect(self)
            parcelle.get_voisin_aleatoire().add_insect(self)

    def mourir(self):
        self._logger.info(
            f"Mort de l'insecte {self._espece}")
        del self
