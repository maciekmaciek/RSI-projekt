__author__ = 'Monis'

from properties import Properties
from PIL import Image
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

#TODO images adresses
images = [Image.open("./goku1.jpg"), Image.open("./goku2.jpg"), Image.open("./goku1.jpg"), Image.open("./goku2.jpg"),
          Image.open("./goku1.jpg"), Image.open("./goku2.jpg"), Image.open("./goku2.jpg")]

if rank == 0:
    images_count = images.__len__()
    size = comm.Get_size()
    rank_images = images_count / size
    print(rank_images)

    for send_rank in range(1, size):
        send_images = []
        for part_image in range(0, rank_images - 1):
            print(part_image, "   rang_imgs:", rank_images, "  size: ", size, images_count)
            send_images.append(images[0])
            images.remove(images[0])
        comm.send(send_images, dest=send_rank, tag=111)

    propertiesList = []
    for recv_rank in range(1, size):
        properties = comm.recv(source=recv_rank, tag=111)
        propertiesList.append(properties)
        print('odebral')

    p = Properties()
    p.load(images)
    properties = p.get_properties()
    propertiesList.append(properties)

    trait = 0.
    dynamic = 0.
    colors = []

    for part in range(0, size):
        trait += propertiesList[part][0]
        dynamic += propertiesList[part][1]
        colors.extend(propertiesList[part][2])

    print('Srednia jasnosc: {0}'.format(trait / size))
    print('Srednia dynamika: {0}'.format(dynamic / size))
    #print('Sredni kolor: {0}'.format(color))
else:
    images = comm.recv(source=0, tag=111)
    p = Properties()
    p.load(images)
    properties = p.get_properties()
    comm.send(properties, dest=0, tag=111)