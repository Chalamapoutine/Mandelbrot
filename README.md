# Mandelbrot


## Presentation

A CPU fractal generator in python, with a tkinter GUI. It's a highschool / personnal project.

I presented it for my computer science oral exam at the baccalaureat (spécialité ISN for the Bac S) and got the maximum grade (20).

I used the anaconda python distribution that packs a lot of modules with it. You may be able to install every module on its own, but I found easier to just install anaconda.

I use numba's decorator @jit for optimisation which is vital, it take computing times from the 20 minutes range to the 30 seconds range (it depends on the size and quality of the picture of course). You can use this project without numba by manually removing the decorators and import statements, but it will be painfully slow.

The image library used is PILLOW (a PIL fork for python 3)

The easiest parts to make parallel were, using the multiprocessing module. Some harder parts were not, because they needed more sophisticated communication between the different processes. I tried to look up how to do GPU computation with python, but it seemed too complicated.

## The Modules

* Mainbrot.py, a module that just computes pictures given complex coordinates and information on coloration and different image characteristics.

* Zoomobrot.py, a module that allows you to create videos of zoom on the mandelbrot set (https://www.youtube.com/watch?v=P1b5j5SNhuM see here for example, though the zoom is very slow). The output is a set of png picture, you need another software to make it into a full fledged video (I used adobe after effect)

* MandelGUI.py, the GUI of the project. Allows to explore the set using simple mouse controls ( left click somewhere to zoom to it, right click to unzoom, middle click to translate the picture). There are a lot of settings (if you want to zoom a bit deep you need to increase iterations, its not automatic). An interresting setting to change is the exponant, it complety change the shape of the fractal.

* Animation Exposant.py is not up to date, but it was supposed to create animation of a change of exponant. I did not upload the results.

Theses modules are the only one you can launch as a user, the other modules are called by them, and do not operate on their own.

* SaveGUI.py A part of the GUI, it allows you to save picture you are exploring. A quick save just save the current image sowed by the GUI, a full save computes a new image, allowing you to change the settings just for the save (every relevent setting is available). 

* DegradeGUI.py is another part of the GUI, which allows you to change the shading used to colour the image. The default setting is the one I found to be the most beautiful and is stored in "quatre.png" (there was 4 colours at one point)

* Degrabrotbrot.py generate a shading from a few colours. A part of the coloration algorithm.

* Histobrot.py contains some parts of the coloration algorithm (when I transformed the project into object oriented python, a lot of this module's code was moved to the Mainbrot class from Mainbrot.py). The coloration algorithm is an histogram equalisation (not linear, the cumulative histogram curve is x^n, where n is the coloration exponant). The equalisation is performed on the raw data before the colors are applied and allows to control the quantity of each color in the picture.


The comments are in both french and english in the GUI part for my physics teacher understood only french and he needed to correct that part. The picture generating part is commented only in english.


## Possibility of improvement

* Using numpy arrays instead of default lists and dics (should be faster)

* Implementing GPU computation (very ambitious ?)

* Using numba on more function and methods (this is work, not just putting @jit in front of every one of them)

* Trying some other optimisation package (cython ?)

* Coding some of the bottleneck functions in C.

* Making a Windows and Linux binary.
