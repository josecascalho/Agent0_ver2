import socket_server as s
import game_board as gb
import socket
import sys
import random
import tkinter as tk
import time
import traceback

def initialize_obstacles(imageDir,list_obstacles):
    i = 1
    for obst in list_obstacles:
       ob = gb.Obstacle(imageDir,'ob'+str(i), obst[0], obst[1], 'obstacle'+str(i), False)
       board.add(ob, obst[0],obst[1])
       i=i+1

    # ob1 = gb.Obstacle('ob1', 0, 3, 'obstacle1', False)
    # board.add(ob1, 0, 3)
    # ob2 = gb.Obstacle('ob2', 3, 4, 'obstacle1', False)
    # board.add(ob2,3, 4)
    # ob3 = gb.Obstacle('ob3', 2, 2, 'obstacle1', False)
    # board.add(ob3, 2, 2)
    # ob4 = gb.Obstacle('ob4', 5, 3, 'obstacle1', False)
    # board.add(ob4, 5, 3)
    # ob5 = gb.Obstacle('ob5', 1, 5, 'obstacle1', False)
    # board.add(ob5, 1, 5)
    # ob6 = gb.Obstacle('ob6', 6, 6, 'obstacle1', False)
    # board.add(ob6, 6, 6)

def initialize_goal(dirImage,list_goals):
#    goal = gb.Goal('goal1', 10, 12, 'goal', False)
#    board.add(goal, 10, 12)
    for g in list_goals:
        goal = gb.Goal(dirImage,'goal1',g[0],g[1], 'goal', False)
        board.add(goal,g[0],g[1])


def initialize_bomb(dirImage,list_bombs,rows,columns):
    i = 1
    for b in list_bombs:
        bomb = gb.Bomb(dirImage,'bomb'+str(i),b[0],b[1])
        board.add(bomb,b[0],b[1])
        if b[0] >= rows - 1:
            new_b = 0
        else:
            new_b = b[0]+1
        bomb_s = gb.BombSound(dirImage,'bomb_sound_s'+str(i),new_b,b[1])
        board.add(bomb_s,new_b,b[1])
        if b[1] >= columns - 1:
            new_b = 0
        else:
            new_b = b[1]+1
        bomb_s = gb.BombSound(dirImage,'bomb_sound_e'+str(i),b[0],new_b)
        board.add(bomb_s,b[0],new_b)
        if b[0] <= 0:
            new_b = columns - 1
        else:
            new_b = b[0]-1
        bomb_s = gb.BombSound(dirImage,'bomb_sound_n'+str(i),new_b,b[1])
        board.add(bomb_s,new_b,b[1])
        if b[1] <= 0:
            new_b = rows - 1
        else:
            new_b = b[1]-1

        bomb_s = gb.BombSound(dirImage,'bomb_sound_w'+str(i),b[0],new_b)
        board.add(bomb_s, b[0],new_b)
        i = i + 1

def initialize_weights(dirImage,list_weights,rows,columns):
#def initialize_weights(imageDir):
    patch = [[0 for x in range(columns)] for x in range(rows)]
    print(patch)
    weight = 1.0
    name=''
    for column in range(0, columns):
        for row in range(0, rows):
            print("column:", column)
            print("row:",row)
            res = random.uniform(0, 1.0)
            if res <= 0.3:
                name = "patch_clear"
                weight=1.0
            elif res <= 0.5:
                weight = 1.1#2.0
                name = "patch_lighter"
            elif res <= 0.7:
                weight = 1.2 #4.0
                name = "patch_middle"
            elif res <= 1.0:
                weight = 1.3 #8.0
                name = "patch_heavy"
            patch[column][row] = gb.Patch(imageDir,'patch' + str(column) + "-" + str(row), name, column, row, weight, False)
            #print(res)
            board.add(patch[column][row], column, row)
