from tkinter import *
from Mainbrot import Mainbrot
from tkinter.ttk import *
from tkinter import filedialog
from MandelGUI import HUDbrot
from DegradeGUI import ColorSelector


class SaveHUD(HUDbrot):
    """ Children class of HUDbrot

    """

    def __init__(self, master, pic, save_win):
        """ Do the normal HUDbrot initialisation, and then replace the color button command by another one.

        :param master:
        :param pic:
        """

        HUDbrot.__init__(self, master, pic)
        self.color_button = Button(self.button_frame, text='Couleurs', command=save_win.change_colors)
        self.show()

    def show(self):
        """ Show some item of the GUI
        Do not show every one of them, for instance the reset button is not needed anymore, so it's not there
        :return: None
        """

        # Big frame, for everything except the buttons
        self.general_frame.grid(row=1, column=0)

        # Max_it and exp widgets
        self.spin_frame.grid(row=0, column=0)

        self.it_text.grid(row=0, column=0)
        self.it_spin.grid(row=0, column=1)

        self.exp_text.grid(row=0, column=2)
        self.exp_spin.grid(row=0, column=3)

        # Resolutions widgets
        self.res_frame.grid(row=2, column=0)

        self.res_text.grid(row=0, column=0)
        self.sub_res_frame.grid(row=0, column=1)

        self.x_text.grid(row=0, column=0)
        self.x_spin.grid(row=0, column=1)
        self.y_text.grid(row=1, column=0)
        self.y_spin.grid(row=1, column=1)

        # Exp_colo widgets
        self.exp_colo_frame.grid(row=3, column=0)
        self.exp_colo_text.grid(row=0, column=0)
        self.exp_colo_spin.grid(row=0, column=1)

        # Buttons widgets
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
