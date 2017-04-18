from tkinter import *
from tkinter.colorchooser import *
from tkinter import filedialog
from PIL import Image, ImageDraw


class ColorSelector:
    """ Class used to choose colors for a MandelPic instance.

    """

    def __init__(self, pic):
        self.win = Tk()  # Creates a tkinter window
        self.pic = pic
        self.colors = pic.colors

        if type(self.colors) == str:

            self.colors = Image.open(self.colors)

        # Frames allow horizontally aligned buttons, they apply to every object a column within that same frame
        self.canvas_frame = Frame(master=self.win)
        self.spin_frame = Frame(master=self.win)
        self.button_frame = Frame(master=self.win)

        # Command buttons
        self.save_button = Button(master=self.button_frame, text='Sauvegarder', command=self.save)
        self.load_button = Button(master=self.button_frame, text='Ouvrir', command=self.open)
        self.end_button = Button(master=self.button_frame, text='Terminer', command=self.end)

        self.spin_text = Label(master=self.spin_frame, text='Nombre de couleurs :')
        self.nb_pixel_spin = Spinbox(self.spin_frame, command=self.canvas_gen, from_=1, to=50)

        self.nb_pixel_spin.delete(0, 'end')
        self.nb_pixel_spin.insert(0, 1)

        self.canvas_list = []
        self.canvas_gen()
        self.show()
        self.img_to_canvas()

    def canvas_gen(self, *trash):
        """ Generate multiple canvases

        Make the number of canvases the same as the spinbox value, do both deleting and adding

        :param trash: Trash parameter for event bindings
        :return: None
        """

        while len(self.canvas_list) < int(self.nb_pixel_spin.get()):
            self.add()

        while len(self.canvas_list) > int(self.nb_pixel_spin.get()):
            self.remove()

    def add(self):

        """ Add a canvas (color block) to select colors

        :return: None
        """

        cache = Canvas(master=self.canvas_frame, width=32, height=32)

        self.canvas_list.append(cache)

        self.canvas_list[len(self.canvas_list) - 1].color = (0, 0, 0)

        self.canvas_list[len(self.canvas_list) - 1].bind('<Button-1>', self.selector)

        self.canvas_list[len(self.canvas_list) - 1].grid(row=0, column=len(self.canvas_list))
        self.colorizer(self.canvas_list[len(self.canvas_list) - 1])

    def remove(self):

        """ Remove a canvas to select colors

        :return: None
        """

        self.canvas_list[len(self.canvas_list) - 1].grid_forget()
        self.canvas_list[len(self.canvas_list) - 1].destroy()
        del self.canvas_list[len(self.canvas_list) - 1]

    def show(self):

        """ Show all the UI (user interface), except for the canvas

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

        """ Save the current canvas colors to a file on the hard drive

        :return: None
        """

        name = filedialog.asksaveasfilename(defaultextension='.png')
        self.colors_gen()

        self.colors.save(name)

    def open(self):

        """ Open a color file and set the UI accordingly

        :return:
        """

        name = filedialog.askopenfilename(defaultextension='.png')
        self.colors = Image.open(name)
        self.img_to_canvas()

    def img_to_canvas(self):

        """ Given an image, set the number of canvas and their colors properly

        :return:
        """
        self.nb_pixel_spin.delete(0, 'end')
        self.nb_pixel_spin.insert(0, self.colors.width)

        self.canvas_gen()

        for pix in range(self.colors.width):
            self.canvas_list[pix].color = self.colors.getpixel((pix, 0))
            self.colorizer(self.canvas_list[pix])
            
    def colors_gen(self):

        """ Given a canvas setup, generate a PIL Image object

        The resulting image can be used by Mainbrot.master_control_program, or saved.

        :return: None, the image is saved as a class argument
        """
        width = int(self.nb_pixel_spin.get())
        self.colors = Image.new("RGB", (width, 1))
        draw = ImageDraw.Draw(self.colors)

        for pix in range(0, width):
            color_tuple = (int(self.canvas_list[pix].color[0]), int(self.canvas_list[pix].color[1]),
                           int(self.canvas_list[pix].color[2]))

            draw.point((pix, 0), fill=color_tuple)

    def colorizer(self, canvas):

        """ Take a canvas as input, and fill it with a rectangle of the specified color

        :param canvas: The canvas to color
        :return: None
        """

        canvas.delete("all")
        canvas.rec = canvas.create_rectangle(0, 0, 32, 32, fill=tuple_to_tk_string(canvas.color))
        self.win.focus_force()

    def end(self):

        """ Used at the end of this instance

        When the user has chosen the colors he wants, this close the window, and send all the data to the MandelPic
        instance.

        :return:
        """
        self.colors_gen()
        self.pic.colors = self.colors
        self.pic.show()
        self.win.destroy()

    def selector(self, event):

        """Allows the user to chose the color of a clicked canvas

        :param event: The click. Useful because it enable this function to know which canvas was clicked.
        :return:
        """

        event.widget.color = askcolor()[0]

        self.colorizer(event.widget)


def tuple_to_tk_string(c_tuple):

    """Convert a color tuple to a color string usable by tkinter.

    :param c_tuple: RGB color tuple
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
