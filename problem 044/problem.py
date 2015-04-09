# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 16:18:26 2015

@author: gruenewa
"""
import itertools

class pentagonal:
    def __init__(self):
        self.lut = set()
        self.pairs = []

    def get_pentagonal_number(self, n):
        return n*(3*n-1)/2

    def create_lut(self, maximum):
        for i in range(1, maximum):
            self.lut.add(self.get_pentagonal_number(i))
        # print self.lut

    def get_pentagonal_pairs(self):
        # get all possible combinations
        pent_combinations = itertools.combinations(self.lut, 2)

        # get sum and difference of a pair, if also a pent number, add to a list
        for items in pent_combinations:
            x, y = items

            pent_sum = x + y
            pent_difference = abs(x-y)
            if pent_sum in self.lut:
                if pent_difference in self.lut:
                    self.pairs.append([x, y, pent_sum, pent_difference])

#    def get_pentagonal_pairs(self):
#        print ((self.lut & self.difference) & self.sum)

    def print_pentagonal_pairs(self):
        for item in self.pairs:
            print item


def main():
    generator = pentagonal()
    generator.create_lut(5000)

    generator.get_pentagonal_pairs()
    generator.print_pentagonal_pairs()


main()

# gives only one pair
# [1560090, 7042750, 8602840, 5482660]
# 5482660 turns out to be correct

# possible optimization

# test first difference
# something with that it has to be an even number...