# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 21:02:08 2014

@author: ventilator



Each character on a computer is assigned a unique code and the preferred standard is ASCII (American Standard Code for Information Interchange). For example, uppercase A = 65, asterisk (*) = 42, and lowercase k = 107.

A modern encryption method is to take a text file, convert the bytes to ASCII, then XOR each byte with a given value, taken from a secret key. The advantage with the XOR function is that using the same encryption key on the cipher text, restores the plain text; for example, 65 XOR 42 = 107, then 107 XOR 42 = 65.

For unbreakable encryption, the key is the same length as the plain text message, and the key is made up of random bytes. The user would keep the encrypted message and the encryption key in different locations, and without both "halves", it is impossible to decrypt the message.

Unfortunately, this method is impractical for most users, so the modified method is to use a password as a key. If the password is shorter than the message, which is likely, the key is repeated cyclically throughout the message. The balance for this method is using a sufficiently long password key for security, but short enough to be memorable.

Your task has been made easy, as the encryption key consists of three lower case characters. Using cipher.txt (right click and 'Save Link/Target As...'), a file containing the encrypted ASCII codes, and the knowledge that the plain text must contain common English words, decrypt the message and find the sum of the ASCII values in the original text.

ascii a = 97, ascii z = 122

"""

import profile

from numpy import loadtxt
from itertools import cycle, product



filename = "p059_cipher.txt"   

key_alphabet = ''     
for k_value in range(ord("a"),ord("z")+1):
    key_alphabet+= chr(k_value)
print(key_alphabet)


def solve_problem():
    encrypted_text = loadtxt(filename, delimiter=",", dtype = int)    
    for key in product(key_alphabet, repeat = 3)     :
        decrypted_text = ''.join(chr(e^ord(k)) for e,k in zip(encrypted_text, cycle(key)))
        if (decrypted_text.find(" the ") > -1): # " the " is better than "the"
            print(decrypted_text)
            print(key)
            sum_ascii = 0
            for char in decrypted_text:
                sum_ascii += ord(char)
            print("Sum of characters")    
            print(sum_ascii)
            break
    
    return 0
    
solve_problem()    
# profile.run('solve_problem()')   