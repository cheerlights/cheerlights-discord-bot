#################################################################################

# CheerLights Discord Server Bot
# Developed by: Jeff Lehman, N8ACL
# Date: 06/08/2022
# Current Version: 3.0
# https://github.com/cheerlights/cheerlights-discord-bot

# Questions? Comments? Suggestions? Contact me one of the following ways:
# E-mail: n8acl@qsl.net
# Twitter: @n8acl
# Discord: Ravendos#7364
# Mastodon: @n8acl@mastodon.radio
# Website: https://www.qsl.net/n8acl

#############################
# Import Libraries
import config as cfg
import os
import json
import requests
import discord # Discord library
import tweepy
from datetime import datetime, date, time, timedelta
from tweepy import OAuthHandler


#############################
# Create Discord Bot
TOKEN = cfg.discord['bot_token']
bot = discord.Bot(debug_guilds=[cfg.discord['server_id']])

#############################
# Twitter API Object Configuration
auth = OAuthHandler(cfg.twitterkeys["consumer_key"], cfg.twitterkeys["consumer_secret"])
auth.set_access_token(cfg.twitterkeys["access_token"], cfg.twitterkeys["access_secret"])

twitter = tweepy.API(auth)

#############################
# Define Variables
# DO NOT CHANGE BELOW

cheerlights_api_url = 'http://api.thingspeak.com/channels/1417/field/2/last.json'
linefeed = "\r\n"

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

#############################
# Define Discord Bot Functions

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(description="Returns Current Color")
async def get_color(ctx):
    color_code = use_api()
    #r, g, b = hex_to_rgb(color_code)

    embed = discord.Embed(title = "Current CheerLights Color",
    description=get_key(color_code.upper(),color_pick),
    color=int(color_code.lstrip('#'), 16)
    )

    await ctx.respond(embed = embed,ephemeral=True)

@bot.command(description="Returns List of Valid colors")
async def color_list(ctx):

    embed = discord.Embed(title = "Valid CheerLights Colors",
    description=valid_colors()
    )

    await ctx.respond(embed = embed,ephemeral=True)

@bot.command(description="Sets CheerLights to Specificed <color>")    
async def set_color(ctx, color):
    if color.lower() in color_pick:
        color_code = color_pick[color.lower()]
        #r, g, b = hex_to_rgb(color_code)

        embed = discord.Embed(title = "Setting CheerLights to Color",
            description=color.lower(),
            color=int(color_code.lstrip('#'), 16)
        )

        now = datetime.now()
        timestamp = now.strftime("%m/%d/%Y %H:%M:%S")

        status = "Set @CheerLights to " + color + " on " + timestamp

        #print(status)
        twitter.update_status(status)

    else:

        response = "That is an invalid color. Valid colors are:" + linefeed + linefeed
        response = response + valid_colors()

        embed = discord.Embed(title = "Invalid CheerLights Color",
            description=response
        )
    await ctx.respond(embed = embed,ephemeral=True)


@bot.command(description="Help Text")
async def help(ctx):

    cmd_list = """
    /cheerlights - Returns the current CheerLights Color.

    /set_color <color> - Set CheerLights to this <color>. ex: /set_color red

    /list - Lists the valid colors that can be used for CheerLights.

    /help - This help text.

    More Information can be found at https://github.com/cheerlights/cheerlights-discord-bot

    """

    embed = discord.Embed(title = "CheerLights Bot Commands",
        description=cmd_list
    )
    await ctx.respond(embed = embed,ephemeral=True)

#############################
# Main Program

# Start Bot
bot.run(TOKEN)