
import random
from Logger import Logger
proba_drageonnage = dict()
proba_drageonnage["Solanum lycopersicum"] = 0.1
proba_drageonnage["Tuberosum"] = 0.1

# TODO:
# - Plantes Drageonantes
logger = Logger()


class Plante():
    def __init__(self, espece: str, tps_maturite: int, nb_recoltes: int, domaine_humidite: list, duree_maturation: int, surface: float) -> None:
        self._espece = str(espece)
        self._tps_maturite = int(tps_maturite)
        self._nb_recoltes = int(nb_recoltes)
        self._domaine_humidite = domaine_humidite
        self._duree_maturation = int(duree_maturation)
        self._surface = float(surface)

        self._proba_drageonnage = proba_drageonnage[self._espece]
        self._duree_insecticide = 0
        self._maturation = 0
        self._maturite = 0
        self._nb_recoltes = 0

    def get_espece(self) -> str:
        return self._espece

    def get_tps_maturite(self) -> int:
        return self._tps_maturite

    def developper(self, parcelle) -> None:
        '''
        Methode permettant de faire evoluer une plante
        '''
        logger.info(f"Developpement de la plante {self._espece}")
        h = 0
        if parcelle.get_humidite() >= self._domaine_humidite[0] and parcelle.get_humidite() <= self._domaine_humidite[1]:
            h = 1
        dev = max(0, (1+parcelle.has_engrais()) *
                  (1+1*h - 1*parcelle.has_insecte()))
        logger.info(f"Dev: {dev}")

        if self._maturite < self._tps_maturite:
            self._maturite += dev
        else:
            self._maturation += dev
            if self._maturation >= self._duree_maturation:
                self._nb_recoltes += 1
                self._maturation = 0
            self.drageonner(parcelle)
        if parcelle.has_insecticide():
            self._duree_insecticide += 1


class Drageonnantes(Plante):
    def __init__(self, espece: str, tps_maturite: int, nb_recoltes: int, domaine_humidite: list, duree_maturation: int, surface: float, nb_drageons: int) -> None:
        pass

    def drageonner(self, parcelle) -> None:
        '''
        Methode permettant de faire drageonner une plante
        '''
        if random.random() <= self._proba_drageonnage:
            voisin = parcelle.get_voisin_aleatoire()
            if not voisin.is_saturated():
                voisin.add_occupant()
