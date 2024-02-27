import lightbulb, hikari
import pypyodbc as odbc
import random
from datetime import datetime

plugin = lightbulb.Plugin('drop')

def load(bot):
    bot.add_plugin(plugin)

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

@plugin.command
@lightbulb.add_cooldown(10,1,lightbulb.UserBucket)
@lightbulb.command("drop","drop a card", aliases="d")
@lightbulb.implements(lightbulb.PrefixCommand)
async def drop(ctx: lightbulb.Context):
        query = "SELECT * FROM player WHERE user_id=?"
        id = str(ctx.author.id)
        c.execute(query, (id, ))
        user = c.fetchone()
        if user != None:
          sql = "SELECT * FROM m_card WHERE id=?"
          number = random.randint(1,5)
          c.execute(sql, (number, ))
          card = c.fetchone()
          sql2 = "SELECT * FROM inventory WHERE user_id = ? AND card_code = ?"
          check = c.execute(sql2, (ctx.author.id, card[4])).fetchone()
          if check != None:
              sql3 = "UPDATE inventory SET amount = ? WHERE user_id = ? AND card_code = ?"
              c.execute(sql3, (check[3]+1, ctx.author.id, card[4]))
              conn.commit()
          else:
              sql3 = "INSERT INTO inventory(user_id, card_code, amount) VALUES(?,?,?)"
              c.execute(sql3, (ctx.author.id, card[4], 1))
              conn.commit()
          check2 = c.execute(sql2, (ctx.author.id, card[4])).fetchone()
          footer = f"you have {check2[3]} copies of this card"     
          embed = (
          hikari.Embed(
              title= "<:heartcard:1206097438650277928> You dropped a card!",
              description= f"You got a new `♠️` card!\n\n`♢ SPADE #{card[4]}: {card[3]} {card[2]}`\n\nThis is your first `♠️` card!",
              colour= 0x92b379,
              )
              .set_image(card[5])
              .set_footer(footer)
      )
          await ctx.respond(embed)
        else:
             await ctx.respond(f"hi, <@{ctx.author.id}>! you need to register your account first")

@plugin.command
@lightbulb.command("register","register to the bot")
@lightbulb.implements(lightbulb.PrefixCommand)
async def register(ctx: lightbulb.Context):
      sql = "SELECT * FROM player WHERE user_id=?"
      id = str(ctx.author.id)
      c.execute(sql, (id, ))
      user = c.fetchone()

      embed = (
        hikari.Embed(
            title= "Your account has been successfully registered!",
            description= f"Welcome to `kaminari`, <@{ctx.author.id}>!\nyou've recieved 20000 as a welcome gift\nhave fun!",
            color= 0xFFCBA4,
            )      
    )
      if user != None:
           await ctx.respond(f"{ctx.author.username}, you've already registered as a player")
      else:
            query2 = "INSERT INTO temp_inv(executer) VALUES (?)"
            sql2 = "INSERT INTO player(user_id, date_reg, currency) VALUES (?,?,?)"
            val1 = str(ctx.author.id)
            c.execute(query2, (val1, ))
            c.execute(sql2, (val1, datetime.now(), 20000))
            conn.commit()
            await ctx.respond(embed)

@plugin.command
@lightbulb.option("user", "(optional) user to check the balance of", type=hikari.User, default=None)
@lightbulb.command("bal","check balance")
@lightbulb.implements(lightbulb.PrefixCommand)
async def balance(ctx: lightbulb.Context):
      sql = "SELECT * FROM player WHERE user_id=?"
      if ctx.options.user != None:
           id = str(ctx.options.user.id)
           name = str(ctx.options.user.username)
      else:
           id = str(ctx.author.id)
           name = str(ctx.author.username)
      c.execute(sql, (id, ))
      user = c.fetchone()

      if user != None:
        embed = (
             hikari.Embed(
            title= f"{name}'s balance",
            description= f"**Balance:** {user[3]}",
            color= 0xFFCBA4,
            )      
    )
        await ctx.respond(embed)
      else:
            await ctx.respond(f"hi, <@{ctx.author.id}>! you need to register your account first")

@plugin.command
@lightbulb.option("amount", "amount of money", int)
@lightbulb.option("user", "get user", type=hikari.User)
@lightbulb.command("pay","pay someone a certain amount of money")
@lightbulb.implements(lightbulb.PrefixCommand)
async def pay(ctx: lightbulb.Context):
     if ctx.author.id == ctx.options.user.id:
          await ctx.respond(f"<@{ctx.author.id}>, you can't pay money to yourself")
     else:
        sql = "SELECT * FROM player WHERE user_id=?"
        author_id = str(ctx.author.id)
        user_id = str(ctx.options.user.id)

        author = c.execute(sql, (author_id, )).fetchone()
        user = c.execute(sql, (user_id, )).fetchone()

        if author != None and user != None:
            m_author = author[3] - ctx.options.amount
            m_user = user[3] + ctx.options.amount

            if m_author > 0:
                  sql2 = "UPDATE player SET currency = ? WHERE user_id = ?"
                  c.execute(sql2, (m_author, ctx.author.id))
                  c.execute(sql2, (m_user, ctx.options.user.id))
                  conn.commit()
                  await ctx.respond(f"<@{ctx.author.id}> has succesfully paid {ctx.options.amount} to <@{ctx.options.user.id}>")
            else:
                  await ctx.respond(f"<@{ctx.author.id}>, you don't have enough money to pay this amount")
            # await ctx.respond(f"{isinstance(m_author, int)} dan {isinstance(m_user, int)}")
        else:
            await ctx.respond("both player need to be registered first")