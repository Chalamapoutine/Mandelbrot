import Mainbrot as mb


def animation_exposant(nb_frame, d_expo, a_expo):
    for i in range(nb_frame):

        expo = i * (a_expo - d_expo) / nb_frame
        mb.master_control_program((2000, 2000), 0, 4, 200, "quatre.png", "expo2 " + str(expo) + ".png", n_core=4, exposant=expo)

if __name__ == "__main__":
    animation_exposant(10, 0, 3)
