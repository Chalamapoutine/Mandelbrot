from tkinter import *
from Mainbrot import Mainbrot
from tkinter.ttk import *
from tkinter import filedialog


class SaveHUD:
    '''
    Interface de sauvegarde
    '''

    def __init__(self, pic, hud):
        self.win = Tk()

        self.hud = hud(self.win, pic)

        self.full_save_button = Button(master=self.button_frame, command=self.full_save, text="Sauvegarde complete")
        self.quick_save_button = Button(master=self.button_frame, command=self.quick_save, text="Sauvegarde rapide")

        self.show()

    def load_from_hud(self):
        self.new_res = (int(self.hud.x_spin.get()), int(self.hud.y_spin.get()))

    def full_save(self):
        name = filedialog.asksaveasfilename(defaultextension='.png')
        res = (int(self.hud.x_spin.get()), int(self.hud.y_spin.get()))
        max_it = int(self.hud.it_spin.get())
        exp_colo = float(self.hud.exp_colo_spin.get())

        Mainbrot(res, self.pic.centre, self.pic.taille_x, max_it, self.pic.degrade,
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
