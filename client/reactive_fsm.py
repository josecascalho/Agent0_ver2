import client
import ast
import random

#FSM STATES
PESQUISA  = 0
ULTRAPASSA_OBST_ESQ = 1
ULTRAPASSA_OBST_DIR = 2
PARAR = 3

class ReactiveFSM:
    def __init__(self,address,port):
        self.state = PESQUISA
        self.c = client.Client(address, port)
        self.res = self.c.connect()
        random.seed()  # To become true random, a different seed is used! (clock time)
        self.objects =[]
        self.end = False
    def getConnectionState(self):
        return self.res

    def pesquisa_exe(self):
        self.c.execute("command","forward")
    def pesquisa_exit(self):
        msg = self.c.execute("info", "view")
        self.objects = ast.literal_eval(msg)

        if self.objects[0] == 'goal':
            self.state = PARAR
        elif self.objects[0] == 'obstacle' or self.objects[0] == 'bomb':
            self.state = ULTRAPASSA_OBST_ESQ
        # Continua no mesmo estado ou salta para estado com obst imaginario na esquerda
        else:
            res = random.randint(0, 4)
            if res >= 3:
                self.state = ULTRAPASSA_OBST_ESQ

    def ultrapassa_obst_esq_exe(self):
        self.c.execute("command","left")

    def ultrapassa_obst_esq_exit(self):
        msg = self.c.execute("info", "view")
        self.objects = ast.literal_eval(msg)
        if self.objects[0] == 'goal':
            self.state = PARAR
        elif self.objects[0] !='obstacle' and self.objects[0] != 'bomb':
            self.state = PESQUISA
        else:
            self.state = ULTRAPASSA_OBST_DIR

    def ultrapassa_obst_dir_exe(self):
        self.c.execute("command" , "right")


    def ultrapassa_obst_dir_exit(self):
        msg = self.c.execute("info", "view")
        self.objects = ast.literal_eval(msg)
        if self.objects[0] !='obstacle' and self.objects[0] != 'bomb':
            self.state = PESQUISA
        elif  self.objects[0]=='goal':
            self.state = PARAR


    def parar_exe(self):
        self.c.execute("command","forward")
        print("Atingi a Goal!")
        self.c.sleeping(2)


    def parar_exit(self):
        self.end = True


    def run(self):
        while self.end == False:
            msg = self.c.execute("info","view")
            objects = ast.literal_eval(msg)
            if self.state == PESQUISA:
                self.pesquisa_exe()
                self.pesquisa_exit()

            elif self.state == ULTRAPASSA_OBST_ESQ:
                self.ultrapassa_obst_esq_exe()
                self.ultrapassa_obst_esq_exit()

            elif self.state == ULTRAPASSA_OBST_DIR:
                self.ultrapassa_obst_dir_exe()
                self.ultrapassa_obst_dir_exit()
            elif self.state == PARAR:
                self.parar_exe()
                self.parar_exit()


def main():
    ag = ReactiveFSM('127.0.0.1', 50001)
    if ag.getConnectionState() != -1:
        ag.run();


main()
