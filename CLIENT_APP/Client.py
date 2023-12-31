import os
import DataSender
import UserAuthenticate
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from datetime import datetime
import smbclient
import visualizer

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

    window.configure(bg='#39AEA9')
    window.title('Login')
    window.resizable(False, False)

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width/2) - (300/2)
    y = (screen_height/2) - (100/2)

    window.geometry('%dx%d+%d+%d' % (300, 100, x, y))

    def login():
        
        if UserAuthenticate.LoginAuthenticate(userEntry.get(), pwEntry.get()):
            user = userEntry.get()
            window.destroy()
            ClientWindow(user)
        else:
            messagebox.showinfo(title='Error', message='Wrong username or password!')

    titleLabel = Label(window, text='You have to login first!', font=('Helvetica', 12), background='#39AEA9').grid(row=0, column=1)

    userLabel = Label(window, text='Username:', font=('Helvetica', 10), background='#39AEA9').grid(row=1, column=0)
    userEntry = Entry(window, width= 30, background='#E5EFC1')
    userEntry.grid(row=1, column=1)

    pwLabel = Label(window, text='Password:', font=('Helvetica', 10), background='#39AEA9').grid(row=2, column=0)
    pwEntry = Entry(window, width= 30, show='*', background='#E5EFC1')
    pwEntry.grid(row=2, column=1)

    loginButton = Button(window, text='Login', font=('Helvetica', 10), command= login, background='#E5EFC1').grid(row=3, column=1)

    window.mainloop()   

    UserName = None
    Path = None
    current_date_and_time = None
    jobID = None

def ClientWindow(user):
    window = Tk()

    window.configure(bg='#39AEA9')
    window.title('Client App')
    window.resizable(False, False)

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    winWidth = 700
    winHeight = 250

    x = (screen_width/2) - (winWidth/2)
    y = (screen_height/2) - (winHeight/2)

    window.geometry('%dx%d+%d+%d' % (winWidth, winHeight, x, y))
    
    def FileWindow():
        directory = filedialog.askdirectory()
        directoryEntry.delete(0, 1000)
        directoryEntry.insert(0, os.path.abspath(directory))
        
    def SendCommand():
        
        if directoryEntry.get() != '' or algorythms.get() != '-- Select from list below --':
                        
            sendBack.User = user #name of the logged in user
            sendBack.Path = directoryEntry.get() #the path of the directory locally that needs to be uploaded to the file server
            sendBack.Date = datetime.now().replace(microsecond=0) #the date and time of the upload start
            sendBack.JobID = algorythms.get() #ID of the algorythm
            
            directoryList = sendBack.Path.split('\\')
            sendBack.directoryName = str(directoryList[len(directoryList) - 1])
            
            if os.path.exists(sendBack.Path):
                
                mrxs_path = sendBack.Path + "\\" + sendBack.directoryName + ".mrxs"
                
                if os.path.exists(mrxs_path):
                    
                    if os.path.getsize(mrxs_path) > 0:
                        
                        if os.path.exists(sendBack.Path + "\\" + sendBack.directoryName):
                            
                            if len(os.listdir(sendBack.Path + "\\" + sendBack.directoryName)) != 0:
                                
                                DataSender.SendToCentralServer(sendBack.Date, sendBack.User, sendBack.JobID, sendBack.directoryName)
                                DataSender.SendToFileServer(sendBack.directoryName)
                                
                            else:
                                messagebox.showinfo(title='Error', message='There are no files in the subdirectory!')
                                
                        else:
                            messagebox.showinfo(title='Error', message='There is no subdirectory within the main folder!')
                            
                    else:
                        messagebox.showinfo(title='Error', message='The .MRXS file is empty!')
                        
                else:
                    messagebox.showinfo(title='Error', message='There is no .MRXS file found in directory!')
                    
            else:
                messagebox.showinfo(title='Error', message='Please select an EXISTING file directory!')
                    
        else:
            messagebox.showinfo(title='Error', message='Please select a file and a job!')    
    
    def ResultsCommand():
        window.destroy()
        ResultWindow(user)
    
    def LogOut():
        window.destroy()
        LoginWindow()
            
    titleLabel = Label(window, text='Welcome ' + user + '!', font=('Helvetica', 26), background='#39AEA9').grid(row=0, column=1)
    
    directoryLabel = Label(window, text='Choose a file: ', font=('Helvetica', 10), background = '#39AEA9', pady=20).grid(row=1, column=0)
    directoryButton = Button(window, text='Open',  font=('Helvetica', 10), background = '#E5EFC1', width=10, command=FileWindow).grid(row=1, column=2)
    
    directoryEntry = Entry(window, width=80, background='#E5EFC1')
    directoryEntry.grid(row=1, column=1)
    
    OPTIONS = [
        '-- Select from list below --',
        'Cell nuclei detection and counting'
    ]

    algorythms = StringVar(window)
    algorythms.set(OPTIONS[0]) # default value
    
    dropDownLabel = Label(window, text='Choose a job: ', font=('Helvetica', 10), background='#39AEA9', pady=20).grid(row=2, column=0)
    dropDown = OptionMenu(window, algorythms, *OPTIONS).grid(row=2, column=1)
    
    uploadButton = Button(window, text='Start job',  font=('Helvetica', 10), background='#E5EFC1', width=10, command=SendCommand).grid(row=3, column=1, sticky='w')
    resultsButton = Button(window, text='Open results',  font=('Helvetica', 10), background='#E5EFC1', width=10, command=ResultsCommand).grid(row=3, column=1, sticky='n')

    quitButton = Button(window, text='Exit',  font=('Helvetica', 10), width=10, background='#E5EFC1', command=window.destroy).grid(row=3, column=2)

    logoutButton = Button(window, text='Logout',  font=('Helvetica', 10), width=10, background='#E5EFC1', command=LogOut).grid(row=3, column=1, sticky='e')

    window.mainloop()

