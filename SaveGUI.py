from tkinter import *
from Mainbrot import Mainbrot
from tkinter.ttk import *
from tkinter import filedialog
from MandelGUI import HUDbrot
from DegradeGUI import ColorSelector


class SaveHUD(HUDbrot):
    """ Save interface class / Classe d'interface de sauvegarde

    Children class of MandelGUI.HUDbrot
    Classe enfant de MandelGUI.HUDbrot

    """

    def __init__(self, master, pic, save_win):
        """ Replace HUDbrot.__init__ / Remplace HUDbrot.__init__

        Do the normal MandelGUI.HUDbrot initialisation, and then replace the color button command by another one.
        Fait l'initialisation normale de MandelGUI.HUDbrot, et remplace le bouton de couleur par un autre.

        :param master:
        :param pic:
        """

        # Initialize the class like MandelGUI.HUDbrot / Initialize la classe comme MandelGUI.HUDbrot
        HUDbrot.__init__(self, master, pic)

        # Replace the color_button, by a new with a new command
        # Remplace le boutom couleur par un nouveau avec une autre commande
        self.color_button = Button(self.button_frame, text='Couleurs', command=save_win.change_colors)

        # Force usage of the replacement show method / Force l'usage de la nouvelle methode show
        self.show()

    def show(self):
        """ Replacement of MandelGUI.HUDbrot.show / Remplace MandelGUI.HUDbrot.show

        Show some item of the original HUD
        Do not show every one of them, for instance the reset button is not needed anymore, so it's not there

        Affiche certains elements de l'HUD originel.
        Ne les affiches pas tous, par exemple, le bouton reinitialisé est inutile ici, il n'y est donc pas
        :return: None
        """

        # Big frame, for everything except the buttons / Gros cadre, pour tout sauf les boutons
        self.general_frame.grid(row=1, column=0)

        # Max_it and exp widgets / Widgets pour max_it et exp
        self.spin_frame.grid(row=0, column=0)

        self.it_text.grid(row=0, column=0)
        self.it_spin.grid(row=0, column=1)

        self.exp_text.grid(row=0, column=2)
        self.exp_spin.grid(row=0, column=3)

        # Resolutions widgets / Widgets de resolution
        self.res_frame.grid(row=2, column=0)
        self.res_text.grid(row=0, column=0)
        self.sub_res_frame.grid(row=0, column=1)

        self.x_text.grid(row=0, column=0)
        self.x_spin.grid(row=0, column=1)
        self.y_text.grid(row=1, column=0)
        self.y_spin.grid(row=1, column=1)

        # Exp_colo widgets / Widgets de exp_colo
        self.exp_colo_frame.grid(row=3, column=0)
        self.exp_colo_text.grid(row=0, column=0)
        self.exp_colo_spin.grid(row=0, column=1)

        # Buttons widgets / Widget des boutons
        self.button_frame.grid(row=3, column=0)
        self.color_button.grid(row=0, column=1)


class SaveWin:
    """ Windows to save an image
    """

    def __init__(self, pic, hud):

        self.win = Tk()

        self.pic = pic
        self.hud_frame = Frame(master=self.win)
        self.button_frame = Frame(master=self.win)

        self.hud = SaveHUD(self.hud_frame, pic, self)

        self.full_save_button = Button(master=self.button_frame, command=self.full_save, text="Sauvegarde complete")
        self.quick_save_button = Button(master=self.button_frame, command=self.quick_save, text="Sauvegarde rapide")

        self.colors = pic.colors
        self.color_selector = ColorSelector(pic, colors=self.colors, dummy=True)
        self.show()

    def change_colors(self):
        """ Create a temporary ColorSelector instance. See the ColorSelector docstring for more detail.

        :return: None
        """

        self.color_selector = ColorSelector(self, self.color_selector.colors)

    def full_save(self):
        name = filedialog.asksaveasfilename(defaultextension='.png')
        res = (int(self.hud.x_spin.get()), int(self.hud.y_spin.get()))
        max_it = int(self.hud.it_spin.get())
        exp_colo = float(self.hud.exp_colo_spin.get())
        colors = self.color_selector.colors

        Mainbrot(res, self.pic.centre, self.pic.taille_x, max_it, colors,
                 n_core=4, exp_colo=exp_colo).image.save(name)

    def quick_save(self):
        name = filedialog.asksaveasfilename(defaultextension='.png')
        self.pic.im_raw.save(name)

    def show(self):
        self.hud_frame.grid(row=0, column=0)

        self.button_frame.grid(row=1, column=0)
        self.full_save_button.grid(row=0, column=1)
        self.quick_save_button.grid(row=0, column=0)
