from plyer import notification
import time
import csv
from datetime import datetime, timedelta
import os
import re
import sys

def main():
    sleep_time = get_sleep_time() # takes sleep time
    while True: # loops until a valid file is given
        filename = take_csv_file_input()
        try:
            with open(filename, 'r') as fisier:
                pass
            break    
        except FileNotFoundError:
            print(f"{filename} does not exist or isn't in reminder_app/ directory")

    while True: # loops until Ctrl + Break
        try:
            print("If you want to add or remove an activity press Ctrl + C")
            notify_me(filename, sleep_time) # loops the notification
        except KeyboardInterrupt: # when Ctrl + C is pressed it goes into another loop where you can pick if you want to add or remove activity
            while True:
                status = 0
                comanda = input("What do you want to do?\nadd an activity : press 1\neliminate activity : press 2\n") 
                if comanda == "1":
                    activity = check_activity()
                    date = check_date()
                    time = check_time()
                    addactivity(activity, date, filename, time)
                    break # break for getting out of the loop and getting into the big one and notifying
                elif comanda == "2":
                    activity = input("enter activity: ")
                    status = removeactivity(activity, filename)
                    if status == 1:
                        print("row eliminated with success")
                        break # break for getting out of the loop and getting into the big one and notifying
                    else:
                        print("retry to eliminate row")
                        break 

def addactivity(activity, end_date, filename, time):
    sigur = input("are you sure you want to add the activity\n yes: press 1\n no: press anything else\n")
    if sigur == "1" and (not does_the_activity_exist(activity, filename)): # adds activity if it doesn't exist and if there is confirmation given
        with open(filename, 'a') as fisier:
            fisier.write("\n") # an endline for safety
            fisier.write(f'"{activity}","{end_date}","{time}"\n')
    else:
        print("the activity exists already or you pressed something other than 1")

def removeactivity(activity, filename):
    sigur = input("are you sure you want to remove?\n yes: press 1\n no: press anything else\n") # confirmation for removing
    if sigur == "1":
        nrLiniiInvalide = 0
        with open(filename, 'r') as fisier:
            reader = csv.reader(fisier)
            for line in reader:
                if not(isCorrect(line)):
                    nrLiniiInvalide += 1 # counts InvalidLines
        with open(filename, 'r') as fisier:
            reader2 = csv.reader(fisier)
            rows = [row for row in reader2 if (isCorrect(row) and row[0] != activity)] 
            length = count_lines(filename) # counts file lines
            len_rows = len(rows) # counts all left lines after listification
        if len(rows) != length: # if it is different
            os.remove(filename) # removes file
            with open(filename, 'w') as fisier: #rewrites it with the list elements
                for row in rows:
                    if isCorrect(row): #might not be needed
                        fisier.write(f'"{row[0]}","{row[1]}","{row[2]}"\n')
                if length - len_rows == nrLiniiInvalide:
                    return 0
                else:
                    return 1
        else:
            return 0
    else:
        return 0

def date_key(row):
    if isCorrect(row): # function used in the sorted function
        return datetime.strptime((row[1] + row[2]), "%d/%m/%Y%H:%M")  
    else:
        return datetime.strptime("00", "%M" )

def notify_me(file, sleep_time):
    while True:
        lista = []
        listuta = []
        with open(file, 'r') as fisier:
            reader = csv.reader(fisier)
            for line in reader:
                if isCorrect(line):
                    listuta.append(line)  # puts all the valid lines in a list

        for line in listuta:
            if int(date_to_current_difference(line[1] + line[2])) > 0:
                removeactivityforsure(line[0], file) # removes all activities with gone deadlines
        string = ""
        with open(file, 'r') as fisier:
            reader = csv.reader(fisier)
            sorted_reader = sorted(reader, key = date_key) # has all the valid activities sorted
            for row in sorted_reader:
                if isCorrect(row):
                    if len(row) > 130:
                        sys.exit("Row way too big")
                    if (len(string) + len(row[0]) + len(row[1]) + len(row[2]) + 22) < 150:
                        string = string + f"Activity: {row[0]}, date: {row[1]} {row[2]}\n" # adds activities in strings until 150 characters
                    else: 
                        lista.append(string)
                        string = f"Activity: {row[0]}, date: {row[1]} {row[2]}\n"
            if string != "":
                lista.append(string) # adds unadded string in list
            if string != "":
                for string in lista: # notifies every 5 seconds until all the strings from the list end
                    notification.notify(
                    title="Reminder to stop procrastinating",
                    message=string
                    )
                    time.sleep(5)
            else:
                notification.notify(
                title="Free day!",
                message="You are free! For now ;)"
                )
        time.sleep(sleep_time) # sleeps for how much it is set

