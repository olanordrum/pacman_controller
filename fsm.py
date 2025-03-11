
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
          if dist < 150:
            res = True
        return res
      
  
    def checkEvent(self, dt):
      self.pacman.updatePowerPellets()
      
      #Eaten pellet
      pellet = self.pacman.eatPellets(self.pacman.allPowerPellets)  
      
      print("\n PELLET :", pellet)
      
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
      if pellet is not None:
              if pellet.visible:
                print(f"DEBUG: Power pellet spist: {pellet.position}")
                self.time = 7
                self.pacman.myState = SEEKGHOST
          
          
      
              
              
    def checkEvent2(self, dt):
      self.pacman.updatePowerPellets()
     
      print("pellet list:", self.pacman.pellets )
      pellet = self.pacman.eatPellets(self.pacman.pellets)  
      print ("PELLET: ",pellet)
      
      
      if pellet is None:
            print("PELLET EATEN")
            self.time = 7
            self.pacman.myState = SEEKGHOST
      
      
      
      #Ghost close bool
      close = self.ghostClose()
      
      if self.pacman.myState == SEEKGHOST:
          self.time -= dt
          
          if self.time <= 0: # seek times up
              self.pacman.myState = SEEKPOWERPELLET
          
          if pellet != None:
              self.time = 7
              self.pacman.myState = SEEKGHOST
              
              
      elif self.pacman.myState == SEEKPOWERPELLET:
          self.pacman.updatePowerPellets()
          if close:
              self.pacman.myState = FLEE
          
          if pellet != None:
              self.time = 7
              self.pacman.myState = SEEKGHOST
              
      elif self.pacman.myState == FLEE:
           if not close:
             self.pacman.myState = SEEKPOWERPELLET
             
           if pellet is not None:
              print("PELLET EATEN")
              self.time = 7
              self.pacman.myState = SEEKGHOST
            

    
    
    
    
    
  
  
  
  
'''  
    def checkEvent(self,dt):
        self.pacman.updatePowerPellets()
        
        
        
        if self.pacman.state == SEEKPOWERPELLET:
            if self.ghostClose:
                self.state = FLEE
                
                
            # Eat powerpellet
            if self.pacman.eatPellets(self.pacman.allPowerPellets) != None:
                self.time = 7
                self.state = SEEKGHOST
                self.pacman.setState(SEEKGHOST)
                
                
                
                
                
            
        elif self.state == SEEKGHOST:
          
            if self.time <= 0:
                self.state = SEEKPOWERPELLET
                self.pacman.setState(SEEKPOWERPELLET)
                
            # Eat power pellet
            if self.pacman.eatPellets(self.pacman.allPowerPellets) != None:
                self.time = 7
                self.state = SEEKGHOST
                self.pacman.setState(SEEKGHOST)
                    
            #Check time
            else:
              self.time -= dt
              
              
              
        elif self.state ==  FLEE:
              if not self.ghostClose:
                self.state = SEEKPOWERPELLET
                self.pacman.setState(SEEKPOWERPELLET)
                
                
              #EAT PELLET
              if self.pacman.eatPellets(self.pacman.allPowerPellets) != None:
                self.time = 7
                self.state = SEEKGHOST
                self.pacman.setState(SEEKGHOST)
                
  '''  
                

          
                
          
                    
                    
        
          
            
            
            
            
    
    

            
                    
        
        
        