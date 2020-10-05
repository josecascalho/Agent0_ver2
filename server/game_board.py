import tkinter as tk
import random
from PIL import Image
#from PIL import ImageTk
import time
import sys
#------------------------------------------------------------
# CLASS OBJECT:
#------------------------------------------------------------
class Object():
    """Every object in the world is an object.

    Different types of objects are special objects with specific attributes. This
    is the general object.

    """
    def __init__(self,imageDir,name,imageFile,type,x,y,dir,eyes_open=False,width=0,heigh=0):
        self.name = name
        self.x = x
        self.y = y
        self.home=(x,y) #by default
        self.width = width
        self.heigh = heigh
        self.direction =dir
        self.type = type
        self.imageDir = imageDir
        self.imagefile = imageFile
        self.set_image(type,imageFile,width,heigh)
        self.eyes_open = eyes_open
        self.view={}
        self.view_type = ''
        self.weight = 0.0
        self.steps_view = False
    def get_weight(self):
        return self.weight
    def is_eyes_open(self):
        return self.eyes_open
    def open_eyes(self):
        self.eyes_open = True
    def close_eyes(self):
        self.eyes_open = False

    def set_image(self,type,imageFile,width,heigh):
        if type == 'bitmap':
            self.image = self.set_bitmapimage(self.imageDir + imageFile + "_" + self.direction + ".xbm")
        else:
            self.image = self.set_photoimage(self.imageDir +imageFile + "_" + self.direction + ".png", width, heigh)

    def __del__(self):
        print('object {}" deleted'.format(self.name))

    def get_name(self):
        return self.name
    def set_home(self,home):
        self.home=home
    def get_home(self):
        return self.home

    def get_stepsview(self):
        return self.steps_view
    def set_stepsview(self):
        self.steps_view = True
    def reset_stepsview(self):
        self.steps_view = False



    def set_position(self, x, y):
        self.x = x
        self.y = y
    def get_y(self):
        return self.y
    def get_x(self):
        return self.x
    def set_y(self, y):
        self.y = y
    def set_x(self, x):
        self.x = x

    def set_direction(self, dir):
        '''dir can be north (up), south(down), east(right), west(left)'''
        self.direction = dir
        self.set_image(self.type,self.imagefile, self.width, self.heigh)

    def get_direction(self):
        return self.direction

    def set_photoimage(self, imageFile, width, height):
        im = Image.open(imageFile)
        im.thumbnail((width,height))
        photo = ImageTk.PhotoImage(im)
        return photo


    def set_bitmapimage(self, imageFile):
        bitmap = tk.BitmapImage(file=imageFile)
        return bitmap

    def get_image(self):
        return self.image

    def get_canvasimage(self):
        return self.canvasimage

    def set_canvasimage(self, canvasimage):
        self.canvasimage = canvasimage

    def get_worldview(self):
        return self.view


    def set_worldview(self, front='', north='', east='', south='', west=''):
        if self.view_type == "front":
            self.view={"front":front}
        elif self.view == "around":
            self.view={"north":north,east:"east","south":south,"west":west}
        else:
            set.view={}

    def get_typeview(self):
        return self.view_type


#------------------------------------------------------------
# CLASS PLAYER:
#------------------------------------------------------------
class Player(Object):
    def __init__(self,imageDir,name,x,y,dir,view_type,width=0,heigh=0,):
        super().__init__(imageDir,name,"agent1","bitmap",x,y,dir,width,heigh)
        self.view_type = view_type
#------------------------------------------------------------
# CLASS OBSTACLE:
#------------------------------------------------------------
class Obstacle(Object):
    def __init__(self,imageDir,name,x,y,width=0,heigh=0):
        super().__init__(imageDir, name,"obstacle1","bitmap",x,y,"south")
#------------------------------------------------------------
# CLASS BOMB:
#------------------------------------------------------------
class Bomb(Object):
    def __init__(self,imageDir,name,x,y,width=0,heigh=0):
        super().__init__(imageDir, name, "bomb1", "bitmap", x, y, "south")

#------------------------------------------------------------
# CLASS BOMBSOUND:
#------------------------------------------------------------
class BombSound(Object):
    def __init__(self,imageDir,name,x,y,width=0,heigh=0):
        super().__init__(imageDir,name,"bomb_sound1","bitmap",x,y,"south")

#------------------------------------------------------------
# CLASS PATCH:
#------------------------------------------------------------
class Patch(Object):
    def __init__(self,imageDir,name,imageFile,x,y,w,width=0,heigh=0):
        super().__init__(imageDir,name, imageFile, "bitmap",x,y, "south")
        self.weight = w

