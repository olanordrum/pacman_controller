
from constants import SEEKPOWERPELLET,SEEKGHOST, FLEE 
from pacman import *



class StateMachine(object):
    def __init__(self, pacman,state):
        self.pacman = pacman
        self.time = 7
        
        
        #True false according to ghost distance
    def ghostClose(self):
        res = False
        for ghost in self.pacman.ghosts:
          dist = self.pacman.dist(ghost.node.position.asTuple(),self.pacman.position.asTuple())
          if dist < 100:
            res = True
        return res
      
      
    def checkEvent(self, dt):
        self.pacman.updatePowerPellets()
        
        # Eaten pellet
        pellet = self.pacman.eatPellets(self.pacman.allPowerPellets)  
        
        # Ghost close bool
        close = self.ghostClose()

        # Hvis Pac-Man har spist en power pellet, aktiver SEEKGHOST uansett
        if pellet is not None and pellet.alive:
            pellet.alive = False
            print(f"DEBUG: Power pellet spist: {pellet.position}")
            self.time = 5  # Riktig tid
            self.pacman.myState = SEEKGHOST

        # Hvis vi er i SEEKGHOST, tell ned tiden
        if self.pacman.myState == SEEKGHOST:
            self.time -= dt  
            if self.time <= 0:
                self.pacman.myState = SEEKPOWERPELLET

        # Hvis Pac-Man er for nærme et spøkelse og IKKE i SEEKGHOST, aktiver FLEE
        if close and self.pacman.myState not in [SEEKGHOST, FLEE]:
            self.pacman.myState = FLEE
            self.flee_time = 6  # Resetter FLEE-tid

        # Hvis vi er i FLEE, sjekk om vi kan stoppe
        if self.pacman.myState == FLEE:
            self.flee_time -= dt
            if self.flee_time <= 0 or not close:
                self.pacman.myState = SEEKPOWERPELLET
                
                
  
    def checkEvent2(self, dt):
      self.pacman.updatePowerPellets()
      
      #Eaten pellet
      pellet = self.pacman.eatPellets(self.pacman.allPowerPellets)  
      
      print("\n PELLET EATEN :", pellet)
      
      #Ghost close bool
      close = self.ghostClose()
      
      if self.pacman.myState == FLEE:
          if not close: #Not close anymore
              self.pacman.myState = SEEKPOWERPELLET
      
      
      #Ghost nearby
      if close and self.pacman.myState != SEEKGHOST:
              self.pacman.myState = FLEE
              
      
      if self.pacman.myState == SEEKGHOST:
          self.time -= dt  # count down
        
          if self.time <= 0: # seek times up
              self.pacman.myState = SEEKPOWERPELLET

      #Eaten power pellet?
      if pellet is not None and pellet.alive:
            pellet.alive = False
            print(f"DEBUG: Power pellet spist: {pellet.position}")
            print("PELLET ALIVE:", pellet.alive)
            self.time = 7
            self.pacman.myState = SEEKGHOST
          
    
        
          
            
            
            
            
    
    

            
                    
        
        
        