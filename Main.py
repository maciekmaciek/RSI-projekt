__author__ = 'Monis'

from properties import Properties
from PIL import Image
from operator import add
import time
from mpi4py import MPI


def get_images_for_properties(images):
    images_for_rank = []
    for img in images:
        img_num = str(img).zfill(4)
        images_for_rank.append(Image.open('./img/IMG_{0}.jpg'.format(img_num)))
    return images_for_rank

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    start = time.time()
    images = []
    for img in range(1, 100):
        images.append(img)
    images_count = images.__len__()
    size = comm.Get_size()
    rank_images = images_count / size

    #-------------------Wyslanie do innych watkow
    for send_rank in range(1, size):
        send_images = []
        for part_image in range(0, rank_images):
            send_images.append(images[0])
            images.remove(images[0])
        comm.send(send_images, dest=send_rank, tag=111)

    #-------------------Policzenie na watku zerowym
    rank0_images = images.__len__()
    images_for_properties = get_images_for_properties(images)
    p = Properties()
    p.load(images_for_properties)
    properties = p.get_properties()
    trait = properties[0] * rank0_images
    dynamic = properties[1] * rank0_images
    colors = [x * rank0_images for x in properties[2]]

    #-------------------Zebranie wynikow
    for recv_rank in range(1, size):
        properties = comm.recv(source=recv_rank, tag=111)
        trait += properties[0] * rank_images
        dynamic += properties[1] * rank_images
        map(add, colors, [x * rank_images for x in properties[2]])

    colors_map = [(0.125, "red"), (0.25, "orange"), (0.375, "yellow"),
                  (0.5, "green"), (0.625, "teal"), (0.75, "blue"),
                  (0.875, "purple"), (1., "pink")]

    print('WYNIKI:')
    print('Srednia jasnosc: {0}'.format(trait / images_count))
    print('Srednia dynamika: {0}'.format(dynamic / images_count))
    print('Dominujacy kolor: {0}'.format(colors_map[colors.index(max(colors))][1]))
    end = time.time()
    print('Czas: {0}'.format(end - start))
else:
    images = comm.recv(source=0, tag=111)
    images_for_properties = get_images_for_properties(images)
    p = Properties()
    p.load(images_for_properties)
    properties = p.get_properties()
    comm.send(properties, dest=0, tag=111)