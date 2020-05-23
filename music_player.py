
# coding: utf-8

# In[1]:


##import libraries
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
import pygame
import os
from mutagen.mp3 import MP3
import time
from tkinter.ttk import Progressbar
from tkinter.ttk import Style
from tkinter.ttk import Separator
import threading


win=Tk()
win.title('Audio player')
win.geometry("600x400")
win.resizable(0, 0) 
#icon
win.iconbitmap(r'icon.ico')


#menu_frame
menu_frame=Frame(win)
menu_frame.grid()

pygame.mixer.init()
#menubar
def browse_file():
    global filename
    filename=filedialog.askopenfilename()
    audio=MP3(filename)   
    add_to_playlist()

menu=Menu(menu_frame)
win.config(menu=menu)

submen=Menu(menu,tearoff=0)
menu.add_cascade(label="File",menu=submen)
submen.add_command(label="Open file",command=browse_file)

#frame for list
list_frame=Frame(win)
list_frame.grid()
songlist=Listbox(list_frame)
songlist.grid(padx=0,pady=10,ipady=50,ipadx=40,column=0)  


#add to playlist
index=0
playlist=[]
def add_to_playlist():
    global index
    songlist.insert(index,os.path.basename(filename))
    playlist.insert(index,filename)
    print(playlist)
    index+=1
add_button=Button(list_frame,text="Add",command=browse_file).place(x=40,y=260)


#remove from playlist
def remove_from_playlist():
    song_now=songlist.curselection()
    song_now=int(song_now[0])
    playlist.pop(song_now)
    songlist.delete(song_now)
    print(playlist)
    
rem_button=Button(win,text="Remove",command=remove_from_playlist).place(x=90,y=260)
#hide, unhide list
img=PhotoImage(file=r'list.png')
hide="no"
def but():
    global hide
    if hide=="no":
        songlist.grid_remove()
        hide="yes"
        
    elif hide=="yes":
        songlist.grid()
        hide="no"
        
button=Button(list_frame,image=img,command=but,bg="white",borderwidth=0)
button.place(x=185,y=0)


#frame for time
time_frame=Frame(win,bg="black")
time_frame.place(x=220,y=90)



timelabel=Label(time_frame,text='00:00',font=("Castellar",30,"bold"),bg="black",fg="white")
timelabel.grid(padx=120)
lengthlabel=Label(time_frame,text='00:00',font=("Castellar",30,"bold"),bg="black",fg="white")
lengthlabel.grid()
def showdetails(play_now):
    #global total_length
    filedata=os.path.splitext(play_now)
    
    if filedata[1]=='.mp3':
        audio=MP3(play_now)
        total_length=audio.info.length
    
    else:
        a=pygame.mixer.Sound(play_now)
        total_length = a.get_length
    

    mins,sec =divmod(total_length,60)
    mins=round(mins)
    sec=round(sec)
    timeformat="{:02d}:{:02d}".format(mins,sec)
    
    lengthlabel['text']=timeformat
    l_length=total_length+1
    t1=threading.Thread(target=start_count,args=(l_length,))
    t1.start()
    seek1['maximum']=total_length
    
    
    
#progressbar
pro_frame=Frame(win)
pro_frame.place(x=0,y=300)
s = Style()
s.theme_use("default")
s.configure("TProgressbar", thickness=1, troughcolor ='#f7f7f7', background='black')
seek1= Progressbar(pro_frame, style="TProgressbar",value=0,length=600)
seek1.pack()

#timing for progressbar 
def start_count(t):
    global x
    x=0
    x=float(x)
    while x<=t and pygame.mixer.music.get_busy():
        if label["text"]=="paused":
            continue
        else:
            seek1['value']=x
            mins,sec =divmod(x,60)
            mins=round(mins)
            sec=round(sec)
            timeformat="{:02d}:{:02d}".format(mins,sec)
            timelabel['text']=timeformat
            time.sleep(1)
            x+=1

        
#functions
def stop():
    pygame.mixer.music.stop() 
    seek1['value']=0
    
def vol(val):
    vo=int(val)/100
    pygame.mixer.music.set_volume(vo)
    
