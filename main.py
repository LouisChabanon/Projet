
import argparse
import xml.etree.ElementTree as ET

from Interface import Interface
from Logger import Logger
from Parcelles import Parcelle
from Insectes import Insecte
from Plantes import Plante, Drageonnante
from Dispositifs import Dispositif, Programme


class Potager():
    ''' Classe representant le potager'''

    def __init__(self, matrice, logger) -> None:
        self._matrice = matrice
        self._logger = logger
        self._pas = 0
        self._duree = args.num

    def get_matrice(self) -> list:
        return self._matrice

    def get_logger(self) -> Logger:
        return self._logger

    def get_pas(self) -> int:
        return self._pas

    def get_duree(self) -> int:
        return self._duree

    def set_duree(self, duree: int) -> None:
        if int(duree) > 0:
            self._duree = int(duree)
        else:
            self._logger.error("La duree doit etre un entier positif")
            raise ValueError("La duree doit etre un entier positif")

    duree = property(get_duree, set_duree)

    def run(self):
        '''Methode gerant la simulation du potager'''
        logger.info(f"Debut de la simulation pour {self._duree} tours")
        for i in range(self._duree):
            logger.debug(f"Tour {i}/{self._duree}")
            for i in self._matrice:
                for j in i:
                    if j != 0:
                        logger.debug(
                            f" Updating parcelle {j.get_coordonees()}")
                        j.update(self)
            self._pas += 1
        logger.info("Fin de la simulation")
        self.bilan()

    def bilan(self) -> None:
        '''Methode permettant de faire le bilan de la simulation'''
        self._logger.create_csv()


def load_config(conf: str = "config.xml") -> Potager:
    '''
    Fonction permettant de charger la configuration du potager depuis un fichier XML
    '''
    tree = ET.parse(conf)
    root = tree.getroot()

    logger.info("Chargement de la configuration du potager")

    nb_parcelles = 0
    nb_plantes = 0
    nb_drageons = 0
    nb_insectes = 0
    nb_dispositifs = 0
    matrice = [[0 for i in range(20)]
               for j in range(20)]  # Change this
    for i in root:
        if i.tag == "Parcelle":
            logger.debug(
                f"Chargement de la parcelle {i.attrib['Pos_x']}, {i.attrib['Pos_y']}")
            parcelle = Parcelle((int(i.attrib["Pos_x"]), int(
                i.attrib["Pos_y"])), [], [], 0.5, False, False, logger)
            matrice[int(i.attrib["Pos_x"])][int(i.attrib["Pos_y"])] = parcelle
            nb_parcelles += 1
            for j in i:
                logger.debug(f"Chargement de {j.tag}")
                if j.tag == "Plante":
                    plante = Plante(j.attrib["Espece"], int(j.attrib["Maturite_pied"]), int(j.attrib["Nb_recolte"]), [
                                    float(j.attrib["Humidite_min"]), float(j.attrib["Humidite_max"])], int(j.attrib["Maturite_fruit"]), float(j.attrib["Surface"]), logger)
                    parcelle.add_plante(plante)
                    nb_plantes += 1

                elif j.tag == "Plante_Drageonnante":
                    plante = Drageonnante(j.attrib["Espece"], int(j.attrib["Maturite_pied"]), int(j.attrib["Nb_recolte"]), [
                        float(j.attrib["Humidite_min"]), float(j.attrib["Humidite_max"])], int(j.attrib["Maturite_fruit"]), float(j.attrib["Surface"]), logger, float(j.attrib["Proba_Colonisation"]))
                    parcelle.add_plante(plante)
                    nb_drageons += 1
                elif j.tag == "Insecte":
                    insecte = Insecte(j.attrib["Espece"], j.attrib["Sexe"], int(j.attrib["Vie_max"]), int(j.attrib["Duree_vie_max"]), float(
                        j.attrib["Proba_mobilite"]), float(j.attrib["Resistance_insecticide"]), int(j.attrib["Temps_entre_repro"]), int(j.attrib["Max_portee"]), logger)
                    parcelle.add_insect(insecte)
                    nb_insectes += 1
                elif j.tag == "Dispositif":
                    programmes = []
                    for programme in j:
                        programmes.append(
                            Programme(int(programme.attrib["Debut"]), int(programme.attrib["Duree"]), int(programme.attrib["Periode"]), str(programme.attrib["Produit"]), ))
                    dispositif = Dispositif(parcelle, int(
                        j.attrib["Rayon"]), programmes)
                    parcelle.dispositif = dispositif
                    nb_dispositifs += 1

    logger.info(
        f"Chargement termine : {nb_parcelles} parcelles, {nb_plantes} plantes, {nb_drageons} plantes drageonnantes, {nb_insectes} insectes, {nb_dispositifs} dispositifs")
    potager = Potager(matrice, logger)
    return potager


def main(args: object) -> None:
    logger.info("Simulation du potager")
    potager = load_config(args.config)

    interface = Interface(potager)


if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Simulateur de potager")
    parser.add_argument("-c", "--config", type=str, default="config.xml",
                        help="Chemin vers le fichier de configuration au format XML")
    parser.add_argument("-n", "--num", type=int, default=100,
                        help="Nombre de tours de simulation")
    parser.add_argument("-d", "--debug", action="store_true",
                        default=False, help="Active le mode verbose")
    args = parser.parse_args()

    logger = Logger(args.debug)
    main(args)