#------------------------------------------------------------
# CLASS GOAL:
#------------------------------------------------------------
class Goal(Object):
    def __init__(self,directory,name,x,y,width=0,heigh=0):
        super().__init__(directory,name,"goal","bitmap",x,y,"south")

#------------------------------------------------------------
# CLASS GAMEBOARD:
#------------------------------------------------------------
class GameBoard(tk.Frame):

    def __init__(self, parent, columns=16,rows=16, size=64, color1="white", color2="grey"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color1
        self.objects = []
        self.parent = parent
        canvas_width = columns * size
        canvas_height = rows * size
        #compreension of the matrix
        self.rectangles=[[0 for x in range(columns)] for x in range(rows)]
        self.weightpattern = [[0 for x in range(columns)] for x in range(rows)]
        tk.Frame.__init__(self, parent)
        self.quitButton = tk.Button(self,text='Quit',command=self.quit)
        self.quitButton.pack(side="bottom", fill="both", expand=False)
        self.startButton = tk.Button(self,text='Start',command=self.start)
        self.startButton.pack(side="top", fill="both", expand=False)

        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)

#        self.quitButton.configure(width=10, activebackground="grey")
#        self.qB_window = self.canvas.create_window(10, 10, window=self.quitButton)



    def quit(self):
        """ handle button click event and output text from entry area"""
        print('quiting!')  # do here whatever you want
        self.parent.destroy()
        sys.exit()

    def start(self):
        pass

    #------------------------------------------------
    # GET_MAXCOORD
    #------------------------------------------------

    def get_maxcoord(self):
        """Get the maximum values of the  coordinates from the actual world"""
        #test
        #print("Coordinates:",(self.columns,self.rows))
        return (self.columns,self.rows)

    #------------------------------------------------
    # PRINT_STEP:
    #------------------------------------------------
    def print_step(self,object,x,y):
        """Set the step of the object, giving the color yellow to the patch"""
        self.canvas.itemconfig(self.rectangles[object.get_x()][object.get_y()], fill='yellow')
    #------------------------------------------------
    # SET_STEPS_VIEW:
    #------------------------------------------------
    def set_stepsview(self, object):
        object.set_stepsview()
        return True

    def reset_stepsview(self, object):
        object.reset_stepsview()
        self.clean_board()
        return False
    #------------------------------------------------
    # REMOVE_VIEWSCREEN
    #------------------------------------------------
    def remove_viewscreen(self, object, x, y):
        """Remove the identification on screen (color) of the patches an object sees"""
        if object.get_typeview() == "front":
            if self.canvas.itemcget(self.rectangles[x][y],"fill") == "red":
                self.canvas.itemconfig(self.rectangles[x][y], fill=self.color1)
        elif object.get_typeview()== "around":
            pass
    #------------------------------------------------
    # SET_VIEWSCREEN:
    #------------------------------------------------
    def set_viewscreen(self, object, x, y):
        """Set the identification on screen (color) of the patches an object sees"""
        if object.get_typeview() == "front":
            if self.canvas.itemcget(self.rectangles[x][y],"fill") == "red":
                self.canvas.itemconfig(self.rectangles[x][y], fill=self.color1)
            else:
                self.canvas.itemconfig(self.rectangles[x][y], fill='red')
        elif object.get_typeview()== "around":
            pass

    #------------------------------------------------
    # CLEAN_BOARD:
    #------------------------------------------------
    def clean_board(self):
        """Clean the board, removing all the colour to the patches"""
        for x in range(self.rows):
            for y in range(self.columns):
                if self.canvas.itemcget(self.rectangles[x][y], "fill") == "yellow":
                    self.canvas.itemconfig(self.rectangles[x][y], fill=self.color1)
        return True
    #------------------------------------------------
    # PLACE:
    # ------------------------------------------------
    def place(self,object,x, y):
        """Place object at x y"""

        #Clean before moving
        if object.is_eyes_open() == True:
            self.remove_viewscreen(object, x, y)
        object.set_position(x, y)
        x0 = (x * self.size) + int(self.size / 2)
        y0 = (y * self.size) + int(self.size / 2)
        self.canvas.coords(object.get_name(), x0, y0)
        #Print object's view on screen after moving
        if object.is_eyes_open() == True:
            (newx,newy)=self.getplaceahead(object)
            self.set_viewscreen(object, newx, newy)
    #------------------------------------------------
    # ADD
    #------------------------------------------------

    def add(self, object, x=0, y=0):
        '''Add object to the playing board'''
        #print("Adding object",object,"in position x y", x, y)
        canvas_image = self.canvas.create_image(x, y, image=object.get_image(), tags=(object.get_name(), "piece"), anchor="c")
        object.set_canvasimage(canvas_image)
        self.place(object, x, y)
        self.objects.append(object)

    #------------------------------------------------
    # REMOVE:
    #------------------------------------------------

    def remove(self, object):
        #del self.pieces[object.name]
        self.canvas.delete(object.get_name())
        self.objects.remove(object)
        del object
        #self.moving_refresh()

    #------------------------------------------------
    # CHANGEPOSITION:
    #------------------------------------------------

    def change_x(self,x):
        if x >= self.columns:
            x = 0
        if x < 0:
            x = self.columns-1
        return x
    def change_y(self,y):
        if y >= self.rows:
            y = 0
        if y < 0:
            y = self.rows-1
        return y

    def change_position(self, object, x, y):
        if object.get_stepsview() == True:
            self.print_step(object,x,y)
        x = self.change_x(x)
        y = self.change_y(y)
        self.place(object,x, y)
        return (x,y)
    #------------------------------------------------
    # TURN north, south, east, west (absolute turn)
    #------------------------------------------------

    def turn_north(self,object):
        (nx,ny)=self.getplaceahead(object)
        self.remove_viewscreen(object, nx, ny)
        object.set_direction("north")
        self.canvas.itemconfig(object.get_canvasimage(), image=object.get_image())
        self.place(object, object.get_x(), object.get_y())
        return  "north"
    def turn_south(self,object):
        (nx,ny)=self.getplaceahead(object)
        self.remove_viewscreen(object, nx, ny)
        object.set_direction("south")
        self.canvas.itemconfig(object.get_canvasimage(), image=object.get_image())
        self.place(object, object.get_x(), object.get_y())
        return "south"
    def turn_east(self,object):
        (nx,ny)=self.getplaceahead(object)
        self.remove_viewscreen(object, nx, ny)
        object.set_direction("east")
        self.canvas.itemconfig(object.get_canvasimage(), image=object.get_image())
        self.place(object, object.get_x(), object.get_y())
        return "east"
    def turn_west(self,object):
        (nx,ny)=self.getplaceahead(object)
        self.remove_viewscreen(object, nx, ny)
        object.set_direction("west")
        self.canvas.itemconfig(object.get_canvasimage(), image=object.get_image())
        self.place(object, object.get_x(), object.get_y())
        return "west"
    #------------------------------------------------
    # TURN left, right (relative turn)
    #------------------------------------------------

    def turn_left(self,object):
        (nx,ny)=self.getplaceahead(object)
        self.remove_viewscreen(object, nx, ny)
        if object.get_direction() == "north":
            res = self.turn_west(object)
        elif object.get_direction()== "south":
            res = self.turn_east(object)
        elif object.get_direction()== "west":
            res = self.turn_south(object)
        else:
            res = self.turn_north(object)
        return res

    def turn_right(self,object):
        (nx,ny)=self.getplaceahead(object)
        self.remove_viewscreen(object, nx, ny)
        if object.get_direction() == "north":
            res = self.turn_east(object)
        elif object.get_direction()== "south":
            res = self.turn_west(object)
        elif object.get_direction()== "west":
            res = self.turn_north(object)
        else:
            res = self.turn_south(object)
        return res
    #------------------------------------------------
    # MOVE (forward and backward*)
    # * backward not yet implemented
    # Find the coordinates to move. The movement is done
    # after testing obstacles in the function which calls this one
    #------------------------------------------------
    def move_north(self,object,movement):
        if movement =="forward":
            x = object.get_x()
            y = object.get_y() - 1
        elif movement == "backward":
            x = object.get_x()
            y = object.get_y() + 1
