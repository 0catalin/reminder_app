from plyer import notification
import time
import csv
from datetime import datetime, timedelta
import os
import re
import sys

def main():
    sleep_time = get_sleep_time()
    lista = []
    while True:
        filename = take_csv_file_input()
        try:
            with open(filename, 'r') as fisier:
                reader = csv.reader(fisier)
                for line in reader:
                    lista.append(line)
            break    
        except FileNotFoundError:
            print(f"{filename} does not exist")

    for line in lista:
        if int(date_to_current_difference(line[1])) > 0:
            removeactivityforsure(line[0], filename)

    while True:
        try:
            print("If you want to add or remove press Ctrl + C")
            notify_me(filename, sleep_time)
        except KeyboardInterrupt:
            while True:
                status = 0
                comanda = input("Ce vrei sa faci?\nadaugare activitate : apasa 1\neliminare activitate : apasa 2\n")
                if comanda == "1":
                    activity = input("enter activity: ")
                    date = check_date()
                    addactivity(activity, date, filename)
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

def addactivity(activity, end_date, filename):
    sigur = input("esti sigur ca vrei sa adaugi activitate\n da: apasa 1\n nu: apasa orice altceva\n")
    if sigur == "1":
        with open(filename, 'a') as fisier:
            fisier.write(f"{activity},{end_date}\n")
    else:
        pass

def removeactivity(activity, filename):
    sigur = input("esti sigur ca vrei sa dai remove?\n da: apasa 1\n nu: apasa orice altceva\n")
    if sigur == "1":
        with open(filename, 'r') as fisier:
            reader = csv.reader(fisier)
            rows = [row for row in reader if row[0] != activity]
            length = count_lines(filename)
        if len(rows) != length:
            os.remove(filename)
            with open(filename, 'w') as fisier:
                for row in rows:
                    fisier.write(f"{row[0]},{row[1]}\n")
                return 1
        else:
            return 0
    else:
        return 0

def date_key(row):
    return datetime.strptime(row[1], "%d/%m/%Y")  

def notify_me(file, sleep_time):
    lista = []
    while True:
        string = ""
        with open(file, 'r') as fisier:
            reader = csv.reader(fisier)
            sorted_reader = sorted(reader, key = date_key)
            for row in sorted_reader:
                if len(row) > 130:
                    sys.exit("Row way too big")
                if (len(string) + len(row[0]) + len(row[1]) + 22) < 150:
                    string = string + f"Activitate: {row[0]}, data: {row[1]}\n"
                else: 
                    lista.append(string)
                    string = f"Activitate: {row[0]}, data: {row[1]}\n"
            if string != "":
                lista.append(string)
            if string != "":
                for string in lista:
                    notification.notify(
                    title="Message",
                    message=string
                    )
                    time.sleep(5)
            else:
                notification.notify(
                title="Message",
                message="You are free! For now ;)"
                )
        time.sleep(sleep_time)


def count_lines(filename):
    with open(filename, 'r') as file:
        line_count = sum(1 for line in file)  
    return line_count

def date_to_current_difference(date_str):
    date = datetime.strptime(date_str, "%d/%m/%Y")
    current_date = datetime.now()
    difference = (current_date - date).days
    return difference


def removeactivityforsure(activity, filename):
    with open(filename, 'r') as fisier:
        reader = csv.reader(fisier)
        rows = [row for row in reader if row[0] != activity]
        # print(rows)
    os.remove(filename)
    with open(filename, 'w') as fisier:
        for row in rows:
            fisier.write(f"{row[0]},{row[1]}\n")

def get_sleep_time():
    while True:
        try:
            numar = int(input("give me an interval for notifications - integer : "))
            if numar > 60:
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
    
main()



