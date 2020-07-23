#############################################################################################################
#   IMPORTING PART
############################################################################################################
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Menu
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk
import os
#helping code for finding python path
#import sys; print(sys.executable)

#Graph plotting
import numpy as np
from numpy import sqrt
import matplotlib.pyplot as plt
import scipy as sp
import math

#csv reading
import csv
from pathlib import Path, PureWindowsPath
import sys

#figure importing
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

#for interpolation
from scipy.interpolate import UnivariateSpline

##############################################################################################

#####################################################################################
#   METHOD PART
##############################################################################
#define postgresql connection

import psycopg2
import os

def connect(): 
    try: 
        conn = psycopg2.connect(database = os.environ.get('DATABASE_NAME'),  
                            user = os.environ.get('DATABASE_USER'),  
                            password = os.environ.get('DATABASE_PASSWORD'),  
                            host = "localhost",  
                            port = "5432") 
        cur = conn.cursor() 
    except (Exception, psycopg2.DatabaseError) as error: 
        print ("Error while creating PostgreSQL table", error) 
    return conn, cur 
#treba dodati FILE_PATH I FILE_NAME
"""def insert_data_first(uid, linecnt, opcnt1, opcnt2, ax, ay, az, hr, hrconf, motstate, measure_flag, fl_name, path_to): 
    conn, cur = connect() 
    try: 
        cur.execute('INSERT INTO measurement(measure_id, user_id, line_number, optical_count1, optical_count2, xax, yax, zax, heart_rate, hrconf, motion_state, measure_flag, file_name, file_path)'
                    +'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                                    (uid, linecnt, opcnt1, opcnt2, ax, ay, az, hr, hrconf, motstate, measure_flag, fl_name, path_to)) 
    except Exception as e: 
        print('error', e)  
    conn.commit() """

