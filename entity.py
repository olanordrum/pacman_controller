import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from random import randint
from algorithms import a_star
from random import choice


class Entity(object):
    def __init__(self, node):
        self.name = None
        self.directions = {UP:Vector2(0, -1),DOWN:Vector2(0, 1), 
                          LEFT:Vector2(-1, 0), RIGHT:Vector2(1, 0), STOP:Vector2()}
        self.direction = STOP
        self.setSpeed(100)
        self.radius = 10
        self.collideRadius = 5
        self.color = WHITE
        self.visible = True
        self.disablePortal = False
        self.goal = None
        self.directionMethod = self.randomDirection
        self.setStartNode(node)
        self.image = None

    def setPosition(self):
        self.position = self.node.position.copy()

    def update(self, dt):
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
          
    def validDirection(self, direction):
        if direction is not STOP:
            if self.name in self.node.access[direction]:
                if self.node.neighbors[direction] is not None:
                    return True
        return False

    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False

    def reverseDirection(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp
        
    def oppositeDirection(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    def validDirections(self):
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.validDirection(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    def randomDirection(self, directions):
        return directions[randint(0, len(directions)-1)]
    
    
    
    #Direction methods

    def goalDirection(self, directions):
        distances = []
        for direction in directions:
            vec = self.node.position  + self.directions[direction]*TILEWIDTH - self.goal
            distances.append(vec.magnitudeSquared())
        index = distances.index(min(distances))
        return directions[index]
    
    def goalDirectionFlee(self, directions):
        distances = []
        for direction in directions:
            vec =  self.node.position - self.goal  + self.directions[direction]*TILEWIDTH 
            distances.append(vec.magnitudeSquared())
        index = distances.index(max(distances))
        return directions[index]
    
    def huntGhostEasy(self,directions):
        self.goal = self.nearbyGhost().position
        
        return self.goalDirection(directions)
    
    
    
    def seekPellet(self, directions):
        self.goal = self.getClosestPellet()
        distances = []
        for direction in directions:
            vec = self.node.position  + self.directions[direction]*TILEWIDTH - self.goal
            distances.append(vec.magnitudeSquared())
        index = distances.index(min(distances))
        return directions[index]
    
    
    
    def seekPowerPelletEasy(self, directions):
        print("\n POWER PELLETS: ",self.powerPellets)
        distances = []
        for direction in directions:
            vec = self.node.position  + self.directions[direction]*TILEWIDTH - self.goal
            distances.append(vec.magnitudeSquared())
        index = distances.index(min(distances))
        return directions[index]
    
    
    def getAstarPath(self,start, goal):
        start = self.nodes.getPixelsFromNode(start)
        pacTarget = self.nodes.getPixelsFromNode(goal)

        # previous_nodes, shortest_path = dijkstra(self.nodes, pacTarget)
        previous_nodes, shortest_path = a_star(
            self.nodes, start, pacTarget
        )
        path = []
        node = pacTarget
        while node != None:
            path.append(node)
            node = previous_nodes[node]
        #path.append(pacTarget)
        path.reverse()
        # print(path)
        return path
    
   
        
        
    def seekAstar(self,directions,start, goal):
        start = start
        path = self.getAstarPath(start, goal)
        startprint = self.nodes.getPixelsFromNode(start)
        goalprint = self.nodes.getPixelsFromNode(goal)
        #print("Start: ", startprint)
        #print("Goal ", goalprint)
        #print("Path: ", path)
        
    
        target = self.nodes.getPixelsFromNode(goal)


        #path.append(target)
        if len(path) < 2 :
            return self.getDirection(self.goal,directions)

        nextNode = path[1]
        
        newGoal = Vector2(nextNode[0],nextNode[1]) - start.position
        

        return self.getDirection(newGoal,directions)
            
            
            
            
    def getDirection(self, goal,directions):
        if abs(goal.x) > abs(goal.y):
            if goal.x > 0:
                return RIGHT  
            else:
                return LEFT  
        elif abs(goal.x) < abs(goal.y):
            if goal.y > 0:
                return DOWN  
            else:
                return UP 
        else:
            print("------ RANDOM DIRECTION ---------")
            return self.randomDirection(directions)





    def setStartNode(self, node):
        self.node = node
        self.startNode = node
        self.target = node
        self.setPosition()

    def setBetweenNodes(self, direction):
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2.0

    def reset(self):
        self.setStartNode(self.startNode)
        self.direction = STOP
        self.speed = 100
        self.visible = True

    def setSpeed(self, speed):
        self.speed = speed * TILEWIDTH / 16

    def render(self, screen):
        if self.visible:
            if self.image is not None:
                adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
                p = self.position - adjust
                screen.blit(self.image, p.asTuple())
            else:
                p = self.position.asInt()
                pygame.draw.circle(screen, self.color, p, self.radius)