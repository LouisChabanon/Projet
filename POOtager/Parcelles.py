import random
from POOtager.Plantes import Plante


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
        self._recoltes = []

    def set_arrosage(self, bool):
        self._est_arrose = bool

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

    def get_recoltes(self):
        return self._recoltes

    logger = property(get_logger)
    humidite = property(get_humidite)
    coordonnes = property(get_coordonees)
    recoltes = property(get_recoltes)

    def get_pas(self):
        return self._potager.get_pas()

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
        """
        Vérifie si la parcelle est saturée en plantes.

        Returns:
            bool: True si la somme de la surface de toutes les plantes dans la parcelle est supérieure ou égale à 1, False sinon.
        """
        somme = 0
        for plante in self._plantes:
            somme += plante.surface
            if somme >= 1:
                return True
        return False

    def has_insecticide(self):
        return self._has_insecticide

    def set_insecticide(self, bool: bool):
        self._has_insecticide = bool

    def choose_partenaire(self, insecte) -> object:
        '''
        Methode choisisant un partenaire pour la reproduction d'un insecte
        '''
        if len(self._insectes) > 1000:
            self._logger.warning(f"La parcelle {self._coordonees} est saturee en insectes")
            return None
        if self._insectes:
            partenaire = self._insectes[random.randint(0, len(self._insectes)-1)]
            if partenaire.get_time_since_last_reproduction() >= partenaire.get_tps_reproduction() and partenaire.get_sexe() != insecte.get_sexe() and partenaire.get_espece() == insecte.get_espece():
                return partenaire
        '''for i in self._insectes:
            if i.get_time_since_last_reproduction() >= i.get_tps_reproduction() and i.get_sexe() != insecte.get_sexe() and i.get_espece() == insecte.get_espece():
                return i'''
        return None

    def get_voisins(self, rayon: int = 1) -> list[int]:
        '''
        Retourne les voisins dans un rayon donne

        Parameters:
            rayon (int): Le rayon dans lequel chercher les voisins. Par défaut, la valeur est 1.

        Returns:
            list[int]: Une liste des voisins trouvés dans le rayon donné.
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

    def get_voisin_aleatoire(self, rayon=1) -> object:
        '''
        Retourne un voisin aleatoire de la parcelle.

        Parameters:
            rayon (int): Le rayon de recherche des voisins. Par défaut, la valeur est 1.

        Returns:
            object: Un voisin aléatoire de la parcelle. Si aucun voisin n'est trouvé, retourne None.
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

        Parameters:
            potager (Potager): L'objet Potager contenant les informations sur le jardin

        Returns:
            None
        '''
        self._potager = potager
        self._recoltes.append([0, self._has_insecticide, []])

        if self._est_arrose == True:
            self._humidite += 0.5*self._humidite  # Doute sur l'ennoncé (+50%)
            if self._humidite > 1:
                self._humidite = 1
        else:
            self._humidite -= 0.2

        for i in self._plantes:
            i.developper(self)
            self._recoltes[self._potager.get_pas()][0] += i.nb_recoltes

        for i in self._insectes:
            i.manger(self)
            if i.get_health() <= 0 or i.life_time < potager.get_pas():
                self.remove_insect(i)
                self._logger.debug(f"Mort de l'insecte {i.get_espece()} par vieillesse ou malnutrition")
                i.mourir()
            elif self._has_insecticide and random.random() >= i.get_resistance():
                self.remove_insect(i)
                self._logger.debug(f"Mort de l'insecte {i.get_espece()} par insecticide")
                i.mourir()
            else:
                i.bouger(self)
                i.se_reproduire(self)

        if len(self._insectes) != 0:
            self._recoltes[self._potager.get_pas()][2] = len(self._insectes)
        else:
            self._recoltes[self._potager.get_pas()][2] = 0

        if self._dispositif:
            self._dispositif.update(self._potager.get_pas())
        self._logger.debug(
            f"[Parcelle {self._coordonees}]: {len(self._plantes)} plantes - {len(self._insectes)} insectes - Dispositif: {False if self._dispositif == None else True}")