def go(play_now):
    if seek1['value']>=1:
        pygame.mixer.music.stop()
        time.sleep(1)
        pygame.mixer.music.load(play_now)
        pygame.mixer.music.play()
        showdetails(play_now)
    else:
        pygame.mixer.music.load(play_now)
        pygame.mixer.music.play()
        showdetails(play_now)

    

#buttons


#loop
def loop():
    global loop_flag
    if loop_flag==1:
        loop_flag=-1
        loop_button['image']=loop_img
    elif loop_flag==-1:
        loop_flag=1
        loop_button['image']=loop_img1
        

loop_img=PhotoImage(file=r'repeat.png')
loop_img1=PhotoImage(file=r'loop.png')
loop_flag=-1
loop_button=Button(win,image=loop_img,command=loop,bg="#f5c400")
loop_button.place(x=40,y=310)




#previous song
def prev():
    global song_now
    song_now=song_now-1
    play_now=playlist[song_now]
    go(play_now)
prev_img=PhotoImage(file=r'left.png')
prev_button=Button(win,image=prev_img,command=prev,bg="#f5c400")
prev_button.place(x=140,y=310)

#play and pause
play_img=PhotoImage(file=r'play.png')
pause_img=PhotoImage(file=r'pause.png')

def play(event):
    global play_now
    global song_now
    
    song_now=songlist.curselection()
    song_now=int(song_now[0])
    play_now=playlist[song_now]
    go(play_now)
    play_button["image"]=pause_img
    label["text"]="Playing"
    
songlist.bind('<Double-Button-1>',play)

def pause():
    pygame.mixer.music.pause()
    label["text"]="paused"
    play_button["image"]=play_img
    
    
def resume():
    pygame.mixer.music.unpause()
    label["text"]="playing"
    play_button["image"]=pause_img

    
def use():
    
    if timelabel['text']=='00:00':
        play()
        
    elif label["text"]=="paused":
        resume()
    else:
        pause()
    
    
play_button=Button(win,image=play_img,command=use,bg="#f5c400")
play_button.place(x=300,y=310)





#next song
def next():
    global song_now
    song_now=song_now+1
    play_now=playlist[song_now]
    go(play_now)
next_img=PhotoImage(file=r'right.png')
next_button=Button(win,image=next_img,command=next,bg="#f5c400").place(x=460,y=310)

#volume
vol_img=PhotoImage(file=r'sound.png')
mute_img=PhotoImage(file=r'mute.png')
vol_frame=Frame(win)
vol_frame.place(y=200,x=520)
mute_flag="no"
def mute():
    global mute_flag
    global vol_scale
    new=vol_scale
    if mute_flag=="no":
        vol_scale.set(0) 
        mute_flag="yes"
        print("mute_flag")
        lab["image"]=mute_img
    else:
        vol_scale.set(60)
        mute_flag="no"
        print("mute_flag1")
        lab["image"]=vol_img
        

vol_scale=Scale(vol_frame,from_=100, to=0,bg="white",command=vol)   
vol_scale.set(60)
def vol_control(event):
    global vol
    global vol_scale
    vol_scale.grid()


def off(event):
    vol_scale.grid_remove()    


lab=Button(vol_frame,image=vol_img,command=mute,bg="#f5c400",borderwidth=0)
lab.grid(sticky=E)
vol_frame.bind("<Enter>", vol_control)
vol_frame.bind("<Leave>",off)


#statusbar
status_frame=Frame(win)
status_frame.place(x=0,y=355)
Separator(status_frame,orient=HORIZONTAL).grid(sticky=EW,ipadx=400)
label=Label(status_frame,text="welcome....")
label.grid(sticky=W)

#for windows close button 
def exit():
    pygame.mixer.music.stop()    
    win.destroy()
    
def on_closing():
    ans=tkinter.messagebox.askquestion("Quit","Are you sure you want to quit?")
    if ans=="yes":
        pygame.mixer.music.stop()    
        win.destroy()

        
win.protocol("WM_DELETE_WINDOW", on_closing)


win.mainloop()

