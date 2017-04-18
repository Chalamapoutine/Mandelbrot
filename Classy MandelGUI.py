from tkinter import *
from tkinter import messagebox
from Mainbrot import Mainbrot
from PIL import ImageTk
from SaveGUI import SaveHUD
from tkinter.ttk import *
from DegradeGUI import ColorSelector
from wckToolTips import register


class HUDbrot:
    """ GUI class for mandelpic.

    Filled with a lot of spinboxes and button, with a few sweet, sweet methods

    """

    def __init__(self, master, pic):

        # Possible values tuples for the different spinboxes
        it_values = tuple(range(0, 1000000, 500))
        exp_values = tuple(range(-100, 100))
        res_values = tuple(range(10, 2000, 10))

        # Frames
        self.general_frame = Frame(master=master, borderwidth=5, relief='groove')
        self.spin_frame = Frame(master=self.general_frame, borderwidth=5, relief='groove')
        self.button_frame = Frame(master=master, borderwidth=5, relief='groove')
        self.res_frame = Frame(master=self.general_frame, borderwidth=5, relief='groove')
        self.sub_res_frame = Frame(master=self.res_frame, borderwidth=5, relief='groove')

        # To change max_it
        self.it_spin = Spinbox(self.spin_frame, values=it_values)
        self.it_text = Label(master=self.spin_frame, text='Nombre d\'itérations :')

        # All the widgets used for resolution settings
        self.res_text = Label(master=self.res_frame, text="Résolution :")
        self.x_spin = Spinbox(master=self.sub_res_frame, values=res_values)
        self.y_spin = Spinbox(master=self.sub_res_frame, values=res_values)
        self.x_text = Label(master=self.sub_res_frame, text="X :")
        self.y_text = Label(master=self.sub_res_frame, text="Y :")

        # Change p in z_{n+1} = z_n^p + c
        self.exp_spin = Spinbox(self.spin_frame, values=exp_values)
        self.exp_text = Label(master=self.spin_frame, text='Exposant :')

        self.reset_button = Button(self.button_frame, text='Réinitialiser', command=pic.set_to_default)
        self.update_button = Button(self.button_frame, text='Mettre à jour', command=pic.load_from_hud)
        register(self.update_button, "F5")
        self.color_button = Button(self.button_frame, text='Couleurs', command=pic.change_colors)

        self.save_button = Button(self.button_frame, text='Sauvegarder', command=pic.save)

        self.set_hud_values(pic)

        master.bind('h', self.show())
        master.bind('<F5>', pic.load_from_hud)
        self.status = False

    def set_hud_values(self, pic):
        """ Get values from pic, and set the HUD accordingly

        :param pic: A MandelPic instance
        :return: None
        """

        self.it_spin.delete(0, 'end')
        self.it_spin.insert(0, pic.max_it)

        self.exp_spin.delete(0, 'end')
        self.exp_spin.insert(0, pic.exposant)

        self.x_spin.delete(0, 'end')
        self.x_spin.insert(0, pic.resolution[0])
        self.y_spin.delete(0, 'end')
        self.y_spin.insert(0, pic.resolution[1])

    def show(self):
        """ Show every item of the GUI

        :return: None
        """

        # Big frame, for everything except the buttons
        self.general_frame.grid(row=1, column=0, sticky='WE')

        # Max_it and exp widgets
        self.spin_frame.grid(row=0, column=0, sticky='WE')

        self.it_text.grid(row=0, column=0, sticky='E')
        self.it_spin.grid(row=0, column=1)

        self.exp_text.grid(row=0, column=2, sticky='W')
        self.exp_spin.grid(row=0, column=3)

        # Resolutions widgets
        self.res_frame.grid(row=2, column=0, sticky='WE')

        self.res_text.grid(row=0, column=0, sticky='W')
        self.sub_res_frame.grid(row=0, column=1, sticky='WE')

        self.x_text.grid(row=0, column=0, sticky='E')
        self.x_spin.grid(row=0, column=1)
        self.y_text.grid(row=0, column=2, sticky='E')
        self.y_spin.grid(row=0, column=3)

        # Buttons widgets
        self.button_frame.grid(row=3, column=0)

        self.reset_button.grid(row=0, column=0)
        self.color_button.grid(row=0, column=1)
        self.update_button.grid(row=0, column=2)
        self.save_button.grid(row=0, column=3)

        self.status = True

    def hide(self):
        """ Hide every item of the GUI (not complete)

        :return: None
        """
        self.it_spin.grid_forget()
        self.it_text.grid_forget()

        self.exp_spin.grid_forget()
        self.exp_text.grid_forget()

        self.update_button.grid_forget()
        self.status = False

    def hide_and_seek(self, event):
        """ Hide the HUD when it's shown, and show it when it is hidden.

        :param event: Useless parameter, but event bindings always pass it, so it has to be expected
        :return: None
        """

        if self.status:
            self.hide()

        else:
            self.show()


class MandelPic:
    """ A picture of the mandelbrot set, with all informations on it, plus usefull methods

    """

    def __init__(self, entrees):
        self.resolution = entrees['resolution']
        self.centre = entrees['centre']
        self.taille_x = entrees['taille_x']
        self.max_it = entrees['max_it']
        self.n_core = entrees['n_core']
        self.exposant = entrees['exposant']
        self.colors = entrees['degr_colo']

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
        self.degrade = dic_entrees['degr_colo']
        self.n_core = dic_entrees['n_core']
        self.exposant = dic_entrees['exposant']

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

        global hud_brot

        self.max_it = int(hud_brot.it_spin.get())
        self.exposant = int(hud_brot.exp_spin.get())

        self.show()

    def show(self):
        """ Print the image using the self stored values.

        :return: None
        """

        try:
            self.im_raw = Mainbrot(self.resolution, self.centre, self.taille_x, self.max_it, self.colors,
                                   n_core=self.n_core, exposant=self.exposant).image
            self.im_cooked = ImageTk.PhotoImage(self.im_raw)
            self.im_widget = Label(image=self.im_cooked)

            self.place()
            self.bindings()
        except ZeroDivisionError:
            error_str = 'Cette zone est totallement noire. Essayez une autre zone, ou augmentez le nombre d\'itérations'
            print(error_str)
            messagebox.showerror('Erreur', error_str)

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
            self.taille_x /= 4

        if event.num == 3:
            self.taille_x *= 4

        self.load_from_hud(None)

        print('\n>>>>//// clicked at {} + {}j'.format(coin.real + pas * event.x, coin.imag - pas * event.y))

    def change_colors(self):
        """ Create a temporary ColorSelector instance. See the ColorSelector docstring for more detail.

        :return: None
        """

        ColorSelector(self)

    def save(self):
        """ Create a temporary SaveHUD instance. See the SaveHUD docstring for more detail.

        :return: None
        """
        SaveHUD(self)


if __name__ == '__main__':
    dic_entrees = {'resolution': (500, 500), 'centre': 0, 'taille_x': 4,
                   'max_it': 1500, 'degr_colo': 'quatre.png', 'exposant': 2, 'n_core': 4}
    root = Tk()
    mandel_pic = MandelPic(dic_entrees)
    hud_brot = HUDbrot(root, mandel_pic)
    mainloop()