def ResultWindow(user):
    window = Tk()

    window.configure(bg='#39AEA9')
    window.title('Results')
    window.resizable(False, False)

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    winWidth = 700
    winHeight = 250

    x = (screen_width/2) - (winWidth/2)
    y = (screen_height/2) - (winHeight/2)

    window.geometry('%dx%d+%d+%d' % (winWidth, winHeight, x, y))
    
    def GoBackCommand():
        window.destroy()
        ClientWindow(user)
        
    def visualizeChart():
        selected_index = listbox.curselection()
        if selected_index:
            selected_item = listbox.get(selected_index[0])
            smbclient.ClientConfig(username='BioTech2070', password='admin2070')    
            file = smbclient.open_file(f'\\DESKTOP-NESD1EN\\Users\\BioTech2070\\Documents\\BARNI\\FILE_SERVER\\results\\{selected_item}.txt', mode="r")
            results = file.readlines()
                        
            job = str(selected_item).split('_')
            
            if job[5] == 'Cell seed detection and counting':                      
                visualizer.barChartCellSeedDetection(results)                
                
            file.close()
    
    scrollbar = Scrollbar(window)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox = Listbox(window)
    listbox.pack(side=TOP, fill=X)
        
    #files = os.listdir(r'\\DESKTOP-NESD1EN\\Users\\BioTech2070\\Documents\\BARNI\\FILE_SERVER\\results\\')
    files = os.listdir(r'C:\\Users\\sasdi\\Documents\\Szakdolgozat_Project\\FILE_SERVER\\results')
    
    for i in files:
        filename = i.split('.')
        listbox.insert(END, filename[0])
    
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    
    print_button = Button(window, text="Show diagramms", font=('Helvetica', 10), background='#E5EFC1', command=visualizeChart)
    print_button.pack()
    
    backButton = Button(window, text='Go back',  font=('Helvetica', 10), background='#E5EFC1', command=GoBackCommand)
    backButton.pack(side=BOTTOM)
    
LoginWindow()