from Parcelles import Parcelle
from Insectes import Insecte
from Plantes import Plante
from Dispositifs import Dispositif


class Potager():
    def __init__(self, matrice) -> None:
        self._matrice = matrice

    def get_matrice(self):
        return self._matrice

    def run(self):
        for i in self._matrice:
            for j in i:
                if j != 0:
                    j.update(self)


def main():
    potager = Potager([[Parcelle((0, 0), [], [], 0.5, False, False)]])


if __name__ == "__main__":
    main()