def count_lines(filename):
    with open(filename, 'r') as file:
        line_count = sum(1 for line in file)  
    return line_count

# Function that calculates the difference between the current time and the activity date to know which ones to remove from the list

def date_to_current_difference(date_str):
    date = datetime.strptime(date_str, "%d/%m/%Y%H:%M")
    current_date = datetime.now()
    difference = (current_date - date).total_seconds()
    return difference

# removes an activity without confirmation 

def removeactivityforsure(activity, filename):
    with open(filename, 'r') as fisier:
        reader2 = csv.reader(fisier)
        rows = [row for row in reader2 if (isCorrect(row) and row[0] != activity)] 
    os.remove(filename)
    with open(filename, 'w') as fisier:
        for row in rows:
            fisier.write(f'"{row[0]}","{row[1]}","{row[2]}"\n')

# functions for checking Input

def get_sleep_time():
    while True:
        try:
            numar = int(input("give an interval for notifications - integer (number of seconds) : "))
            if numar >= 60:
                return numar
            else:
                print("Value lower than 60, you might want to change")
        except ValueError:
            print("Not an integer")
            pass

def take_csv_file_input():
    wish = input("do you want to add an own .csv file or do you want to work with the implemented one?\nimplemented one: press 1\nanother one: press anything else\n")
    if wish == '1':
        return "reminder.csv"
    else:
        while True:
            filename = input("give csv file name, don't forget to add .csv extension: ")
            match = re.search(r"^.+\.csv$", filename)
            if match:
                return filename
            else:
                print("you did not enter a .csv file")

def check_date():
    pattern = r'^(((0[1-9]|[12][0-9]|30)[-/]?(0[13-9]|1[012])|31[-/]?(0[13578]|1[02])|(0[1-9]|1[0-9]|2[0-8])[-/]?02)[-/]?[0-9]{4}|29[-/]?02[-/]?([0-9]{2}(([2468][048]|[02468][48])|[13579][26])|([13579][26]|[02468][048]|0[0-9]|1[0-6])00))$'
    while True:
        date = input("enter date: ")
        match = re.search(pattern, date)
        if match:
            return date
        else:
            print("you need to enter a valid date format: dd/mm/yyyy")

def check_time():
    pattern = r'^(?:[01][0-9]|2[0-3]):[0-5][0-9]$'
    while True:
        time = input("enter time(example : 23:58 format): ")
        match = re.search(pattern, time)
        if match:
            return time
        else:
            print("you need to enter a valid time format: hh/mm")

def check_activity():
    while True:
        activity = input("enter activity: ")
        if activity != "":
            return activity

# Checks whether a row from the csv is in the right format
def isCorrect(row):
    if len(row) != 3:
        return False
    cuvant = ",".join(row)
    pattern = r'^.+,(((0[1-9]|[12][0-9]|30)[-/]?(0[13-9]|1[012])|31[-/]?(0[13578]|1[02])|(0[1-9]|1[0-9]|2[0-8])[-/]?02)[-/]?[0-9]{4}|29[-/]?02[-/]?([0-9]{2}(([2468][048]|[02468][48])|[13579][26])|([13579][26]|[02468][048]|0[0-9]|1[0-6])00)),(?:[01][0-9]|2[0-3]):[0-5][0-9]$'
    match = re.search(pattern, cuvant)
    if match:
        return True
    else:
        return False

# Checks whether the activity is in the csv file

def does_the_activity_exist(activity, filename):
    with open(filename, 'r') as fisier:
        reader = csv.reader(fisier)             
        for line in reader:
            if isCorrect(line):
                if line[0] == activity:
                    return True
    return False

if __name__ == "__main__":
    main()