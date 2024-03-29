
import argparse
import xml.etree.ElementTree as ET
import datetime
import time

from Utils.Interface import Interface
from Utils.Logger import Logger
from POOtager.Parcelles import Parcelle
from POOtager.Insectes import Insecte
from POOtager.Plantes import Plante, Drageonnante
from POOtager.Dispositifs import Dispositif, Programme


class Potager():
    ''' Classe representant le potager'''

    def __init__(self, matrice: list[list], logger: Logger) -> None:
        self._matrice = matrice
        self._logger = logger
        self._pas = 0
        self._duree = args.num
        self._interface = None

    def get_matrice(self) -> list:
        return self._matrice
    
    def get_logger(self) -> Logger:
        return self._logger
    
    def get_interface(self) -> Interface:
        return self._interface
    
    def set_interface(self, interface: Interface) -> None:
        self._interface = interface

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
    interface = property(get_interface, set_interface)

    def create_xml(self) -> None:
        '''Methode permettant de creer un fichier XML contenant les resultats de la simulation'''
        root = ET.Element("resultats")
        for i in range(self._pas):
            tour = ET.SubElement(root, "tour", name=str(i))
            for ligne in self._matrice:
                for p in ligne:
                    if p != 0:
                        recoltes = p.recoltes
                        parcelle = ET.SubElement(
                            tour, "parcelle", pos=str(p.get_coordonees()), recoltes=str(recoltes[i][0]), insecticide=str(recoltes[i][1]), nb_insectes=str(recoltes[i][2]))
        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        try:
            tree.write("resultats/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") +
                       "-resultats.xml", encoding="UTF-8")
        except Exception as e:
            self._logger.error("Impossible de creer le fichier XML")
            raise Exception(f"Impossible de creer le fichier XML: {str(e)}")
        logger.info("Fichier XML cree")

    def plot(self) -> list:
        '''Methode permettant de renvoyer les resultats necessaire à l'affichage sur l'interface de la simulation
        :return: liste contenant le nombre de pas, le nombre de recoltes et le nombre d'insectes par pas'''
        plantes = [0 for i in range(self._pas)]
        insectes = [0 for j in range(self._pas)]
        for i in range(self._pas):
            for ligne in self._matrice:
                for p in ligne:
                    if p != 0:
                        plantes[i] += p.recoltes[i][0]
                        insectes[i] += p.recoltes[i][2]
        return [self._pas, plantes, insectes]

    def run(self):
        '''Methode gerant la simulation du potager'''
        logger.info(f"Debut de la simulation pour {self._duree} tours")
        start = time.time()
        for i in range(self._duree):
            logger.debug(f"Tour {i}/{self._duree}")
            for i in self._matrice:
                for j in i:
                    if j != 0:
                        logger.debug(
                            f" Updating parcelle {j.get_coordonees()}")
                        j.update(self)
            self._pas += 1
        end = time.time()
        # Mise a jour de l'interface à la fin de la simulation
        if self._interface is not None:
                self._interface.update()
        logger.info(f"Fin de la simulation en {(end-start):.2} secondes")
        logger.info("Creation du fichier XML")
        self.create_xml()


def load_config(conf: str = "configs/config.xml") -> Potager:
    '''
    Fonction permettant de charger la configuration du potager depuis un fichier XML
    :param conf: chemin vers le fichier XML contenant la configuration du potager
    :return: Objet Potager
    '''
    tree = ET.parse(conf)
    root = tree.getroot()

    logger.info("Chargement de la configuration du potager")

    nb_parcelles = 0
    nb_plantes = 0
    nb_drageons = 0
    nb_insectes = 0
    nb_dispositifs = 0
    matrice = [[0 for i in range(int(root.attrib["Size_y"]))] for j in range(int(root.attrib["Size_x"]))]

    for i in root:
        if i.tag == "Parcelle":
            logger.debug(f"Chargement de la parcelle {i.attrib['Pos_x']}, {i.attrib['Pos_y']}")
            parcelle = Parcelle((int(i.attrib["Pos_x"]), int(i.attrib["Pos_y"])), [], [], 0.5, False, False, logger)
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
                            Programme(int(programme.attrib["Debut"]), int(programme.attrib["Duree"]), int(programme.attrib["Periode"]), str(programme.attrib["Produit"])))
                    dispositif = Dispositif(parcelle, int(
                        j.attrib["Rayon"]), programmes)
                    parcelle.dispositif = dispositif
                    nb_dispositifs += 1

    logger.info(f"Chargement termine : {nb_parcelles} parcelles, {nb_plantes} plantes, {nb_drageons} plantes drageonnantes, {nb_insectes} insectes, {nb_dispositifs} dispositifs")
    potager = Potager(matrice, logger)
    return potager


def main(args: object) -> None:
    '''Fonction principale du programme
    :param args: objet contenant les arguments passes au programme
    :return: None
    '''
    logger.info("Simulation du potager")
    potager = load_config(args.config)
    if args.interface:
        interface = Interface(potager)
        potager.interface = interface
        interface.start()
        resultats = potager.plot()
        interface.plot_resultat(resultats[0], resultats[1], resultats[2])
    else:
        potager.run()


if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Simulateur de potager")
    parser.add_argument("-c", "--config", type=str, default="config.xml",
                        help="Chemin vers le fichier de configuration au format XML")
    parser.add_argument("-n", "--num", type=int, default=100,
                        help="Nombre de tours de simulation")
    parser.add_argument("-d", "--debug", action="store_true",
                        default=False, help="Active le mode verbose")
    parser.add_argument("-i", "--interface", action="store_true",
                        default=False, help="Active l'interface graphique")
    args = parser.parse_args()

    logger = Logger(args.debug)
    main(args)
