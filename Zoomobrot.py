import Mainbrot


def zoom(d_taille_x, a_taille_x, point, max_it,  resolution=(1920, 1080), nb_etapes=1, q=0, e=0):
    """

    :param d_taille_x: Taille horizontale de la première frame dans le plan complexe
    :param a_taille_x: Taille horizontale de la dernière frame dans le plan complexe
    :param point: centre de toute les frame
    :param nb_etapes: nombre de frame à rendre
    :param resolution: resolution des images générées
    :param q: raison de la suite géométrique du zoom. Si pas de valeur, déterminé avec depart/arrivée
    :param e: numéro de départ des nom des images
    :param max_it: nombre maximal d'itérations
    :return: ne retourne rien, sauvegarde simplement les images.
    """
    print(">>>> zoom started\n\n")
    ratio = resolution[0]/resolution[1]
    taille_x = d_taille_x
    if q == 0:
        q = (a_taille_x/d_taille_x)**(1/nb_etapes)

    while e < nb_etapes:

        print(">>> image n°{}" .format(e))
        name = str(e) + '.png'
        Mainbrot.master_control_program(resolution, point, taille_x, max_it, "quatre.png", name, n_core=4).save(name)
        taille_x *= q
        e += 1
    print("q = {}" .format(q))
if __name__ == '__main__':
    zoom(4, 0.00000000000001, -0.16326823255986433 + 1.0353680299635175j, 40000, nb_etapes=2000)
