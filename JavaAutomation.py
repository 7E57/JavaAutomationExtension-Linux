import discord
from discord.ext import commands
import json
import aiohttp
import os
import sys
import psutil
import subprocess
import signal
from discord import Embed, Colour
from discord import Game
from robloxapi import Client
import httpx
import asyncio
import os



#Made by Java#9999


ROBLOX_API_URL = "https://users.roblox.com/v1/users/authenticated"   #The roblox auth api to check if the cookie is valid or not
intents = discord.Intents.default()
intents.message_content = True     
bot = commands.Bot(command_prefix='!', intents=intents)    #The bot prefix



def set_console_color(color_code):
    os.system(f'color {color_code}')





def is_owner(): #To recognize if the user executing the command is the owner or not.
    async def predicate(ctx):
        with open('settings.json', 'r') as f:
            settings = json.load(f)
        owner_id = int(settings['MISC']['DISCORD_BOT']['OWNER_USER_ID'])
        return ctx.author.id == owner_id
    return commands.check(predicate)






@bot.event  # Bot status
async def on_ready():
    set_console_color("0C")  # Set console text color to red
    os.system('cls' if os.name == 'nt' else 'clear')

    print(r"""
.gg/89EcZ4KAa6
       __                     ___         __                        __  _           
      / /___ __   ______ _   /   | __  __/ /_____  ____ ___  ____ _/ /_(_)___  ____ 
 __  / / __ `/ | / / __ `/  / /| |/ / / / __/ __ \/ __ `__ \/ __ `/ __/ / __ \/ __ \
/ /_/ / /_/ /| |/ / /_/ /  / ___ / /_/ / /_/ /_/ / / / / / / /_/ / /_/ / /_/ / / / /
\____/\__,_/ |___/\__,_/  /_/  |_\__,_/\__/\____/_/ /_/ /_/\__,_/\__/_/\____/_/ /_/ 
                                                                                    
""")
    await bot.change_presence(activity=Game(name="!info"))
    print(f'Logged in as bot: {bot.user.name}')

    main_cookie = settings['MAIN_COOKIE']
    details_cookie = settings['DETAILS_COOKIE']

    checks = 0
    while True:
        checks += 1
        # Check MAIN_COOKIE
        main_cookie_valid, main_username = await check_cookie(main_cookie)
        if not main_cookie_valid:
            await send_cookie_invalid_webhook("MAIN_COOKIE", "cookie")

        # Check DETAILS_COOKIE
        details_cookie_valid, details_username = await check_cookie(details_cookie)
        if not details_cookie_valid:
            await send_cookie_invalid_webhook("DETAILS_COOKIE", "altcookie")

        print(f"\033[3A\033[2KCookie Checking ({checks}):\nMain Cookie: {main_username}\nAlt Cookie: {details_username}")

        # Wait for 5 minutes seconds before checking again
        await asyncio.sleep(300)


