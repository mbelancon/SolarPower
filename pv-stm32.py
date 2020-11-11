from tkinter import *
import time
import numpy as np
import matplotlib.pyplot as plt
import threading
import pandas as pd
import serial

nome='data'
timestamp=time.time()
root = Tk()
root.title("Solar cell power measurement")

l=np.zeros(13)
t=0
h=0
cal=np.array([0,0,0,0])
cal0=0
ser=serial.Serial('/dev/ttyACM0',115200,timeout=20)

def clock():
    global timestamp,t,l
    seconds=time.time()-timestamp
    horas=int(seconds/3600)
    minutos=int(seconds/60-horas*60)
    segundos=int((seconds/60-int(seconds/60))*60)
    tempo.config(text='{:02.0f}'.format(horas)+":"+'{:02.0f}'.format(minutos)+":"+'{:02.0f}'.format(segundos))
    tempo.after(1000,clock)
    calib.config(text='{:03.1f}'.format(l[0]-cal0))
    v1.config(text='{:04.0f}'.format(l[2]))
    v2.config(text='{:04.0f}'.format(l[4]))
    v3.config(text='{:04.0f}'.format(l[6]))
    v4.config(text='{:04.0f}'.format(l[8]))
    a1.config(text='{:04.0f}'.format(l[1]))
    a2.config(text='{:04.0f}'.format(l[3]))
    a3.config(text='{:04.0f}'.format(l[5]))
    a4.config(text='{:04.0f}'.format(l[7]))
    p1.config(text='{:05.1f}'.format(l[9]))
    p2.config(text='{:05.1f}'.format(l[10]))
    p3.config(text='{:05.1f}'.format(l[11]))
    p4.config(text='{:05.1f}'.format(l[12]))
    temperatura.config(text=t)
    humidity.config(text=h)
    
def save():
    global pandas,nome
    nome=filename.get()
    pandas.to_csv("~/"+nome+"-PV.csv")

def zerar():
    global timestamp,pandas,leitura
    l=np.zeros(13)
    timestamp=time.time()
    pandas=pd.DataFrame([[pd.Timestamp.now(),t,h,0,0,0,0,0,0,0,0,0,0,0,0]],columns=['datetime','t','rh','v1','a1','p1','v2','a2','p2','v3','a3','p3','v4','a4','p4'])
 
def leserial():
    global pandas,l,t,h,leitura,cal0
    time.sleep(1)
    ser.flush()
    ser.flushInput()
    ser.flushOutput()
    while True:
        if ser.in_waiting>0:
            leitura=np.array(ser.readline().decode().rstrip().split(' ')).astype(float)
            t=0
            h=0
            i=1
            leitura=leitura*0.8056
            if cal[0]==0:
                cal0=leitura[0]
                cal[0]=leitura[1]-leitura[0]
                cal[1]=leitura[3]-leitura[0]
                cal[2]=leitura[5]-leitura[0]
                cal[3]=leitura[7]-leitura[0]
            while i<9:
                l[i]=leitura[i]-leitura[0]
                i+=2
            i=2
            while i<9:
                l[i]=leitura[i]
                i+=2
            l[0]=leitura[0]
            l[1]=(l[1]-cal[0])/0.9
            l[3]=(l[3]-cal[1])/0.9
            l[5]=(l[5]-cal[2])/0.9
            l[7]=(l[7]-cal[3])/0.9
            l[9]=l[1]*l[2]/1000
            l[10]=l[3]*l[4]/1000
            l[11]=l[5]*l[6]/1000
            l[12]=l[7]*l[8]/1000
            pandas=pandas.append(pd.DataFrame([[pd.Timestamp.now(),t,h,l[2],l[1],l[9],l[4],l[3],l[10],l[6],l[5],l[11],l[8],l[7],l[12]]],columns=['datetime','t','rh','v1','a1','p1','v2','a2','p2','v3','a3','p3','v4','a4','p4']),ignore_index=True)
            
def graph():
    fig, ax=plt.subplots()
    p1,=ax.plot(pandas.set_index('datetime')['p1'],label='Cell 1')
    p2,=ax.plot(pandas.set_index('datetime')['p2'], label='Cell 2')
    p3,=ax.plot(pandas.set_index('datetime')['p3'], label='Cell 3')
    p4,=ax.plot(pandas.set_index('datetime')['p4'], label='Cell 4')
    ax.legend()
    ax.set_ylabel('Power (mW)')
    ax.tick_params('x',labelrotation=45)
    plt.tight_layout()
    plt.show()
    
Label(root,text="Temperature (°C)").grid(row=0,column=1)
temperatura=Label(root,text="")
temperatura.grid(row=1,column=1)

Label(root,text="VCC Cal").grid(row=0,column=3)
calib=Label(root,text="")
calib.grid(row=1,column=3)

Label(root,text="RH (%)").grid(row=0,column=2)
humidity=Label(root,text="")
humidity.grid(row=1,column=2)

Label(root,text="Elapsed time").grid(row=0,column=0)
tempo=Label(root,text="",fg="green")
tempo.grid(row=1,column=0)

Label(root,text="Voltage(mV)",fg="blue").grid(row=3,column=1)
Label(root,text="Current(mA)",fg="red").grid(row=3,column=2)
Label(root,text="Power(mW)",fg="red3").grid(row=3,column=3)

Label(root,text="Cell 1:").grid(row=4,column=0)
v1=Label(root,text="0",fg="blue")
v1.grid(row=4,column=1)
a1=Label(root,text="0",fg="red")
a1.grid(row=4,column=2)
p1=Label(root,text="0",fg="red3")
p1.grid(row=4,column=3)

Label(root,text="Cell 2:").grid(row=5,column=0)
v2=Label(root,text="0",fg="blue")
v2.grid(row=5,column=1)
a2=Label(root,text="0",fg="red")
a2.grid(row=5,column=2)
p2=Label(root,text="0",fg="red3")
p2.grid(row=5,column=3)

Label(root,text="Cell 3:").grid(row=6,column=0)
v3=Label(root,text="0",fg="blue")
v3.grid(row=6,column=1)
a3=Label(root,text="0",fg="red")
a3.grid(row=6,column=2)
p3=Label(root,text="0",fg="red3")
p3.grid(row=6,column=3)

Label(root,text="Cell 4:").grid(row=7,column=0)
v4=Label(root,text="0",fg="blue")
v4.grid(row=7,column=1)
a4=Label(root,text="0",fg="red")
a4.grid(row=7,column=2)
p4=Label(root,text="0",fg="red3")
p4.grid(row=7,column=3)

Label(root,text="Insert the filename").grid(row=8,column=1)
Label(root,text="~/").grid(row=9,column=0)

filename=Entry(root,width=20)
filename.grid(row=9,column=1)
filename.insert(0,nome)

Button(root,text="Graph: Power",command=graph).grid(row=10,column=0)

Button(root,text="Save data",command=save).grid(row=10,column=1)

Button(root,text="Restart Measurement",command=zerar).grid(row=10,column=2)

clock()
pandas=pd.DataFrame([[pd.Timestamp.now(),t,h,0,0,0,0,0,0,0,0,0,0,0,0]],columns=['datetime','t','rh','v1','a1','p1','v2','a2','p2','v3','a3','p3','v4','a4','p4'])
t1=threading.Thread(target=leserial)
t1.start()

root.mainloop()
