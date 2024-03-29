import logging
import datetime
import os

class Logger():
    '''Classe permettant de gerer les logs de la simulation et le rapport final de la simulation au format csv'''

    def __init__(self, debug: bool = False) -> None:
        self._debug = debug
        
        logs_dir = "logs/"
        os.makedirs(logs_dir, exist_ok=True)
        os.makedirs("resultats/", exist_ok=True)
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S', filename=logs_dir + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "-simulation.log")

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