def insert_data(uid, linecnt, opcnt1, opcnt2, ax, ay, az, hr, hrconf, motstate, measure_flag, fl_name, path_to): 
    conn, cur = connect() 
    try: 
        cur.execute('INSERT INTO measurement(user_id, line_number, optical_count1, optical_count2, xax, yax, zax, heart_rate, hrconf, motion_state, measure_flag, file_name, file_path)'
                    +'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                                    (uid, linecnt, opcnt1, opcnt2, ax, ay, az, hr, hrconf, motstate, measure_flag, fl_name, path_to)) 
    except Exception as e: 
        print('error', e)  
    conn.commit() 

def measure_id_data(): 
    conn, cur = connect() 
    try: 
        cur.execute('SELECT DISTINCT COUNT(measure_flag) FROM measurement;') 
    except: 
        print('error !')
        print("Result -->", cur.fetchall())
    data = int(len(cur.fetchall())) 
    return data

def get_user_id(usr):
    conn, cur = connect()
    try: 
        cur.execute("SELECT user_id FROM account WHERE username='"+usr+"';") 
    except Exception as e: 
        print('error', e)
        print("Couldnt find user")
    #conn.commit()
    try:
        row = cur.fetchone()
    except:
        print("Couldnt find user")
    if row:
       return str(row[0])
    
def check_if_file_exists(usr):
    conn, cur = connect()
    try: 
        cur.execute("SELECT user_id FROM account WHERE username='"+usr+"';") 
    except Exception as e: 
        print('error', e)
        print("Couldnt find user")
    #conn.commit()
    try:
        row = cur.fetchone()
    except:
        print("Couldnt find user")
    if row:
       return str(row[0])
    
        
#Method for adding file at menu
def addNewFile(path_to, fileCnt, line_count, x1, y1, x2, y2, ax, ay, az, hr, hrconf, motstate, spo2, a, a11, a12, a13, a2, a3, a41, a42, a43, canvas, canvas11, canvas12, canvas13, canvas2, canvas3, canvas41, canvas42, canvas43, usr):
    a.cla()
    a11.cla()
    a12.cla()
    a13.cla()
    a2.cla()
    a3.cla()
    line_count = 0
    x1[:] = []
    y1[:] = []
    x2[:] = []
    y2[:] = []
    ax[:] = []
    ay[:] = []
    az[:] = []
    hr[:] = []
    hrconf[:] = []
    motstate[:] = []
    spo2[:] = []
    file = filedialog.askopenfilename(filetypes = (("Csv files","*.csv"),))
    Upath = Path(file)
    Wpath = PureWindowsPath(Upath)
    path_to = str(Wpath)
    print(path_to)
    clean_data = []
    y3 = []
    fl_name=os.path.basename(path_to)
    fl_name = str(fl_name)
    print(fl_name)
    try:
        with open(path_to) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if line_count > 15:
                    x1.append(line_count)
                    y1.append(int(row[1]))
                    x2.append(line_count)
                    y2.append(int(row[2]))
                    y3.append(int(row[1]) + int(row[2]))
                    info = {'Sample count':line_count, 'Green LED 1':row[1], 'Green LED 2':row[2]}
                    clean_data.append(info)
                    if len(row) == 9:
                        hr.append(int(row[6]))
                        ax.append(float(row[3]))
                        ay.append(float(row[4]))
                        az.append(float(row[5]))
                        hrconf.append(float(row[7]))
                        motstate.append(str(row[8]))
                    else:
                        hr.append(int(row[9]))
                        ax.append(float(row[4]))
                        ay.append(float(row[6]))
                        az.append(float(row[8]))
                        hrconf.append(float(row[10]))
                        motstate.append(str(row[11]))
                else:
                    if len(row) == 9:
                        print("Android csv file")
                        print(row)
                        #print(row[3], "x os")
                        #print(row[4], "y os")
                        #print(row[5], "z os")
                    else:
                        print("PC csv file")
                        print(row)
                        #print(row[4], "x os")
                        #print(row[6], "y os")
                        #print(row[8], "z os")
                line_count += 1
                #print(row)
        print(f'Processed {line_count} lines.')
        if fileCnt < 10:
            fileCnt += 1
            #if fileCnt == 1:
                #rad1.configure(text=path_to)
        else:
            messagebox.showinfo('Importiing alert', 'You can add max 10 files!')
    except OSError as err:
        print("OS error: {0}".format(err))
    except (OSError, IOError) as e:
        print("Tip greske e-->", e)
    except ValueError:
        print("Could not convert data to an integer.")
    except FileNotFoundError as fnf:
        print("Datoteka nije pronađena exception:", fnf)
    except:
        print("Greška kod otvaranja datoteke")
        print("Unexpected error:", sys.exc_info()[0])
    maxVal = 0
    minVal = 1000000000
    for i in range(3):
        x1.pop(len(x1)-1)
        x2.pop(len(x2)-1)
        y1.pop(len(y1)-1)
        y2.pop(len(y2)-1)
        y3.pop(len(y3)-1)
        hr.pop(len(hr)-1)
        ax.pop(len(ax)-1)
        ay.pop(len(ay)-1)
        az.pop(len(az)-1)
    for i in y1:
        if i > maxVal:
            maxVal = i
        if i < minVal:
            minVal = i
    print("Max value of the signal 1--> ", maxVal)
    print("Min value of the signal 1--> ", minVal)
    for j in y2:
        if j > maxVal:
            maxVal = j
        if j < minVal:
            minVal = j
    print("Max value of the signal 2--> ", maxVal)
    print("Min value of the signal 2--> ", minVal)
    
    print("Max value of the signal --> ", max(y3))
    print("Min value of the signal --> ", min(y3))
    mf = measure_id_data()
    #mid = 1
    #insert_data_first(mid, 1, i, y1[0], y2[0], ax[0], ay[0], az[0], hr[0], hrconf[0], motstate[0], mf)
    uid = get_user_id(usr)
    for i in range(1,len(x1)):
        insert_data(uid, i, y1[i], y2[i], ax[i], ay[i], az[i], hr[i], hrconf[i], motstate[i], mf, fl_name, path_to)
    AC_DCLine = []
    for i in x1:
        AC_DCLine.append(minVal)
    #a.plot(x1, AC_DCLine, label = "AC/DC component")
    signal = noiseReduction(y1, y2, ax, ay, az)
    calculateSpo2(len(x1), y1, y2, spo2)
    drawShape(x1, y1, a, canvas, "Signal 1")
    drawShape(x2, y2, a, canvas, "Signal 2")
    drawShape(x1, ax, a11, canvas11, "Acc signal x")
    drawShape(x1, ay, a12, canvas12, "Acc signal y")
    drawShape(x1, az, a13, canvas13, "Acc signal z") 
    drawShape(x1, hr, a2, canvas2, "Heart Rate Signal")
    hrmg = []
    hrmm = []
    hrmb = []
    hrmn = []
    for i in range(len(hr)):
        if hrconf[i] > 85 and hr[i] >= 60 and hr[i] <= 120:
            hrmg.append(i)
        elif hrconf[i] < 85 and hr[i] >= 60 and hr[i] <= 100:
            hrmm.append(i)
        elif hrconf[i] > 85 and hr[i] < 60 and hr[i] > 120:
            hrmb.append(i)
        else:
            hrmn.append(i)
    #print("marker good", hrmg)
    #print("marker medium", hrmm)
    #print("marker bad", hrmb)
    """for i in hrmg:
        markg.append(i);
    if len(markm) > 0:
        
    if len(markb) > 0:
        markb = [x1.index(i) for i in hrmb]"""
 
    a2.plot(x1,hr,markevery=hrmg, ls="", marker="o", markerfacecolor='green', markersize='7', markeredgecolor='green', label="good points")
    a2.plot(x1,hr,markevery=hrmm, ls="", marker="*", markerfacecolor='orange', markersize='7', markeredgecolor='orange', label="medium points")
    a2.plot(x1,hr,markevery=hrmb, ls="", marker="x", markerfacecolor='red', markersize='7', markeredgecolor='red', label="bad points")
    a2.plot(x1,hr,markevery=hrmn, ls="", marker="x", markerfacecolor='black',markersize='7', markeredgecolor='black', label="neutral points")
    #a2.plot(x1,hr,markevery=markb, ls="", marker="x", markerfacecolor='red', label="bad points")
    canvas2.draw()
    spo2x = x1.copy()
    while(len(spo2x)!= len(spo2)):
        spo2x.pop()
    #print(spo2x)
    #print("Spo2 je ovo --> ", spo2)
    drawShape(spo2x, spo2, a3, canvas3, "SpO2 factor")
    """ for i in range(len(spo2x)):
        if spo2[i] >=95:"""
    """       
   
    xs = [a for a,b in zip(spo2x, spo2x) if b >= 95]
    ys = [a for a,b in zip(spo2x, spo2x) if b >= 95]
    a3.scatter(xs, ys, marker='s')

    xt = [a for a,b in zip(spo2x, spo2x) if b < 95 and b >= 85]
    yt = [a for a,b in zip(spo2x, spo2x) if b < 95 and b >= 85]
    a3.scatter(xt, yt, marker='^')
        #a3.scatter(x, y, marker='.', s=0)"""
    spmg = []
    spmb = []
    spmn = []
    for i in range(len(spo2x)):
        if spo2[i] >= 95:
            spmg.append(i)
        elif spo2[i] < 95 and spo2[i] > 85:
            spmb.append(i)
        else:
            spmn.append(i)
    a3.plot(spo2x,spo2,markevery=spmg, ls="", marker="o", markerfacecolor='green', markersize='7', markeredgecolor='green', label="good points")
    a3.plot(spo2x,spo2,markevery=spmb, ls="", marker="*", markerfacecolor='red', markersize='7', markeredgecolor='red', label="varning points")
    a3.plot(spo2x,spo2,markevery=spmn, ls="", marker="x", markerfacecolor='black', markersize='7', markeredgecolor='black', label="bad points")
    y_spl = UnivariateSpline(x1,y1,s=0,k=4)
    #print(y_spl.get_coeffs())
    #print(y_spl.get_knots())
    #print(y_spl.get_residual())
    #print(y_spl)
    caculateVascularCondition(x1, signal, a41, a42, a43, canvas41, canvas42, canvas43)
    #calculateRespRate(x1, y3)
    messagebox.showinfo('File successfuly added!', 'Successfuly added')

#Noise reduction method
def noiseReduction(comp1, comp2, ax, ay, az):
    from numpy import mean
    refVal = 25
    D = []
    for i in range(len(ax)):
        if ax[i] > ax[25] - 0.1 and ax[i] < ax[25] + 0.1 and ay[i] > ay[25] -0.1 and ay[i] < ay[25] + 0.1 and az[i] > az[25] -0.1 and az[i] < az[25] + 0.1:
            refVal = i
            print("Value for calibration finded!")
            break
        else:
            print("Podaci su previse nestabilni!")
    Ks = comp1[refVal] / comp2[refVal]
    for i in range(len(ax)):
        D.append(Ks*comp2[i] - comp1[i])
    avr = []
    for i in range(len(ax)):
        avr.append(comp1[i]-comp1[refVal])
   
    Km = mean(avr) / mean(D)
    C = []
    for i in range(len(ax)):
        C.append(comp1[i] -Km*D[i])
    return C

#ploting graph with data from csv file
def drawShape(x1, y1, aplt, canvas, desc):
    """try:
        aplt.unplot()
    except:
        print("Nije uspijelo remove")"""
    #aplt.unplot()
    if len(x1) > len(y1):
        x1.pop(len(x1)-1)
    elif len(x1) < len(y1):
        y1.pop(len(y1)-1)
    else:
        print("x and y have the same amount of data.")
    aplt.plot(x1, y1, label = desc)
    canvas.draw()
    #aplt.xlabel('x - samples') 
    #aplt.ylabel('y - lith detected') 
    #aplt.title('1 Green LED - 2 fotodiodes')  
    #aplt.legend() 
    #aplt.show()

#method for Submit button
def renderClicked(y1, y2):
    messagebox.showinfo('Submit Info', 'Successfuly submited!')


def convertToFloat(num):
    res = 0.0
    while(num >= 1):
        ost = num % 10
        res += ost
        res /= 10
        num /= 10
    return res

def calculateSpo2(lines, y1, y2, spo2):
    def allElementsEqual(arr):
        res = True
        for i in range(len(arr)-1):
            if arr[i] != arr[i+1]:
                res = False
                return res
        return res
            
    a,b,c = -16.67,8.333,100
    R = 1
    frame = 25
    hframe = frame
    offset = 0
    lines = lines - (lines % frame)
    #spo2 = []*lines
    y1a = [None]*frame
    y2a = [None]*frame
    miny = 0
    maxy = 0
    val = 0
    for i in range(lines):
        spo2.append(-1)
        y1a[frame-hframe] = int(y1[i])
        y2a[frame-hframe] = int(y2[i])
        hframe -= 1
        if hframe == 0:
            hframe = frame
            if allElementsEqual(y1a) or allElementsEqual(y2a):
                for i in range(frame):
                    spo2[i+offset] = 0
            else:
                maxy = max(y1a)
                miny = min(y1a)
                R = (maxy-miny)/maxy
                maxy = max(y2a)
                miny = min(y2a)
                R /= (maxy - miny) / maxy
                val = a*R*R+b*R+c
                for i in range(frame):
                    spo2[i+offset] = val
            offset += frame

def caculateVascularCondition(x, y, a41, a42, a43, canvas41, canvas42, canvas43):
    import matplotlib.pyplot as plt
    from scipy.interpolate import UnivariateSpline
    y_spl = UnivariateSpline(x,y,s=0,k=4)

    plt.semilogy(x,y,'ro',label = 'data')
    x_range = x#np.linspace(x[0],x[-1],1000)
    #plt.semilogy(x_range,y_spl(x_range))
    drawShape(x_range, y, a41, canvas41, "PPG signal")
    y_spl_1d = y_spl.derivative(n=1)
    y_1st_der = []
    for i in range(len(x_range)):
        y_1st_der.append(y_spl_1d(i))
    drawShape(x_range, y_1st_der, a42, canvas42, "First Derivative")
    y_spl_2d = y_spl.derivative(n=2)
    y_2nd_der = []
    for i in range(len(x_range)):
        y_2nd_der.append(y_spl_2d(i))
    drawShape(x_range, y_2nd_der, a43, canvas43, "Second Derivative")

#def calculateRespRate(x, y):
#EMD_method_complication
################################################################################################# 


#####################################################################################
# MAIN PROGRAM PART
##################################################################################
def start_app(usr = "Anonimus"):
    root=Tk()  
    root.title("HealthCareApp")  
    root.geometry("1275x700")
    #data variables
    x1 = [] 
    y1 = [] 
    x2 = [] 
    y2 = []
    ax = []
    ay = []
    az = []
    hr = []
    hrconf = []
    motstate = []
    spo2 = []
    maxVal = 0
    minVal = 1000000000
    line_count = 0

    #variable that contains path to selected file
    path_to = ''
    fileCnt = 0
    selected = IntVar()
    #menu feature
    menu = Menu(root)
    new_item = Menu(menu, tearoff=0)
    new_item1 = Menu(menu, tearoff=0)
    
    new_item.add_command(label='Add', command= lambda : addNewFile(path_to, fileCnt, line_count, x1, y1, x2, y2, ax, ay, az, hr, hrconf, motstate, spo2, a, a11, a12, a13, a2, a3, a41, a42, a43, canvas, canvas11, canvas12, canvas13, canvas2, canvas3, canvas41, canvas42, canvas43, usr))
    new_item.add_command(label='Export as PDF', command='Command for export')
    menu.add_cascade(label='File', menu=new_item)
    new_item.add_separator()
    new_item1.add_command(label='Help info', command="Help Info")
    menu.add_cascade(label='Help', menu=new_item1)
    root.config(menu=menu)

    #Frames
    topFrame=tk.Frame(root, bg='cyan', width = 1275, height=75)#.place(x=0, y=0)
    middleFrame=tk.Frame(root, bg='blue', width=1275, height=550)#.place(x=0, y=75)
    bottomFrame=tk.Frame(root, bg='yellow', width=1275, height=50)#.place(x=0, y=575)

    topFrame.grid(row=0, column=0, sticky='ew')
    middleFrame.grid(row=1, column=0, sticky='ew')
    bottomFrame.grid(row=2, column=0, sticky='ew')

    leftFrame=tk.Frame(middleFrame, bg='green', width=250, height=550)#.place(x=0, y=75)
    rightFrame=tk.Frame(middleFrame, bg='white', width=950, height=550)

    leftFrame.grid(row=0,column=0,sticky="ns")
    rightFrame.grid(row=0, column=1, sticky='nsew')

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=3)
    root.grid_rowconfigure(2, weight=1)
    leftFrame.grid_columnconfigure(0, weight=0)
    #topFrame.grid_columnconfigure(0, weight=1)
    middleFrame.grid_columnconfigure(1, weight=1)
    #bottomFrame.grid_columnconfigure(0, weight=1)

    yradioVal = 5

    username = usr

    #leftFrame
    Ulabel1 = Label(leftFrame, text="User: ").grid(row=0, column=0, padx=25, pady=yradioVal)
    Ulabel2 = Label(leftFrame, text=username).grid(row=1, column=0, padx=25, pady=yradioVal)
    """fileLbl = Label(leftFrame, text="Files("+str(fileCnt)+")").grid(row=0, column=0, padx=25, pady=yradioVal)
    selected = IntVar()
    rad1 = Radiobutton(leftFrame,text='First file', value=1, variable=selected).grid(row=1, column=0, padx=25, pady=yradioVal, sticky='w')
    rad2 = Radiobutton(leftFrame,text='Second file', value=2, variable=selected).grid(row=2, column=0, padx=25, pady=yradioVal, sticky='w')
    rad3 = Radiobutton(leftFrame,text='Third file', value=3, variable=selected).grid(row=3, column=0, padx=25, pady=yradioVal, sticky='w')
    rad4 = Radiobutton(leftFrame,text='Fourth file', value=4, variable=selected).grid(row=4, column=0, padx=25, pady=yradioVal, sticky='w')
    rad5 = Radiobutton(leftFrame,text='Fifth file', value=5, variable=selected).grid(row=5, column=0, padx=25, pady=yradioVal, sticky='w')
    """
    #Tabs
    tab_control = ttk.Notebook(rightFrame)
    tab1 = Frame(tab_control)
    tab2 = Frame(tab_control)
    tab3 = Frame(tab_control)
    tab4 = Frame(tab_control)
    tab5 = Frame(tab_control)
    tab_control.add(tab1, text='Signal')
    tab_control.add(tab2, text='Heart rate')
    tab_control.add(tab3, text='Oxygen saturation')
    tab_control.add(tab4, text='Vascular aging')
    #tab_control.add(tab5, text='Respiratory rate')
    tab_control.pack(expand=1, fill='both')
    #Tab1canvas = tk.Canvas(tab1, width=950, height=200)

    #scrollx = tk.Scrollbar(tab1, orient="horizontal", command=Tab1canvas.xview)
    #scrollx.grid(row=1, column=0, sticky="ew")

    #scrolly = tk.Scrollbar(tab1, orient="vertical", command=Tab1canvas.yview)
    #scrolly.grid(row=0, column=1, sticky="ns")
    #Tab1canvas.config(xscrollcommand=scrollx.set, yscrollcommand=scrolly.set, scrollregion=Tab1canvas.bbox("all"))
    #Tab1canvas.grid(row=0, column=0)


    #Tab1frame = tk.Frame(Tab1canvas, bg='white', width=2, height=1000)
    #Tab1canvas.create_window(100, 500, window=Tab1frame)

    canvas1 = Canvas(tab1, width=1100, height=550)
    scroll1 = Scrollbar(tab1, command=canvas1.yview)
    canvas1.config(yscrollcommand=scroll1.set, scrollregion=(0,0,1000,1500))
    #canvas1.pack(side=LEFT, fill=BOTH, expand=True)
    canvas1.grid(row=1, column=0, sticky="nsew")
    #scroll.pack(side=RIGHT, fill=Y)
    scroll1.grid(row=1, column=1, sticky="ns")

    canvas2 = Canvas(tab2, width=1100, height=550)
    scroll2 = Scrollbar(tab2, command=canvas2.yview)
    canvas2.config(yscrollcommand=scroll2.set, scrollregion=(0,0,1000,1000))
    #canvas2.pack(side=LEFT, fill=BOTH, expand=True)
    canvas2.grid(row=1, column=0, sticky="nsew")
    #scroll2.pack(side=RIGHT, fill=Y)
    scroll2.grid(row=1, column=1, sticky="ns")

    canvas3 = Canvas(tab3, width=1100, height=550)
    scroll3 = Scrollbar(tab3, command=canvas3.yview)
    canvas3.config(yscrollcommand=scroll3.set, scrollregion=(0,0,1000,1000))
    #canvas2.pack(side=LEFT, fill=BOTH, expand=True)
    canvas3.grid(row=1, column=0, sticky="nsew")
    #scroll2.pack(side=RIGHT, fill=Y)
    scroll3.grid(row=1, column=1, sticky="ns")

    canvas4 = Canvas(tab4, width=1100, height=550)
    scroll4 = Scrollbar(tab4, command=canvas4.yview)
    canvas4.config(yscrollcommand=scroll4.set, scrollregion=(0,0,1000,1500))
    #canvas4.pack(side=LEFT, fill=BOTH, expand=True)
    canvas4.grid(row=1, column=0, sticky="nsew")
    #scroll4.pack(side=RIGHT, fill=Y)
    scroll4.grid(row=1, column=1, sticky="ns")

    canvas5 = Canvas(tab5, width=1100, height=550)
    scroll5 = Scrollbar(tab5, command=canvas5.yview)
    canvas5.config(yscrollcommand=scroll5.set, scrollregion=(0,0,1400,1400))
    #canvas4.pack(side=LEFT, fill=BOTH, expand=True)
    canvas5.grid(row=1, column=0, sticky="nsew")
    #scroll4.pack(side=RIGHT, fill=Y)
    scroll5.grid(row=1, column=1, sticky="ns")

    frameOne = tk.Frame(canvas1, bg="white", width=975, height=525)
    canvas1.create_window(500, 750, window=frameOne)
    frameTwo = tk.Frame(canvas2, bg="black", width=975, height=525)
    canvas2.create_window(450, 250, window=frameTwo)
    frameThree = tk.Frame(canvas3, bg="white", width=975, height=525)
    canvas3.create_window(450, 250, window=frameThree)
    frameFour = tk.Frame(canvas4, bg="black", width=975, height=525)
    canvas4.create_window(450, 600, window=frameFour)
    frameFive = tk.Frame(canvas5, bg="white", width=975, height=525)
    canvas5.create_window(350, 650, window=frameFive)

    #Tab1
    lbl1 = Label(frameOne, text= 'PPG Signal')
    lbl1.grid(row=0, column=0, padx=5, pady=5)

    signalFrame=tk.Frame(frameOne, bg='red', width=950, height=300)#, yscrollcommand = w.set)
    signalFrame.grid(row=1, column=0, sticky='nsew')

    lblax = Label(frameOne, text='Accelerometer x axis').grid(row=2, column=0, padx=5, pady=5)
    axisxFrame=tk.Frame(frameOne, bg='green', width=950, height=300)
    axisxFrame.grid(row=3, column=0, sticky='nsew')

    lblay = Label(frameOne, text='Accelerometer y axis').grid(row=4, column=0, padx=5, pady=5)
    axisyFrame=tk.Frame(frameOne, bg='blue', width=950, height=300)
    axisyFrame.grid(row=5, column=0, sticky='nsew')

    lblaz = Label(frameOne, text='Accelerometer z axis').grid(row=6, column=0, padx=5, pady=5)
    axiszFrame=tk.Frame(frameOne, bg='purple', width=950, height=300)
    axiszFrame.grid(row=7, column=0, sticky='ew')
    signalFrame.grid_columnconfigure(0, weight=1)
    axisxFrame.grid_columnconfigure(1, weight=1)

    f = Figure(figsize=(6,3), dpi=100)
    a = f.add_subplot(111)
    a.plot(x1, y1, label="Green 1")
    a.plot(x2, y2, label="Green 2")
    canvas = FigureCanvasTkAgg(f, signalFrame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    toolbar = NavigationToolbar2Tk(canvas, signalFrame)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    f11 = Figure(figsize=(6,3), dpi=100)
    a11 = f11.add_subplot(111)
    a11.plot(x1, ax, label="Axis X")
    canvas11 = FigureCanvasTkAgg(f11, axisxFrame)
    canvas11.draw()
    canvas11.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    toolbar11 = NavigationToolbar2Tk(canvas11, axisxFrame)
    toolbar11.update()
    canvas11._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    f12 = Figure(figsize=(6,3), dpi=100)
    a12 = f12.add_subplot(111)
    a12.plot(x1, ay, label="Axis Y")
    canvas12 = FigureCanvasTkAgg(f12, axisyFrame)
    canvas12.draw()
    canvas12.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    toolbar12 = NavigationToolbar2Tk(canvas12, axisyFrame)
    toolbar12.update()
    canvas12._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    f13 = Figure(figsize=(6,3), dpi=100)
    a13 = f13.add_subplot(111)
    a13.plot(x1, az, label="Axis Z")
    canvas13 = FigureCanvasTkAgg(f13, axiszFrame)
    canvas13.draw()
    canvas13.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    toolbar13 = NavigationToolbar2Tk(canvas11, axiszFrame)
    toolbar13.update()
    canvas13._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    """f = Figure(figsize=(5,5), dpi=100)
    a = f.add_subplot(111)
    a.plot(x1, y1, label="Green 1")
    a.plot(x2, y2, label="Green 2")
    canvas = FigureCanvasTkAgg(f, tab1)
    canvas.draw()
    canvas.get_tk_widget().place(x=15, y=30)#pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    toolbar = NavigationToolbar2Tk(canvas, tab1)
    toolbar.update()
    canvas._tkcanvas.place(x=15, y=55)#pack(side=tk.TOP, fill=tk.BOTH, expand=True)"""

    #Tab2
    lbl2 = Label(frameTwo, text= 'BPM')
    lbl2.grid(row=0, column=0)
    HRFrame=tk.Frame(frameTwo, bg='red', width=750, height=550)#, yscrollcommand = w.set)
    HRFrame.grid(row=1, column=0, padx=15, pady=15, sticky='nsew')
    f2 = Figure(figsize=(6,3), dpi=100)
    a2 = f2.add_subplot(111)
    a2.plot(x2, hr, label="Heart Rate")
    canvas2 = FigureCanvasTkAgg(f2, HRFrame)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    toolbar2 = NavigationToolbar2Tk(canvas2, HRFrame)
    toolbar2.update()
    canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    #Tab3
    lbl3 = Label(frameThree, text= 'SpO2')
    lbl3.grid(row=0, column=0, padx=15, pady=15)
    Spo2Frame=tk.Frame(frameThree, bg='red', width=750, height=550)#, yscrollcommand = w.set)
    Spo2Frame.grid(row=1, column=0, padx=15, pady=15, sticky='nsew')

    f3 = Figure(figsize=(6,3), dpi=100)
    a3 = f3.add_subplot(111)
    a3.plot(x2, hr, label="Sp02")
    canvas3 = FigureCanvasTkAgg(f3, Spo2Frame)
    canvas3.draw()
    canvas3.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    toolbar3 = NavigationToolbar2Tk(canvas3, Spo2Frame)
    toolbar3.update()
    canvas3._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    lbl31 = Label(frameThree, text="Measurement count")
    lbl31.grid(row=2, column=0, padx=15, pady=15)
    #Spo2Frame.grid_columnconfigure(0, weight=1)
    #Spo2Frame.grid_rowconfigure(1, weight=3)

    #Tab4
    lbl41 = Label(frameFour, text= 'Signal')
    lbl41.grid(row=0, column=0, padx=15, pady=15)
    VascularSignalFrame=tk.Frame(frameFour, bg='red', width=750, height=550)#, yscrollcommand = w.set)
    VascularSignalFrame.grid(row=1, column=0, padx=15, pady=15, sticky='nsew')
    lbl42 = Label(frameFour, text= 'First derivative')
    lbl42.grid(row=2, column=0, padx=15, pady=15)
    FirstDerivativeFrame=tk.Frame(frameFour, bg='red', width=750, height=550)#, yscrollcommand = w.set)
    FirstDerivativeFrame.grid(row=3, column=0, padx=15, pady=15, sticky='nsew')
    lbl43 = Label(frameFour, text= 'Second derivative')
    lbl43.grid(row=4, column=0, padx=15, pady=15)
    SecondDerivativeFrame=tk.Frame(frameFour, bg='red', width=750, height=550)#, yscrollcommand = w.set)
    SecondDerivativeFrame.grid(row=5, column=0, padx=15, pady=15, sticky='nsew')

    f41 = Figure(figsize=(6,3), dpi=100)
    a41 = f41.add_subplot(111)
    a41.plot(x1, y1, label="PPG Signal")
    canvas41 = FigureCanvasTkAgg(f41, VascularSignalFrame)
    canvas41.draw()
    canvas41.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    toolbar41 = NavigationToolbar2Tk(canvas41, VascularSignalFrame)
    toolbar41.update()
    canvas41._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    f42 = Figure(figsize=(6,3), dpi=100)
    a42 = f42.add_subplot(111)
    a42.plot(x1, y1, label="First Derivatve")
    canvas42 = FigureCanvasTkAgg(f42, FirstDerivativeFrame)
    canvas42.draw()
    canvas42.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    toolbar42 = NavigationToolbar2Tk(canvas42, FirstDerivativeFrame)
    toolbar42.update()
    canvas42._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    f43 = Figure(figsize=(6,3), dpi=100)
    a43 = f43.add_subplot(111)
    a43.plot(x1, y1, label="Second Derivative")
    canvas43 = FigureCanvasTkAgg(f43, SecondDerivativeFrame)
    canvas43.draw()
    canvas43.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    toolbar43 = NavigationToolbar2Tk(canvas43, SecondDerivativeFrame)
    toolbar43.update()
    canvas43._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    #Tab5 - Respirator rate Tab
    """
    lbl51 = Label(frameFive, text= 'Respirator rate extraction')
    lbl51.grid(row=0, column=0, padx=15, pady=15)

    InputSignalFrame=tk.Frame(frameFive, bg='red', width=750, height=350)#, yscrollcommand = w.set)
    InputSignalFrame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
    f51 = Figure(figsize=(6,3), dpi=100)
    a51 = f51.add_subplot(111)
    a51.plot(x1, y1, label="PPG Signal")
    canvas51 = FigureCanvasTkAgg(f51, InputSignalFrame)
    canvas51.draw()
    canvas51.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    toolbar51 = NavigationToolbar2Tk(canvas51, InputSignalFrame)
    toolbar51.update()
    canvas51._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    lbl52 = Label(frameFive, text= 'Extracted signal')
    lbl52.grid(row=2, column=0, padx=15, pady=15)
    ExtractedSignalFrame=tk.Frame(frameFive, bg='red', width=750, height=350)#, yscrollcommand = w.set)
    ExtractedSignalFrame.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')
    f52 = Figure(figsize=(6,3), dpi=100)
    a52 = f52.add_subplot(111)
    a52.plot(x1, y1, label="Extracted Signal")
    canvas52 = FigureCanvasTkAgg(f52, ExtractedSignalFrame)
    canvas52.draw()
    canvas52.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    toolbar52 = NavigationToolbar2Tk(canvas52, ExtractedSignalFrame)
    toolbar52.update()
    canvas52._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    lbl53 = Label(frameFive, text= 'Final Extracted Signal')
    lbl53.grid(row=4, column=0, padx=15, pady=15)
    FinalSignalFrame=tk.Frame(frameFive, bg='red', width=750, height=350)#, yscrollcommand = w.set)
    FinalSignalFrame.grid(row=5, column=0, padx=5, pady=5, sticky='nsew')
    f53 = Figure(figsize=(6,3), dpi=100)
    a53 = f53.add_subplot(111)
    a53.plot(x1, y1, label="Final Signal")
    canvas53 = FigureCanvasTkAgg(f53, FinalSignalFrame)
    canvas53.draw()
    canvas53.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    toolbar53 = NavigationToolbar2Tk(canvas53, FinalSignalFrame)
    toolbar53.update()
    canvas53._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    lbl53 = Label(frameFive, text= 'Respiratory rate: ' + str(0.00) + 'Hz or ' + str(0.00) + "bpm (breathes per minute)")
    lbl53.grid(row=6, column=0, padx=15, pady=15)

    btn = tk.Button(bottomFrame, text="Render", bg="blue", fg="white", command= lambda : renderClicked(y1, y2)).place(x=15, y=10)
    """
    #Label
    Headerlbl = tk.Label(topFrame, text="Output Data Analyzer for #MAXREFDES101", bg='cyan', fg='green', font=("Arial Bold", 25))
    Headerlbl.grid(row=0, column=0, padx=15, pady=25)

    #Submit button
    #btn = tk.Button(bottomFrame, text="Render", bg="blue", fg="white", command= lambda : renderClicked(y1, y2)).place(x=15, y=10)
    root.mainloop()
###Main command to start the app

###############################################################################
