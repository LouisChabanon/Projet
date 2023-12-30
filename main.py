
import argparse
import xml.etree.ElementTree as ET

from Logger import Logger
from Parcelles import Parcelle
from Insectes import Insecte
from Plantes import Plante, Drageonnante
from Dispositifs import Dispositif, Programme


class Potager():
    def __init__(self, matrice, logger) -> None:
        self._matrice = matrice
        self._logger = logger
        self._pas = 0

    def get_matrice(self):
        return self._matrice

    def get_logger(self):
        return self._logger

    def get_pas(self):
        return self._pas

    def run(self):
        logger.info("Debut de la simulation")
        for i in range(args.num):
            logger.info(f"Tour {i}/{args.num}")
            for i in self._matrice:
                for j in i:
                    if j != 0:
                        logger.debug(
                            f" Updating parcelle {j.get_coordonees()}")
                        j.update(self)
            self._pas += 1
        logger.info("Fin de la simulation")
        logger.info(
            f"Bilan de la simulation : {self.bilan()[0]} récoltes - {self.bilan()[1]} insectes")

    def bilan(self):
        total_plantes, total_insectes = 0, 0
        for ligne in self._matrice:
            for parcelle in ligne:
                if parcelle != 0:
                    bp = parcelle.bilan()
                    total_plantes += bp[0]
                    total_insectes += bp[1]
        return total_plantes, total_insectes


def load_config(conf: str = "config.xml"):
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


def main(args):
    logger.info("Simulation du potager")
    potager = load_config(args.config)

    # Simulation
    potager.run()


if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Simulateur de potager")
    parser.add_argument("-c", "--config", type=str, default="config.xml",
                        help="Chemin vers le fichier de configuration")
    parser.add_argument("-n", "--num", type=int, default=100,
                        help="Nombre de tours de simulation")
    parser.add_argument("-d", "--debug", action="store_true",
                        default=False, help="Active le mode debug")
    args = parser.parse_args()

    logger = Logger(args.debug)
    main(args)
