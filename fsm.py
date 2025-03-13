
from constants import SEEKPOWERPELLET,SEEKGHOST, FLEE 
from pacman import *



# Controlls pacman behavior according to events
class StateMachine(object):
    def __init__(self, pacman):
        self.pacman = pacman
        self.time = 7
        
        
    # Checks if the closest ghost is closer than some threshold
    def ghostClose(self,distance):
        res = False
        for ghost in self.pacman.ghosts:
          dist = self.pacman.dist(ghost.node.position.asTuple(),self.pacman.position.asTuple())
          if dist < distance:
            res = True
        return res
    
    # Checks if the closest power pellet is closer than some threshold
    def pelletClose(self,distance):
        if not self.pacman.powerPellets:
            return False
        
        PP = self.pacman.nearbyPowerPellet()
        dist = self.pacman.dist(PP.position.asTuple(),self.pacman.position.asTuple())
        if dist < distance:
            return True
        return False





 
      
    # Checks for events and changes pacman states according to event
    def checkEvent(self, dt):
        self.pacman.updatePowerPellets()
        
        # Eaten pellet
        pelletEaten = self.pacman.eatPellets(self.pacman.allPowerPellets)  
        
        
        #Bool: ghost distance < threshold
        close = self.ghostClose(100)
        
        #Bool: power pellet distance < threshold
        closePP = self.pelletClose(150)
        
        
        
        #seek power pellet if its close
        if closePP:
            self.pacman.myState = SEEKPOWERPELLET
        
            
        # If pacman eats power pellet, seek ghost
        if pelletEaten is not None and pelletEaten.alive:
            pelletEaten.alive = False
            self.time = 6  # Seek time
            self.pacman.myState = SEEKGHOST
            

        # Count down time or stop seeking ghost
        if self.pacman.myState == SEEKGHOST:
            self.time -= dt  
            if self.time <= 0:
                self.pacman.myState = SEEKPELLET

        # Check distance to closest ghost and if true, FLEE
        if close and self.pacman.myState not in [SEEKGHOST, FLEE]:
            self.pacman.myState = FLEE
            self.flee_time = 6  # Reset FLEE-tid


        # If flee-state, check if we should stop
        if self.pacman.myState == FLEE:
            self.flee_time -= dt
            if self.flee_time <= 0 or not close:
                self.pacman.myState = SEEKPELLET
                
          
    
        
          
            
            
            
            
    
    

            
                    
        
        
        