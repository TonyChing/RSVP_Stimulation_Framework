#!/usr/bin/env python3
# -*- coding: utf-8 -*

import abstract_config_class


class para_config(abstract_config_class.abstract_config_class):
    def __init__(self):
        self.para_config = {}
        self.para_config['trail_number'] = 1
        self.para_config['image_per_trail'] = 100
        self.para_config['stimulation_freq'] = 10

    def load_to(self, para_config: dict):
        para_config['trail_number'] = self.para_config['trail_number']
        para_config['image_per_trail'] = self.para_config['image_per_trail']
        para_config['stimulation_freq'] = self.para_config['stimulation_freq']
        return para_config
