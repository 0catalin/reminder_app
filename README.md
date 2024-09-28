# The motivation of my program

- something to remind you while you're on your PC or laptop that you are supposed to do tasks in the future

- something that will send you notifications every n seconds while you are on

- something that shows the tasks in the order of the deadlines of each task

- something that eliminates tasks after the deadline is over

- something where you are able to insert the tasks and remove them manually or through the terminal

- something that doesn't crash when getting wrong input

# Instructions for the Usage of My Reminding Program

You can add activities and remove them, and they will show up in a notification sorted by the set deadline time every n seconds, those being set by you in the beginning.

The purpose is that when you use your laptop, you become aware that you should be working and not playing games and start to think about stopping procrastinating :)

## Things to install before Usage

Install python from microsoft store-any version should be ok and open cmd prompt and use the following commands: 

```bash
sudo apt-get install pip        #this line only works on Linux, on Windows you might already have it, if not you have to install it
pip install plyer
pip install datetime
```
## Running the program

Change directory until you reach the reminder_app directory with "cd 'directory'" then run "python remind_me.py"

![Exemplu2](https://github.com/0catalin/reminder_app/blob/master/exemplu2.png)

# IMPORTANT! only run the script when you are in the reminder_app directory!

# Each activity must be on one line and in the right format, if you change the csv file manually it might not work if you put in the wrong format

## More about the program

Do not have 2 activities with the same name! It WILL cause issues!!!

If you mistakenly added something wrong you can either remove and read or just open the csv file and change the data

It can work with a lot of activities as long as the refresh time is big enough, but it will display everything in A LOT OF notifications (256 characters max per notification message) 

For stopping the program I recommend a Ctrl + break or what alternatives there are on your computer ( on mine Ctrl + Fn + B works )

# For any bugs contact me