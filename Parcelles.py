import random
from Plantes import Plante


class Parcelle:
    def __init__(self, coordonees: tuple, plantes: list, insectes: list, humidite: float, has_engrais: bool, has_insecticide: bool, logger):
        self._coordonees = tuple(coordonees)
        self._humidite = float(humidite)
        self._has_engrais = bool(has_engrais)
        self._has_insecticide = bool(has_insecticide)
        self._est_arrose = False
        self._plantes = list(plantes)
        self._insectes = list(insectes)
        self._potager = None
        self._logger = logger
        self._dispositif = None

    def set_arrosage(self, bool):
        self._est_arrose = bool(bool)

    def get_coordonees(self):
        return self._coordonees

    def get_plantes(self):
        return self._plantes

    def get_insects(self):
        return self._insectes

    def get_humidite(self):
        return self._humidite

    def get_logger(self) -> object:
        return self._logger

    logger = property(get_logger)
    humidite = property(get_humidite)
    coordonnes = property(get_coordonees)

    def get_dispositif(self):
        if self._dispositif:
            return self._dispositif
        return None

    def set_dispositif(self, dispositif):
        self._dispositif = dispositif

    dispositif = property(get_dispositif, set_dispositif)

    def add_insect(self, insecte):
        self._insectes.append(insecte)

    def add_plante(self, plante):
        self._plantes.append(plante)

    def remove_insect(self, insecte):
        self._insectes.remove(insecte)

    def has_engrais(self):
        return self._has_engrais

    def set_engrais(self, bool):
        self._has_engrais = bool

    def has_insecte(self):
        if len(self._insectes) > 0:
            return True
        return False

    def is_saturated(self):
        somme = 0
        for plante in self._plantes:
            somme += plante.surface
            if somme >= 1:
                return True
        return False

    def has_insecticide(self):
        return self._has_insecticide

    def set_insecticide(self, bool: bool):
        self._has_insecticide = bool(bool)

    def choose_partenaire(self, insecte) -> object:
        '''
        Methode choisisant un partenaire pour la reproduction d'un insecte
        '''
        for i in self._insectes:
            if i.get_time_since_last_reproduction() >= i.get_tps_reproduction() and i.get_sexe() != insecte.get_sexe() and i.get_espece() == insecte.get_espece():
                return i
        return None

    def get_voisins(self, rayon: int = 1) -> list:
        '''
        Retourne les voisins dans un rayon donne
        '''
        matrice = self._potager.get_matrice()
        voisins = []
        x, y = self._coordonees
        for dx in range(-rayon, rayon + 1):
            for dy in range(-rayon, rayon + 1):
                if abs(dx) + abs(dy) <= rayon and (dx, dy) != (0, 0):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < len(matrice) and 0 <= ny < len(matrice[0]) and matrice[nx][ny] != 0:
                        voisins.append(matrice[nx][ny])
        return voisins

    # Que 4 voisins + check si la case est pas 0 !
    def get_voisin_aleatoire(self, rayon=1) -> object:
        '''
        Retourne un voisin aleatoire de la parcelle
        '''
        voisins = self.get_voisins(rayon)

        if voisins:
            return random.choice(voisins)
        else:
            # Si les voisins sont tous des 0 (ie pas des parcelles)
            return None

    def update(self, potager) -> None:
        '''
        Methode mettant a jour la parcelle:
        - Mise a jour de l'humidite
        - Mise a jour des plantes
        - Mise a jour des insectes
        - Mise a jour du dispositif
        '''
        self._potager = potager

        total_recoltes = 0

        if self._est_arrose == True:
            self._humidite += 0.5*self._humidite  # Doute sur l'ennoncé (+50%)
            if self._humidite > 1:
                self._humidite = 1
        else:
            self._humidite -= 0.2

        for i in self._plantes:
            i.developper(self)
            total_recoltes += i.nb_recoltes

        for i in self._insectes:
            i.manger(self)
            if i.get_health() <= 0 or i.life_time < potager.get_pas():
                self.remove_insect(i)
                i.mourir()
            elif self._has_insecticide and random.random() <= i.get_resistance():
                self.remove_insect(i)
                i.mourir()
            else:
                i.bouger(self)
                i.se_reproduire(self)
        if self._dispositif:
            self._dispositif.update(self._potager.get_pas())
        self._logger.debug(
            f"[Parcelle {self._coordonees}]: {len(self._plantes)} plantes - {len(self._insectes)} insectes - Dispositif: {False if self._dispositif == None else True}")

        if not self._coordonees in self._logger.resultats.keys():
            self._logger.resultats[self._coordonees] = [[len(self._plantes), len(self._insectes), total_recoltes,
                                                        self._est_arrose, self._has_engrais, self._has_insecticide, self._humidite]]
        else:
            self._logger.resultats[self._coordonees] += [[len(self._plantes), len(self._insectes), total_recoltes,
                                                         self._est_arrose, self._has_engrais, self._has_insecticide, self._humidite]]
