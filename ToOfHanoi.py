#!/usr/bin/env python
from sys import stdout

class Disc:
    def __init__(self, size):
        self.size = size
        
    def __str__(self):
        return '(' + '//' * self.size  + ')'
        
    def __repr__(self):
        return str(self.size)
        
    def __cmp__(self, other):
        return self.size - other.size
        
    
    

class Tower:
    def __init__(self, maxSize, name):
        self.maxSize = maxSize
        self.name = name
        self.discs = []
        
    def __getitem__(self, n):
        return self.discs[n]
        
    def isEmpty(self):
        return self.size() == 0 
    
    def size(self):
        return len(self.discs)
        
    def getTopDisc(self):
        return self.discs[len(self.discs) - 1]
        
    def spaceForOneMore(self):
        return (self.maxSize - self.size()) > 0
        
    def pop(self):
        if self.isEmpty():
            raise TriedToGetDiscFromEmptyTower(self.name)  
        return self.discs.pop()
        
    def append(self, disc):
        if not self.spaceForOneMore():
            raise NoSpaceLeftOnTower(self.name, self.maxSize, self.size())
        if not self.isEmpty():
            if self.getTopDisc() < disc:
                raise BiggerOntoSmallerDisc(self.getTopDisc(), disc)
        self.discs.append(disc)
        self
        
    def __str__(self):
        sM = self.maxSize
        poleStrings = [ (sM - 1) * ' ' + ' || ' + (sM - 1) * ' ' for _ in xrange(sM - self.size()) ]
        diskStrings = [ (sM - d.size) * ' ' + str(d) + (sM - d.size) * ' ' for d in self.discs ]
        diskStrings.reverse()
        titleStringBlank = (sM - len(str(self.name)) / 2 ) * ' '
        titleString = titleStringBlank + '#' +  str(self.name) + titleStringBlank  + '\n\n'
        return titleString + '\n'.join(poleStrings + diskStrings)
            
        
    def __repr__(self):
        return str(self.discs)
        

#todo make tower exception and derive from there

class TowerException(Exception):
    def __init__(self, name):
        self.name = name

class TriedToGetDiscFromEmptyTower(TowerException):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "You tried to get a disc from the empty tower " + str(self.name)
        
    
class BiggerOntoSmallerDisc(TowerException):
    def __init__(self, smaller, bigger):
        self.smaller = smaller
        self.bigger = bigger
    
    def __str__(self):
        return "You tried to put a disc with a size " + self.bigger.__str__() + " onto a size " + self.smaller.__str__() + " disc. This however is not allowed"

            
class NoSpaceLeftOnTower(TowerException):
    def __init__(self, name, maxSize, currentSize):
        self.name = name
        self.maxSize = maxSize
        self.currentSize
        
    def __str__(self):
        return "You tried to put another disc on tower, " +  self.name.__str__() + " the maximum size however is " + self.maxSize.__str__() + " and the current size is " + self.currentSize.__str__() + " - the tower is full!"
        
        
class Game:
    def __init__(self, size, display):
        self.towers = [Tower(size, 0), Tower(size, 1), Tower(size, 2)]
        self.gameIsOn = True
        self.gameWon = False
        
        for i in xrange(size):
            self.towers[0].append(Disc(size -i))
            
        self.noOfMoves = 0
        self.size = size
        self.display = display
        self.display.display(self.towers, self.size)
        
        
    def __repr__(self):
        return str(self.towers)
        
    def __str__(self):
        return self.__repr__()
        
    def move(self, a, b):
        if self.gameIsOn:
            try:
                print ("Move no: %d\nTrying to move top disc from tower %d to tower %d\n" % (self.noOfMoves + 1, a, b))
                self.towers[b].append(self.towers[a].pop())
                self.noOfMoves += 1
                self.display.display(self.towers, self.size)
                self.isGameOver()
            except TowerException as e:
                print "An error was encountered: ", e.__str__(), "\n closing game"
                print "\n you can access the error as nameOfYourReference.lastError ."
                self.lastError = e
                self.gameIsOn = False
        else:
            if self.gameWon:
                print "You already won the game! It took you ", self.noOfMoves, " moves."
            else:
                print "You lost the game probably you triend an illegal move, this was the errormessage encountered: ", self.lastError.strerror
        
        
    def isGameOver(self):
        if self.towers[2].size() == self.size:
            self.gameIsOn = False
            self.gameWon = True
            print "Yeah you won! It took you ", self.noOfMoves , "moves"
            

"""prints a list of towers to stdout"""
class TowersCliDisplay:    
    def display(self, towers, maxSize):
        tStrings = zip(*[t.__str__().split('\n') for t in towers ])
        for line in tStrings:
            print ''.join(line)

"""example function

   g is a Game Object
   src is the index of the source tower
   target is the index of the target tower (captain obvious)
   
   if you want to move a disc from tower zero to 
   tower two you would call the function 
   like this:
   moveOne(g, 0, 2)
"""
def moveOne(g, src, target):
    g.move(src, target)

       
if __name__ == "__main__":
    size = 7
    g = Game(size,TowersCliDisplay())
    #example usage:
    moveOne(g, 0, 2)
    
## It is your task now to move all discs
## from tower 0 to tower 2
#
# You might want to define a function
# 
# def moveN(g, src, target, swp, n):
#
# that moves n discs from the tower with the index 
# src to the tower with the index target
#
# if you are able to achieve this you can solve
# the game with moveN(g, 0, 2, size)
#
# If you are interested in learning how to draw an owl
# visit http://www.survivedavis.com/april-28-2012/owl/
