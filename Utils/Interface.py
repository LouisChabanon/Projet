
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
        self._bt = dict()

        TK.Label(self.fenetre, text="Nombre de pas de simulation: ").grid(
            row=0, column=0)
        TK.Spinbox(self.fenetre, from_=10, to=1000, width=5, textvariable=self._nb_pas).grid(
            row=0, column=1)
        TK.Button(self.fenetre, text="Valider", command=self.changer_nb_pas).grid(row=0, column=2,padx=5, pady=5)

        TK.Button(self.fenetre, text="Lancer la simulation", command=self._potager.run).grid(row=1, column=0, columnspan=2)

        for i in range(len(self._potager.get_matrice())):
            for j in range(len(self._potager.get_matrice()[i])):
                if self._potager.get_matrice()[i][j] != 0:
                    parcelle = self._potager.get_matrice()[i][j]
                    texte = f"{parcelle.get_coordonees()}\n{0} récoltes \n insecticide: {parcelle.has_insecticide()}\n{len(parcelle.get_insects())} insectes"
                    TK.Button(self.fenetre, bg="gray85", text=texte, padx=100, pady=100).grid(row=i+2, column=j+3)
                    if len(self._potager.get_matrice()[i][j].get_plantes()) != 0:
                        TK.Button(self.fenetre, bg="green", text=texte, padx=100, pady=100).grid(row=i+2, column=j+3)

    def get_nb_pas(self) -> int:
        return self._nb_pas.get()

    def changer_nb_pas(self) -> None:
        self._potager.set_duree(self._nb_pas.get())

    def start(self) -> None:
        self.fenetre.mainloop()


    def plot_resultat(self, pas: int, recoltes: list, insectes: list) -> None:
        """
        Affiche un graphique des résultats de la récolte et des insectes.

        Args:
            pas (int): Le nombre de pas de temps.
            recoltes (list): La liste des valeurs de récolte pour chaque pas de temps.
            insectes (list): La liste des valeurs d'insectes pour chaque pas de temps.

        Returns:
            None
        """
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


    def update(self):
        """
        Met à jour l'interface utilisateur avec l'état actuel du potager.

        Cette méthode parcourt la matrice du potager et crée des boutons pour chaque parcelle.
        Le texte du bouton affiche des informations sur la parcelle, telles que ses coordonnées, le nombre de récoltes,
        la présence d'insecticide et le nombre d'insectes.
        Si la parcelle contient des plantes, un bouton vert est créé à la place.
        """
        for i in range(len(self._potager.get_matrice())):
            for j in range(len(self._potager.get_matrice()[i])):
                if self._potager.get_matrice()[i][j] != 0:
                    parcelle = self._potager.get_matrice()[i][j]
                    texte = f"{parcelle.get_coordonees()}\n{parcelle.get_recoltes()[-1][0]} récoltes \n insecticide: {parcelle.has_insecticide()}\n{len(parcelle.get_insects())} insectes"
                    TK.Button(self.fenetre, bg="gray85", text= texte, padx=100, pady=100).grid(row=i+2, column=j+3)
                    if len(self._potager.get_matrice()[i][j].get_plantes()) != 0:
                        TK.Button(self.fenetre, bg="green", text=texte, padx=100, pady=100).grid(row=i+2, column=j+3)