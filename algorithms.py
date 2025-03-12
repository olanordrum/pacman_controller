from collections import defaultdict
from heapq import heappush, heappop
from nodes import Node,NodeGroup

def a_star (nodes, start, goal):

    #distanceMap, true distance
    trueDist = defaultdict(lambda:float('inf'))
    trueDist[start] = 0
    

    #Distancemap Calculated distance
    dist = defaultdict(lambda:float('inf'))
    dist[start] = 0
    
    parents = {start : None}
    
    #Pri-que:(priority, node)
    queue = [(0, start)]
    
    while queue:
        cost, u = heappop(queue)
        
        #If cost is not the same as dist[u] we have found another faster way to u while u was in 
        #cost is therefore outdated
        if cost != dist[u]:
            continue
        
        neighbors = nodes.getNeighbors(u)
        for v in neighbors:
            #Real cost to v
            c = trueDist[u] + 1
            
            #If the real cost to v is smaller than pervious cost
            if c < trueDist[v]:
                trueDist[v] = c
                
                #Calculates cost from v to goal
                f_cost = c + heuristic(v,goal)
                dist[v] = f_cost
                
                heappush(queue, (f_cost, v))
                parents[v] = u
                
                if v == goal:
                    return parents, trueDist
                

    return parents, trueDist




def heuristic(node1, node2):
    # manhattan distance
    return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])