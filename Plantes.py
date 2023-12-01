

class Plantes():
    def __init__(self, espece: str, tps_maturite: int, nb_recoltes: int, domaine_humidite: list, duree_maturation: int, surface: float) -> None:
        self._espece = str(espece)
        self._tps_maturite = int(tps_maturite)
        self._nb_recoltes = int(nb_recoltes)
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
        h = 0
        if parcelle.get_humidite() >= self._domaine_humidite[0] and parcelle.get_humidite() <= self._domaine_humidite[1]:
            h = 1
        dev = max(0, (1+parcelle.has_engrais()) *
                  (1+1*h - 1*parcelle.has_insecte()))

        if self._maturite < self._tps_maturite:
            self._maturite += dev
        else:
            self._maturation += dev
            if self._maturation >= self._duree_maturation:
                self._nb_recoltes += 1
                self._maturation = 0

    def drageonner(self, parcelle) -> None:
        '''
        Methode permettant de faire drageonner une plante
        '''


class Drageonnantes(Plantes):
    def __init__(self, espece: str, tps_maturite: int, nb_recoltes: int, domaine_humidite: list, duree_maturation: int, surface: float, nb_drageons: int) -> None:
        pass
