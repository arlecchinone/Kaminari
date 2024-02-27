import hikari, lightbulb

plugin = lightbulb.Plugin('ping')

def load(bot):
    bot.add_plugin(plugin)

@plugin.listener(hikari.GuildMessageCreateEvent)
async def message(event):
    print(event.content)

# @plugin.listener(hikari.GuildMessageCreateEvent)
# async def message(event):
#     loop = True
#     while loop:
#         await event.respond("halo")

@plugin.command
@lightbulb.add_checks(lightbulb.has_role_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.add_cooldown(30,1,lightbulb.UserBucket)
@lightbulb.command('ping', 'sends pong')
@lightbulb.implements(lightbulb.PrefixCommand)
async def ping(event: lightbulb.context):
    user = event.author.username
    await event.message.respond("hai " + user)
        
