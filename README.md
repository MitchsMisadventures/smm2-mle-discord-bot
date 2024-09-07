# Mitch's Level Exchange, A Super Mario Maker 2 Discord Bot!

A bot that allows the user to share and discover levels from Super Mario Maker 2 all from the comfort of their Discord server! 
| ![Image 1](https://github.com/user-attachments/assets/74805261-f54c-400b-9d1c-420d414723f8) | ![Image 2](https://github.com/user-attachments/assets/da7c169e-8344-4bac-b385-32a15e688fc6) |
|:---:|:---:|
| ![Image 3](https://github.com/user-attachments/assets/1bd23cb2-0ad1-4414-9884-8edff1dbae87) | ![Image 4](https://github.com/user-attachments/assets/11a03c32-fae2-4453-896f-8f03fd5e7c3f) |





## Table of Contents

* [Bot Installation](#bot-installation)
* [Requirements](#requirements)
* [Project Structure](#project-structure)
* [Features and Commands](#features-and-commands)
* [Changelog](#changelog)
* [To Do](#to-do)

## Bot Installation

Click the following link to get the bot installed on your server! 

🌱 [Mitch's Level Exchange](https://discord.com/oauth2/authorize?client_id=1280663533503123469)

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
    │       ├── helpc.py                  # Bot commands related to Help
    │       ├── levels.py                 # Bot commands related to Levels
    │       ├── tables.py                 # Bot commands related to Table Queries
    │       ├── users.py                  # Bot commands related to User data
    │       └── viewer.py                 # Bot commands related to Level Viewer
    ├── .gitignore    
    ├── CHANGELOG.md
    ├── LICENSE              
    ├── README.md            
    ├── creds.py                          # Area where you will place your Discord bot token! ⚠️
    ├── main.py                           # Main start file.
    └── requirements.txt         
     

## Features and Commands

### Clear Video Commands

* [addclearvid](#addclearvid)
* [clearvid](#clearvid)
* [removeclearvid](#removeclearvid)

### Credits Commands

* [about](#about)

### Help Commands

* [help](#help)
* [help2](#help2)

### Level Commands

* [add](#add)
* [remove](#remove)

### Table Commands

* [mylevels](#mylevels)
* [random](#random)
* [levelcount](#levelcount)


### User Commands

* [register](#register)
* [unregister](#unregister)
* [myid](#myid)

### Viewer Commands

* [peek](#register)
* [viewer](#unregister)
* [viewersimple](#myid)

---

#### About

Returns general infomration about bot and creator!

`!about`

---

#### Add

Allows you to add a level to the server's list!

`!add LEV-ELC-ODE`

---

#### AddClearVid

Allows you to add a clear video to a level from the server.

`!addclearvid LEV-ELC-ODE URL`

---

#### ClearVid

Recalls Clear Video to a level if one is set.

`!clearvid LEV-ELC-ODE`

---

#### Help

Returns Page 1 of available bot commmands.

`!help`

---

#### Help2

Returns Page 2 of available bot commands.

`!help2`

---

#### LevelCount

Returns count of levels currently stored on the server.

`!LevelCount`

---

#### MyId

If registered, returns the Maker ID associated with the user.

`!myid`

---

#### MyLevels

Returns a list of levels User has submitted to the server.

`!mylevels`

---

#### Peek

Returns an image of the full overworld of a level.

`!peek LEV-ELC-ODE`

---

#### Random

Returns a random level from the server's level list.

`!random`

---

#### Register

Allows you to link Discord user with Super Mario Maker 2 Maker ID.

`!register MAK-ERC-ODE`

---

#### Remove

Removes level from server list.

`!remove LEV-ELC-ODE`

---

#### RemoveClearVid

Removes a Clear Video from a level if one is already assigned to it.

`!removeclearvid LEV-ELC-ODE`

---

#### Unregister

Allows you to unlink Discord user with Super Mario Maker 2 Maker ID.

`!unregister`

---

#### Viewer

Returns a direct link to the Wizul SMM2 Level Viewer for given level.

`!viewer LEV-ELC-ODE`

---

#### ViewerSimple

Returns a direct link to the Wizul SMM2 Level Viewer for given level *without* accessing API.

`!viewersimple LEV-ELC-ODE`

---

## Changelog

You can access the CHANGELOG by checking the `CHANGELOG.md` file or click [here](https://github.com/MitchsMisadventures/smm2-mle-discord-bot/blob/main/CHANGELOG.md)!

---

## To Do

* Improve database management
* Add more commands!


