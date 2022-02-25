#!/usr/bin/env python3
# -*- coding: utf-8 -*

import abstract_config_class


class image_config(abstract_config_class.abstract_config_class):
    def __init__(self):
        self.image_config = {}
        self.image_config[
            'image_address'] = 'D:\刺激电脑硬盘\qinyu\RSVP_python\image'
        self.image_config['image_size'] = [600, 600]
        self.image_config['image_center'] = [200, 400]
        self.image_config['Image_No'] = [1, 2, 1, 2]
        self.image_config['Image_ID'] = [1, 100, 100, 10]

    def load_to(self, image_config: dict):
        image_config['image_size'] =  self.image_config['image_size']
        image_config['image_address'] = self.image_config['image_address']
        image_config['image_center'] =  self.image_config['image_center']
        image_config['Image_No'] = self.image_config['Image_No']
        image_config['Image_ID'] = self.image_config['Image_ID']
        return image_config
