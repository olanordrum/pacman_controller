import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from sprites import PacmanSprites
from heapq import heappush, heappop
from pellets import PelletGroup,Pellet

class Pacman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node )
        self.name = PACMAN    
        self.color = YELLOW
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.sprites = PacmanSprites(self)
    
        
        self.directionMethod = self.goalDirectionFlee
        self.goal = Vector2()
        
        #States
        self.states = [SEEKPELLET,SEEKGHOST,FLEE]
        self.myState = SEEKPELLET #Current state
        

    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()

    def die(self):
        self.alive = False
        self.direction = STOP
        
    def update(self, dt):
        self.sprites.update(dt)
        
    
        #Update 
        self.stateChecker()
        
        #Find closest ghost
        closetsGhost = self.getClosestNode(self.ghostpositions)
        print(closetsGhost)
        
        self.position += self.directions[self.direction]*self.speed*dt
        
        self.goal = closetsGhost
         
        if self.overshotTarget():
            self.node = self.target
            directions = self.validDirections()
            direction = self.directionMethod(directions)
            if not self.disablePortal:
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                if self.oppositeDirection(direction):
                   self.reverseDirection()

            self.setPosition()

    def update2(self, dt):	
        self.sprites.update(dt)
        self.position += self.directions[self.direction]*self.speed*dt
        
        ghostList = self.ghosts.getGhosts()
        self.goal = ghostList[0].position
        
        direction = self.goal
        
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else: 
            if self.oppositeDirection(direction):
                self.reverseDirection()
                


    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None    
    
    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False
    
    
    # My code
    def setGhosts(self,ghosts):        
        self.ghosts = ghosts
        self.ghostpositions = [ghost.position for ghost in self.ghosts] 
        
    
    def setPellets(self,pellets: PelletGroup):
        self.pellets = pellets.pelletList
        self.pelletpositions = [pellet.position for pellet in self.pellets]
        
        
        #Finds the closest ghost to pacman. Using manhattan
    def getClosestPellet(self):
        self.setPellets
        pellets = self.pellets
        
        pacman_pos = self.position.asTuple()  #Get pacman pos as tuple
        
        visible_pellets = (pellet.position for pellet in pellets if pellet.visible)
        

        if not pellets: 
            return None

        closest_pellet = min(visible_pellets, key=lambda pellet: self.heuristic(pacman_pos, pellet.asTuple()))
        return closest_pellet
    
    
    
    
    #Takes a list of nodes and returns the closest one to pacman
    def getClosestNode(self,nodes):
        pacman_pos = self.position.asTuple()  #Get pacman pos as tuple

        if not nodes: 
            return None

    
        closest_node = min(nodes, key=lambda node: self.heuristic(pacman_pos, node.asTuple()))
        return closest_node
        
        
    
    def heuristic(self,node1, node2):
    # manhattan distance
        return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])
    
    
        
    
    
    #Statchecker
    def stateChecker(self):
        print("MY STATE: ", self.myState)
        if self.myState == SEEKPELLET:
            print("\n SEEK \n")
            self.directionMethod = self.seekPellet #A*
            
        elif self.myState == SEEKGHOST:
            print("\n FLEE \n")
            self.directionMethod = self.goalDirection
            
        elif self.myState == FLEE:
            print("\n WANDER \n")
            self.directionMethod = self.goalDirectionFlee
            


        
    
        


'''
    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP  
'''