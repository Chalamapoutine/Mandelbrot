from time import time
from numba import jit
from PIL import Image, ImageDraw
from Histobrot import cumulative_distibutive_function
from multiprocessing import Pool
import Degrabrot


@jit(nopython=True)
def determiner_mandelbrot(c, max_it, expo=2):
    """Given a poin

    :param c: Point to check, a complex number
    :param max_it: Number of checked sequence iterations
    :param expo: z_n power
    :return: -1 if the point never go outside the radius 2 circle, or the number of iterations it take to get it out.
    """

    i = max_it
    z = complex(0, 0)

    for a in range(i):
        z_p = z
        z = z ** expo + c
        if z_p == z:  # If two iteration are equals, it is not needed to keep checking.
            return -1
        if ((z.real ** 2) + (z.imag ** 2)) >= 4:
            return a

    return -1


class Mainbrot:
    def __init__(self, resolution, centre, taille_x, max_it, colors, n_core=1, exposant=2, colo_expo=4):

        """Coordinates all the functions and manage multi-core processing.

        :param resolution: Aimed resolution
        :param centre: Middle of the final picture in the complex plane
        :param taille_x: Horizontal size of the picture in the complex plane
        :param max_it: Number of iterations checked by determiner_mandelbrot
        :param colors: Color file name, or color Image PIL object itself
        :param n_core: The number of cores that will be used for the calculations.
        :param exposant: Power of z_n in the sequence. Usually 2.

        :return: A PILLOW Image object
        """
        print('>> master control program launched\n')

        start_mcp = time()

        self.listobrot = []

        # Make the __init__ arguments class arguments
        self.resolution = resolution
        self.centre = centre
        self.taille_x = taille_x
        self.max_it = max_it
        self.colors = colors
        self.colo_expo = colo_expo
        self.n_core = n_core
        self.exposant = exposant

        # Compute general values about the image
        self.taille_y = (taille_x * (resolution[1] / resolution[0]))
        self.y_res = int(self.resolution[1] / self.n_core)  # Vertical resolution of each sub-image
        self.bord_im = self.centre.imag - 0.5 * self.taille_y  # Higher rim of the image in the complex plan
        self.c_taille_y = self.taille_y / self.n_core  # Vertical size of each sub-image in the complex plan

        self.image = None  # Will contain the image later on

        # Generate the shading from the colors
        self.shading = Degrabrot.multi_degrade_list(self.max_it + 1, self.colors)

        with Pool(processes=n_core) as p:
            listolistobrot = p.map(self.dictiobrot_builder, [0, 1, 2, 3])

        for c in range(n_core):
            for part in listolistobrot:
                if part[1] == c:
                    self.listobrot += part[0]

        self.equalize()
        self.image_builder()

        delta_t = time() - start_mcp
        print('>>// done in {} sec'.format(delta_t), end='')

    def dictiobrot_builder(self, core):

        """Builds a dictionary with pictures coordinate as key, and iteration number as item.
            :param core: The position of this listobrot in the picture

            :return: un dictionnaire avec pour clé un tuple de coordonnées dans l'image
            et en objet la valeur à partir laquelle la suite sors du cercle de rayon 2

        """

        start = time()
        print('> building dictiobrot')

        # The center of this sub-image in the complex plan
        c_centre = complex(self.centre.real, self.bord_im + (core + 0.5) * self.c_taille_y)

        listobrot = []

        pas = self.taille_x / self.resolution[0]
        coin = complex(c_centre.real - self.taille_x / 2, c_centre.imag + self.c_taille_y / 2)

        for y in range(self.y_res):  # Problem here : thrice deep list, should be twice
            listobrot.append([])

            for x in range(self.resolution[0]):
                listobrot[y].append((determiner_mandelbrot(complex(coin.real + pas * x, coin.imag - pas * y),
                                                           self.max_it, expo=self.exposant)))

        # Timer output and print
        delta_t = time() - start
        print('>/ listobrot built in {} sec\n'.format(delta_t))

        return listobrot, core

    def equalize(self):

        t = time()
        print("> equalizing")
        sortobrot = [0]  # Just a dummy item so numba is able to compute the fingerprint of the list

        for row in self.listobrot:
            sortobrot.extend(row)

        del sortobrot[0]  # Delete the dummy item
        sortobrot.sort()

        f = sortobrot[0]
        while f == -1:
            del sortobrot[0]
            f = sortobrot[0]

        cdf = cumulative_distibutive_function(sortobrot, self.max_it, self.resolution)

        for row in self.listobrot:
            for point, pixel in enumerate(row):
                if pixel != -1:
                    row[point] = (cdf[pixel] ** self.colo_expo) * self.max_it

        delta_t = time() - t
        print(">/equalised in {}sec".format(delta_t))

    def image_builder(self):
        """ Build the image
        """
        print('> image building started')
        self.image = Image.new('RGB', self.resolution)

        print('> colorizing')

        start_colo = time()  # Setting the chronometer

        # Set the entry for parallel color mapping
        entrees_list = []

        for core in range(self.n_core):
            entrees_list.append(core)

        # Do the parallel color mapping
        with Pool(processes=self.n_core) as p:
            list_subimg = p.map(self.colorizer, entrees_list)

        # Reput the mapped data together
        for core, sub_img in enumerate(list_subimg):

            core = self.n_core - core - 1
            box = (0, core * self.y_res, self.resolution[0], (core + 1) * self.y_res)
            self.image.paste(sub_img, box)

        # Just the chronometer
        delta_t_colo = time() - start_colo
        print('>/ colorized in {} sec\n\n'.format(delta_t_colo))

    @jit
    def colorizer(self, core):
        """

        :param core: The sub-image position
        :return: A colorized PILLOW Image object.
        """

        # The sub-image object, and the associated Draw.
        sub_image = Image.new('RGB', (self.resolution[0], self.y_res))
        draw = ImageDraw.Draw(sub_image)

        y_range = range(core * self.y_res, (core + 1) * self.y_res)

        for y in y_range:
            for x, c in enumerate(self.listobrot[y]):
                if c != -1:
                    draw.point((x, y - core * self.y_res), fill=self.shading[int(c)])

        return sub_image
