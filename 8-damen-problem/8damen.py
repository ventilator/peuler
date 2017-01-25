# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 21:02:08 2014
@author: ventilator 


best practice:
    hashable, immutable datatypes are your friend. no need for deepcopy etc, faster and safer
    use Counter or NamedTuple for clean code

Es dürfen keine zwei Damen auf derselben Reihe, Linie oder Diagonale stehen.

Daraus folgt:
    * nur eine Dame pro Zeile -> Anzahl Zeilen == Anzahl Damen --> jede Zeile eine Dame --> jede Zeile hat dim Verzweigungen
    
    
Konventionen:
    x = Zeile
    y = Spalte
"""
import numpy as np
import copy
from matplotlib import pyplot as plt

dame = 2
frei = 0
besetzt = 1 # von anderer dame verhindert, dass dort eine gesetzt werden kann
dim = 8
n_gefunden = 0
lösungen = []

def plot_brett(brett):
    figsize = (4, 4)
    fig, axes = plt.subplots(1,1, figsize=figsize)    
    ax = axes
    plt.axis("off")
    image_plot = ax.imshow(brett, cmap='viridis', interpolation="None")
    image_plot.set_clim(vmin=frei, vmax=dame)
    plt.show()
    

def zaehle_damen(brett):
    anzahl = 0
    for x in range(dim):
        for y in range(dim):
            if brett[x,y]==dame:
                anzahl += 1
    return anzahl    
    

# markiert Positionen auf dem Brett, die in Schlagdistanz liegen (=unbeseztbar) sowie die Dame
def setze_dame(old_brett, x, y):    
    brett = copy.deepcopy(old_brett)
    # spalten
    for ix in range(dim):
        brett[ix,y] = besetzt

    # zeilen
    for iy in range(dim):
        brett[x,iy] = besetzt

    # diagnonale
    for iy in range(-dim,dim):
        for ix in [-iy,iy]: # == definition einer diagonale
            if 0 <= x+ix < dim and 0 <= y+iy < dim:
                brett[x+ix,y+iy] = besetzt
    
    #dame selbst
    brett[x,y] = 2 
#    plot_brett(brett)
    return brett
    
    
# reject
def weitere_dame_möglich(brett, nte_dame, spalte):
    x = nte_dame-1 # erste Dame in Zeile 0, zweite Dame in Zeile 1
    y = spalte    
    return brett[x,y] == frei

# accept
def gültige_lösung(brett, nte_dame):
    global dim    
    if nte_dame == dim+1: #fast path to reject
        n_damen = zaehle_damen(brett)        
        return n_damen == dim    
    else: 
        return False        
        
        
def backtrack(brett, nte_dame):
    global dim    
    # accept
    if gültige_lösung(brett, nte_dame):
        speichere_lösung(brett)    
        return
    # if on lowest level and not already accepted: don't go deeper
    if nte_dame == dim+1:
        return
    # do deeper and make dim new paths        
    for spalte in range(dim):            
        if weitere_dame_möglich(brett, nte_dame, spalte):
            next_brett = setze_dame(brett, nte_dame-1, spalte)
            backtrack(next_brett, nte_dame+1)
                    
        
# output            
def speichere_lösung(brett):
#        plot_brett(brett)  
    global n_gefunden
    n_gefunden +=1
#    print("Anzahl gültiger Lösungen: ", n_gefunden)
    global lösungen
    doppelt = False
    for element in lösungen:
        if np.array_equal(element, brett):
            print("doppelte lösung")
            doppelt = True
            break
        
    if doppelt == False:
        lösungen.append(brett)       
        

def array_bereits_in_liste(liste, array, teste_auch_rotationen=False, teste_spiegelungen_auch_rotiert=False):
    for element in liste:
        if np.array_equal(element, array):
            return True
        if teste_auch_rotationen == True:
            if np.array_equal(element, np.rot90(array, k=1)):
                return True            
            if np.array_equal(element, np.rot90(array, k=2)):
                return True    
            if np.array_equal(element, np.rot90(array, k=3)):
                return True        
        if teste_spiegelungen_auch_rotiert == True:
            array = np.fliplr(array)
            if np.array_equal(element, array):
                return True            
            if np.array_equal(element, np.rot90(array, k=1)):
                return True            
            if np.array_equal(element, np.rot90(array, k=2)):
                return True    
            if np.array_equal(element, np.rot90(array, k=3)):
                return True                   
    return False        
            
        
def unique_lösungen(bretter):
    unique = []
    for brett in bretter:
        if not array_bereits_in_liste(unique, brett, teste_auch_rotationen=True, teste_spiegelungen_auch_rotiert=True):
            unique.append(brett)
            
    return len(unique)
            
    
def solve_problem():    
    brett = np.zeros([dim,dim]) 
    backtrack(brett, 1)
    global lösungen
    print("es gibt lösungen, n =", len(lösungen))   
    print("es gibt unique lösungen, n =", unique_lösungen(lösungen))        
    
        
if __name__ == "__main__":    
    import time
    start_time = time.time()         
    solve_problem()  
    print("runtime: \x1b[1;31m%.1fs\x1b[0m" % (time.time() - start_time))

#import profile 
#profile.run('solve_problem()')   