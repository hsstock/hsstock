# -*- coding: utf-8 -*-

__author__ = 'reedy'

import random

def generate_random_id(lens=8):
    _list = [str(i) for i in range(10)]
    nums = random.sample(_list, lens)
    return "{}".format("".join(nums))

if __name__ == "__main__":
    print(generate_random_id(10))