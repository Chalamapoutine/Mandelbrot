from tkinter import *
from tkinter.colorchooser import *
from tkinter import filedialog
from PIL import Image, ImageDraw


class ColorSelector:
    """ Class used to choose colors for a MandelPic instance.
    Classe utilisée pour choisir les couleur d'une instance Mandelpic.

    """

    def __init__(self, pic, colors, dummy=False):
        """

        :param pic:
        :param dummy: If True, the windows is closed immediately.
                      Used to generate an instance without any actual user choice.
                      Si True, la fenetre est fermée sur le champ.
                      Cela sert a generer une instance sans choix par l'utilisateur.
        """
        self.win = Tk()  # Creates a tkinter window / cree une fenetre tkinter

        # Save arguments in class attributs / Sauvegarde les arguments dans des attributs de classe
        self.pic = pic
        self.colors = colors

        # If colors is just a filename, open the file itself and put it in the attribute.
        # Si colors est un nom de fichier, ouvre le fichier et le met dans l'attribut de classe.
        if type(self.colors) == str:

            self.colors = Image.open(self.colors)

        # Frames / Cadres
        self.canvas_frame = Frame(master=self.win)
        self.spin_frame = Frame(master=self.win)
        self.button_frame = Frame(master=self.win)

        # Buttons / Boutons
        self.save_button = Button(master=self.button_frame, text='Sauvegarder', command=self.save)
        self.load_button = Button(master=self.button_frame, text='Ouvrir', command=self.open)
        self.end_button = Button(master=self.button_frame, text='Terminer', command=self.end)

        self.spin_text = Label(master=self.spin_frame, text='Nombre de couleurs :')
        self.nb_pixel_spin = Spinbox(self.spin_frame, command=self.canvas_gen, from_=1, to=50)

        # Put the default value in the spinbox / Met la valeur par default dans la spinbox
        self.nb_pixel_spin.delete(0, 'end')
        self.nb_pixel_spin.insert(0, 1)

        # The canvas_list is a list filled with all the canvases. Each canvas represents a color.
        self.canvas_list = []
        self.canvas_gen()
        self.show()

        # Because the first canvases should be accorded to the image's colors
        # Parce que les premiers canvas doivent etre accordés aux couleurs de l'image.
        self.img_to_canvas()

        # If it's a dummy instance, it's closed now / Si c'est une instance dummy, on la ferme maintenant.
        if dummy:
            self.end()

    def canvas_gen(self, *trash):
        """ Generate multiple canvases / Genere plusieurs canvas

        Make the number of canvases the same as the spinbox value, do both deleting and adding
        Rend le nombre de canvas egal a la valeur de la spinbox, en ajoutant et supprimant des canvas

         :param trash: Just to catch the event parameter that is useless here, but still mandatory.
                      Juste pour attraper le parametre d'evenemnt qui est ici inutile, mais neanmoins obligatoire.
        :return: None
        """

        while len(self.canvas_list) < int(self.nb_pixel_spin.get()):
            self.add()

        while len(self.canvas_list) > int(self.nb_pixel_spin.get()):
            self.remove()

    def add(self):

        """ Add a canvas (color block) / Ajoute un canvas (bloc de couleur)

        :return: None
        """

        cache = Canvas(master=self.canvas_frame, width=32, height=32)
        cache.color = (255, 255, 255)

        self.canvas_list.append(cache)

        # Make the added canvas clickable / Rend le canvas ajouté cliquable
        self.canvas_list[len(self.canvas_list) - 1].bind('<Button-1>', self.selector)

        # Show the added canvas / Affiche le canvas ajouté
        self.canvas_list[len(self.canvas_list) - 1].grid(row=0, column=len(self.canvas_list))

        self.colorizer(self.canvas_list[len(self.canvas_list) - 1])

    def remove(self):

        """ Remove a canvas (the last one) / Supprime un canvas (le dernier de la liste)

        :return: None
        """

        # Deadly nasty stuff
        self.canvas_list[len(self.canvas_list) - 1].grid_forget()
        self.canvas_list[len(self.canvas_list) - 1].destroy()
        del self.canvas_list[len(self.canvas_list) - 1]

    def show(self):

        """ Show all the UI (user interface), except for the canvas, using the grid geometry manager
        Affiche toute l'interface, a l'exception des canvas, avec le gestionnaire de geometrie grid

        :return: None
        """
        self.spin_frame.grid(row=0, column=0)
        self.canvas_frame.grid(row=0, column=1)
        self.button_frame.grid(row=0, column=2)

        self.spin_text.grid(row=0, column=0)
        self.nb_pixel_spin.grid(row=1, column=0)

        self.save_button.grid(row=0, column=0)
        self.load_button.grid(row=1, column=0)
        self.end_button.grid(row=2, column=0)

    def save(self):

        """ Save the current canvas colors to a PNG file on the hard drive
        Sauvegarde les couleurs du canvas dans un fichier PNG sur le disque dur

        :return: None
        """

        # Opens a tkinter-premade save windows / Ouvre une fenetre de sauvegarde fournie dans tkinter
        name = filedialog.asksaveasfilename(defaultextension='.png')

        self.colors_gen()
        self.colors.save(name)

    def open(self):

        """ Open a PNG file and set the canvases accordingly / Ouvre un fichier PNG et met les canvas conformement

        :return: None
        """

        name = filedialog.askopenfilename(defaultextension='.png')
        self.colors = Image.open(name)
        self.img_to_canvas()

    def img_to_canvas(self):

        """ Given an image, set the number of canvas and their colors properly
        Avec une image, regle le nombre et la couleur des canvas correctement
        :return: None
        """
        self.nb_pixel_spin.delete(0, 'end')
        self.nb_pixel_spin.insert(0, self.colors.width)

        self.canvas_gen()

        for pix in range(self.colors.width):
            self.canvas_list[pix].color = self.colors.getpixel((pix, 0))
            self.colorizer(self.canvas_list[pix])
            
    def colors_gen(self):

        """ Given a canvas setup, generate a PIL Image object / Genere une image PIL avec l'ensemble des canvas

        The resulting image can be used by Mainbrot.master_control_program, or saved as a PNG.
        L'image resultante peut etre utilisée par Mainbrot.master_control_program, ou sauvegardée au format .

        :return: None
        """
        width = int(self.nb_pixel_spin.get())
        self.colors = Image.new("RGB", (width, 1))
        draw = ImageDraw.Draw(self.colors)

        for pix in range(0, width):
            color_tuple = (int(self.canvas_list[pix].color[0]), int(self.canvas_list[pix].color[1]),
                           int(self.canvas_list[pix].color[2]))

            draw.point((pix, 0), fill=color_tuple)

    def colorizer(self, canvas):

        """ Take a canvas as input, and fill it with a rectangle of the self-stored color
        Prend un canvas en entrée, et le colore de la couleur stockée par le canvas

        :param canvas: The canvas to color / Le canvas a colorer
        :return: None
        """

        canvas.delete("all")
        canvas.rec = canvas.create_rectangle(0, 0, 32, 32, fill=tuple_to_tk_string(canvas.color))
        self.win.focus_force()

    def end(self):

        """ Used to close the windows / Utilisé pour fermer la fenetre

        When the user has chosen the colors he wants, this close the window, but the ColorSelector instance is not
        destroyed, so the generated data is still accessible as class attribute.
        Quand l'utilisateur a fini de choisir ses couleurs, cela ferme la fenetre, mais l'instance de ColorSelector
        n'est pas detruite, pour que les données generée soient toujours accessibles comme attributs de classe.

        :return: None
        """
        self.colors_gen()
        self.win.destroy()

    def selector(self, event):

        """Allows the user to chose the color of a clicked canvas
        Permet a l'utilisateur de choisir la couleur d'un canvas sur lequel il clique.

        :param event: The click. Useful because it enable this function to know which canvas was clicked.
                      Le clic. Utile car cette fonctionh a besoin de savoir quel canvas a ete cliqué
        :return: None
        """

        event.widget.color = askcolor()[0]

        self.colorizer(event.widget)