def loop():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        print("Listening...")
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                #                    if not data:
                #                        break

                print(data.decode())
                type, value = data.decode().split()
                res = ""
                if type == 'command':
                    #-----------------------
                    # movements without considering the direction
                    # of the face of the object but testing the objects
                    #-----------------------
                    if   value == 'north':
                        object.close_eyes()
                        res = board.move_north(object,'forward')
                        if not board.is_target_obstacle(res):
                            board.change_position(object, res[0], res[1])

                    elif value == 'south':
                        object.close_eyes()
                        res = board.move_south(object,'forward')
                        if not board.is_target_obstacle(res):
                            board.change_position(object, res[0], res[1])

                    elif value == 'east':
                        object.close_eyes()
                        res = board.move_east(object,'forward')
                        if not board.is_target_obstacle(res):
                            board.change_position(object, res[0], res[1])

                    elif value == 'west':
                        object.close_eyes()
                        res = board.move_west(object,'forward')
                        if not board.is_target_obstacle(res):
                            board.change_position(object, res[0], res[1])

                    #-----------------------
                    # move to home
                    #-----------------------
                    elif value == 'home':
                        res = board.move_home(object)

                    elif value == 'forward':
                        res = board.move(object, 'forward')

                    elif value == 'left':
                        res = board.turn_left(object)

                    elif value == 'right':
                        res = board.turn_right(object)

                    elif value =="set_steps":
                        res=board.set_stepsview(object)

                    elif value =="reset_steps":
                        res=board.reset_stepsview(object)

                    elif value =="open_eyes":
                        res=object.open_eyes()

                    elif value =="close_eyes":
                        res=object.close_eyes()
                    elif value=="clean_board":
                        res = board.clean_board()
                    elif value == "bye" or value =="exit":
                        conn.close()
                        exit(1)
                    else:
                        pass
                elif type == 'info':
                    if value == 'direction':
                        res = object.get_direction()
                    elif value == 'view':
                        front = board.getplaceahead(object)
                        res = board.view_object(object,front)
                    elif value == "weights":
                        res = board.view_weights(object,'front')
                    elif value == 'map':
                        print('Map:',board.view_global_weights(object))
                        res = board.view_global_weights(object)
                    elif value == 'obstacles':
                        print('Obstacles:',board.view_obstacles(object))
                        res = board.view_obstacles(object)
                    elif value =='goal' or value=='target':
                        res = board.getgoalposition(object)
                        #print('Goal:',res)
                    elif value =='position':
                        res = (object.get_x(), object.get_y())
                        #print('Position:', res)
                    elif value=='maxcoord':
                        res = board.get_maxcoord()
                        #print('MaxCoordinates:', res)
                    elif value =='north':
                        #View north
                        front = board.getplacedir(object,'north')
                        res = board.view_object(object,front)
                    elif value =='south':
                        #View north
                        front = board.getplacedir(object,'south')
                        res = board.view_object(object,front)
                    elif value =='east':
                        #View north
                        front = board.getplacedir(object,'east')
                        res = board.view_object(object,front)
                    elif value =='west':
                        #View north
                        front = board.getplacedir(object,'west')
                        res = board.view_object(object,front)

                    else:
                        pass
                if res != '':
                    return_data = str.encode(str(res))
                else:
                    return_data = str.encode("what? commands= <forward,left,right,set_steps,reset_steps, open_eyes, close_eyes> info=<direction,view,weights,map,goal,postion,obstacles,maxcoord>")
                conn.sendall(return_data)
                root.update()

if __name__== "__main__":
    #Host and Port
    if len(sys.argv) == 3:
        host, port = sys.argv[1], int(sys.argv[2])
    else:
        host = '127.0.0.1'
        port = 50000
    # Size of the world ...
    print("Starting the Game Board")
    gameboard_file = '..//input_files/gameboard_file.txt'
    f = open(gameboard_file)
    l = f.readline().split(",")
    columns = int(l[0])
    rows = int(l[1])
    f.close()
    root = tk.Tk()
    images_directory = '../images/'
    board = gb.GameBoard(root,columns,rows)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    # BOARD BOARD:
    # Read from files obstacles ...
    obstacles_file = '..//input_files//obstacles_file.txt'
    f = open(obstacles_file)
    obst_list = []
    for l in f.readlines():
        l = l.split(",")
        if len(l) > 1:
          obst_list.append( (int(l[0]),int(l[1])) )
    initialize_obstacles(images_directory,obst_list)
    #initialize_obstacles(images_directory,[(0,1),(4,6),(7,6),(6,7),(8,8)])
    f.close()
    # Defining the position of the 'goal' ...
    goal_file = '..//input_files//goal_file.txt'
    f = open(goal_file)
    goal_list = []
    for l in f.readlines():
        if len(l) > 1:
          l = l.split(",")
          goal_list.append( (int(l[0]),int(l[1])) )
        #print(goal_list)
    initialize_goal(images_directory,goal_list)
    f.close()
    # Defining the bomb ...
    bomb_file = '..//input_files//bomb_file.txt'
    f = open(bomb_file)
    bomb_list = []
    for l in f.readlines():
        if len(l) > 1:
          l = l.split(",")
          bomb_list.append( (int(l[0]),int(l[1])) )
        #print(bomb_list)
    initialize_bomb(images_directory,bomb_list,rows,columns)
    f.close()
    weight_file = '..//input_files//weight_file.txt'
    f = open(weight_file)
    weight_list = []
    for l in f.readlines():
        if len(l) > 1:
            l = l.split(",")
            weight_list.append((int(l[0]), int(l[1])))
        # print(bomb_list)
    initialize_weights(images_directory, weight_list, rows, columns)
    f.close()
    # Initialize the weights ...
    initialize_weights(images_directory)
    root.update()
    # SERVER SERVER:
    # Starting server ...
    print("Starting the server!")
    server = s.Server()
    # PLAYER PLAYER:
    # Initialize player ...
    object = gb.Player(images_directory,'player', 0, 0, 'south', 'front', True)
    object.set_home((0,0))
    object.close_eyes()
    # Add player ...
    board.add(object, 0, 0)
    root.update()
    # Loop ...
    loop()
