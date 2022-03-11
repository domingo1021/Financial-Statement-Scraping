#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd

class InputLoader:

    def __init__(self, csv_path:str) -> None:
        self.__basename = os.path.basename(csv_path)
        self.__df = pd.read_csv(csv_path, encoding = "Big5")
        
    @property
    def df(self):
        return self.__df

    @property
    def num_of_request(self):
        return self.__df.shape[0]
    
    @property
    def basename(self):
        return self.__basename