import discord, random, string, requests, asyncio
from discord.ext import commands
from Secrets import token


client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print("Bot is Ready!")


@client.command()
async def verify(ctx, user: discord.Member):
    await ctx.send(f"Hey{user.mention} **Check your DM to get full access to the server!**")

    length_of_string = 12
    input_ = "".join(random.choice(string.ascii_letters) for i in range(length_of_string))
    await user.send(f"https://www.bogan.cool/api/recaptcha/verify/{input_}") # Change URL

    for _ in range(10):
        r = requests.get(f"https://www.bogan.cool/api/recaptcha/check/{input_}") # Change URL

        if "Verfication successed" in r.text:
            role = discord.utils.get(user.guild.roles, name='verified')
            await user.add_roles(role)
            break

        else:
            asyncio.sleep(5)


client.run(token) # Discord Token
