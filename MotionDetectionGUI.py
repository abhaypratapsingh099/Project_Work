# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 17:36:54 2019

@author: Satyam Rajput
"""

from tkinter import *
from tkinter.font import Font
from tkinter import messagebox
import numpy as np
import cv2
import time
import sys
import os, signal
import smtplib
from urllib.request import urlopen

email_id = 'Email Id to which you want to sent the Email'
Path = os.path.abspath(os.getcwd())+r'\Recording'  #"E:\\MCA\Programming\Python\Recording\\"

def isconnected():
    try:
        urlopen('http://216.58.192.142')
        return True
    except:
        return False

def Email_Sender():
    global email_id
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)

        # start TLS for security
        s.starttls()

        # Authentication
        s.login("Email Id from which you want to sent the Email", "Password")

        # message to be sent

        message = "Intruder ALERT ! Someone is Detected in your Room "

        s.sendmail("Email Id from which you want to sent the Email", email_id, message)
        s.quit()
    except:
        pass
    finally:
        return


def detectmotion():

    Ans = True
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame1 = cap.read()
    else:
        ret = False
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    minute = int(str(time.ctime(time.time()))[14:16])
    minute += 1
    while minute >= int(str(time.ctime(time.time()))[14:16]):


        dif = cv2.absdiff(frame1, frame2)

        if (np.average(dif) >= 4.0):
            return True

        frame3 = frame1
        frame1 = frame2
        ret, frame2 = cap.read()

        if Ans:
            cv2.imshow('Output', frame2)
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            Ans = False

            cv2.destroyAllWindows()
            sys.exit()
            break

    else:

        cap.release()
        cv2.destroyAllWindows()
        return False


def Path_Setter():
    global Path
    folder_name = Path + str(time.ctime(time.time()))[:10]
    if os.path.exists(folder_name):
        path = folder_name
    else:
        os.mkdir(folder_name)
        path = folder_name
    return path + "\\"


def record():
    Ans = True
    Email_Sender()
    cap = cv2.VideoCapture(0)
    hour = int(str(time.ctime(time.time()))[11:13])
    minute = int(str(time.ctime(time.time()))[14:16])
    filename = Path_Setter() + str(hour) + "-" + str(minute) + ".avi"
    codec = cv2.VideoWriter_fourcc(*'XVID')
    framerate = 10
    resolution = (640, 480)
    videoFileOutput = cv2.VideoWriter(filename, codec, framerate, resolution)
    ret, frame = cap.read()
    minute = int(str(time.ctime(time.time()))[14:16])
    if minute == 59:
        minute = 1
    minute += 1
    while ret:

        ret, frame = cap.read()
        videoFileOutput.write(frame)
        ret, frame = cap.read()
        ret, frame1 = cap.read()

        if Ans: cv2.imshow('Output', frame)
        dif = cv2.absdiff(frame, frame1)
        if (cv2.waitKey(1) & 0xFF == ord('q')):

            Ans = False

            cv2.destroyAllWindows()
            sys.exit()
            break

        if (np.average(dif) > 4.0) and minute == int(str(time.ctime(time.time()))[14:16]):
            minute += 1

        elif minute == int(str(time.ctime(time.time()))[14:16]):
            videoFileOutput.release()
            cap.release()
            cv2.destroyAllWindows()
            return


def open_camera(event):
    if not isconnected():
        messagebox.showerror('Error','Internet is not connected kindly check internet connection otherwise you will not able to get email notification')
    messagebox.showinfo('Information', 'pressing Q will exit the camera')
    while True:
        if detectmotion():
            record()


def close_button(event):
    x = messagebox.askyesno(title='Cancel', message='Do you really want to exit')
    print(x)
    if x:
        root.quit()



def settings(event):
    def backButton():
        settings_frame.pack_forget()
        main_frame.pack()

    def update_email(event):
        global email_id
        email_id = email_var.get()
        messagebox.showinfo('Information', 'Email Updated')

    def update_path(event):
        global Path
        Path = path_var.get()
        messagebox.showinfo('Information', 'Working Directory Changed')

    main_frame.pack_forget()
    my_font = Font(family='Times New Roman', size=20, weight='bold', slant='italic')
    settings_frame = Frame(root, width=280, height=250, bg='darkgray')
    settings_frame.pack()
    path_label = Label(settings_frame, text='Select new Path ', bg='darkgray')
    path_label.place(x=15, y=50)
    email_label = Label(settings_frame, text='Enter new Email ID ', bg='darkgray')
    email_label.place(x=0, y=100)
    setting_label = Label(settings_frame, text='Settings ', bg='darkgray', font=my_font)
    setting_label.place(x=80, y=5)
    path_var = StringVar()
    path_entry = Entry(settings_frame, width=10, textvariable=path_var)
    path_entry.place(x=105, y=50)
    email_var = StringVar()
    email_entry = Entry(settings_frame, width=10, textvariable=email_var)
    email_entry.place(x=105, y=100)
    path_button = Button(settings_frame, text='Update Path')
    path_button.place(x=175, y=50)
    email_button = Button(settings_frame, text='Update Email ID')
    email_button.place(x=175, y=100)
    back_button = Button(settings_frame, text='Back', width=20, command=backButton)
    back_button.place(x=50, y=150)
    path_button.bind("<Button-1>", update_path)
    email_button.bind("<Button-1>", update_email)
    path_entry.focus()


if __name__ == "__main__":
    root = Tk()

    root.title('Motion Detector')
    root.geometry('280x250+200+200')
    main_frame = Frame(root, width=280, height=250, bg='darkgray')
    main_frame.pack()
    my_font = Font(family='Times New Roman', size=20, weight='bold', slant='italic')
    welcome_label = Label(main_frame, text='Motion Detector', fg='black', bg='darkgray', font=my_font)
    welcome_label.place(x=50, y=10)
    open_canvas = Canvas(main_frame, width=48, height=46, bg='darkgray')
    open_canvas.place(x=20, y=100)
    mainpath=os.path.abspath(os.getcwd()) #os.path.abspath(__file__)
    mainpath+=r'\Resources\Images'
    open_photo = PhotoImage(file= mainpath+r'\open.png', )
    open_canvas.create_image(0, 0, image=open_photo, anchor=NW)
    settings_canvas = Canvas(main_frame, width=45, height=45, bg='darkgray')
    settings_canvas.place(x=120, y=100)
    settings_photo = PhotoImage(file=mainpath+r'\settings.png', )
    settings_canvas.create_image(0, 0, image=settings_photo, anchor=NW)
    close_canvas = Canvas(main_frame, width=45, height=45, bg='darkgray')
    close_canvas.place(x=220, y=100)
    close_photo = PhotoImage(file=mainpath+r'\close.png', )
    close_canvas.create_image(0, 0, image=close_photo, anchor=NW)
    close_canvas.bind('<Button-1>', close_button)
    settings_canvas.bind('<Button-1>', settings)
    open_canvas.bind('<Button-1>', open_camera)
    root.mainloop()


