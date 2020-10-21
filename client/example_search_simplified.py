import client
import ast
import random
import copy

# SEARCH AGENT

class Node:
    def __init__(self,state,parent,action,path_cost):
        #AgentNode
        self.state = state
        self.parent = parent
        self.action =action
        self.path_cost = path_cost

    def getState(self):
        return self.state

    def getParent(self):
        return self.parent

    def getAction(self):
        return self.action

    def getPathCost(self):
        return self.path_cost

    def getParent(self):
        return self.parent

#
# class Queue:
#     def __init__(self):
#         self.queue_data = []
#
#     def isEmpty(self):
#         if len(self.queue_data) == 0:
#             return True
#         else:
#             return False
#
#     def pop(self):
#         return self.queue_data.pop(0)
#
#     def insert(self,element):
#         return self.queue_data.append(element)
#
#     def getQueue(self):
#         return self.queue_data

class Agent:
    def __init__(self):
        self.c = client.Client('127.0.0.1', 50001)
        self.res = self.c.connect()
        random.seed()  # To become true random, a different seed is used! (clock time)
        self.visited_nodes = []#Queue()
        self.frontier_nodes = []#Queue()
        self.weightMap =[]
        self.goalNodePos =(0,0)
        self.state = (0,0)
        self.maxCoord = (0,0)

    def getConnection(self):
        return self.res

    def getGoalPosition(self):
        msg = self.c.execute("info", "goal")
        goal = ast.literal_eval(msg)
        # test
        print('Goal is located at:', goal)
        return goal

    def getSelfPosition(self):
        msg = self.c.execute("info", "position")
        pos = ast.literal_eval(msg)
        # test
        print('Received agent\'s position:', pos)
        return pos

    def getWeightMap(self):
        msg = self.c.execute("info", "map")
        w_map = ast.literal_eval(msg)
        # test
        print('Received map of weights:', w_map)
        return w_map

    def getPatchCost(self,pos):
        return self.weightMap[pos[0]][pos[1]]

    def getMaxCoord(self):
        msg = self.c.execute("info","maxcoord")
        max_coord =ast.literal_eval(msg)
        # test
        print('Received maxcoord', max_coord)
        return max_coord

    def getObstacles(self):
        msg = self.c.execute("info","obstacles")
        obst =ast.literal_eval(msg)
        # test
        print('Received map of obstacles:', obst)
        return obst



    def getPosition(self,pos,action):
        if action == "east":
            if pos[0] + 1 < self.maxCoord[0]:
                new_pos = (pos[0] + 1, pos[1])
            else:
                new_pos =(0,pos[1])

        if action == "west":
            if pos[0] - 1 >= 0:
                new_pos = (pos[0] - 1, pos[1])
            else:
                new_pos = (self.maxCoord[0] - 1, pos[1])


        if action == "north":
            if pos[1] + 1 < self.maxCoord[1]:
                new_pos = (pos[0], pos[1] + 1 )
            else:
                new_pos = (pos[0], 0)

        if action == "south":
            if pos[1] - 1 >= 0:
                new_pos = (pos[0], pos[1] - 1)
            else:
                new_pos = (pos[0], self.maxCoord[1] - 1 )
        return new_pos


    def getNode(self,parent_node,action):
        state = self.getPosition(parent_node.getState(),action)
        pathCost = parent_node.getPathCost() + self.getPatchCost(state)
        return AgentNode(state, parent_node, action, pathCost)


    def run(self):

        # Get the position of the Goal
        self.goalNodePos = self.getGoalPosition()
        #  Get information of the world
        # Get information of the weights for each step in the world ...
        self.weightMap = self.getWeightMap()
        # Get max coordinates
        self.maxCoord = self.getMaxCoord()
        #test
        #print("Example: Weight at x=1 and y=2:", self.weightMap[1][2])
        # Get the initial position of the agent
        self.state = self.getSelfPosition()
        # Start thinking
        i = 0
        end = False
        found = None
        #Add first node (root)
        root = AgentNode(self.state,self.state,"",0)
        self.visited_nodes.insert(root)
        # Get first four nodes
        self.frontier_nodes.insert(self.getNode(root,"north"))
        self.frontier_nodes.insert(self.getNode(root,"east"))
        self.frontier_nodes.insert(self.getNode(root,"west"))
        self.frontier_nodes.insert(self.getNode(root,"south"))

        # Add them to
        while end == False:
            node_to_expand = self.frontier_nodes.pop()
            self.state = node_to_expand.getState()
            #test
            print("Node's position (expand):", self.state)
            for dir in ["north","east","west","south"]:
                new_node = self.getNode(node_to_expand,dir)
                if new_node not in self.visited_nodes.getQueue():
                    self.frontier_nodes.insert(new_node)
            for node in self.frontier_nodes.getQueue():
                if node.getState() == self.goalNodePos:
                    print("Node state:",node.getState())
                    print("GoalNodePos",self.goalNodePos)
                    end = True
                    found = node
        if end == True:
            print("Found the goal with cost:",found.getPathCost())
            if __name__ == '__main__':
                node = found
                print(node.getState(),"<-",node.getPathCost(),"-")
                while ( node.getPathCost() != 0):
                    node = node.getParent()
                    print(node.getState(),"<-",node.getPathCost(),"-")
        input("Waiting for return!")


#STARTING THE PROGRAM:
def main():
    print("Starting client!")
    ag = Agent()
    if ag.getConnection()!= -1:
        ag.run()

main()
