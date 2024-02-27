import hikari
import lightbulb
import miru

bot = lightbulb.BotApp(token='MTE4NTQ0NDQ1ODUwNzAzMDU5OQ.G1r1yy.Xdr6y6IJf61Y0oQscRcu85kqle7p6MZ7cqJRyw',
                       prefix='.',
                        intents=hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT )

bot.load_extensions_from('./extensions')
bot.d.miru = miru.Client(bot)

# @bot.listen(lightbulb.CommandErrorEvent)
# async def errorHandler(errEvent: lightbulb.CommandErrorEvent) -> None:
#     exception = errEvent.exception or errEvent.exception.__cause__
    
#     if isinstance(exception, lightbulb.CommandInvocationError):
#         await errEvent.context.respond(f"command `{errEvent.context.command.name}` error")
#     elif isinstance(exception, lightbulb.MissingRequiredPermission):
#         await errEvent.context.respond(f"you don't have permission to run this command")
#     # elif isinstance(exception, lightbulb.NotEnoughArguments):
#     #     await errEvent.context.respond(f"please add your text")
#     elif isinstance(exception, lightbulb.CommandIsOnCooldown):
#         time = exception.retry_after
#         await errEvent.context.respond(f"your `{errEvent.context.command.name}` is on cooldown. try again after `{time:.2f}` seconds")
#     else:
#         raise exception

bot.run()