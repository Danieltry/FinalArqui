#Matrix libraries
#from pynput.Keyboard import Listener}

import RPi.GPIO as GPIO
from luma.core.interface.serial import noop, spi
from luma.core.render import canvas
from luma.led_matrix.device import max7219
import time as tp
import random
from time import time

pin_btn_1 = 17
pin_btn_2 = 27
pin_btn_3 = 22
pin_btn_4 = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_btn_1, GPIO.IN)
GPIO.setup(pin_btn_2, GPIO.IN)
GPIO.setup(pin_btn_3, GPIO.IN)
GPIO.setup(pin_btn_4, GPIO.IN)
GPIO.add_event_detect(pin_btn_1, GPIO.BOTH)
GPIO.add_event_detect(pin_btn_2, GPIO.BOTH)
GPIO.add_event_detect(pin_btn_3, GPIO.BOTH)
GPIO.add_event_detect(pin_btn_4, GPIO.BOTH)

def main():
    matrix = Matrix()
    z = True
    varx = 4
    vary = 7
    matrix.draw_point(varx,vary)
    start_time = time()
    start_time_disp_propio = time()-3
    start_time_disp_enemigo = time - 3
    start_time_disp = [0,0,0,0]
    start_time_disp_propio_2 = 0
    disp_libre = 0
    disp_player = 0
    disparosx = [-1,-1,-1,-1]
    disparosy = [-1, -1, -1, -1]
    disparo_propio_x = -1
    disparo_propio_y = -1
    d_libre = [0,0,0,0]
    enemigos = [[1,0,1,0,1,0,1,0],[0,1,0,1,0,1,0,1]]
    puntos = 0
    vidas = [1,1,1]
    time_ini = time()
    time_ini_2 = time()

    while z:
        ctt = 0
        for in range(0,4):
            ctt = ctt +d_libre[i]+disp_player
        enemigos_disp_x = []
        enemigos_disp_y = []

        for i in range(0,2):
            for j in range(0,8):
                if(enemigos[i][j] == 1):
                    matrix.draw_point(j,i)
                    enemigos_disp_x.append(j)
                    enemigos_disp_y.append(i)
                    if (disparo_propio_y == i and disparo_propio_x == j):
                        enemigos[i][j] = 0
                        disparo_propio_x = -1
                        disparo_propio_y = -1
                        disp_player = disp_player-1
                        disp_libre = 0
                        puntos = puntos + 1
        time_dif = time()-start_time
        if (time_dif>=5):
            move_enemy(enemigos)
            start_time = time()

        time_dif_2 = time()-start_time_disp_enemigo

        if (time_dif_2 >=2):
            start_time_disp_enemigo = time()
            if(disp_player == 0):
                n=random.randint(0,len(enemigos_disp_x))
                pos_esc.append(l)
                for i in range (0,len(pos_esc)):
                    if(pos_esc[i] == l):
                        cont+=1
                if(cont<2):
                    k+=1
                elif(len(pos_esc)!=0)):
                    pos_esc.pop()

            else:
                n = random.randint(3,4)
                pos_esc=[]
                k=0
                while(k<n):
                    cont = 0
                    l = random.randint(0,len(enemigos_disp_x)-1)
                    pos_esc.append(l)
                    for i in range(0,len(pos_esc)):
                        if(pos_esc[i] == l):
                            cont+=1
                    if (cont<2):
                        k+=1
                    elif(len(pos_esc)!=0):
                        pos_esc.pop()

            for i in range(0,len(pos_esc)):
                rep = False
                for j in range(0,4):
                    if(d_libre[j] == 0 and rep = False):
                        g = pos_esc[i] - 1
                        disparosx[j] = enemigos_disp_x[g]
                        disparosy[j] = enemigos_disp_y[g]+1
                        d_libre[j] = 1
                        start_time_disp[j] = time()
                        rep = TimeoutError

        for i in range(0,4):
            ctt = ctt + d_libre[i]+disp_player

        matrix.draw_point(varx,vary)
        time_dif = time()-start_time
        varx = move_player_left(varx,vary,matrix)
        varx = move_player_right(varx,vary,matrix)

        for i in range(0,4):
            ctt = ctt+ d_libre[i] + disp_player

        dx,dy,ct,end = shoot(varx, vary, start_time_disp_propio)
        start_time_disp_propio = end
        if (ct == 1):
            disp_player = 1
            disparo_propio_x = dx
            disparo_propio_y = dy
            start_time_disp_propio_2 = time()

        matrix.draw_point(disparo_propio_x,disparo_propio_y)

        for i in range(0,4):
            matrix.draw_point(disparosx[i],disparosy[i])
            if(disparo_propio_y>=-1):
                if(disparo_propio_y == -1):
                    disp_player = disp_player-1
                    disparo_propio_x = -1
                    disparo_propio_y = -1

                if(time()-start_time_disp_propio_2>=0,25):
                    disparo_propio_y = disparo_propio_y-1
                    start_time_disp_propio_2 = time()

            if(disparosy[i]<=7):
                if(disparosy[i] == 7):
                    d_libre[i] = 0
                    disparosx[i] = -1
                    disparosy[i] = -1
                 if(time()-start_time_disp[i]>=0.25):
                     disparosy[i] = disparosy[i]+1

                     ##############################################3
                     start_time_disp[i] == time()
            if (disparosx[i] == varx and disparosy[i] == vary):
                if (vidas != []):
                    vidas.pop()
                    time_ini = time()
                else:
                    end_game(matrix)

            if (time() - time_ini <= 1):
                for i in range(0, len(vidas)):
                    matrix.draw_point(7, 4 + i)

            if (time_ini + 5 <= time()):
                time_ini = time()
            if (puntos == 5):
                win_game(matrix)

