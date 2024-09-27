# Instructions for the Usage of My Reminding Program

You can add activities and remove them, and they will show up in a notification every n seconds, those being set by you in the beginning.

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

## more about the program

Do not put strings bigger than 125 chars on a csv file row!!!

If you mistakenly added something wrong you can either remove and read or just open the csv file and change the data

If you have x rows in the csv you need to see x+1 in the VSCode file, and the mouse cursor has to be on the x+1th one

![Exemplu](https://github.com/0catalin/reminder_app/blob/master/exemplu.png)

Explanation : As you see there are only 2 written lines, the 3rd line has the cursor on it and there are only 3 lines in total

It can't match TOO many activities (256 characters max per notification message)

For stopping the program I recommend a Ctrl + break or what alternatives there are on your computer ( on mine Ctrl + Fn + B works )

# For any bugs contact me