async def check_cookie(cookie):
    async with httpx.AsyncClient() as client:
        headers = {"Cookie": f".ROBLOSECURITY={cookie}"}
        response = await client.get(ROBLOX_API_URL, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        username = user_data["name"]
        return True, username
    else:
        return False, None


async def send_cookie_invalid_webhook(cookie_name, command_name):
    webhook_url = settings['MISC']['WEBHOOK']['URL']
    embed = discord.Embed(
        title="Cookie check notification!",
        description=f" ``` The {cookie_name} has become invalid. Please update it by using the command !{command_name}. ```",
        color=discord.Color.red()
    )
    embed_dict = embed.to_dict()

    async with aiohttp.ClientSession() as session:
        async with session.post(
            webhook_url,
            json={
                "embeds": [embed_dict],
                "username": bot.user.name,
                "avatar_url": str(bot.user.avatar.url) if bot.user.avatar else None,
            },
        ) as response:
            if response.status != 204:
                print(f"Failed to send the embed to the webhook. HTTP status: {response.status}")




@bot.command()
async def invite(ctx):
    response_message = "```Are you happy with JavaAutomation extension? Join our server to checkout more products like this!```\n https://discord.gg/89EcZ4KAa6"
    await ctx.send(response_message)


@bot.command() #Change webhook command
@is_owner()
async def webhook(ctx, webhook_url: str):
    # Load the JSON file
    with open('settings.json', 'r') as f:
        settings = json.load(f)

        # Restart the bot
        if await restart_bot():
            print("Succesfully restarted mewt after updating the speed")
        else:
            print("Error while trying to restart mewt after updating the speed.")

    # Update the webhook URL
    settings['MISC']['WEBHOOK']['URL'] = webhook_url

    # Save the updated JSON file
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

    # Create an embed with a pink color
    embed = discord.Embed(
        title="Success!",
        description=" ``` This webhook has been succesfully set and will be used for the next notifications! ```",
        color=discord.Color.from_rgb(255, 182, 193)
    )

    # Convert the embed to a dictionary
    embed_dict = embed.to_dict()

    # Send the embed to the webhook URL
    async with aiohttp.ClientSession() as session:
        async with session.post(
            webhook_url,
            json={
                "embeds": [embed_dict],
                "username": bot.user.name,
                "avatar_url": str(bot.user.avatar.url) if bot.user.avatar else None,
            },
        ) as response:
            if response.status != 204:
                await ctx.send(f"Failed to send the embed to the webhook. HTTP status: {response.status}")
                return








@bot.command(name='onlyfree')  # Only free command
@is_owner()
async def onlyfree(ctx, status: str):
    if status.lower() not in ['on', 'off']:
        embed = Embed(title='Error', description='```Please use !onlyfree on or !onlyfree off```', color=Colour.from_rgb(255, 0, 0))
        await ctx.send(embed=embed)
        return

    # Load the JSON file
    with open('settings.json', 'r') as f:
        settings = json.load(f)


        # Restart the bot
        if await restart_bot():
            print("Succesfully restarted mewt after updating the speed")
        else:
            print("Error while trying to restart mewt after updating the speed.")

    # Update the BUY_ONLY_FREE setting
    if status.lower() == 'on':
        settings['MISC']['BUY_ONLY_FREE'] = True
        description = 'Mewt sniper will now only snipe free items. Run !onlyfree off to deactivate this setting.'
    else:
        settings['MISC']['BUY_ONLY_FREE'] = False
        description = 'Mewt sniper will now snipe paid items too. Run !onlyfree on to activate this setting.'

    # Save the updated JSON file
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

    embed = Embed(title='Success!', description=f'```{description}```', color=Colour.from_rgb(255, 182, 193))
    await ctx.send(embed=embed)






@bot.command(name='speed')  # Change speed command
@is_owner()
async def speed(ctx, new_speed: str):
    try:
        new_speed_float = float(new_speed)
    except ValueError:
        embed = Embed(title=' ```The scan speed must be a number. ```', color=Colour.from_rgb(255, 0, 0))
        await ctx.send(embed=embed)
        return

    # Load the JSON file
    with open('settings.json', 'r') as f:
        settings = json.load(f)

         # Restart the bot
        if await restart_bot():
            print("Succesfully restarted mewt after updating the speed")
        else:
            print("Error while trying to restart mewt after updating the speed.")


    # Check if the input has a decimal part
    if new_speed_float.is_integer():
        new_speed_str = str(int(new_speed_float))
        new_speed_value = int(new_speed_float)
    else:
        new_speed_str = str(new_speed_float)
        new_speed_value = new_speed_float

    # Update the scan speed
    settings['MISC']['SCAN_SPEED'] = new_speed_value

    # Save the updated JSON file
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

    embed = Embed(title='Success!', description=f'```New scan speed: {new_speed_str}```', color=Colour.from_rgb(255, 182, 193))
    await ctx.send(embed=embed)








@bot.command() #info command
async def info(ctx):
    embed = discord.Embed(
        title="JavaExtension Commands:",
        description="```\n!cookie     --To change your main cookie\n!altcookie   --To change your alt cookie\n!webhook   --To change your webhook\n!token   --To change your discord bot token\n!speed  --To change your speed\n!onlyfree off  --To snipe paid items too\n!onlyfree on  -to snipe free items only \n!restart  --To Restart mewt sniper\n!invite --To join JavaAutomation server\n``` \n",
        color=discord.Color.from_rgb(255, 182, 193)
    )
    embed.set_footer(text="Developed by: Java#9999 \nHelped by: Lag#1234")
    await ctx.send(embed=embed)

async def restart_bot():
    try:
        for proc in psutil.process_iter():
            name = proc.name()
            if name == "python.exe":
                cmdline = proc.cmdline()
                if "main.py" in cmdline[1]:
                    pid = proc.pid
                    os.kill(pid, signal.SIGTERM)
        os.system('start cmd /k python main.py')
        return True
    except:
        return False






@bot.command() #restart command
@is_owner()
async def restart(ctx):
    try:
        for proc in psutil.process_iter():
            name = proc.name()
            if name == "python.exe":
                cmdline = proc.cmdline()
                if "main.py" in cmdline[1]:
                    pid = proc.pid
                    os.kill(pid, signal.SIGTERM)
        os.system('start cmd /k python main.py')
        embed = Embed(title="Success!", description=" ```Successfully restarted mewt sniper ```", color=Colour.from_rgb(255, 182, 193))
        await ctx.send(embed=embed)
    except:
        embed = Embed(title="Error", description=" ```Error while trying to restart mewt ```", color=Colour.red())
        await ctx.send(embed=embed)





@bot.command() #change cookie command
@is_owner()
async def cookie(ctx, new_cookie: str):
    # Validate the cookie
    async with httpx.AsyncClient() as client:
        headers = {"Cookie": f".ROBLOSECURITY={new_cookie}"}
        response = await client.get(ROBLOX_API_URL, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        username = user_data["name"]
        user_id = user_data["id"]

        # Get avatar URL
        avatar_api_url = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=420x420&format=Png&isCircular=false"
        async with httpx.AsyncClient() as client:
            avatar_response = await client.get(avatar_api_url)
        avatar_data = avatar_response.json()
        avatar_url = avatar_data["data"][0]["imageUrl"]

        # Load the JSON file
        with open('settings.json', 'r') as f:
            settings = json.load(f)

        # Update the MAIN_COOKIE value
        settings['MAIN_COOKIE'] = new_cookie

        # Save the updated JSON file
        with open('settings.json', 'w') as f:
            json.dump(settings, f, indent=4)

        # Create an embed with a light pink color
        embed = discord.Embed(
            title="MAIN Cookie Update",
            description=f" ```The MAIN cookie was valid for the username: {username}```\n  \n **If the bot dosen't react to !stats it means that either your main/alt cookie was invalid. In this case update them.** ",
            color=discord.Color.from_rgb(255, 182, 193)
        )

        # Set the embed thumbnail to the player's avatar
        embed.set_thumbnail(url=avatar_url)

        # Send the embed in the current channel
        await ctx.send(embed=embed)

        # Restart the bot
        if await restart_bot():
            print("Bot restarted after updating the cookie.")
        else:
            print("Error while trying to restart the bot after updating the cookie.")

    else:
        # Create an embed with a red color
        embed = discord.Embed(
            title="Error",
            description=" ```The cookie you have input was invalid. ```",
            color=discord.Color.red()
        )

        # Send the embed in the current channel
        await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = Embed(title="Error", description=" ``` Only the owner can use such commands. ```", color=Colour.red())
        await ctx.send(embed=embed)







@bot.command() #Change altcookie command
@is_owner()
async def altcookie(ctx, new_cookie: str):
    # Validate the cookie
    async with httpx.AsyncClient() as client:
        headers = {"Cookie": f".ROBLOSECURITY={new_cookie}"}
        response = await client.get(ROBLOX_API_URL, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        username = user_data["name"]
        user_id = user_data["id"]

        # Get avatar URL
        avatar_api_url = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=420x420&format=Png&isCircular=false"
        async with httpx.AsyncClient() as client:
            avatar_response = await client.get(avatar_api_url)
        avatar_data = avatar_response.json()
        avatar_url = avatar_data["data"][0]["imageUrl"]

        # Load the JSON file
        with open('settings.json', 'r') as f:
            settings = json.load(f)

        # Update the MAIN_COOKIE value
        settings['DETAILS_COOKIE'] = new_cookie

        # Save the updated JSON file
        with open('settings.json', 'w') as f:
            json.dump(settings, f, indent=4)

        # Create an embed with a light pink color
        embed = discord.Embed(
            title="ALT Cookie Update",
            description=f" ```The ALT cookie was valid for the username: {username} ```\n  \n **If the bot dosen't react to !stats it means that either your main/alt cookie was invalid. In this case update them.** '",
            color=discord.Color.from_rgb(255, 182, 193)
        )

        # Set the embed thumbnail to the player's avatar
        embed.set_thumbnail(url=avatar_url)

        # Send the embed in the current channel
        await ctx.send(embed=embed)

         # Restart the bot
        if await restart_bot():
            print("Bot restarted after updating the ALT cookie.")
        else:
            print("Error while trying to restart the bot after updating the cookie.")


    else:
        # Create an embed with a red color
        embed = discord.Embed(
            title="Error",
            description=" ```The cookie you have input was invalid. ```",
            color=discord.Color.red()
        )

        # Send the embed in the current channel
        await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = Embed(title="Error", description=" ```Only the owner can use such commands. ```", color=Colour.red())
        await ctx.send(embed=embed)







@bot.command()  #Change token command
@is_owner()
async def token(ctx, new_token: str):
    # Load the JSON file
    with open('settings.json', 'r') as f:
        settings = json.load(f)

    # Update the TOKEN value
    settings['MISC']['DISCORD_BOT']['TOKEN'] = new_token

    # Save the updated JSON file
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

                 # Restart the bot
        if await restart_bot():
            print("Bot restarted after updating the token.")
        else:
            print("Error while trying to restart the bot after updating the token.")

    # Create an embed with a green color
    embed = discord.Embed(
        title="Token Update",
        description=" ``` Successfully changed the discord bot TOKEN, make sure that you have invited the new bot to the server. ```",
        color=discord.Color.from_rgb(255, 182, 193)
    )


    # Send the embed to the channel where the command was executed
    await ctx.send(embed=embed)






# Load the JSON file
with open('settings.json', 'r') as f:
    settings = json.load(f)

# Get the bot token from the settings
bot_token = settings['MISC']['DISCORD_BOT']['TOKEN']

# Run the bot using the token from the settings
bot.run(bot_token)

