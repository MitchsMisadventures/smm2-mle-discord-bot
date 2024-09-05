# Mitch's Level Exchange, A Super Mario Maker 2 Discord Bot!

A bot that allows the user to share and discover levels from Super Mario Maker 2 all from the comfort of their Discord server! 

## Table of Contents

* [Installation](#installation)
* [Project Structure](#project-structure)
* [Features and Commands](#features-and-commands)
* [Changelog](#changelog)

## Installation

Proper instructions with a requirements file and installation guide will be added once the bot is closer to completion.

## Project Structure

    .
    ├── main.py                   # Main start file.
    ├── commands.py               # Bot commands related to Levels
    ├── credits.py                # Bot commands related to Bot itself and owner (me!)
    ├── users.py                  # Bot commands related to User data.
    ├── creds.py                  # Area where you will place your Discord bot token! DON'T SHARE IT!
    ├── LICENSE
    └── README.md

## Features and Commands

### Level Commands

* [add](#add)
* [remove](#remove)
* [addclearvid](#addclearvid)
* [clearvid](#clearvid)

### User Commands

* [register](#register)
* [unregister](#unregister)
* [myid](#myid)

### Credit Commands

* [about](#about)
* [changelog](#changelog)
* [helpme](#helpme)

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

`!addclearvid LEV-ELC-ODE`

---

#### ClearVid

Allows you to a view a clear video for a level if one is associated with it.

`!clearvid LEV-ELC-ODE`

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

#### HelpMe

Gives a list of all available Bot commands.

`!helpme`

---

## Changelog

### Version 1.0
* Initial Bulk Upload
