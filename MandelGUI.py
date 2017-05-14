from tkinter import *
from tkinter import messagebox
from Mainbrot import Mainbrot
from PIL import ImageTk

from tkinter.ttk import *
from DegradeGUI import ColorSelector
import SaveGUI as sg
from wckToolTips import register


class HUDbrot:
    """ GUI class for MandelPic.
    Classe d'interface faite pour fonctionner avec MandelPic

    Filled with a lot of useful spinboxes and buttons, with a few methods to make them visible, and make good use
    of them.
    Remplie de boutons et spinbox utiles, avec quelques methodes pour les rendre visibles, et les rendre utiles.
    """

    def __init__(self, master, pic):
        """ Creates all the buttons, frames and spinboxes, and save them in class attributes.
        Creer tout les boutons, cadres et spinbox, et les sauvegarde dasn des attributs de classe.

        :param master: The widget that will contain all the widgets created here.
                       Le widget qui contiendra tout les widgets crees ici.

        :param pic: The MandelPic instance to which this HUDbrot instance is linked.
                    L'instance de MandelPic qui est reliée a cette instance de HUDbrot.
        """

        # Possible values tuples for the different spinboxes / Valeurs possibles pour les differentes spinbox
        it_values = tuple(range(0, 1000000, 500))
        exp_values = tuple(range(-100, 100))
        res_values = tuple(range(10, 2000, 10))
        exp_colo_values = tuple(range(0, 500))
        coeff_zoom_values = tuple(range(2, 100))

        # Frames / Cadres
        relief = 'flat'
        self.general_frame = Frame(master=master, borderwidth=5, relief=relief)
        self.spin_frame = Frame(master=self.general_frame, borderwidth=5, relief=relief)
        self.button_frame = Frame(master=master, borderwidth=5, relief=relief)
        self.res_frame = Frame(master=self.general_frame, borderwidth=5, relief=relief)
        self.sub_res_frame = Frame(master=self.res_frame, borderwidth=5, relief='groove')
        self.exp_colo_frame = Frame(master=self.general_frame, borderwidth=5, relief=relief)

        # To change max_it / Pour changer max_it
        self.it_spin = Spinbox(self.spin_frame, values=it_values)
        self.it_text = Label(master=self.spin_frame, text='Nombre d\'itérations :')

        # The color power settings / Les reglages de l'exposant de coloration
        self.exp_colo_text = Label(master=self.exp_colo_frame, text='Exposant de l\'égalisation :')
        self.exp_colo_spin = Spinbox(master=self.exp_colo_frame, values=exp_colo_values)
        self.coeff_zoom_text = Label(master=self.exp_colo_frame, text='Puissance du zoom :')
        self.coeff_zoom_spin = Spinbox(master=self.exp_colo_frame, values=coeff_zoom_values)

        # The resolution settings / Les reglages de resolution
        self.res_text = Label(master=self.res_frame, text="Résolution :")
        self.x_spin = Spinbox(master=self.sub_res_frame, values=res_values)
        self.y_spin = Spinbox(master=self.sub_res_frame, values=res_values)
        self.x_text = Label(master=self.sub_res_frame, text="X :")
        self.y_text = Label(master=self.sub_res_frame, text="Y :")

        # Change p in z_{n+1} = z_n^p + c
        self.exp_spin = Spinbox(self.spin_frame, values=exp_values)
        self.exp_text = Label(master=self.spin_frame, text='Exposant :')

        # Those are latter called the "buttons" / Ces widgets sont appelés plus tard les "boutons"
        self.reset_button = Button(self.button_frame, text='Réinitialiser', command=pic.__init__)

        self.update_button = Button(self.button_frame, text='Mettre à jour', command=pic.load_from_hud)
        register(self.update_button, "F5")  # Links a tooltip / Attache un tooltip

        self.color_button = Button(self.button_frame, text='Couleurs', command=pic.change_colors)
        register(self.color_button, "Ctrl+C")  # Links a tooltip / Attache un tooltip

        self.undo_button = Button(self.button_frame, text='Annuler', command=pic.undo)
        register(self.undo_button, "Ctrl+Z")  # Links a tooltip / Attache un tooltip

        self.save_button = Button(self.button_frame, text='Sauvegarder', command=pic.save)
        register(self.save_button, "Ctrl+S")  # Links a tooltip / Attache un tooltip

        self.set_hud_values(pic)

        # Binds the button related methods to keyboard shortcuts
        # Attache les methodes des boutons a des raccourcis clavier
        master.bind('<Control-s>', pic.save)
        master.bind('<F5>', pic.load_from_hud)
        master.bind('<Control-z>', pic.undo)
        master.bind('<Control-c>', pic.change_colors)

        self.status = False
        self.show()

    def set_hud_values(self, pic):
        """ Get values from pic, and set the HUD's spinboxes accordingly
        Recupere les valeurs de pic, et regle les spinbox de l'HUD avec.

        :param pic: A MandelPic instance / Une instance de MandelPic
        :return: None
        """

        #  This structure replace the spinbox value. Only the last argument is to be change to change the value
        # Cette structure remplace la valeur de la spinbox. Seule la derniere valeur compte.
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
        """ Show every widget of the HUD, using the grid geometry manager.
        Affiche tout les widgets de l'HUD, en utilisant le gestionnaire de geometrie grid.

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

        # Exp_colo widgets / Wdget pour exp_colo
        self.exp_colo_frame.grid(row=3, column=0)
        self.exp_colo_text.grid(row=0, column=0)
        self.exp_colo_spin.grid(row=0, column=1)
        self.coeff_zoom_text.grid(row=0, column=2)
        self.coeff_zoom_spin.grid(row=0, column=3)

        # Button widgets / Widgets de boutons
        self.button_frame.grid(row=3, column=0)

        self.save_button.grid(row=0, column=0)
        self.color_button.grid(row=0, column=1)
        self.update_button.grid(row=0, column=2)
        self.undo_button.grid(row=0, column=3)
        self.reset_button.grid(row=0, column=4)

        self.status = True


class MandelPic:

    """ A picture of the mandelbrot set, with all information on it, plus useful transformation methods
    Une image de l'ensemble de mandelbrot, avec toute les informations a son propos, et des methodes de transformation
    """

    def __init__(self, *entrees):
        """ Set all the default settings, and then launch the image computation
        Met tout les reglages par defaut, puis lance les caculs de l'image

        :param entrees: The dictionnary that contains default settings / Le dictionnaire avec les reglages par defaut
        """

        try:
            self.entrees = entrees[0]
        except IndexError:
            pass

        self.resolution = self.entrees['resolution']
        self.centre = self.entrees['centre']
        self.taille_x = self.entrees['taille_x']
        self.max_it = self.entrees['max_it']
        self.n_core = self.entrees['n_core']
        self.exposant = self.entrees['exposant']
        self.colors = self.entrees['degr_colo']
        self.exp_colo = self.entrees['exp_colo']
        self.coeff_zoom = self.entrees['coeff_zoom']
        self.color_selector = ColorSelector(self, colors=self.colors, dummy=True)
        self.hud = HUDbrot(root, self)
        self.hud.set_hud_values(self)

        # This list allows the user to undo what he did, as it save the differents locations visited by the user
        # See the MandelPic.set_to_prec and MandelPic.undo methods to have more details
        self.undo_list = [{'centre': self.centre, 'taille_x': self.taille_x}]

        self.show()  # Show an image / Affiche une image

    def bindings(self):

        """ Binds the image to different clicks. Allows it to react to mouse clicks
        """

        self.im_widget.bind('<Button-1>', self.clicked)
        self.im_widget.bind('<Button-2>', self.clicked)
        self.im_widget.bind('<Button-3>', self.clicked)

    def obliterate(self):
        """ Completely remove the image
        Enleve completement l'image
        """

        self.im_widget.grid_forget()
        self.im_widget.destroy()

    def load_from_hud(self, *trash):
        """ Get user set values from the HUD, and update the image.
        Recupere les valeurs rentrées par l'utilisateur dans le HUD, et met l'image a jour.

        :param trash: Just to catch the event parameter that is useless here, but still mandatory.
                      Juste pour attraper le parametre d'evenemnt qui est ici inutile, mais neanmoins obligatoire.

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
        Used when the self stored values has been updated, and the user wants to apply the changes.

        :return: None
        """

        try:

            # To trigger the black image associated exception before the widget is deleted, this is done first
            # Pour declencher l'exception associee a une image noire avant que le widget d'image ne soit supprime

            cache = Mainbrot(self.resolution, self.centre, self.taille_x, self.max_it, self.colors,
                             n_core=self.n_core, exposant=self.exposant, exp_colo=self.exp_colo).image
            try:
                # Try to delete the widget / Essaye de supprimer le widget
                self.im_widget.grid_forget()
                del self.im_widget
            except AttributeError:
                # If there is no widget to delete (if it's the first the image to be shown for instance), do nothing.
                # S'il n'y a pas de widget a supprimer (si c'est la premiere image par exemple), ne fait rien.
                pass

            # If no exception was raised by creating the image, it is stored in class attributes and place
            # Si aucune exception n'est remontee par la creation de l'image, tout est stocke dans des attribut de classe

            self.im_raw = cache
            self.im_cooked = ImageTk.PhotoImage(self.im_raw)
            self.im_widget = Label(image=self.im_cooked)

            # Once it is stored, it is shown by those method / Une fois stocké, c'est montré par ces methodes
            self.place()
            self.bindings()

        except IndexError:

            # The IndexError is raised when the user try to go in an all-black zone. When he does, an string is printed
            # in the console, an error windows pops up, and the change caused by the click (or else) is reversed
            # L'IndexError est remontee quand l'utilisateur essaye de se rendre dans une zone toute noire.
            # Un message est alors affiché dans la console, et une fenetre d'erreur apparait.

            error_str = 'Cette zone est totallement noire. Essayez une autre zone, ou augmentez le nombre d\'itérations'
            print(error_str)
            messagebox.showerror('Erreur', error_str)
            self.set_to_prec()

    def set_to_prec(self):
        """ Set the location related attributes to their last values, as stored in MandelPic.undo_list
        Met les attributs lié au lieu a leur derniere valeur

        :return: None
        """

        self.centre = self.undo_list[1]['centre']
        self.taille_x = self.undo_list[1]['taille_x']

    def undo(self, *trash):
        """ Calls MandelPic.set_to_prec, and then update the image
        Appelle MandelPic,set_to_prec, puis met l'image a jour.

        Linked to the "annuler" button
        Lié au bouton "annuler"

        :param trash: Just to catch the event parameter that is useless here, but still mandatory.
                      Juste pour attraper le parametre d'evenemnt qui est ici inutile, mais neanmoins obligatoire.
        :return:
        """
        self.set_to_prec()
        self.show()

    def place(self):
        """ Place the image on the grid """
        self.im_widget.grid(row=0, column=0)

    def clicked(self, event):
        """ When the image is clicked, change its location parameter appropriately.
        Quand on clique sur l'image, changes ses parametres correctement.

        :param event: The event object. Used to determine wich mouse button was used.
                      L'objet d'evenement. Sert a determiner avec quel bouton de la souris le clic a ete fait.
        :return: None
        """

        taille_y = self.taille_x * (self.resolution[1] / self.resolution[0])
        pas = self.taille_x / self.resolution[0]

        coin = complex(self.centre.real - self.taille_x / 2, self.centre.imag + taille_y / 2)

        self.centre = complex(coin.real + pas * event.x, coin.imag - pas * event.y)

        if event.num == 1:
            # If left click is used, it's a zoom forward, and taille_x is reduced (divided by coeff_zoom)
            # Si c'est un clic gauche, il s'agit d'un zoom en avant, et taille_x est reduit (divisé par coeff_zoom)
            self.taille_x /= self.coeff_zoom

        if event.num == 3:
            # If right click is used, it's a zoom backward, and taille_x is increased (multiplied by coeff_zoom)
            # Si c'est un clic droit, c'est un zoom en arriere, et taille_x est augmenté (multiplié par coeff_zoom)
            self.taille_x *= self.coeff_zoom

        # Print where in the complex plane the user clicked / Affiche ou dans le plan complexe l'utilisateur a cliqué
        print('\n>>>>//// clicked at {} + {}j, taille_x={}'
              .format(coin.real + pas * event.x, coin.imag - pas * event.y, self.taille_x))

        # Add the new location to the undo list / Ajoute le nouveau lieu a la undo_list
        self.undo_list.insert(0, {'centre': self.centre, 'taille_x': self.taille_x})

        # Used tu
        self.load_from_hud(None)

    def change_colors(self, *trash):
        """ Launch the color selecting interface / Lance l'interface de choix de couleurs

        Creates a  ColorSelector instance. See the ColorSelector docstring for more details.
        Creer une instance de ColorSelector. Voir la docstring de ColorSelector pour plus de details.

        :param trash: Just to catch the event parameter that is useless here, but still mandatory.
                      Juste pour attraper le parametre d'evenemnt qui est ici inutile, mais neanmoins obligatoire.
        :return: None
        """

        self.color_selector = ColorSelector(self, self.colors)

    def save(self, *trash):
        """ Launch the save interface / Lance l'interface de sauvegarde

        Creates a temporary SaveHUD instance. See the SaveHUD docstring for more detail.
        Creer une instance temporaire de SaveWin. Voir la docstring de ColorSelector pour plus de details.

        :param trash: Just to catch the event parameter that is useless here, but still mandatory.
                      Juste pour attraper le parametre d'evenemnt qui est ici inutile, mais neanmoins obligatoire.
        :return: None
        """
        sg.SaveWin(self, HUDbrot)


if __name__ == '__main__':

    # This if block is executed only if MandelGUI is launched by the user, and not by another module's
    # import statement.
    # Ce bloque if est executé seulement si MandelGUI est lancé par l'utilisateur et pas par l'importation de ce
    # module par un autre.

    # The default setting are stored in this dictionnary / Les reglages par default sont stockés dans ce dictionnaire.
    dic_entrees = {'resolution': (500, 500), 'centre': 0, 'taille_x': 4, 'max_it': 500, 'degr_colo': 'quatre.png',
                   'exposant': 2, 'n_core': 4, 'exp_colo': 4, 'coeff_zoom': 4}

    # Creates a windows / creer une fenetre
    root = Tk()

    # Launch the proper execution
    mandel_pic = MandelPic(dic_entrees)

    # Forbid the programm to just close once computation are done
    # Empeche le programme de juste se fermer une fois les calculs finis
    mainloop()
