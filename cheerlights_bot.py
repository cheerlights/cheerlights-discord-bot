#!/usr/bin/env python

#################################################################################

# CheerLights Discord Server Bot
# Developed by: Jeff Lehman, N8ACL
# Date: 04/18/2023
# Current Version: 6.0
# https://github.com/cheerlights/cheerlights-discord-bot

# Questions? Comments? Suggestions? Contact me one of the following ways:
# E-mail: n8acl@qsl.net
# Discord: Ravendos
# Mastodon: @n8acl@mastodon.radio
# Website: https://www.qsl.net/n8acl

#############################
# Import Libraries
# import config as cfg
import os
import json
import requests
import discord # Discord library
from datetime import datetime, date, time, timedelta
import time

#############################
# import config json file

with open("config.json", "r") as read_file:
    config = json.load(read_file)

#############################
# Create Discord Bot
TOKEN = config['discord']['bot_token']
activity = discord.Activity(type=discord.ActivityType.listening, name='/cheerlights')
bot = discord.Bot(debug_guilds=[config['discord']['server_id']], activity=activity, status=discord.Status.online)

#############################
# Define Variables
# DO NOT CHANGE BELOW

cheerlights_api_url = 'http://api.thingspeak.com/channels/1417/field/2/last.json'
linefeed = "\r\n"
rate_limiter = {}
button_timeout = 5

color_pick = {
    "red" : "#FF0000",
    "green" : "#008000",
    "blue" : "#0000FF",
    "cyan" :"#00FFFF",
    "white" : "#FFFFFF",
    "oldlace" : "#FDF5E6",
    "purple" : "#800080",
    "magenta" : "#FF00FF",
    "yellow" : "#FFFF00",
    "orange" : "#FFA500",
    "pink" : "#FFC0CB"
}

#############################
# Define Functions

def use_api():
    # Pulls latest Color from Cheerlights API

    r = requests.get(cheerlights_api_url, timeout=None)
    json = r.json()
    return json['field2']

def hex_to_rgb(col_hex):
    #Convert a hex colour to an RGB tuple.

    col_hex = col_hex.lstrip('#')
    return bytearray.fromhex(col_hex)

def get_key(val, my_dict):
    # Return the Key from a value in a dictionary

    for key, value in my_dict.items():
         if val == value:
             return key

def valid_colors():
    # Returns list of valid colors

    valid_colors = ''

    for item in list(color_pick.keys()):
        valid_colors = valid_colors + item + linefeed

    return valid_colors

def send_to_webhook(msg,wh_url):
    response = requests.post(
        wh_url, data=json.dumps(msg),
        headers={'Content-Type': 'application/json'},
        auth = (config['wh_user'],config['wh_password'])
    )

def logging(log_message):
    today = date.today()
    bot_log_file = os.path.dirname(os.path.abspath(__file__)) + "/log/cheerlights_bot_log-" + today.strftime("%m%d%Y") + ".txt"

    with open(bot_log_file,"a") as f:
        f.write(log_message)
    f.close()

def get_block_list():

    block_list = []

    with open("block_list.json", "r") as read_file:
        blocked_users = json.load(read_file)
    
    for i in range(0,len(blocked_users["block_list"])):
        for key, value in blocked_users["block_list"][i].items():
            if key == "userid":
                block_list.append(value)
    
    return block_list

def set_color(color, author, user_id):

    now = int(time.time())
    block_list = get_block_list()

    if user_id not in block_list:

        if user_id not in rate_limiter:
            rate_limiter[user_id] = 9999999

        if rate_limiter[user_id] == 9999999 or (now - rate_limiter[user_id] >= config['msg_wait_time']):
            rate_limiter[user_id] = now
            color_code = color_pick[color.lower()]

            embed = discord.Embed(title = "Setting CheerLights to Color",
                description=color.lower(),
                color=int(color_code.lstrip('#'), 16)
            )

            now = datetime.now()
            timestamp = now.strftime("%m/%d/%Y %H:%M:%S")

            status = "Set @CheerLights to " + color + " on " + timestamp

            cl_msg = {'source': 'discord', 'colours': [color], 'username': author}
            send_to_webhook(cl_msg, config['cl_wh'])

            if config['logging_enabled']:
                logging(timestamp + " - " + author + "(" + user_id + ") | command: set_color | status: " + status + linefeed)

        else:
            response = "Slow down there sport! You are trying to send colors way too fast. Please wait "+ str(config['msg_wait_time']) + " seconds before trying again."
            
            embed = discord.Embed(title = "Too Fast!",
                description=response
            )

    else:
        now = datetime.now()
        timestamp = now.strftime("%m/%d/%Y %H:%M:%S")
        if config['logging_enabled']:
            logging(timestamp + " - " + author + "(" + author + ") | User Blocked" + linefeed)

        response = "Sorry, but this user has been blocked from sending colors due to spamming. If this is in error, please contact an Admin."

        embed = discord.Embed(title = "User Blocked",
            description=response
        )

    return embed

