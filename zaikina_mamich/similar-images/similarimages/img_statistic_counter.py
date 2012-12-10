from __builtin__ import classmethod

__author__ = 'Katerina'

import Image
import colorsys
import math

import logging

logger = logging.getLogger('img_statistic_counter')
logger.setLevel(logging.DEBUG)

class ColorValueTransform:
    def __init__(self):
        raise Exception("Unexpected initialization of class RGBValueTransform.")

    @staticmethod
    def rgb_to_hex_string(rgb):
        hex_chars = "0123456789ABCDEF"
        result = ""
        for i in rgb:
            result += hex_chars[int(i) / 16] + hex_chars[int(i) % 16]
        return "#" + result


class ImgStatisticCounter:
    image = None

    histogram = []
    main_colors = []
    expectation_value = 0
    dispersion = 0
    standard_deviation = 0

    __colour_num_ = 256
    __min_color_difference = ((pow(255, 3) * 3) ** (1 / 3.0)) * 0.05

    UPPER_THRESHOLD = 500
    LOWER_THRESHOLD = 250

    def __init__(self, image=None, path=""):
        if image is not None:
            self.image = image
        elif len(path) > 0:
            self.image = Image.open(path)
            self.path = path

        self.histogram = ImgStatisticCounter.__count_colors_(self.image.getdata())
        self.histogram.sort(key=lambda (x, y): x)

        self.expectation_value = ImgStatisticCounter.__expectation_value_(self.histogram)
        self.dispersion = ImgStatisticCounter.__dispersion_(self.histogram, self.expectation_value)
        self.standard_deviation = (
            math.sqrt(self.dispersion[0]), math.sqrt(self.dispersion[1]), math.sqrt(self.dispersion[2]))

        self.main_colors = ImgStatisticCounter.__get_main_colors(self.image, self.standard_deviation)

    @staticmethod
    def __get_main_colors(image, deviation):
        image.thumbnail(ImgStatisticCounter.__get_small_size_(image.size, deviation), Image.ANTIALIAS)
        data = image.getdata()
        small_hist = ImgStatisticCounter.__count_colors_(data)
        result = []
        result_len = 0
        main_colors_count = 5
        for item in small_hist:
            same_idx = -1
            for i in xrange(result_len):
                if not ImgStatisticCounter.__color_is_enough_far(item[0], result[i][0]):
                    same_idx = i
                    break
            if same_idx == -1:
                result.append(item)
                result_len += 1
            else:
                result[i] = (result[i][0], item[1] + result[i][1])

        result.sort(key=lambda (x, y): y)
        return [x for (x, y) in result[:min(main_colors_count, len(result))]]

    @staticmethod
    def __color_is_enough_far(rgb1, rgb2):
        return ImgStatisticCounter.point_3d_distance(rgb1, rgb2) > ImgStatisticCounter.__min_color_difference

    @staticmethod
    def point_3d_distance(rgb1, rgb2):
        result = 0
        for i in xrange(3):
            result += pow(int(math.fabs(rgb1[i] - rgb2[i])), 3)
        return result ** (1 / 3.0)


    @staticmethod
    def __get_small_size_(size, deviation):
        return min(size[0], 10), min(size[1], 10)

    @staticmethod
    def __count_colors_(img_data):
        color_dict = {}
        for pixel in img_data:
            if not color_dict.has_key(pixel):
                color_dict[pixel] = 0
            color_dict[pixel] += 1
        lst = list(color_dict.items())
        return lst

    @staticmethod
    def __expectation_value_(histogram):
        result = [0, 0, 0]
        s = 0
        for item in histogram:
            result = [result[idx] + (item[0][idx] * item[1]) for idx in range(3)]
            s += item[1]
        return [x / (s + 0.0) for x in result]


    @staticmethod
    def __dispersion_(histogram, expectation_value):
        def channel_dispersion(idx):
            s = sum(pow(expectation_value[idx] - (x[idx] * y), 2) for (x, y) in histogram)
            return s / sum([y for (x, y) in histogram])

        return channel_dispersion(0), channel_dispersion(1), channel_dispersion(2)

    @classmethod
    def __color_distance_(cls, rgb1, rgb2):
        def saturation(rgb):
            return colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])[1]

        def value(rgb):
            return 1 - colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])[2]

        s = (min(saturation(rgb1), saturation(rgb2)) + 0.5 * min(value(rgb1), value(rgb2)))
        s = s if s > 1 else 2
        return cls.point_3d_distance(rgb1, rgb2) / math.log(s)


    @classmethod
    def distance(cls, ref, image):
        logger.info('distance_between_two_images() entered')
        logger.debug('Reference: {0}'.format(ref))
        logger.debug('Image: {0}'.format(image))

        image = image.__dict__ if not isinstance(image, dict) else image
        ref = ref.__dict__ if not isinstance(ref, dict) else ref

        return (cls.__count_img_distance_(ref, image) + cls.__count_img_distance_(image, ref)) / 2.0

    @classmethod
    def __count_img_distance_(cls, ref, image):
        result = 0
        l = len(image['main_colors'])

        for i in ref['main_colors']:
            min_value = cls.__color_distance_((0, 0, 0), (255, 255, 255))
            min_idx = 0
            for j in xrange(l):
                value = cls.__color_distance_(i, image['main_colors'][j])
                if value < min_value:
                    min_idx = j
                    min_value = value

            #arr = [cls.__color_distance_(i, j) for j in image['main_colors']]
            #result += min(arr)
            result += min_value
            arr = [cls.__color_distance_(image['main_colors'][min_idx], j) for j in ref['main_colors']]
            result += 0.5 * round(math.fabs(min(arr) - min_value))


    @classmethod
    def are_similar(cls, ref, image, counted_distance=None):
        if counted_distance is None:
            counted_distance = cls.distance(ref, image)

        if counted_distance < cls.LOWER_THRESHOLD:
            return True

        image = image.__dict__ if not isinstance(image, dict) else image
        ref = ref.__dict__ if not isinstance(ref, dict) else ref

        deviation_dist = cls.deviation_distance(image, ref)
        bounds = [(0.95, 350), (0.5, 400), (0.25, 450), (0.11, 500)]
        f = lambda seed, (x, y): seed or (deviation_dist < x and counted_distance < y)

        return reduce(f, bounds, True)


    @classmethod
    def deviation_distance(cls, img1, img2):
        deviation1 = img1['standard_deviation'] if isinstance(img1, dict) else img1.standard_deviation
        deviation2 = img2['standard_deviation'] if isinstance(img2, dict) else img2.standard_deviation

        result = cls.point_3d_distance(deviation1, deviation2)
        divisor = cls.point_3d_distance((0, 0, 0), [x + y for x, y in zip(deviation1, deviation2)])
        return result / divisor

