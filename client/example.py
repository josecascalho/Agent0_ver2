import client
import ast
import random
c = client.Client('127.0.0.1', 50000)
res = c.connect()
random.seed() #To become true random, a different seed is used! (clock time)

#Exemplo 1:
if res != -1:
    while True:
        msg = c.execute("info","view")
        objects = ast.literal_eval(msg)
        if objects[0]=='obstacle' or objects[0]=='bomb':
            c.execute("command","left")
        else:
            res = random.randint(0,4)
            if res <= 3:
                c.execute("command", "forward")
            else:
                c.execute("command","right")

#Exemplo 2:
if res != -1:
    while True:
        msg = c.execute("info","view")
        objects = ast.literal_eval(msg)
        if objects[0]=='obstacle' or objects[0]=='bomb':
            c.execute("command","left")
        else:
            res = random.randint(0,4)
            if res <= 3:
                c.execute("command", "forward")
            else:
                c.execute("command","right")


