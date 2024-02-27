import lightbulb, hikari
import pypyodbc as odbc
import miru

plugin = lightbulb.Plugin('inventory')

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-HFFP4M5'
DATABASE_NAME = 'kaminaribot'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
    uid=sa;
    pwd=P@ssw0rd;
"""
conn = odbc.connect(connection_string)
c = conn.cursor()

class InvView(miru.View):

    @miru.text_select(
        placeholder="select group",
        options=[
            miru.SelectOption(label="NewJeans", value="NewJeans"),
            miru.SelectOption(label="THE BOYZ", value="THE BOYZ")
        ],
        custom_id="inventory"
        )

    async def callback(self, context:miru.ViewContext, select:miru.TextSelect) -> None:
        self.answer = select.values[0]
        print(self.answer)

def load(bot):
    bot.add_plugin(plugin)

@plugin.command
@lightbulb.option("player", "(optional) user to check inv of", type=hikari.User, default=None)
@lightbulb.command("inv","drop a card", aliases="i")
@lightbulb.implements(lightbulb.PrefixCommand)
async def inventoryy(ctx: lightbulb.Context):
    query = "SELECT * FROM player WHERE user_id=?"
    if ctx.options.player == None:
        id = str(ctx.author.id)
        username = str(ctx.author.username)
    else: 
        id = str(ctx.options.player.id)
        username = str(ctx.options.player.username)
    c.execute(query, (id, ))
    user = c.fetchone()
    if user != None:
        query2 = "UPDATE temp_inv SET userid = ? WHERE executer = ?"
        c.execute(query2, (id, str(ctx.author.id)))
        conn.commit()
        view = InvView()
        await ctx.respond(f"{username}'s Inventory", components=view)
        ctx.app.d.miru.start_view(view)
    else:
        await ctx.respond(f"hi, <@{ctx.author.id}>! you need to register your account first")


@plugin.listener(hikari.InteractionCreateEvent)
async def on_component_interaction(event: hikari.InteractionCreateEvent) -> None:
    # Filter out all unwanted interactions
    if not isinstance(event.interaction, hikari.ComponentInteraction):
        return

    if event.interaction.custom_id == "inventory":
        query2 = "SELECT userid FROM temp_inv WHERE executer=?"
        user = c.execute(query2, (str(event.interaction.user.id), )).fetchone()
        id = str(user[0])
        username = await plugin.bot.rest.fetch_user(user[0])
        if user != None:
            sql = """
            SELECT
                kartu.group_name,
                string_agg(kartu.card, '\n') as cards
            FROM (
                SELECT
                    c.group_name,
                    CONCAT('``',i.card_code,'``',' ',c.name,' - ',i.amount) as card
                FROM inventory i
                    left join m_card c ON i.card_code = c.code
                WHERE user_id=? AND group_name=? AND amount > 0
            ) as kartu
            GROUP BY group_name
            """
            inv = c.execute(sql, (id, event.interaction.values[0])).fetchall()

            embed1 = (
                hikari.Embed(
                )
            )

            if inv != []:
                for x in inv:
                    embed1.add_field(x[0], x[1])
            else:
                embed1.add_field(f"{event.interaction.values[0]}", "-")

        await event.interaction.create_initial_response(
            hikari.ResponseType.MESSAGE_UPDATE,  # Create a new message as response to this interaction
            f"{username.username}'s Inventory",embed=embed1
        )


@plugin.command
@lightbulb.option("card", "which card to give", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.option("user", "get user", type=hikari.User)
@lightbulb.command("gift","drop a card", aliases="g")
@lightbulb.implements(lightbulb.PrefixCommand)
async def inv(ctx: lightbulb.Context):
    cards = ctx.options.card.split()

    await ctx.respond(f"{ctx.options.user.username} + {ctx.options.card}")
