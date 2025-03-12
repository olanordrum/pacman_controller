import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from sprites import PacmanSprites
from heapq import heappush, heappop
from pellets import PelletGroup,Pellet
from fsm import StateMachine
from random import choice


class Pacman(Entity):
    def __init__(self, node, nodes, pellets):
        Entity.__init__(self, node )
        self.name = PACMAN    
        self.color = YELLOW
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.sprites = PacmanSprites(self)
        self.nodes = nodes # all nodes
    
        
        self.directionMethod = self.goalDirectionFlee
        self.goal = Vector2()
        
        #States
        self.states = [SEEKPOWERPELLET,SEEKPELLET,SEEKGHOST,FLEE]
        self.myState = SEEKPELLET #Current state
        
        
        
        self.pellets = pellets.pelletList
        self.allPowerPellets = pellets.powerpellets
        
        self.statemachine = StateMachine(self,self.myState )
        
        

    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()
        self.myState = SEEKPELLET
        self.updatePowerPellets()

    def die(self):
        self.alive = False
        self.direction = STOP
        
        
        
        
        
    def update(self, dt):

        self.sprites.update(dt)
        
        
        #Check for event each uodate
        self.statemachine.checkEvent(dt)
        
        #Update power pellets
        self.updatePowerPellets()
        
        #Update states
        self.stateChecker()
        

        
        self.position += self.directions[self.direction]*self.speed*dt
        
         
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
                self.target = self.getNewTarget(self.direction)

            self.setPosition()


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
    
    
    
    
    # Sets pacman ghosts (GhostGroup) variable
    def setGhosts(self,ghosts):        
        self.ghosts = ghosts

        
    #Updates the powerPellets instance variable
    def updatePowerPellets(self):
        self.powerPellets = [pellet for pellet in self.pellets if pellet.alive and pellet.name == POWERPELLET]
        
        
    #Finds the closest pellet to pacman
    def getClosestPellet(self):
        pellets = self.pellets
        pacman_pos = self.position.asTuple()  #Get pacman pos as tuple
        
        visible_pellets = [pellet.position for pellet in pellets if pellet.visible]
        

        if not visible_pellets: # Level done
            return None

        closest_pellet = min(visible_pellets, key=lambda pellet: self.dist(pacman_pos, pellet.asTuple()))
        return closest_pellet
    
    
    #Finds the closest 'alive' power pellet to pacman
    def getClosestPowerPellet(self):
        pacman_pos = self.position.asTuple()  #Get pacman pos as tuple
        
        visible_pellets = [pellet.position for pellet in self.powerPellets if pellet.alive and pellet.name == POWERPELLET]
        
        print("\n Visble power pellets: ", visible_pellets, "\n")

        if not visible_pellets: 
            print("NO POWER PELLETS")
            return None

        closest_pellet = min(visible_pellets, key=lambda pellet: self.dist(pacman_pos, pellet.asTuple()))
        return closest_pellet
    
    
    

    
    # manhattan distance
    def dist(self,node1, node2):
        return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])
    

        

    #Finding nearest ghosts for flee purpose
    def nearbyGhostFlee(self):
        queue = []
        count = 0
        for ghost in self.ghosts:
            if self.homeNodes(ghost):
                continue

            dist = (ghost.node.position - self.node.position).magnitudeSquared()
            heappush(queue,(dist,count,ghost.node))
            count += 1
            
        if queue:
            return heappop(queue)[2]
        
        return self.target
            
            
    #Finding nearest ghost for hunting ghosts
    def nearbyGhost(self):
        queue = []
        count = 0
        ghostList = [ghost for ghost in self.ghosts]
        
        for ghost in ghostList:
            ret = ghost
            # If ghost is not in FREIGHT we cant eat it
            if self.homeNodes(ghost) or ghost.mode.current != FREIGHT:
                continue

            dist = (ghost.node.position - self.node.position).magnitudeSquared()
            heappush(queue,(dist,count,ghost))
            count += 1
            
        if queue:
            return heappop(queue)[2]
        
        return choice(ghostList)
    
    # Find the closest power pellet
    def nearbyPowerPellet(self):
        queue = []
        
        self.updatePowerPellets()
        
        count = 0
        for pellet in self.powerPellets:
            dist = (pellet.node.position - self.node.position).magnitudeSquared()
            heappush(queue,(dist,count,pellet.node))
            count += 1
            
        return heappop(queue)[2]
    
    
    
    #Checking if a ghost is 'home'
    def homeNodes(self, ghost):
        if ghost.node == ghost.homeNode or ghost.node == ghost.spawnNode:
            return True

        for key in ghost.node.neighbors:
            neighbor = ghost.node.neighbors[key]
            if neighbor == ghost.homeNode or neighbor == ghost.spawnNode:
                return True
            
        return False
                

        
                
    #Check states and sets directionMethod accordingly
    def stateChecker(self):
        if self.myState == SEEKPELLET:
            print("\n STATE: PELLET \n")
            self.directionMethod = self.seekPellet
            
        elif self.myState == SEEKPOWERPELLET:
            if self.powerPellets:
                print("\n STATE: POWERPELLET \n")
                self.directionMethod = self.seekPowerPellet
            else:
                self.myState = SEEKPELLET
                self.directionMethod = self.seekPellet
            
        elif self.myState == SEEKGHOST:
            print("\n STATE: SEEKGHOST \n")
            self.directionMethod = self.huntGhostAstar
            
        elif self.myState == FLEE:
            print("\n STATE: FLEE \n")
            self.directionMethod = self.flee
            
            
            
    #PAC MAN direction methods
    def flee(self,directions):
        self.goal = self.nearbyGhostFlee().position
        return self.goalDirectionFlee(directions)
    
    
    def huntGhostAstar(self,directions):
        goal = self.nearbyGhost()
        self.goal = goal.position
        return self.seekAstar(directions, self.node, goal.target)
    
    
    def seekPowerPellet(self,directions):
        self.goal = self.getClosestPowerPellet()
        return self.seekPowerPelletEasy(directions)
    
        
        
        
            
    
        
        
        
        
        