#############################
# Define CheerLights Menu Functions

class ColorSelect(discord.ui.View):

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(content="Set Color", view=self)


    @discord.ui.button(label="Red", row=0, style=discord.ButtonStyle.primary)
    async def set_color_red(self, button, interaction):
        user = str(interaction.user)
        userid = str(interaction.user.id)
        await interaction.response.send_message(embed=set_color("red", user, userid),ephemeral = True)

    @discord.ui.button(label="Green", row=0, style=discord.ButtonStyle.primary)
    async def set_color_green(self, button, interaction):
        user = str(interaction.user)
        userid = str(interaction.user.id)
        await interaction.response.send_message(embed=set_color("green", user, userid),ephemeral = True)

    @discord.ui.button(label="Blue", row=0, style=discord.ButtonStyle.primary)
    async def set_color_blue(self, button, interaction):
        user = str(interaction.user)
        userid = str(interaction.user.id)
        await interaction.response.send_message(embed=set_color("blue", user, userid),ephemeral = True)

    @discord.ui.button(label="Cyan", row=0, style=discord.ButtonStyle.primary)
    async def set_color_cyan(self, button, interaction):
        user = str(interaction.user)
        userid = str(interaction.user.id)
        await interaction.response.send_message(embed=set_color("cyan", user, userid),ephemeral = True)

    @discord.ui.button(label="White", row=1, style=discord.ButtonStyle.primary)
    async def set_color_white(self, button, interaction):
        user = str(interaction.user)
        userid = str(interaction.user.id)
        await interaction.response.send_message(embed=set_color("white", user, userid),ephemeral = True)

    @discord.ui.button(label="Oldlace", row=1, style=discord.ButtonStyle.primary)
    async def set_color_oldlace(self, button, interaction):
        user = str(interaction.user)
        userid = str(interaction.user.id)
        await interaction.response.send_message(embed=set_color("oldlace", user, userid),ephemeral = True)

    @discord.ui.button(label="Purple", row=1, style=discord.ButtonStyle.primary)
    async def set_color_purple(self, button, interaction):
        user = str(interaction.user)
        userid = str(interaction.user.id)
        await interaction.response.send_message(embed=set_color("purple", user, userid),ephemeral = True)

    @discord.ui.button(label="Magenta", row=1, style=discord.ButtonStyle.primary)
    async def set_color_magenta(self, button, interaction):
        user = str(interaction.user)
        userid = str(interaction.user.id)
        await interaction.response.send_message(embed=set_color("magenta", user, userid),ephemeral = True)

    @discord.ui.button(label="Yellow", row=2, style=discord.ButtonStyle.primary)
    async def set_color_yellow(self, button, interaction):
        user = str(interaction.user)
        userid = str(interaction.user.id)
        await interaction.response.send_message(embed=set_color("yellow", user, userid),ephemeral = True)

    @discord.ui.button(label="Orange", row=2, style=discord.ButtonStyle.primary)
    async def set_color_orange(self, button, interaction):
        user = str(interaction.user)
        userid = str(interaction.user.id)
        await interaction.response.send_message(embed=set_color("orange", user, userid),ephemeral = True)

    @discord.ui.button(label="Pink", row=2, style=discord.ButtonStyle.primary)
    async def set_color_pink(self, button, interaction):
        user = str(interaction.user)
        userid = str(interaction.user.id)
        await interaction.response.send_message(embed=set_color("pink", user, userid),ephemeral = True)


class MainMenu(discord.ui.View):

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(content="CheerLight Commands", view=self)


    @discord.ui.button(label="Get Color", style=discord.ButtonStyle.primary)
    async def get_color(self, button, interaction):
        color_code = use_api()


        embed = discord.Embed(title = "Current CheerLights Color",
        description=get_key(color_code.upper(),color_pick),
        color=int(color_code.lstrip('#'), 16)
        )

        await interaction.response.send_message(embed=embed,ephemeral = True)

    @discord.ui.button(label="Set Color", style=discord.ButtonStyle.primary)
    async def set_color(self, button, interaction):
        await interaction.response.send_message("Set Color", view = ColorSelect(timeout = button_timeout), ephemeral = True)

#############################
# Define Discord Bot Functions

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.slash_command()
async def cheerlights(ctx):
    await ctx.respond("CheerLight Commands", view=MainMenu(timeout= button_timeout), ephemeral = True)

#############################
# Main Program

# Start Bot
bot.run(TOKEN)