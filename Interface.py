import tkinter as TK
from tkinter.ttk import Progressbar


class Interface():
    def __init__(self, potager) -> None:
        self.fenetre = TK.Tk()
        self.fenetre.title("Interface POOtager")
        self._potager = potager
        self._nb_pas = potager.duree

        TK.Label(self.fenetre, text="Nombre de pas de simulation: ").grid(
            row=0, column=0, padx=5, pady=5)
        TK.Spinbox(self.fenetre, from_=10, to=1000, width=5, textvariable=self._nb_pas).grid(
            row=0, column=1, padx=5, pady=5)
        TK.Button(self.fenetre, text="Valider", command=self.changer_nb_pas).grid(row=0, column=2,
                                                                                  padx=5, pady=5)

        TK.Button(self.fenetre, text="Lancer la simulation",
                  command=self._potager.run).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self._liste_parcelles = TK.Listbox(self.fenetre).grid(row=2, column=0, columnspan=2,
                                                              rowspan=4, padx=5, pady=5)

        self.fenetre.mainloop()

    def get_nb_pas(self) -> int:
        return self._nb_pas

    def changer_nb_pas(self) -> None:
        self._potager.set_duree(self._nb_pas)