def tuple_to_tk_string(c_tuple):

    """Convert a (DDD, DDD, DDD) color tuple to a #HHHHHH hexadecimal based color string usable by tkinter.
    Converti un tuple de couleur de la forme (DDD,DDD,DDD) en une chaine de la forme #HHHHHH, compatible avec tkinter


    :param c_tuple: RGB color tuple (DDD, DDD, DDD) (3 decimal numbers, up to 3 digits)
                    Tuple de couleur RGB (DDD, DDD, DDD) (3 nombres decimaux jusqu'a 3 chiffres par nombres)
    :return: HTML-like color string (3 pairs of characters representing hexadecimal number, and a '#' before them)
    """

    tk_string = '#' + str(dec_to_tkhex(c_tuple[0])) + str(dec_to_tkhex(c_tuple[1])) + str(dec_to_tkhex(c_tuple[2]))
    return tk_string


def dec_to_tkhex(dec):

    """ Convert a decimal number into hexadecimal.
    Works accurately only for integers between 0 and 256

    I am aware of the pre existing hexadecimal class, but I need a very specific string format.

    :param dec: The decimal number to convert.
    :return: A 2 characters string, representing an hexadecimal number.
    """

    dec = int(dec)
    tkhex = ''

    if dec == 0:
        return '00'

    while dec != 0:

        if dec % 16 == 10:
            cache = 'a'

        if dec % 16 == 11:
            cache = 'b'

        if dec % 16 == 12:
            cache = 'c'

        if dec % 16 == 13:
            cache = 'd'

        if dec % 16 == 14:
            cache = 'e'

        if dec % 16 == 15:
            cache = 'f'

        if dec % 16 < 10:
            cache = str(dec % 16)

        tkhex = cache + tkhex

        dec //= 16
    if len(tkhex) == 1:
        tkhex += '0'
    return tkhex


if __name__ == '__main__':
    kek = ColorSelector()
    mainloop()
