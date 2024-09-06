# Mitch's Level Exchange, A Super Mario Maker 2 Discord Bot!

A bot that allows the user to share and discover levels from Super Mario Maker 2 all from the comfort of their Discord server! 

## Table of Contents

* [Bot Installation](#bot-installation)
* [Requirements](#requirements)
* [Project Structure](#project-structure)
* [Features and Commands](#features-and-commands)
* [Changelog](#changelog)
* [To Do](#to-do)

## Bot Installation

Click the following link to get the bot installed on your server! 

[Link will go here once Version 1.0 is released!] :) 

## Requirements

All required libraries can be found in the `requirements.txt` file. If you want to directly install them into your environment, run the following command:

```
pip install -r requirements.txt
```

## Project Structure

    .
    ├── commands 
    │       ├── clearvideos.py            # Bot commands related to Clear Videos  
    │       ├── credits.py                # Bot commands related to Bot itself and owner (me!)
    │       ├── levels.py                 # Bot commands related to Levels
    │       └── users.py                  # Bot commands related to User data.
    ├── .gitignore    
    ├── CHANGELOG.md
    ├── LICENSE              
    ├── README.md            
    ├── creds.py                          # Area where you will place your Discord bot token! ⚠️
    ├── main.py                           # Main start file.
    └── requirements.txt         
     

## Features and Commands

### Level Commands

* [add](#add)
* [remove](#remove)

### Clear Video Commands

* [addclearvid](#addclearvid)
* [clearvid](#clearvid)
* [removeclearvid](#removeclearvid)

### User Commands

* [register](#register)
* [unregister](#unregister)
* [myid](#myid)

### Credit Commands

* [about](#about)
* [changelog](#changelog)
* [help](#help)

---

#### Add 

Allows you to add a level to the database!

`!add LEV-ELC-ODE`

---

#### Remove

Allows you to remove a level from the database. However, this only works by the user that added the level *or* if the user is unregistered.

`!remove LEV-ELC-ODE`

---

#### AddClearVid

Allows you to add a Clear Video to a level if one is not already associated with it.

`!addclearvid LEV-ELC-ODE VIDEO_URL`

---

#### ClearVid

Allows you to a view a clear video for a level if one is associated with it.

`!clearvid LEV-ELC-ODE`

---

#### RemoveClearVid

Allows you to remove a clear video for a level if User is one that uploaded it.

`!removeclearvid LEV-ELC-CODE`

---

#### Register

Allows User to link their Maker ID to their Discord User.

`!register MAK-ERC-ODE`

---

#### Unregister

Allows user to unlink their Maker ID from their Discord User.

`!unregister MAK-ERC-ODE`

---

#### MyID

Bot tells Maker ID of User who summoned command if they have one registered.

`!myid`

---

#### About

Gives general bot information such as Version Number and links to the Creator (me!)

`!about`

---

#### Changelog

Gives a short list of the most recent changes made to the bot. For the full list of changes, you'll have to click here.

`!changelog`

---

#### Help

Gives a list of all available Bot commands.

`!help`

---

## Changelog

You can access the CHANGELOG by checking the `CHANGELOG.md` file or click [here](https://github.com/MitchsMisadventures/smm2-mle-discord-bot/blob/main/CHANGELOG.md)!

---

## To Do

* Create database wide commands
* * Give the ability to view all levels from server, all levels from user, remove all user levels etc.
* Create SMM2 profile commands


