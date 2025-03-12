
from constants import SEEKPOWERPELLET,SEEKGHOST, FLEE 
from pacman import *



# Controlls pacman behavior according to events
class StateMachine(object):
    def __init__(self, pacman,state):
        self.pacman = pacman
        self.time = 7
        
        
    # Checks if the closest ghost is closer than some threshold
    def ghostClose(self):
        res = False
        for ghost in self.pacman.ghosts:
          dist = self.pacman.dist(ghost.node.position.asTuple(),self.pacman.position.asTuple())
          if dist < 100:
            res = True
        return res
      
      
    # Checks for events and changes pacman states according to event
    def checkEvent(self, dt):
        self.pacman.updatePowerPellets()
        
        # Eaten pellet
        pellet = self.pacman.eatPellets(self.pacman.allPowerPellets)  
        
        #Bool: ghost distance < threshold
        close = self.ghostClose()
        # If pacman eats power pellet, seek ghost
        if pellet is not None and pellet.alive:
            pellet.alive = False
            print(f"DEBUG: Power pellet spist: {pellet.position}")
            self.time = 5  # Riktig tid
            self.pacman.myState = SEEKGHOST
            

        # Count down time or stop seeking ghost
        if self.pacman.myState == SEEKGHOST:
            self.time -= dt  
            if self.time <= 0:
                self.pacman.myState = SEEKPOWERPELLET

        # Check distance to closest ghost and if true, FLEE
        if close and self.pacman.myState not in [SEEKGHOST, FLEE]:
            self.pacman.myState = FLEE
            self.flee_time = 6  # Resetter FLEE-tid


        # If flee-state, check if we should stop
        if self.pacman.myState == FLEE:
            self.flee_time -= dt
            if self.flee_time <= 0 or not close:
                self.pacman.myState = SEEKPOWERPELLET
                
                    self.pacman.myState = SEEKPOWERPELLET
                
          
    
        
          
            
            
            
            
    
    

            
                    
        
        
        