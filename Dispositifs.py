
class Type_Produit():
    ''' Enumeration des types de produits'''
    EAU = 0
    ENGRAIS = 1
    INSECTICIDE = 2


class Dispositif():
    ''' Dispositif permettant de gerer les programmes d'arrosage, d'engrais et d'insecticide '''

    def __init__(self, parcelle, rayon: int, programmes: list) -> None:
        self._programmes = programmes
        self._rayon = int(rayon)
        self._parcelle = parcelle

    def update(self, pas: int) -> None:
        ''' Mise a jour du dispositif'''
        for programme in self._programmes:
            if pas == programme.debut:
                if programme.type_produit == Type_Produit.ENGRAIS:
                    self._parcelle.set_engrais(True)
                elif programme.type_produit == Type_Produit.INSECTICIDE:
                    self._parcelle.set_insecticide(True)
                elif programme.type_produit == Type_Produit.EAU:
                    self._parcelle.set_arrosage(True)

            elif pas == programme.debut + programme.duree:
                programme.debut += programme.periode
                if programme.type_produit == Type_Produit.ENGRAIS:
                    self._parcelle.set_engrais(False)
                elif programme.type_produit == Type_Produit.INSECTICIDE:
                    self._parcelle.set_insecticide(False)
                elif programme.type_produit == Type_Produit.EAU:
                    self._parcelle.set_arrosage(False)


class Programme():
    ''' Programme d'un dispositif '''

    def __init__(self, debut: int, duree: int, periode: int, type_produit) -> None:
        self._debut = int(debut)
        self._duree = int(duree)
        self._periode = int(periode)
        self._type_produit = type_produit

    def get_debut(self) -> int:
        return self._debut

    def get_duree(self) -> int:
        return self._duree

    def get_type_produit(self) -> str:
        return self._type_produit

    def get_periode(self) -> int:
        return self._periode

    def set_debut(self, new_debut: int) -> None:
        self._debut = new_debut

    debut = property(get_debut, set_debut)
    duree = property(get_duree)
    periode = property(get_periode)
    type_produit = property(get_type_produit)
