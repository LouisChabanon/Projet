
import random
from Logger import Logger


class Plante():
    def __init__(self, espece: str, tps_maturite: int, nb_max_recoltes: int, domaine_humidite: list, duree_maturation: int, surface: float) -> None:
        self._espece = str(espece)
        self._tps_maturite = int(tps_maturite)
        self._nb_max_recoltes = int(nb_max_recoltes)
        self._domaine_humidite = domaine_humidite
        self._duree_maturation = int(duree_maturation)
        self._surface = float(surface)

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
        print(f"Developpement de la plante {self._espece}")
        h = 0
        if parcelle.get_humidite() >= self._domaine_humidite[0] and parcelle.get_humidite() <= self._domaine_humidite[1]:
            h = 1
        dev = max(0, (1+int(parcelle.has_engrais())) *
                  (1+1*h - 1*int(parcelle.has_insecte())))

        if self._maturite < self._tps_maturite:
            print(
                f"Maturation de la plante {self._espece} : {self._maturite + dev} / {self._tps_maturite}")
            self._maturite += dev
        else:
            self._maturation += dev
            if self._maturation >= self._duree_maturation:
                self._maturation = 0
                if self._nb_max_recoltes > self._nb_recoltes:
                    self._nb_recoltes += 1
        if parcelle.has_insecticide():
            self._duree_insecticide += 1
        print(f"nb de recoltes: {self._nb_recoltes}")


class Drageonnante(Plante):
    def __init__(self, espece: str, tps_maturite: int, nb_max_recoltes: int, domaine_humidite: list, duree_maturation: int, surface: float, proba_drageon: float) -> None:
        super().__init__(espece, tps_maturite, nb_max_recoltes,
                         domaine_humidite, duree_maturation, surface)
        self._proba_drageonnage = float(proba_drageon)

    def developper(self, parcelle) -> None:
        super().developper(parcelle)
        self.drageonner(parcelle)

    def drageonner(self, parcelle) -> None:
        '''
        Methode permettant de faire drageonner une plante
        '''
        if random.random() <= self._proba_drageonnage:
            voisin = parcelle.get_voisin_aleatoire()
            if not voisin.is_saturated():
                drageon = Drageonnante(self._espece, self._tps_maturite, self._nb_max_recoltes,
                                       self._domaine_humidite, self._duree_maturation, self._surface, proba_drageon=self._proba_drageonnage)
                voisin.add_occupant(drageon)
