import client
import ast
import random
import copy

# In this example it is used the BREADTH FIRST.

class Client:
    def __init__(self,HOST='127.0.0.1',PORT=50001):
        self.host = HOST
        self.port = PORT
    def print_message(self,data):
        print("Data:",data)
    def connect(self):
       try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.host, self.port))
            return(0)
       except:
            print('A connection error occurred!')
            return(-1)
    def execute(self,action,value,sleep_t = 0.5):
        self.s.sendall(str.encode(action+" "+value))
        data = self.s.recv(2048)
        print('Received', repr(data))
        msg = data.decode()
        #message(ast.literal_eval(data.decode()))
        time.sleep(sleep_t)
        return msg

class Agent:
    def __init__(self):
        self.c = client.Client('127.0.0.1', 50001)
        self.res = self.c.connect()
        random.seed()  # To become true random, a different seed is used! (clock time)

    def getState(self):
        return self.res

    def getGoal(self):
        msg = self.c.execute("info", "goal")
        goal = ast.literal_eval(msg)
        # test
        print('Goal is located at:', goal)
        return goal
    def getPos(self):
        msg = self.c.execute("info", "position")
        pos = ast.literal_eval(msg)
        # test
        print('Received agent\'s position:', pos)
        return pos
    def getMap(self):
        msg = self.c.execute("info", "map")
        w_map = ast.literal_eval(msg)
        # test
        print('Received map of weights:', w_map)
        return w_map
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

    #RETURN A LIST OF NEXT POSITIONS (not considering the obstacles!)
    def getNextPositions(self,pos, used_pos):
        '''Return the possible next positions of the agent, given the present position and not moving beyond the limits of
        the field and removing previously touched patches.'''
        next_pos = []
        max_coord = self.getMaxCoord()
        if pos[0] + 1 < max_coord[0]:
            new_pos = (pos[0]+1,pos[1])
            if new_pos not in used_pos:
                next_pos.append(new_pos)
        if pos[1] + 1 < max_coord[1]:
            new_pos =(pos[0],pos[1]+1)
            if new_pos not in used_pos:
                next_pos.append(new_pos)
        if pos[0] - 1 >= 0:
            new_pos = (pos[0] - 1 ,pos[1])
            if new_pos not in used_pos:
                next_pos.append(new_pos)
        if pos[1] - 1 >= 0:
            new_pos = (pos[0],pos[1] - 1)
            if new_pos not in used_pos:
                next_pos.append(new_pos)
        return next_pos

    def run(self):
        # Positions already used
        used_pos = []
        # Get the position of the Goal
        goal = self.getGoal()
        #  Get information of the world
        #  Print the obstacles position
        obstacles = self.getObstacles()
        # TEST:
        #print("Obstacles 0 1 =", obstacles[0][1])
        # Get information of the weights for each step in the world ...
        map = self.getMap()
        #TEST:
        #print("Example: Weight at x=1 and y=2:", map[1][2])

        #PATHS will keep all the possible paths to the goal
        # 1-Get the initial position of the agent
        pos = self.getPos()
        paths = [[pos]]
        # START THINKING ...
        i = 0
        end = False
        while end == False:
        # TEST: to test the model using only 3 cycles
        #for i in range(3):
            new_paths = []
            #For each path in the list of paths
            for path in paths:
                # Get the first element for each elem_list
                # Element_list is  one possible path to Goal
                elem = path[0]
                #Test
                print("First element of the Paths:",elem)
                # 2-Add the actual position to the list of positions already tested
                used_pos.append(elem)
                # 3-Get list of possible positions from the actual position
                next_pos = self.getNextPositions(elem, used_pos)
                # Test
                print("List of possible next positions:", next_pos)
                # 4-Remove from the list the obstacles!
                # (to be implemented)
                # 5- Add the new elements found to a new list
                new_path =[]
                # Each element of the list is a new position
                for np in next_pos:
                    # Get the previous path...
                    new_path = copy.deepcopy(path)
                    # Add the new element...,
                    new_path.insert(0,np)
                    # Test
                    print("New path apprending ", np," is:",new_path)
                    # Keep the new paths in a new list
                    new_paths.append(new_path)
            # 6-Test if any new position found is the Goal
            for new_path in new_paths:
                #Test
                print("First element of path ", path, " is ", path[0]," while goal is ",goal)
                if new_path[0] == goal:
                    end = True
                    break
            #    for p in next_pos:
            #        if p == goal:
            #            # If it is the Goal, stops!
            #            end = True
            # Update paths with the new paths
            paths = copy.deepcopy(new_paths)
            # 6-For each element in the list, expand it for the next possible positions (don't include position already in the previous list)
            print("Iteration ",i,":",paths)
            i = i + 1
        # Etc
        # Print "Found a Path!"
        if end == True:
            print("Found the Goal!")
            print("The path is: ", paths[0])

        # EXECUTE THE PATH!
        # ....
        input("Waiting for return!")


#STARTING THE PROGRAM:
def main():
    print("Starting client!")
    ag = Agent()
    if ag.getState() != -1:
        ag.run()


main()
