# CheerLights Discord Bot
This bot was created for use in the CheerLights Discord Server.

It will allow you to get the current color and set a new color.

---

## Bot Commands

The bot uses a keyboard button interface to make life easier. 

To invoke the bot use ```/cheerlights``` and then follow the onscreen button prompts

## Installation/Setup

#### Installation Steps
1) Obtain API Keys
2) Install needed packages, clone Repo and install library dependencies
3) Configure the script

Remember that all the commands shared here are for Linux. So if you want you can run this on a Linux Server or even a Raspberry Pi.

If you want to run this on a Windows or Mac machine, you will need to install Python3 and be familiar installing from a requirements.txt.

#### Obtaining API Keys

The first step in this process will be obtaining the API keys that you need. 

###### Discord

* Go to: [https://discord.com/developers/applications](https://discord.com/developers/applications)
* Click ```New Application```
* Give it a name (I called it CheerLights)
* On the next screen, you can upload an avatar for the bot.
* Click the ```bot``` selection under settings
* Click ```Add Bot```
* Give it a Name (I used the same name )
* Then Copy the Bot Token (you will need this for the ```config.json``` part of the script)
* Turn off ```Public Bot```
* Make sure to turn on the ```Message Intents``` Setting under ```Privileged Gateway Intents```.
* Save Settings
* Click ```OAuth2``` and then ```URL Generator```
* For Scope Choose ```bot``` and ```appplications.commands```
* For Permissions, choose the following:
    - Under General Permissions:
        - Read Messages/View Channels
    - Under Text Permissions:
        - Send messages
        - Send Messages in threads
        - Embed Links
        - Attach Files
        - Read message History
        - Use Slash Commands
* Copy the generated URL
* Paste it into a browser window Address bar
* Choose the Server you want to authorize it to and then click authorize.
* It should pop into the server.
* Next you will need to get your server id.
  * To get this, you will need to, on Discord, go into ```User Settings```->```Advanced``` and turn on ```Developer Mode``` (if it is not already on.)
  * Then just right click on your server's icon and click ```Copy ID```. Then go back into your ```config.json``` and paste that ID in the ```server_id``` field.

Once you have the keys you need, you will eventually copy them into the appropriate places in the ```config.json``` file, but now we need to get the files and get things installed.


#### Installing the Script

The next step is installing the needed packages, cloning the repo to get the script and then installing the needed libraries for the script to work properly. 

This is probably the easiest step to accomplish.

Please run the following commands:

```bash
sudo apt-get update && sudo apt-get -y upgrade && sudo apt-get -y dist-upgrade

sudo apt-get install python3 python3-pip git screen

git clone https://github.com/cheerlights/cheerlights-discord-bot.git

cd cheerlights-discord-bot

pip3 install -r requirements.txt
```

Now you have everything installed and are ready to configure the script.

### Configure the Script
Once you have your API Keys, have cloned the repo and installed everything, you can now start configuring the bot. 

Open the ```config.json``` file in your editor of choice and copy in the keys you obtained from Discord into the appropriate spots and save.

Open the ```block_list.json``` file and remove the example rows. Leave the rest of the json structure, otherwise the program will error. See below on how to use the ```block_list.json``` file.

You will also need a webhook to send the messages to.


### Running the Script
Once you have the config file edited, the bot can be run 1 of two ways:

#### From the console

First you can run it in a screen session and let it run in the background:

```bash
screen -R cheerlights-discord-bot
```

Then in the new window:
```bash
cd cheerlights-discord-bot

python3 cheerlights_bot.py
```

It should say < Bot Name > has connected to Discord. Once that is done, hit ```CTRL-A-D``` to disconnect from the screen session. If something ever happens, you can reconnect to the session by typing:

```bash
screen -R cheerlights-discord-bot
```

#### Running in Docker (Recommended)

You can also run the bot in Docker. Make sure to have Docker installed and Docker-Compose installed.

Next, create two folders in the location where you are going to run the bot from:
* data
* log

Move the ```config.json``` and ```block_list.json``` files into the data folder (see below on how to use the block list).

Next, edit the ```docker-compose.yaml``` file.

Where it says 

```yaml
    volumes:
      - <full path to bot folder>/log/:/app/log/
      - <full path to bot folder>/data/config.json:/app/config.json
      - <full path to bot folder>/data/block_list.json:/app/block_list.json
```
Change where it says ```<full path to bot folder>``` to the path of where you have the bot located. (Example: ```/pi/home/cheerlights-discord-bot```).

Next run ```docker-compose build```

Once the build is complete, you can then run ```docker-compose up -d```. This should start the bot and have it connect.

### Block List

The ```block_list.json``` file allows the bot administrator to block users from using the bot. When edits are made to this file, they are automatically picked up by the script, so there is no need to restart the script or the container.

You will need to obtain the numeric userid of the user from Discord and copy it out.

Then paste it into the ```userid``` field in the json file. The ```username``` is where you put the username. This is more for reference in case you need to know who all is on the block list and who can be removed, etc. 

When a user is blocked, they will get a message in Discord that tells them they are blocked and will need to contact the bot administrator as to why and if they can be removed. They will not be able to use the interface when blocked.

---

## Change Log

- 05/02/2023 - Release 6.0
  - Addition of block list
  - Addition of logging
  - Removal of Twitter usage
  - Changed config.py to config.json
  - Moved from text commands to onscreen button interface
  - Updates to README.md

- 06/10/2022 - Release 3.0
  - Moved the commands interface to the new slash commands interface.
  - Updates to README.md file

- 01/30/2022 - Release 1.1
  - Refined how the color picker works in the code
  - Refined building the list of valid colors

- 12/21/2021 - Initial Release 1.0