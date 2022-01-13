#################################################################################

# CheerLights Discord Server Bot
# Developed by: Jeff Lehman, N8ACL
# Date: 12/22/2021
# Current Version: 1.0
# https://github.com/cheerlights/cheerlights-discord-bot

# Questions? Comments? Suggestions? Contact me one of the following ways:
# E-mail: n8acl@qsl.net
# Twitter: @n8acl
# Discord: Ravendos#7364
# Mastodon: @n8acl@mastodon.radio
# Website: https://www.qsl.net/n8acl

#############################
# Import Libraries
import config
import os
import json
import requests
import discord
import tweepy
from datetime import datetime, date, time, timedelta
from tweepy import OAuthHandler
from discord.ext import commands


#############################
# Create Discord Bot
TOKEN = config.discord_bot_token
bot = commands.Bot(command_prefix='/', help_command = None)

#############################
# Twitter API Object Configuration
auth = OAuthHandler(config.twitterkeys["consumer_key"], config.twitterkeys["consumer_secret"])
auth.set_access_token(config.twitterkeys["access_token"], config.twitterkeys["access_secret"])

twitter = tweepy.API(auth)

#############################
# Define Variables
# DO NOT CHANGE BELOW

cheerlights_api_url = 'http://api.thingspeak.com/channels/1417/field/2/last.json'
linefeed = "\r\n"

color_pick_hex = {
    "#FF0000": "red",
    "#008000": "green",
    "#0000FF": "blue",
    "#00FFFF": "cyan",
    "#FFFFFF": "white",
    "#FDF5E6": "oldlace",
    "#FDF5E6": "warmwhite",
    "#800080": "purple",
    "#FF00FF": "magenta",
    "#FFFF00": "yellow",
    "#FFA500": "orange",
    "#FFC0CB": "pink"
}

color_pick_name = {
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

valid_color_list = """
    red
    green
    blue
    cyan
    white
    oldlace
    purple
    magenta
    yellow
    orange
    pink
"""


#############################
# Define Functions

def use_api():
    r = requests.get(cheerlights_api_url, timeout=None)
    json = r.json()
    return json['field2']

def hex_to_rgb(col_hex):
    """Convert a hex colour to an RGB tuple."""
    col_hex = col_hex.lstrip('#')
    return bytearray.fromhex(col_hex)


#############################
# Define Discord Bot Functions

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='cheerlights')
async def get_color(ctx, color = 'none'):
    
    if color == 'none':
        color_code = use_api()
        r, g, b = hex_to_rgb(color_code)

        embed = discord.Embed(title = "Current CheerLights Color",
            description=color_pick_hex[color_code.upper()],
            colour=discord.Color.from_rgb(r,g,b)
        )
        # await ctx.send(embed = embed)
    elif color == 'list':
        embed = discord.Embed(title = "Valid CheerLights Colors",
        description=valid_color_list
        )
        #await ctx.send(embed = embed)
    else:
        if color.lower() in color_pick_name:
            color_code = color_pick_name[color.lower()]
            r, g, b = hex_to_rgb(color_code)

            embed = discord.Embed(title = "Setting CheerLights to Color",
                description=color.lower(),
                colour=discord.Color.from_rgb(r,g,b)
            )
            #await ctx.send(embed = embed)

            now = datetime.now()
            timestamp = now.strftime("%m/%d/%Y %H:%M:%S")

            status = "Set @CheerLights to " + color + " on " + timestamp

            print(status)
            twitter.update_status(status)

        else:

            response = "That is an invalid color. Valid colors are:" + linefeed
            response = response + valid_color_list

            embed = discord.Embed(title = "Invalid CheerLights Color",
                description=response
            )
            #await ctx.send(embed = embed)
    await ctx.send(embed = embed)


@bot.command(name='help')
async def help(ctx):

    cmd_list = """
    /cheerlights - Returns the current CheerLights Color.

    /cheerlights <color> - Set CheerLights to this <color>. ex: /cheerlights red

    /cheerlights list - Lists the valid colors that can be used for CheerLights.

    """

    embed = discord.Embed(title = "CheerLights Bot Commands",
        description=cmd_list
    )
    await ctx.send(embed = embed)

#############################
# Main Program

# Start Bot
bot.run(TOKEN)