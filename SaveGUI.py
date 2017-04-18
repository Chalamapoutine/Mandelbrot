from tkinter import *
from Mainbrot import Mainbrot
from tkinter.ttk import *
from tkinter import filedialog


class SaveHUD:
    '''
    Interface de sauvegarde
    '''

    def __init__(self, pic):
        self.win = Tk()

        self.pic = pic

        self.entry_frame = Frame(master=self.win)

        self.x_entry = Entry(self.entry_frame)
        self.x_text = Label(master=self.entry_frame, text='Largeur :')

        self.y_entry = Entry(self.entry_frame)
        self.y_text = Label(master=self.entry_frame, text='Hauteur :')

        self.button_frame = Frame(master=self.win)

        self.full_save_button = Button(master=self.button_frame, command=self.full_save, text="Sauvegarde complete")
        self.quick_save_button = Button(master=self.button_frame, command=self.quick_save, text="Sauvegarde rapide")

        self.show()

    def full_save(self):
        name = filedialog.asksaveasfilename(defaultextension='.png')
        new_res = (int(self.x_entry.get()), int(self.y_entry.get()))
        Mainbrot(new_res, self.pic.centre, self.pic.taille_x, self.pic.max_it, self.pic.degrade,
                               n_core=4).image.save(name)

    def quick_save(self):
        name = filedialog.asksaveasfilename(defaultextension='.png')
        self.pic.im_raw.save(name)

    def show(self):
        self.entry_frame.grid(row=0, column=0)
        self.x_entry.grid(row=0, column=1, columnspan=2)
        self.x_text.grid(row=0, column=0, sticky='E')

        self.y_entry.grid(row=1, column=1, columnspan=2)
        self.y_text.grid(row=1, column=0, sticky='E')

        self.button_frame.grid(row=1, column=0)
        self.full_save_button.grid(row=0, column=1)
        self.quick_save_button.grid(row=0, column=0)
