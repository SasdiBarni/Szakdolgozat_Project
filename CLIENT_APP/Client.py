import os
import DataSender
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime

class DatasForServer:
    def __init__(myobject, Date, User, JobID, Path, directoryName):
        myobject.Date = None
        myobject.User = None
        myobject.JobID = None
        myobject.Path = None
        myobject.directoryName = None

sendBack = DatasForServer(None, None, None, None, None)

def LoginWindow():
    window = Tk()

    window.title('Login')
    window.resizable(False, False)

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width/2) - (300/2)
    y = (screen_height/2) - (100/2)

    window.geometry('%dx%d+%d+%d' % (300, 100, x, y))

    def login():
        userName = 'admin'
        pw = 'admin'
    
        if userEntry.get() == userName and pwEntry.get() == pw:
            user = userEntry.get()
            window.destroy()
            ClientWindow(user)
        else:
            messagebox.showinfo(title='Error', message='Wrong username or password!')


    titleLabel = Label(window, text='You have to login first!', font=('Helvetica', 12)).grid(row=0, column=1)

    userLabel = Label(window, text='Username:', font=('Helvetica', 10)).grid(row=1, column=0)
    userEntry = Entry(window, width= 30)
    userEntry.grid(row=1, column=1)

    pwLabel = Label(window, text='Password:', font=('Helvetica', 10)).grid(row=2, column=0)
    pwEntry = Entry(window, width= 30, show='*')
    pwEntry.grid(row=2, column=1)

    loginButton = Button(window, text='Login', font=('Helvetica', 10), command= login).grid(row=3, column=1)

    window.mainloop()   

    UserName = None
    Path = None
    current_date_and_time = None
    jobID = None

def ClientWindow(user):
    window = Tk()

    window.title('Client App')
    window.resizable(False, False)

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    winWidth = 750
    winHeight = 300

    x = (screen_width/2) - (winWidth/2)
    y = (screen_height/2) - (winHeight/2)

    window.geometry('%dx%d+%d+%d' % (winWidth, winHeight, x, y))
    
    def FileWindow():
        directory = filedialog.askdirectory()
        directoryEntry.delete(0, 1000)
        directoryEntry.insert(0, os.path.abspath(directory))
    
    def SendCommand():
        
        #! CHANGE BACK LATER TO ONLY FILE SENDING OPTION
        if (directoryEntry.get() != '' or clicked.get() != '') and algorythms.get() != '-- Select from list below --':
                        
            sendBack.User = user #name of the logged in user
            sendBack.Path = directoryEntry.get() #the path of thr directory locally that needs to be uploaded to the file server
            sendBack.Date = datetime.now() #the date of the upload start
            sendBack.JobID = algorythms.get() #ID of the algorythm
            
            directoryList = sendBack.Path.split('\\')
            sendBack.directoryName = str(directoryList[len(directoryList) - 1])
            
            DataSender.SendToCentralServer(sendBack.Date, sendBack.User, sendBack.JobID, sendBack.directoryName)
            DataSender.SendToFileServer(sendBack.directoryName)
            
        else:
            messagebox.showinfo(title='Error', message='Please select a file and a job!')    
    
    #! TEST
    def ResultsCommand():
        DataSender.GetResultsFromServer()
        os.system(f"explorer C:\\Users\\sasdi\\Documents\\Szakdolgozat_Project\\CLIENT_APP\\")
        
    
    def LogOut():
        window.destroy()
        LoginWindow()
            
    titleLabel = Label(window, text='Welcome ' + user + '!', font=('Helvetica', 26)).grid(row=0, column=1)
    
    directoryLabel = Label(window, text='Choose a file: ', font=('Helvetica', 10), pady=20).grid(row=1, column=0)
    directoryButton = Button(window, text='Open',  font=('Helvetica', 10), width=10, command=FileWindow).grid(row=1, column=2)
    
    directoryEntry = Entry(window, width=80)
    directoryEntry.grid(row=1, column=1)
    
    clicked = StringVar(window)
    
    #! TEST, IF WORKING DELETE
    fileList = DataSender.GetFilesFromServer()
    
    dropDownLabel = Label(window, text='Choose a file from server: ', font=('Helvetica', 10), pady=20).grid(row=2, column=0)
    dropDown = OptionMenu(window, clicked, *fileList).grid(row=2, column=1)
    
    OPTIONS = [
        '-- Select from list below --',
        'Cell seed detection and counting'
    ]

    algorythms = StringVar(window)
    algorythms.set(OPTIONS[0]) # default value
    
    dropDownLabel = Label(window, text='Choose a job: ', font=('Helvetica', 10), pady=20).grid(row=3, column=0)
    dropDown = OptionMenu(window, algorythms, *OPTIONS).grid(row=3, column=1)
    
    uploadButton = Button(window, text='Start job',  font=('Helvetica', 10), width=10, command=SendCommand).grid(row=4, column=1, sticky='w')
    resultsButton = Button(window, text='Open results',  font=('Helvetica', 10), width=10, command=ResultsCommand).grid(row=4, column=1, sticky='n')

    quitButton = Button(window, text='Exit',  font=('Helvetica', 10), width=10, command=window.destroy).grid(row=4, column=2)

    logoutButton = Button(window, text='Logout',  font=('Helvetica', 10), width=10, command=LogOut).grid(row=4, column=1, sticky='e')

    
    window.mainloop()
    
LoginWindow()