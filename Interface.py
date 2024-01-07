
import tkinter as TK

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


class Interface():
    def __init__(self, potager) -> None:
        self.fenetre = TK.Tk()
        self.fenetre.title("Interface POOtager")
        self._potager = potager
        self._nb_pas = TK.IntVar()
        self._nb_pas.set(potager.get_duree())

        TK.Label(self.fenetre, text="Nombre de pas de simulation: ").grid(
            row=0, column=0)
        TK.Spinbox(self.fenetre, from_=10, to=1000, width=5, textvariable=self._nb_pas).grid(
            row=0, column=1)
        TK.Button(self.fenetre, text="Valider", command=self.changer_nb_pas).grid(row=0, column=2,
                                                                                  padx=5, pady=5)

        TK.Button(self.fenetre, text="Lancer la simulation",
                  command=self._potager.run).grid(row=1, column=0, columnspan=2)

    def get_nb_pas(self) -> int:
        return self._nb_pas.get()

    def changer_nb_pas(self) -> None:
        self._potager.set_duree(self._nb_pas.get())

    def start(self) -> None:
        self.fenetre.mainloop()

    def plot_resultat(self, pas: int, recoltes: list, insectes: list) -> None:
        fenetre_resultat = TK.Tk()
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.add_subplot(211).plot(
            [i for i in range(pas)], recoltes, label="recoltes", color="red")
        fig.add_subplot(212).plot(
            [i for i in range(pas)], insectes, label="insectes")
        fig.legend()
        canvas = FigureCanvasTkAgg(fig, master=fenetre_resultat)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TK.TOP, fill=TK.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, fenetre_resultat)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TK.TOP, fill=TK.BOTH, expand=1)
        fenetre_resultat.mainloop()
