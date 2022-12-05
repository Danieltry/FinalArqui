# Matrix libraries
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi,noop
from luma.core.render import canvas
from luma.core.legacy import text

import threading
import time
import numpy as np
import random

import RPi.GPIO as GPIO

pinL=2
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinL,GPIO.IN,pull_up_down=GPIO.PUD_UP)

previous_button_stateL=GPIO.input(pinL)

pinR=3
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinR,GPIO.IN,pull_up_down=GPIO.PUD_UP)

previous_button_stateR=GPIO.input(pinR)

pinD=4
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinD,GPIO.IN,pull_up_down=GPIO.PUD_UP)

previous_button_stateD=GPIO.input(pinD)

serial=spi(port=0,device=0)
device=max7219(serial)

N = 8
n_balas = 0
choque = False
viedas=3

mat_enemigos = np.zeros((N, N), dtype='int32')
mat_enemigos[N-1, :] = np.random.randint(0, 2, size=N)
mat_enemigos[N-2, :] = np.random.randint(0, 2, size=N)
temp_enemigos = mat_enemigos

mat_jugador = np.zeros((N, N), dtype='int32')
mat_jugador[0, 4] = 1
temp_jugador = mat_jugador

mat_balasJ = np.zeros((N, N), dtype='int32')
temp_balasJ = np.zeros((N, N), dtype='int32')
mat_balasE = np.zeros((N, N), dtype='int32')
temp_balasE = np.zeros((N, N), dtype='int32')

mat_juego = (mat_balasJ ^ mat_enemigos) | mat_balasE | mat_balasJ | mat_jugador

def shiftMtx(mat, dir):
    tempMat = np.zeros((N, N), dtype='int32')
    for i in range(len(mat)):
        if dir == 'up':
            if i < N - 1:
                tempMat[i + 1, :] = mat[i, :]
        elif dir == 'down':
            if i > 0:
                tempMat[i - 1, :] = mat[i, :]
    return tempMat
#jugador con bala
def evaluarChoques():
    global mat_juego, mat_jugador, mat_enemigos, mat_balasJ, mat_balasE, viedas, choque
    temp_enemigos = mat_enemigos
    temp_balasJ = mat_balasJ
    mat_enemigos = ( temp_enemigos ^ temp_balasJ ) & temp_enemigos
    mat_balasJ = ( temp_enemigos ^ temp_balasJ ) & mat_balasJ

    temp_jugador = mat_jugador
    temp_balasE = mat_balasE

    if np.sum( temp_jugador & temp_balasE) == 1:
        choque = True
        viedas=viedas-1

        

def imprimirMatriz():
    global n_fig, matrix, choque, viedas
    while(True):
        if choque==False:
            time.sleep(0.01)

            evaluarChoques()
            mat_juego = mat_enemigos | mat_balasE | mat_balasJ | mat_jugador

            for i in range(N):
                for j in range(N):
                    if mat_juego[i, j] == 1:
                        matrix.draw_point(i,j)
        else:
            if viedas>0:
                msg=str(viedas)
                with canvas(device) as draw:
                    text(draw, (0, 0), msg, fill="white")
                time.sleep(1)
                choque=False

            else:
                msg=str(viedas)
                with canvas(device) as draw:
                    text(draw, (0, 0), msg, fill="white")
                time.sleep(1)    
                matrix.draw_point(3, 3)
                exit()
                


def dispararE():
    global n_balas, mat_balasE, mat_balasJ, mat_enemigos
    while(True):
        n_balas = np.sum(mat_balasJ) + np.sum(mat_balasE)
        while n_balas < 3:
            n_balas = np.sum(mat_balasJ) + np.sum(mat_balasE)
            ii = np.random.randint(N-2, N)
            ind = np.where(mat_enemigos[ii] == 1)
            if len(ind[0]) != 0:
                jj = random.choice(ind[0])
                if (mat_enemigos[ii, jj] == 1) and (mat_enemigos[ii-1, jj] == 0):
                    mat_balasE[ii-1, jj] = 1
        time.sleep(2)

def moverBalas():
    global mat_balasJ, mat_balasE
    while(True):
        if choque==False:
            time.sleep(0.5)
            temp_balasJ = mat_balasJ
            temp_balasE = mat_balasE
            mat_balasJ = shiftMtx(temp_balasJ, 'up')
            mat_balasE = shiftMtx(temp_balasE, 'down')

def cambiarPatronE():
    global mat_enemigos
    while(True):
        if choque==False:
            time.sleep(5)
            mat_enemigos[N-1, :] = np.random.randint(0, 2, size=N)
            mat_enemigos[N-2, :] = np.random.randint(0, 2, size=N)

def moverJLeft():
    global mat_jugador, mat_balasJ, n_balas, previous_button_stateL
    
    while(True):
        j=np.where(mat_jugador[0,:]==1)[0]
        time.sleep(0.01)
        button_state=GPIO.input(pinL)
        if button_state != previous_button_stateL:
            previous_button_stateL=button_state
            if button_state==GPIO.HIGH:
                if j != 0:
                    mat_jugador = np.roll(mat_jugador, -1, axis=1)

def moverJRight():
    global mat_jugador, mat_balasJ, n_balas, previous_button_stateR
   
    while True:
        j=np.where(mat_jugador[0,:]==1)[0]
        time.sleep(0.01)
        button_state=GPIO.input(pinR)
        if button_state != previous_button_stateR:
            previous_button_stateR=button_state
            if button_state==GPIO.HIGH:
                if j != 7:
                    mat_jugador = np.roll(mat_jugador, 1, axis=1)

def disparoJ():
    global mat_jugador, mat_balasJ, n_balas, previous_button_stateD
    j=np.where(mat_jugador[0,:]==1)[0]
    while True:
        time.sleep(0.01)
        button_state=GPIO.input(pinD)
        if button_state != previous_button_stateD:
            previous_button_stateD=button_state
            if button_state==GPIO.HIGH:
                if n_balas < 5:
                    temp_balasJ = mat_balasJ
                    temp_jugador = shiftMtx(mat_jugador, 'up')
                    mat_balasJ = temp_balasJ | temp_jugador
                    time.sleep(2)

class Matrix(object):
    def __init__(self):
        super(Matrix, self).__init__()
        self.device = self.create_matrix_device(1, 0, 0)

    def create_matrix_device(self, n, block_orientation, rotate):
        # Create matrix device
        print("Creating device...")
        serial = spi(port=0, device=0, gpio=noop())
        device = max7219(serial, cascaded=n, block_orientation=block_orientation, rotate=rotate)
        print("Device created.")
        return device

    def draw_point(self, x, y):
        with canvas(self.device) as draw:
            draw.point((y,7-x), fill="green")

matrix = Matrix()

t1 = threading.Thread(target=imprimirMatriz)

t3 = threading.Thread(target=cambiarPatronE)
t4 = threading.Thread(target=moverBalas)
t5 = threading.Thread(target=dispararE)
t1.start()

t3.start()
t4.start()
t5.start()


t7 = threading.Thread(target=moverJLeft)
t7.start()

t8 = threading.Thread(target=moverJRight)
t8.start()

t9 = threading.Thread(target=disparoJ)
t9.start()

