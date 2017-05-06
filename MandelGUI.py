from tkinter import *
from tkinter import messagebox
from Mainbrot import Mainbrot
from PIL import ImageTk

from tkinter.ttk import *
from DegradeGUI import ColorSelector
import SaveGUI as sg
from wckToolTips import register


class HUDbrot:
    """ GUI class for mandelpic.

    Filled with a lot of spinboxes and buttons, with a few sweet, sweet methods

    """

    def __init__(self, master, pic):

        # Possible values tuples for the different spinboxes
        it_values = tuple(range(0, 1000000, 500))
        exp_values = tuple(range(-100, 100))
        res_values = tuple(range(10, 2000, 10))
        exp_colo_values = tuple(range(0, 500))
        coeff_zoom_values = tuple(range(2, 100))

        # Frames
        relief = 'flat'
        self.general_frame = Frame(master=master, borderwidth=5, relief=relief)
        self.spin_frame = Frame(master=self.general_frame, borderwidth=5, relief=relief)
        self.button_frame = Frame(master=master, borderwidth=5, relief=relief)
        self.res_frame = Frame(master=self.general_frame, borderwidth=5, relief=relief)
        self.sub_res_frame = Frame(master=self.res_frame, borderwidth=5, relief='groove')
        self.exp_colo_frame = Frame(master=self.general_frame, borderwidth=5, relief=relief)

        # To change max_it
        self.it_spin = Spinbox(self.spin_frame, values=it_values)
        self.it_text = Label(master=self.spin_frame, text='Nombre d\'itérations :')

        # The color power settings
        self.exp_colo_text = Label(master=self.exp_colo_frame, text='Exposant de l\'égalisation :')
        self.exp_colo_spin = Spinbox(master=self.exp_colo_frame, values=exp_colo_values)
        self.coeff_zoom_text = Label(master=self.exp_colo_frame, text='Puissance du zoom :')
        self.coeff_zoom_spin = Spinbox(master=self.exp_colo_frame, values=coeff_zoom_values)

        # All the widgets used for resolution settings
        self.res_text = Label(master=self.res_frame, text="Résolution :")
        self.x_spin = Spinbox(master=self.sub_res_frame, values=res_values)
        self.y_spin = Spinbox(master=self.sub_res_frame, values=res_values)
        self.x_text = Label(master=self.sub_res_frame, text="X :")
        self.y_text = Label(master=self.sub_res_frame, text="Y :")

        # Change p in z_{n+1} = z_n^p + c
        self.exp_spin = Spinbox(self.spin_frame, values=exp_values)
        self.exp_text = Label(master=self.spin_frame, text='Exposant :')

        # Those are latter called the "buttons"
        self.reset_button = Button(self.button_frame, text='Réinitialiser', command=pic.set_to_default)
        register(self.reset_button, "Ctrl+R")

        self.update_button = Button(self.button_frame, text='Mettre à jour', command=pic.load_from_hud)
        register(self.update_button, "F5")

        self.color_button = Button(self.button_frame, text='Couleurs', command=pic.change_colors)
        register(self.color_button, "Ctrl+C")

        self.undo_button = Button(self.button_frame, text='Annuler', command=pic.undo)
        register(self.undo_button, "Ctrl+Z")

        self.save_button = Button(self.button_frame, text='Sauvegarder', command=pic.save)
        register(self.save_button, "Ctrl+S")

        self.set_hud_values(pic)

        master.bind('<Control-s>', pic.save)
        master.bind('<F5>', pic.load_from_hud)
        master.bind('<Control-z>', pic.undo)
        master.bind('<Control-c>', pic.change_colors)
        master.bind('<Control-r>', pic.set_to_default)

        self.status = False
        self.show()

    def set_hud_values(self, pic):
        """ Get values from pic, and set the HUD accordingly

        :param pic: A MandelPic instance
        :return: None
        """

        self.it_spin.delete(0, 'end')
        self.it_spin.insert(0, pic.max_it)

        self.exp_spin.delete(0, 'end')
        self.exp_spin.insert(0, pic.exposant)

        self.coeff_zoom_spin.delete(0, 'end')
        self.coeff_zoom_spin.insert(0, pic.coeff_zoom)

        self.x_spin.delete(0, 'end')
        self.x_spin.insert(0, pic.resolution[0])
        self.y_spin.delete(0, 'end')
        self.y_spin.insert(0, pic.resolution[1])

        self.exp_colo_spin.delete(0, 'end')
        self.exp_colo_spin.insert(0, pic.exp_colo)

    def show(self):
        """ Show every item of the GUI

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
        self.coeff_zoom_text.grid(row=0, column=2)
        self.coeff_zoom_spin.grid(row=0, column=3)

        # Buttons widgets
        self.button_frame.grid(row=3, column=0)

        self.save_button.grid(row=0, column=0)
        self.color_button.grid(row=0, column=1)
        self.update_button.grid(row=0, column=2)
        self.undo_button.grid(row=0, column=3)
        self.reset_button.grid(row=0, column=4)

        self.status = True


class MandelPic:
    """ A picture of the mandelbrot set, with all information on it, plus useful methods

    """

    def __init__(self, entrees):
        self.resolution = entrees['resolution']
        self.centre = entrees['centre']
        self.taille_x = entrees['taille_x']
        self.max_it = entrees['max_it']
        self.n_core = entrees['n_core']
        self.exposant = entrees['exposant']
        self.colors = entrees['degr_colo']
        self.exp_colo = entrees['exp_colo']
        self.coeff_zoom = entrees['coeff_zoom']
        self.color_selector = ColorSelector(self, colors=self.colors, dummy=True)
        self.hud = HUDbrot(root, self)

        self.undo_list = [{'centre': self.centre, 'taille_x': self.taille_x}]
        self.show()

    def set_to_default(self):
        """ Set the values to default, and update the image.

        :return: None
        """
        global dic_entrees
        global hud_brot
        self.resolution = dic_entrees['resolution']
        self.centre = dic_entrees['centre']
        self.taille_x = dic_entrees['taille_x']
        self.max_it = dic_entrees['max_it']
        self.colors = dic_entrees['degr_colo']
        self.n_core = dic_entrees['n_core']
        self.exposant = dic_entrees['exposant']
        self.exp_colo = dic_entrees['exp_colo']

        hud_brot.set_hud_values(self)

        self.show()

    def bindings(self):
        self.im_widget.bind('<Button-1>', self.clicked)
        self.im_widget.bind('<Button-2>', self.clicked)
        self.im_widget.bind('<Button-3>', self.clicked)

    def obliterate(self):
        """ Completly remove the image"""

        self.im_widget.grid_forget()
        self.im_widget.destroy()

    def load_from_hud(self, *event):
        """ Get user set values from the HUD, and update the image.

        :param event: Trash parameter for event bindings
        :return: None
        """

        self.max_it = int(self.hud.it_spin.get())
        self.exposant = float(self.hud.exp_spin.get())
        self.resolution = (int(self.hud.x_spin.get()), int(self.hud.y_spin.get()))
        self.exp_colo = float(self.hud.exp_colo_spin.get())
        self.colors = self.color_selector.colors
        self.show()

    def show(self):
        """ Compute and print an image using the self stored values.

        :return: None
        """

        try:

            # To trigger the exception before the widget is deleted
            cache = Mainbrot(self.resolution, self.centre, self.taille_x, self.max_it, self.colors,
                             n_core=self.n_core, exposant=self.exposant, exp_colo=self.exp_colo).image
            try:
                self.im_widget.grid_forget()
                del self.im_widget
            except AttributeError:
                pass

            self.im_raw = cache
            self.im_cooked = ImageTk.PhotoImage(self.im_raw)
            self.im_widget = Label(image=self.im_cooked)

            self.place()
            self.bindings()
        except IndexError:
            error_str = 'Cette zone est totallement noire. Essayez une autre zone, ou augmentez le nombre d\'itérations'
            print(error_str)
            messagebox.showerror('Erreur', error_str)
            self.set_to_prec()

    def set_to_prec(self):
        self.centre = self.undo_list[1]['centre']
        self.taille_x = self.undo_list[1]['taille_x']

    def undo(self, *trash):
        self.set_to_prec()
        self.show()

    def place(self):
        """ Place the image on the grid """
        self.im_widget.grid(row=0, column=0)

    def clicked(self, event):
        """ When the image is clicked, change it appropriately.

        :param event: mouse clicked
        :return:
        """

        taille_y = self.taille_x * (self.resolution[1] / self.resolution[0])
        pas = self.taille_x / self.resolution[0]

        coin = complex(self.centre.real - self.taille_x / 2, self.centre.imag + taille_y / 2)

        self.centre = complex(coin.real + pas * event.x, coin.imag - pas * event.y)

        if event.num == 1:
            self.taille_x /= self.coeff_zoom

        if event.num == 3:
            self.taille_x *= self.coeff_zoom

        self.load_from_hud(None)
        self.undo_list.insert(0, {'centre': self.centre, 'taille_x': self.taille_x})
        print('\n>>>>//// clicked at {} + {}j'.format(coin.real + pas * event.x, coin.imag - pas * event.y))

    def change_colors(self):
        """ Create a temporary ColorSelector instance. See the ColorSelector docstring for more detail.

        :return: None
        """

        self.color_selector = ColorSelector(self, self.colors)

    def save(self, *trash):
        """ Create a temporary SaveHUD instance. See the SaveHUD docstring for more detail.

        :return: None
        """
        sg.SaveWin(self, HUDbrot)


if __name__ == '__main__':
    dic_entrees = {'resolution': (500, 500), 'centre': 0, 'taille_x': 4,'max_it': 1500, 'degr_colo': 'quatre.png',
                   'exposant': 2, 'n_core': 4, 'exp_colo': 4, 'coeff_zoom': 4}
    root = Tk()
    mandel_pic = MandelPic(dic_entrees)

    mainloop()
