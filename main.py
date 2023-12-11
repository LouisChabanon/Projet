
import argparse
import xml.etree.ElementTree as ET

from Logger import Logger
from Parcelles import Parcelle
from Insectes import Insecte
from Plantes import Plante, Drageonnante
# from Dispositifs import Dispositif


class Potager():
    def __init__(self, matrice) -> None:
        self._matrice = matrice
        self._total_recoltes = 0

    def get_matrice(self):
        return self._matrice

    def run(self):
        for i in self._matrice:
            for j in i:
                if j != 0:
                    logger.debug(f" Updating parcelle {j.get_coordonees()}")
                    j.update(self)

    def bilan(self):
        return self._total_recoltes


def load_config(conf: str = "config.xml"):
    '''
    Fonction permettant de charger la configuration du potager depuis un fichier XML
    '''
    tree = ET.parse(conf)
    root = tree.getroot()

    logger.info("Chargement de la configuration du potager")

    matrice = [[0 for i in range(20)]
               for j in range(20)]  # Change this
    for i in root:
        if i.tag == "Parcelle":
            logger.debug(
                f"Chargement de la parcelle {i.attrib['Pos_x']}, {i.attrib['Pos_y']}")
            parcelle = Parcelle((int(i.attrib["Pos_x"]), int(
                i.attrib["Pos_y"])), [], [], 0.5, False, False)
            matrice[int(i.attrib["Pos_x"])][int(i.attrib["Pos_y"])] = parcelle
            for j in i:
                logger.debug(f"Chargement de {j.tag}")
                if j.tag == "Plante":
                    plante = Plante(j.attrib["Espece"], int(j.attrib["Maturite_pied"]), int(j.attrib["Nb_recolte"]), [
                                    float(j.attrib["Humidite_min"]), float(j.attrib["Humidite_max"])], int(j.attrib["Maturite_fruit"]), float(j.attrib["Surface"]))
                    parcelle.add_plante(plante)

                elif j.tag == "Plante_Drageonnante":
                    plante = Drageonnante(j.attrib["Espece"], int(j.attrib["Maturite_pied"]), int(j.attrib["Nb_recolte"]), [
                        float(j.attrib["Humidite_min"]), float(j.attrib["Humidite_max"])], int(j.attrib["Maturite_fruit"]), float(j.attrib["Surface"]), float(j.attrib["Proba_Colonisation"]))
                elif j.tag == "Insecte":
                    insecte = Insecte(j.attrib["Espece"], j.attrib["Sexe"], int(j.attrib["Duree_vie_max"]), 100, float(
                        "Proba_mobilite"), int(j.attrib["Resistance_insecticide"]), int(j.attrib["temps_entre_repro"]), int(j.attrib["Max_portee"]))
                    parcelle.add_insect(insecte)
                elif j.tag == "Dispositif":
                    pass

    potager = Potager(matrice)
    return potager


def main(args):
    logger.info("Simulation du potager")
    potager = load_config(args.config)

    # Simulation

    logger.info("Debut de la simulation")
    for i in range(args.num):
        potager.run()
    logger.info("Fin de la simulation")


if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Simulateur de potager")
    parser.add_argument("-c", "--config", type=str, default="config.xml",
                        help="Chemin vers le fichier de configuration")
    parser.add_argument("-n", "--num", type=int, default=1000,
                        help="Nombre de tours de simulation")
    parser.add_argument("-d", "--debug", action="store_true",
                        default=False, help="Active le mode debug")
    args = parser.parse_args()

    logger = Logger(args.debug)
    main(args)
