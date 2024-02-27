import hikari, lightbulb
from PIL import Image

placeholder = Image.open('./image/placeholder.png')
image1 = Image.open('./image/minji.png')
image2 = Image.open('./image/hyein.png')
image3 = Image.open('./image/hanni.png')
area1 = (10, 10, 1410, 2110)
area2 = (1420, 10, 2820, 2110)
area3 = (2830, 10, 4230, 2110)

image_full = placeholder.copy()
image_full.paste(image1, area1)
image_full.paste(image2, area2)
image_full.paste(image3, area3)
image_full.save('./image/image_full.png')


plugin = lightbulb.Plugin('embed')

def load(bot):
    bot.add_plugin(plugin)

@plugin.command
# @lightbulb.add_checks(lightbulb.has_roles(1205865818877988914))
# @lightbulb.option("user", "get user", type=hikari.User)
@lightbulb.command("profile", "get user profile", aliases='p')
@lightbulb.implements(lightbulb.PrefixCommand)
async def profile(ctx) -> None:
    await ctx.respond("Loading your profile, please wait...", delete_after=10)
    user = ctx.author
    embed = (
        hikari.Embed(
            title= f"{user.username}'s Profile",
            description= "ini nanti bio",
            color= 0xFFCBA4,
            )
            .set_thumbnail(user.avatar_url)
            .set_footer('ini footer')
            .add_field('field 2', 'ini field 2', inline=True)
            .add_field('field 3', 'ini field 3', inline=True)
            .set_image('./image/image_full.png')
            
    )
    await ctx.respond(embed)