import logging
import datetime
import csv


class Logger():
    '''Classe permettant de gerer les logs de la simulation et le rapport final de la simulation au format csv'''

    def __init__(self, debug: bool = False) -> None:
        self._debug = debug
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO,
                            format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S', filename=datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "-simulation.log")
        self._resultats = dict()

    def get_resultats(self) -> list:
        return self._resultats

    def set_resultats(self, resultats: list) -> None:
        self._resultats = resultats

    resultats = property(get_resultats, set_resultats)

    def debug(self, msg: str) -> None:
        if self._debug:
            print(f"\033[1;37m[DEBUG]\033[0m {msg}")
        logging.debug(msg)

    def info(self, msg: str) -> None:
        logging.info(msg)
        print(f"\033[1;32m[INFO]\033[0m {msg}")

    def warning(self, msg: str) -> None:
        logging.warning(msg)
        print(f"\033[1;33m[WARNING]\033[0m {msg}")

    def error(self, msg: str) -> None:
        logging.error(msg)
        print(f"\033[1;31m[ERROR]\033[0m {msg}")

    def critical(self, msg: str) -> None:
        logging.error(msg)
        print(f"\033[1;31m[CRITICAL]\033[0m {msg}")

    def create_csv(self) -> None:
        '''Methode permettant de creer un fichier csv contenant les resultats de la simulation'''
        total_recoltes = 0
        self.info("Creation du fichier CSV")
        for i in self._resultats.keys():
            total_recoltes += self._resultats[i][1][2]
        with open(datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "-resultats.csv", "w") as f:
            w = csv.writer(f)
            w.writerows(self._resultats.items())
        self.info("Fichier CSV cree")
        self.info(f"Total recoltes: {total_recoltes}")
