import hikari, lightbulb

plugin = lightbulb.Plugin('dm')

def load(bot):
    bot.add_plugin(plugin)

@plugin.command
@lightbulb.command('dm', 'sends dm')
@lightbulb.implements(lightbulb.PrefixCommand)
async def dm(event):
    target = await event.bot.rest.create_dm_channel('873940508504883261')
    await target.send('hai')