#        self.change_position(object, x, y)
        return (x,y)
    def move_south(self,object,movement):
        if movement =="forward":
            x = object.get_x()
            y = object.get_y() + 1
        elif movement == "backward":
            x = object.get_x()
            y = object.get_y() - 1
#       self.change_position(object, x, y)
        return (x,y)
    def move_east(self,object,movement):
        if movement =="forward":
            x = object.get_x() + 1
            y = object.get_y()
        elif movement == "backward":
            x = object.get_x() - 1
            y = object.get_y()
 #       self.change_position(object, x, y)
        return (x,y)
    def move_west(self,object,movement):
        if movement =="forward":
            x = object.get_x() - 1
            y = object.get_y()
        elif movement =="backward":
            x = object.get_x() + 1
            y = object.get_y()
#        self.change_position(object, x, y)
        return (x,y)

    def move_idle(self,object,movement):
        x = object.get_x()
        y = object.get_y()
        return (x,y)

    def is_target_obstacle(self,coordinates):
        """Test if in the coordinates there is an obstacle"""
        for obj in self.objects:
            if isinstance(obj, Obstacle):
                if obj.get_x() == coordinates[0] and obj.get_y() == coordinates[1]:
                    return True
        return False

    def move(self,object,movement):
        """Moves to direction selected but only if there is no obstacle!"""
        if object.get_direction()== "north":
            res = self.move_north(object,movement)
            if not self.is_target_obstacle(res):
                self.change_position(object, res[0], res[1])

        elif object.get_direction()== "south":
            res = self.move_south(object,movement)
            if not self.is_target_obstacle(res):
                self.change_position(object, res[0], res[1])

        elif object.get_direction()== "east":
            res = self.move_east(object,movement)
            if not self.is_target_obstacle(res):
                self.change_position(object, res[0], res[1])

        elif object.get_direction()== "west":
            res = self.move_west(object,movement)
            if not self.is_target_obstacle(res):
                self.change_position(object, res[0], res[1])
        else:
            res = self.move_idle(object,movement)
        return res

    #------------------------------------------------
    # MOVE_HOME ()
    #------------------------------------------------
    def move_home(self,object):
        home = object.get_home()
        self.place(object,home[0],home[1])
    #------------------------------------------------
    # GETPLACEAHEAD (return coordinates of place ahead)
    #------------------------------------------------
    def getplaceahead(self,object):
        '''Preview position ahead of the object'''
        if object.get_direction()== "north":
                return (object.get_x(), self.change_y(object.get_y() - 1))

        elif object.get_direction()== "south":
                return (object.get_x(), self.change_y(object.get_y() + 1))

        elif object.get_direction()== "east":
                return (self.change_x(object.get_x() + 1), object.get_y())
        elif object.get_direction()== "west":
                return (self.change_x(object.get_x() - 1), object.get_y())
        else:
                return (object.get_x(), object.get_y())


    def getplacedir(self,object,direction):
        '''Preview position in direction'''
        if direction== "north":
                return (object.get_x(), self.change_y(object.get_y() - 1))

        elif direction== "south":
                return (object.get_x(), self.change_y(object.get_y() + 1))

        elif direction== "east":
                return (self.change_x(object.get_x() + 1), object.get_y())
        elif direction== "west":
                return (self.change_x(object.get_x() - 1), object.get_y())
        else:
                return (object.get_x(), object.get_y())

    #------------------------------------------------
    # GETGOALPOSITION (return the position of the goal)
    #------------------------------------------------
    def getgoalposition(self, object):
        for ag in self.objects:
            if isinstance(ag,Goal):
                return (ag.get_x(), ag.get_y())
        return None

    #------------------------------------------------
    # VIEW OBJECTS (return objects ahead)
    #------------------------------------------------

    def view_object(self,object,coordinates):
        """Return the type of object in the position given by 'coordinates'"""
        res=[]
        #front = self.getplaceahead(object)
        for ag in self.objects:
            if (ag.get_x() == coordinates[0] and ag.get_y() == coordinates[1]):
                print('There is something in postion:',coordinates)
                if isinstance(ag,Player):
                    res.append('player')
                elif isinstance(ag,Bomb):
                    res.append('bomb')
                elif isinstance(ag,BombSound):
                    res.append('bomb_sound')
                elif isinstance(ag,Obstacle):
                    res.append('obstacle')
                elif isinstance(ag,Goal):
                    res.append('goal')
                else:
                    res.append('unkown')
        else:
            pass
        return res

    def view_weights(self,object,view):
        if view =="front":
            front = self.getplaceahead(object)
            for ag in self.objects:
                if isinstance(ag,Patch):
                    if ag.get_x() == front[0] and ag.get_y() == front[1]:
                        print("Found weights! x=",front[0]," y=",front[1]," weight=",ag.get_weight())
                        return ag.get_weight()
            return 0.0
        else:
            return 0.0

    def view_global_weights(self,object):
        weights =[[0 for x in range(self.columns)] for x in range(self.rows)]
        for ag in self.objects:
            if isinstance(ag,Patch):
                weights[ag.get_x()][ag.get_y()]=ag.get_weight()
        return weights

    def view_obstacles(self, object):
        obstacles = [[0 for x in range(self.columns)] for x in range(self.rows)]
        for ag in self.objects:
            if isinstance(ag, Obstacle):
                obstacles[ag.get_x()][ag.get_y()] = 1
        return obstacles


    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width - 1) / self.columns)
        ysize = int((event.height - 1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.rectangles[col][row] = self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for object in self.objects:
            print(object.get_name())
            self.place(object, object.get_x(), object.get_y())
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")




