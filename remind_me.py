from plyer import notification
import time
import csv
from datetime import datetime, timedelta
import os
import re
import sys

def main():
    sleep_time = get_sleep_time()
    while True:
        filename = take_csv_file_input()
        try:
            with open(filename, 'r') as fisier:
                pass
            break    
        except FileNotFoundError:
            print(f"{filename} does not exist")

    while True:
        try:
            print("If you want to add or remove an activity press Ctrl + C")
            notify_me(filename, sleep_time)
        except KeyboardInterrupt:
            while True:
                status = 0
                comanda = input("What do you want to do?\nadd an activity : press 1\neliminate activity : press 2\n")
                if comanda == "1":
                    activity = check_activity()
                    date = check_date()
                    time = check_time()
                    addactivity(activity, date, filename, time)
                    break
                elif comanda == "2":
                    activity = input("enter activity: ")
                    status = removeactivity(activity, filename)
                    if status == 1:
                        print("row eliminated with success")
                        break
                    else:
                        print("retry to eliminate row")
                        break

def addactivity(activity, end_date, filename, time):
    sigur = input("are you sure you want to add the activity\n yes: press 1\n no: press anything else\n")
    if sigur == "1":
        with open(filename, 'a') as fisier:
            fisier.write("\n")
            fisier.write(f'"{activity}","{end_date}","{time}"\n')
    else:
        pass

def removeactivity(activity, filename):
    sigur = input("are you sure you want to remove?\n yes: press 1\n no: press anything else\n")
    if sigur == "1":
        nrLiniiInvalide = 0
        with open(filename, 'r') as fisier:
            reader = csv.reader(fisier)
            for line in reader:
                if not(isCorrect(line)):
                    nrLiniiInvalide += 1
        with open(filename, 'r') as fisier:
            reader2 = csv.reader(fisier)
            rows = [row for row in reader2 if (isCorrect(row) and row[0] != activity)] # aici e problema
            length = count_lines(filename)
            len_rows = len(rows)
        if len(rows) != length:
            os.remove(filename)
            with open(filename, 'w') as fisier:
                for row in rows:
                    if isCorrect(row): # might not need this, logically
                        fisier.write(f"{row[0]},{row[1]},{row[2]}\n")
                if length - len_rows == nrLiniiInvalide:
                    return 0
                else:
                    return 1
        else:
            return 0
    else:
        return 0

def date_key(row):
    if isCorrect(row):
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
                    listuta.append(line)

        for line in listuta:
            if int(date_to_current_difference(line[1] + line[2])) > 0:
                removeactivityforsure(line[0], file)
        string = ""
        with open(file, 'r') as fisier:
            reader = csv.reader(fisier)
            sorted_reader = sorted(reader, key = date_key)
            for row in sorted_reader:
                if isCorrect(row):
                    if len(row) > 130:
                        sys.exit("Row way too big")
                    if (len(string) + len(row[0]) + len(row[1]) + len(row[2]) + 22) < 150:
                        string = string + f"Activity: {row[0]}, date: {row[1]} {row[2]}\n"
                    else: 
                        lista.append(string)
                        string = f"Activity: {row[0]}, date: {row[1]} {row[2]}\n"
            if string != "":
                lista.append(string)
            if string != "":
                for string in lista:
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
        time.sleep(sleep_time)


def count_lines(filename):
    with open(filename, 'r') as file:
        line_count = sum(1 for line in file)  
    return line_count

def date_to_current_difference(date_str):
    date = datetime.strptime(date_str, "%d/%m/%Y%H:%M")
    current_date = datetime.now()
    difference = (current_date - date).total_seconds()
    return difference


def removeactivityforsure(activity, filename):
    with open(filename, 'r') as fisier:
        reader = csv.reader(fisier)
        rows = [row for row in reader if row[0] != activity]
        # print(rows)
    os.remove(filename)
    with open(filename, 'w') as fisier:
        for row in rows:
            if isCorrect(row):
                fisier.write(f"{row[0]},{row[1]},{row[2]}\n")

def get_sleep_time():
    while True:
        try:
            numar = int(input("give me an interval for notifications - integer : "))
            if numar >= 60:
                return numar
            else:
                print("Value lower than 60, you might want to change")
        except ValueError:
            print("Not an integer")
            pass

def take_csv_file_input():
    while True:
        filename = input("give csv file name, don't forget to add .csv extension: ")
        match = re.search(r"^.+.csv$", filename)
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


main()