def move_player_left(varx, vary, matrix)
    if (GPIO.event_detected(pin_btn_1) == 1 and GPIO.input(pin_btn_1) == GPIO.HIGH):
        if (varx == 0):
            varx = 7
        else:
            varx = varx - 1
        matrix.draw_point(varx, vary)
    return varx

def move_player_right(varx, vary, matrix)
    if (GPIO.event_detected(pin_btn_2) == 1 and GPIO.input(pin_btn_2) == GPIO.HIGH):
        if (varx == 7):
            varx = 0
        else:
            varx = varx + 1
        matrix.draw_point(varx, vary)
    return varx

def move_enemy(enemigos):
    for i in range(0, 2):
        for j in range(0, 8):
            enemigos[i][j] = random.radint(0, 1)
    return enemigos

def shoot(varx, vary, start):
    varx_aux = -1
    vary_aux = -1
    cont = 0
    dif = time() - start
    end_time = start
    if (GPIO.event_detected(pin_btn_3) == 1 an GPIO.input(pin_btn_3) == GPIO.HIGH)
        varx_aux = varx
        vary_aux = 6
        cont = 1
        end_time = time()

                return varx_aux, vary_aux, cont, end_time

def win_game(matrix):
    f = True
        while (f):
            P[[0,0,1,1,1,1,1,1],[0,0,1,1,1,1,1,1],[0,0,1,1,1,1,1,1],[0,0,1,1,1,1,1,1],[0,0,1,1,1,1,1,1],[0,0,1,1,1,1,1,1],[0,0,1,1,1,1,1,1],[0,0,1,1,1,1,1,1]]
            P=transpose(p)
            for i in range (0,8):
                for j in range (0,8):
                    if (P[i][j]==1):
                        matrix.draw_point(i,j)
            start()
def end_game(matrix):
    f = True
        while (f):
            P[[0,0,1,1,1,1,1,1],[0,0,1,1,1,1,1,1],[0,0,1,1,1,1,1,1],[0,0,1,1,1,1,1,1],[0,0,1,1,1,1,1,1],[0,0,1,1,1,1,1,1],[0,0,1,1,1,1,1,1],[0,0,1,1,1,1,1,1]]
            P=transpose(p)
            for i in range (0,8):
                for j in range (0,8):
                    if (P[i][j]==1):
                        matrix.draw_point(i,j)
            start()

def transpose(matrix):
    if matrix == None of len(matrix) == 0:
        return []
    result = [[None for i in range(len(matrix))] for j in range (len(matrix[0]))]
    for i in range(len(matrix[0])):
        for j in range (len(matrix)):
            result[i][j]=matrix[j][i]
    return result

def start ():
    if (GPIO.event_detected(pin_btn_4)==1 and GPIO.input(pin_btn_4)==GPIO.HIGH):
        main()
    return None







