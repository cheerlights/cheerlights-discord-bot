# CheerLights Discord Bot
This bot was created for use in the CheerLights Discord Server.

It will allow you to get the current color, set a new color and list valid colors.

---

# Installation/Setup

### Installation Steps
1) Obtain API Keys
2) Install needed packages, clone Repo and install library dependencies
3) Configure the script

Remember that all the commands shared here are for Linux. So if you want you can run this on a Linux Server or even a Raspberry Pi.

If you want to run this on a Windows or Mac machine, you will need to install Python3 and be familiar installing from a requirements.txt.

### Obtaining API Keys

The first step in this process will be obtaining the API keys that you need. Some of the services you choose to use may take a couple of days to approve the access to their API's, so you will want to start this step before installing the script. That way when you are done installing the script and are ready to configure, you have everything ready to go.

##### Twitter

You will need to create a new app and get a consumer key, consumer secret, access token and access secret for the account you are wanting to post to. You can get those keys from the Twitter development site. Here is a walk through how: [Generate Twitter API Keys](https://www.slickremix.com/docs/how-to-get-api-keys-and-tokens-for-twitter/)

Note that it takes a couple of days to get your app approved.

##### Discord

* Go to: [https://discord.com/developers/applications](https://discord.com/developers/applications)
* Click New Application
* Give it a name (I called it Cheerlights bot)
* On the next screen, you can upload an avatar for the bot.
* Click the bot selection under settings
* Click Add Bot
* Give it a Name (I used the same name )
* Then Copy the Bot Token (you will need this for the config.py part of the script along with the twitter keys)
* Do not set as public bot (you only want this on servers you are in)
* Save Settings
* Click OAuth2 and then URL Generator
* Click OAuth2 and then URL Generator
* For Scope Choose bot
* For Permissions, choose the following:
    - Under General Permissions:
        - Read Messages/View Channels
    - Under Text Permissions:
        - Send messages
        - Send Messages in threads
        - Embed Links
        - Read message History
        - Use Slash Commands
* Copy the generated URL
* Paste it into a browser window Address bar
* Choose the Server you want to authorize it to and then click authorize.
* It should pop into the server.

Once you have the keys you need, you will eventually copy them into the appropriate places in the config.py file, but now we need to get the files and get things installed.


### Installing the Script

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

## Configure the Script
Once you have your API Keys, have cloned the repo and installed everything, you can now start configuring the bot. Open the config.py file in your editor of choice and copy in the keys you obtained from Twitter and Discord into the appropriate spots.


## Running the Script

Once you have the config file edited, start the bot by typing the following:

```bash
screen -R cheerlights-discord-bot
```

Then in the new window:
```bash
cd cheerlights-discord-bot

python3 cheerlights_bot.py
```

It should say <bot Name> has connected to Discord. Once that is done, hit CTRL-A-D to disconnect from the screen session. If something ever happens, you can reconnect to the session by typing:

```bash
screen -R cheerlights-discord-bot
```