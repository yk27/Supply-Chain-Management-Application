from tkinter import *
from tkinter import ttk
import tkinter as tk
import time
import random
import pandas as pd
import xlsxwriter
from datetime import date, datetime
from datetime import datetime
import getpass
import os
import smtplib
from email.message import EmailMessage
import paho.mqtt.client as paho
from paho import mqtt

qwe = [0,0,0,'0']

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connection Success! Received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

#Sends Automatic Mail once the Shift gets over
def automaticEmail():
    sender_email= "mayoisnicee@gmail.com"
    sender_pass="Mayonnaise24"
    receiver_email="balakumarbk03@gmail.com"

    msg = EmailMessage()
    msg['Subject'] = "REPORT"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content('Shift Report Has Been Attached...') #to be filled

    
    #User Name
    user = getpass.getuser()

    file_directory=["C:/Users/"+ user + "/Documents/" + qwe[3] +  ".xlsx"]

    for file in file_directory:
        with open(file, 'rb') as f:
            file_data=f.read()
            file_name=qwe[3]+'.xlsx'
            print("filename",file_name)
        msg.add_attachment(file_data, maintype='application',
        subtype='octet-stream', filename=file_name)


    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email,sender_pass)
        smtp.send_message(msg)
    Label(root, text='Report Generated!', font = 'arial 15 bold').place(x=800, y=450)
    print("Mail Sent!")

def vals(count,good,bad):
    qwe[0] = count; qwe[1] = good; qwe[2] = bad

#Generates the current report when the Generate Report Button is clicked.
def generateReport(): #(t,number,name,count,good,bad):
    #Date Time
    now = datetime.now()
    dt_string = now.strftime("%B %d %Y,%H-%M-%S")
    qwe[3] = dt_string
    #User Name
    user = getpass.getuser()
    
    count_val,good_val,bad_val,shift_dt = [0],[0],[0],[0]
    
    count_val[0] = qwe[0]
    good_val[0] = qwe[1]
    bad_val[0] = qwe[2]
    shift_dt[0] = dt_string

    df = pd.DataFrame({'Shift Time':shift_dt[0],
                    'Shift Duration(secs)':t.get(),
                    'Shift Number':number.get(),
                    'Supervisor':name.get(),
                    'Production Count':count_val,
                    'Good Products':good_val,
                    'Defected Products':bad_val})

    writer = pd.ExcelWriter(r"C:\Users\\"+ user + "\Documents\\" + dt_string +  ".xlsx")

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1',index = False)
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']
    worksheet.set_column('A:G',25 )
    writer.save()
    print("Report Generated Successfully on "+dt_string)
    
    
    
#Shift Runtime
def shiftRun():
    l = []
    time_sec = int(t.get())
    count = 0; good = 0; bad = 0    
    while time_sec:
        mins, secs = divmod(time_sec, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        #print(timeformat, end='\r')
        l.append(timeformat)
        #print(l[-1])
        count += 1
        if random.randint(0,1):
            good += 1
        else:
            bad += 1
        Label(root, text=l[-1], font = 'arial 15 bold').place(x=800, y=50)
        Label(root, text="Production Count: "+str(count), font = 'arial 20 bold').place(x=20, y=360)
        Label(root, text="Good: "+str(good), font = 'arial 20 bold').place(x=20, y=400)
        Label(root, text="Defects: "+str(bad), font = 'arial 20 bold').place(x=20, y=440)
        client.publish("test/Bosch_Good",payload=str(good),qos=0)
        time.sleep(1)
        time_sec -= 1
        root.update()

        vals(count,good,bad)
    Label(root, text='Shift Ended!', font = 'arial 15 bold').place(x=800, y=80)
    generateReport()
    automaticEmail()

try:
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    client.on_connect = on_connect

    # enable TLS
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

    client.username_pw_set("industry4.0", "Qwerty@123")
    client.connect("1d1587d792b6466fa8f2db432d9d3db2.s1.eu.hivemq.cloud", 8883)

    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_publish = on_publish

    root = Tk()
    root.geometry('1000x500')
    #production_name = input("Production Name(Eg: Bulb/Indicator/Housing/Electrical): ")
    Label(root, text = 'Indicator Production' , font = 'arial 20 bold').pack()

    #Starting Protocols
    Label(root, font ='arial 15 bold', text = 'Set Time').place(x = 20 ,y = 50)
    t = Entry(root,width=15)
    t.place(x=180, y=55)
    Label(root, font ='arial 15 bold', text = 'Shift Number').place(x = 20 ,y = 80)
    number = Entry(root,width=15)
    number.place(x=180, y=85)
    Label(root, font ='arial 15 bold', text = 'Supervisor').place(x = 20 ,y = 110)
    name = Entry(root,width=15)
    name.place(x=180,y=115)

    #Start Button
    Button(root, text='START', bd ='5', command = shiftRun, font = 'arial 10 bold').place(x=80, y=160)

    #Generate Report Button
    Button(root, text='Generate Report', bd ='5', command = generateReport, font = 'arial 10 bold').place(x=800, y=400)


    #Quit Button
    ttk.Button(root, text="Quit", command=root.destroy).place(x=450,y=450)
    root.mainloop()
    print("Press 'Ctrl+C' to close the application.")
    client.loop_forever()


except KeyboardInterrupt:
        print("Byeeee!!")
        pass
