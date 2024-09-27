# Instructions for the Usage of My Reminding Program

You can add activities and remove them, and they will show up in a notification every n seconds, those being set by you in the beginning.

The purpose is that when you use your laptop, you become aware every once in a while and start to think about stopping procrastinating.

## Usage

install python from microsoft store-any version should be ok and open cmd prompt and use the following commands: 

```bash
sudo apt-get install pip        #only works for Linux, on windows you might already have it, if not install it
pip install plyer
pip install datetime
```

# IMPORTANT! only run the script when you are in the reminder_app directory!

## more about the program

Do not put strings bigger than 125 chars on a csv file row!!!

If you mistakenly added something wrong you can either remove and read or just open the csv file and change the data

If you have x rows in the csv you need to see x+1 in the VSCode file, and the mouse cursor has to be on the x+1th one

![Exemplu](https://github.com/0catalin/reminder_app/blob/master/exemplu.png)

It can't match TOO many activities (256 characters max per notification message)

For kiling the process I recommend a Ctrl + break or what alternatives there are on your computer


