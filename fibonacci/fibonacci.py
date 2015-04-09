# -*- coding: utf-8 -*-
"""
Created on Mon Mar 09 15:00:41 2015

@author: gruenewa
"""
from math import *
import matplotlib.pyplot as plt

class fibunacci_generator:
    def __init__(self):
        self.n_before = 1
        self.n_current = 1
        self.n_start = 1

    def get_fibunacci_number(self, n):
        n_new = self.n_start
        n_current = self.n_current
        n_before = self.n_before
        for i in range(self.n_start,n-1):
            n_new = n_current + n_before
            n_before = n_current
            n_current = n_new
        return n_new

    def get_fibunacci_number_by_moivre(self, n):
        n_new = 1/sqrt(5)*(((1+sqrt(5))/2)**n-((1-sqrt(5))/2)**n)
        return n_new

    def get_fibunacci_number_by_reduced_moivre(self, n):
        n_new = 1/sqrt(5)*(((1+sqrt(5))/2)**n)
        return n_new

    def get_fibunacci_number_by_further_reduced_moivre(self, n):
        n_new = 2**(-n)*5**((n-1)/2)
        return n_new


def main():
    generator = fibunacci_generator()
    print'{:>12}  {:>24}  {:>24}  {:>24}  {:>12}'.format("iterative", "explicit", "reduced moivre", "further reduced moivre", "moivre identical")

    fib_i = []
    fib_numbers = []
    fib_moivre = []
    fib_moivre_reduced = []
    fib_moivre_further_reduced = []


    for i in range (1,20):
        number = generator.get_fibunacci_number(i)
        moivre_number = generator.get_fibunacci_number_by_moivre(i)
        moivre_number_reduced = generator.get_fibunacci_number_by_reduced_moivre(i)
        number_by_further_reduced_moivre = generator.get_fibunacci_number_by_further_reduced_moivre(i)

        fib_i.append(i)
        fib_numbers.append(number - number)
        fib_moivre.append(moivre_number - number)
        fib_moivre_reduced.append(moivre_number_reduced - number)
        fib_moivre_further_reduced.append(number_by_further_reduced_moivre - number)

        # print'{:12.0f}  {:24.18f}  {:24.18f}  {:24.18f} {:>12}'.format(number, moivre_number, moivre_number_reduced-number, number_by_further_reduced_moivre, str(number == moivre_number))


    plt.figure()
    plt.plot(fib_i, fib_numbers, 'r-', fib_i, fib_moivre, 'g-', fib_i, fib_moivre_reduced, 'b-', fib_i, fib_moivre_further_reduced, 'o-')
    plt.show()

     # test for drift
    print "first fibonacci number which is off by 1"
    i = 0
    while i<100000:
        i += 1
        if generator.get_fibunacci_number(i) != round(generator.get_fibunacci_number_by_reduced_moivre(i)):
            print'{:12.0f}  {:24.18f}  {:>12}'.format(generator.get_fibunacci_number(i), generator.get_fibunacci_number_by_reduced_moivre(i), i)
            break

main()