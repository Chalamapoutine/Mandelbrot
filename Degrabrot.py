from numba import jit
from PIL import Image, ImageDraw
from time import time


def multi_degrade_img(target_length, image):
    start = time()

    start_pic = Image.open(image)
    end_pic = Image.new("RGB", (target_length, 1))
    size = start_pic.size[0]

    for pixel in range(size + 1):
        part_length = int(target_length / (size - 1))
        subdegrad = degrade_img(part_length, start_pic.crop((pixel, 0, pixel + 2, 1)))
        end_pic.paste(subdegrad, (part_length * pixel, 0, part_length * (pixel + 1), 1))
    delta_t = time() - start
    print("degradation done in {} sec" .format(delta_t))
    return end_pic


def multi_degrade_list(target_length, image):

    """ Take a one line image and return a larger list.

    :param target_length: length of the target image. it is equal to max_it.
    :param image: Source image.
    :return: An enlarged list. It is enlarged by shading between the gaps. The list contain (R, G, B) tuples.
    """

    start = time()

    if type(image) == str:

        start_pic = Image.open(image)

    else:
        start_pic = image

    end_list = []

    size = start_pic.width

    for pixel in range(size + 1):
        part_length = int(target_length / (size - 1))
        subdegrad = degrade_list(part_length, start_pic.crop((pixel, 0, pixel + 2, 1)))
        end_list += subdegrad
    delta_t = time() - start
    print("degradation done in {} sec" .format(delta_t))
    return end_list


def degrade_img(target_length, image, average_mode="RGB"):

    if type(image) == "str":
        start_pic = Image.open(image).load()
    else:
        start_pic = image.load()
        image.save("start.png")

    end_pic = Image.new("RGB", (target_length, 1))
    draw = ImageDraw.Draw(end_pic)

    if average_mode == "RGB":
        for pixel in range(target_length):
            coeffs = (target_length-pixel, pixel)
            color = []
            for channel in range(3):
                color.append(int(average(a=start_pic[0, 0][channel],
                                         b=start_pic[1, 0][channel],
                                         coeff_a=coeffs[0],
                                         coeff_b=coeffs[1])),
                             )
            draw.point((pixel, 0), fill=tuple(color))

        if average_mode == "HSV":
            pass
    end_pic.save("end.png")
    return end_pic


def degrade_list(target_length, image, average_mode="RGB"):

    if type(image) == "str":
        start_pic = Image.open(image).load()
    else:
        start_pic = image.load()

    end_list = []

    for pixel in range(target_length):
        coeffs = (target_length - pixel, pixel)
        color = []
        for channel in range(3):
            color.append(int(average(a=start_pic[0, 0][channel],
                                     b=start_pic[1, 0][channel],
                                     coeff_a=coeffs[0],
                                     coeff_b=coeffs[1])),
                         )
        end_list.append(tuple(color))
        
    return end_list

@jit
def average(a=1, b=1, coeff_a=1, coeff_b=1):
    """
    :param a:
    :param b:
    :param coeff_a:
    :param coeff_b:
    :return: la moyenne de a et b pondérée par leurs coefficients respectifs
    """
    return(a * coeff_a + b * coeff_b) / (coeff_a + coeff_b)


