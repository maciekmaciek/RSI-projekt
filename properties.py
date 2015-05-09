# coding=utf-8
from PIL import Image
import colorsys

class Properties:
    colors = [(0.125, "red"), (0.25, "orange"), (0.375, "yellow"),
              (0.5, "green"), (0.625, "teal"), (0.75, "blue"),
              (0.875, "purple"), (1., "pink")]

    def __init__(self):
        self.images = []
        self.pix = []

    def load(self):
        #self.images = [Image.open("./goku1.jpg"), Image.open("./goku2.jpg")]
        for image in self.images:
            self.pix.append(image.load())

    def load(self, images):
        self.images = images
        for image in self.images:
            self.pix.append(image.load())

    def rgb_int_to_percent(self, rgb):
            d_tup = (float(rgb[0])/255, float(rgb[1])/255, float(rgb[2])/255)
            return d_tup

#-------------------------------------------------- średnia jasność

    def trait_avg_value(self, images):
        avg = 0.
        for image in images:
            avg += self.v_in_image(image)
        return avg/len(images)

    def v_in_image(self, image):
        avgv = 0.
        pixels = image.load()
        for i in xrange(image.size[0]):
            for j in xrange(image.size[1]):
                per = self.rgb_int_to_percent(pixels[i,j])
                value = colorsys.rgb_to_hsv(per[0],per[1],per[2])[2]
                avgv += value

        return avgv/image.size[0]/image.size[1]


#--------------------------------------------------średnia dynamika

    def trait_avg_value_change(self, images):
        avg = 0.
        size = len(images)
        if size > 1:
            for i in range(1, size):
                avg += self.avg_pair_value_change(images[i-1], images[i])
            return avg/(size-1)
        return 0

    def avg_pair_value_change(self, image, image1): #ten sam rozmiar!
        avgv = 0.
        pixels = image.load()
        pixels1 = image1.load()
        for i in xrange(image.size[0]):
            for j in xrange(image.size[1]):
                avgv += self.pixel_value_change(pixels[i,j], pixels1[i,j])
        return avgv/image.size[0]/image.size[1]

    def pixel_value_change(self, pixel, pixel1):
        per = self.rgb_int_to_percent(pixel)
        h = colorsys.rgb_to_hsv(per[0],per[1],per[2])[2]
        per = self.rgb_int_to_percent(pixel1)
        h1 = colorsys.rgb_to_hsv(per[0],per[1],per[2])[2]
        return abs(h1-h)

#----------------------------------------------------------najczęstszy kolor
    def trait_dominating_color(self, images):
        results = self.dominating_image_colors(images[0])
        for i in range(1, len(images)):
            results = [x + y for x, y in zip(results, self.dominating_image_colors(images[i]))]
        return self.colors[results.index(max(results))]

    def dominating_image_colors(self, image):
        results = [0, 0, 0, 0, 0, 0, 0, 0]
        pixels = image.load()
        for i in xrange(image.size[0]):
            for j in xrange(image.size[1]):
                results[self.assign_pixel_to_color(pixels[i, j])] += 1
        return results

    def assign_pixel_to_color(self,pixel):
        per = self.rgb_int_to_percent(pixel)
        hue = colorsys.rgb_to_hsv(per[0], per[1], per[2])[0]
        return int((hue - 0.0625) * 8)

    def get_properties(self):
        return self.trait_avg_value(self.images), \
               self.trait_avg_value_change(self.images), \
               self.trait_dominating_color(self.images)