import os, asyncio, logging
from discord import Embed,Color
from discord.ext import commands
from data_handler import data_handler #Import data handler code
#Logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG
)
logger.info("Discord-bot for editing homework/Discord-bot för att redigera läxor.")
logger.info("Made with <3 by 20alse")
#Bot
bot = commands.Bot(command_prefix="'", help_command=None)

#Embeds for certain messages
INTRO_EMBED=Embed(
    title="Jag hör dig!",
    description="Skriv titeln på den läxa som du vill lägga till.",
    color=Color.blue()
)
DESCRIPTION_EMBED=Embed(
    title="Fyll i",
    description="Skriv beskrivningen för läxan.",
    color=Color.blue()
)
SUBJECT_EMBED=Embed(
    title="Fyll i",
    description="Skriv ämnet som läxan är i.",
    color=Color.blue()
)
DUE_DATE_EMBED=Embed(
    title="Fyll i!",
    description="Ange vilket inlämningsdatum som läxan har.",
    color=Color.blue()
)
FLAG_EMBED=Embed(
    title="Fyll i!",
    description="""
    Nu är det dags att sätta några attribut för läxan.
    Reagera med emojis för att markera som:
    🎓 - Prov
    """,
    color=Color.blue()
)
FLAG_EMBED.set_footer(text="Du har 10 sekunder på dig att lägga till reaktioner.")
@bot.command(aliases=["ahw", "a"])
@commands.is_owner()
async def add_homework(ctx):
    '''Command for adding homework.'''

    def is_response_to_me(ctx2):
        '''Function for checking if a message is in the response to the bot.'''
        return ctx2.author.id == ctx.author.id and ctx2.channel.id == ctx.channel.id
    await ctx.send(
        embed=INTRO_EMBED
    )
    #Wait for answer
    #Get title
    title = await bot.wait_for("message", check=is_response_to_me, timeout=120)
    title = title.content
    #Get description
    await ctx.send(embed=DESCRIPTION_EMBED)
    description = await bot.wait_for("message", check=is_response_to_me, timeout=120)
    description = description.content
    #Get course
    await ctx.send(embed=SUBJECT_EMBED)
    course = await bot.wait_for("message", check=is_response_to_me, timeout=120)
    course = course.content
    #Get due date
    await ctx.send(embed=DUE_DATE_EMBED)
    due_date = await bot.wait_for("message", check=is_response_to_me, timeout=120)
    due_date = due_date.content
    #Ask for any further details
    further_details_message = await ctx.send(embed=FLAG_EMBED)
    await further_details_message.add_reaction("🎓")
    #Leave 10 seconds for reactions.
    await asyncio.sleep(10)
    #Get reactions
    further_details_message = await ctx.fetch_message(further_details_message.id)
    is_exam_flag = False
    #Iterate through reactions and try to find things that edits attributes of the homework that will be created.
    for reaction in further_details_message.reactions:
        #reaction_users = [reaction_user.id for reaction_user in reaction.reaction_users]
        if str(reaction.emoji) == "🎓" and reaction.count > 1:
            is_exam_flag = True
    #Send confirmation message
    homework_information_message = f"""
    **Titel:** `{title}`
    **Beskrivning:** `{description}`
    **Ämne:** `{course}`
    **Ska vara klar:** `{due_date}`
    **Är:** `{'prov' if is_exam_flag else 'läxa'}`.
    """
    confirmation_embed = Embed(
        title="Klar!",
        description=f"Jag kommer skicka upp följande till servern inom kort: \n{homework_information_message}",
        color=Color.blue()
    )
    await ctx.send(embed=confirmation_embed)
    #Download current homework file
    status_embed = Embed(
        title="Status: Läser in...",
        description="Laddar ner tidigare fil med läxor...",
        color=Color.dark_orange()
    )
    status_message = await ctx.send(embed=status_embed)
    homework = data_handler.get_homework_file()
    homework.append({
        "title": title,
        "description": description,
        "course": course,
        "due": due_date,
        "is_exam": is_exam_flag
    })
    status_embed.title = "Status: Skickar via SFTP..."
    status_embed.description="Läxfilen har laddats ner och uppdaterats i minnet. Skickar den via SFTP..."
    await status_message.edit(embed=status_embed)
    #Connect to SFTP server and send
    data_handler.upload_homework_file(homework)
    status_embed.title = "Status: Klar!"
    status_embed.description = "✅ Allt klart. Läxfilen har skickats till servern via SFTP."
    await status_message.edit(embed=status_embed)

@bot.command(aliases=["lhw", "l"])
@commands.is_owner()
async def list_homework(ctx):
    '''Lists homework and shows the command to use to edit them.'''
    logger.info("Listing homework...")
    homework = data_handler.get_homework_file()
    final_homework_message = ""
    i = 1
    for assignment in homework:
        final_homework_message += f"""`{i}`. **{assignment['title']}** ({assignment['course']})
        {assignment['description']}
        Klar: `{assignment['due']}`
        Är prov: `{'Ja' if assignment['is_exam'] else 'Nej'}`
        *Kommando för redigering:* `'ehw {i} <sak att redigera> <nytt värde>`\n"""
        i += 1
    logger.info("Homework list generated. Sending confirmation message...")
    final_embed = Embed(
        title="Läxor",
        description=final_homework_message,
        color=Color.blue()
    )
    await ctx.send(embed=final_embed)

@bot.command(aliases=["ehw", "e"])
@commands.is_owner()
async def edit_homework(ctx, assignment_number: int, thing_to_change:str, new_value: str):
    '''Edits a homework.'''
    status_embed = Embed(
        title="Status: Läser in...",
        description="Laddar ner tidigare fil med läxor...",
        color=Color.dark_orange()
    )
    status_message = await ctx.send(embed=status_embed)
    homework = data_handler.get_homework_file()
    await status_message.delete()
    if assignment_number > len(homework):
        await ctx.send(Embed(title="Fel",
                             description=f"Det finns ingen läxa som har nummer `{assignment_number}`.",
                             color=Color.red()))
        return
    VALID_EDIT_KEYS = ["title", "description", "course", "due", "is_exam"]
    if thing_to_change not in VALID_EDIT_KEYS:
        await ctx.send(Embed(title="Fel",
                             description=f"Du kan bara redigera följande: {','.join(VALID_EDIT_KEYS)}",
                             color=Color.red()))
        return
    assignment = homework[assignment_number - 1]
    #Edit assignment values
    if thing_to_change in ["is_exam"]:
        new_value = bool(new_value) #Convert to bool if the thing to change is is_exam
    assignment[thing_to_change] = new_value
    #Create pending embed
    status_embed = Embed(
        title="Status: Skickar via SFTP...",
        description="Läxfilen har laddats ner och uppdaterats i minnet. Skickar den via SFTP...",
        color=Color.dark_orange())
    status_message = await ctx.send(embed=status_embed)
    #Update homework file
    data_handler.upload_homework_file(homework)
    status_embed.title = "Status: Klar!"
    status_embed.description = "✅ Allt klart. Läxfilen har skickats till servern via SFTP."
    await status_message.edit(embed=status_embed)
    #Send confirmation message
    confirmation_embed = Embed(
        title="Klar!",
        description=f"Jag har uppdaterat läxan med nummer `{assignment_number}`. Parametern som har uppdaterats är {thing_to_change} och det nya värdet är `{new_value}`.",
        color=Color.blue())
    await ctx.send(embed=confirmation_embed)

@bot.command(aliases=["rhw", "r"])
async def remove_homework(ctx, assignment_number:int):
    '''Removes a homework from the list of homework.'''
    homework = data_handler.get_homework_file()
    #Validate homework number
    if assignment_number > len(homework):
        await ctx.send(
            embed=Embed(
                title="Fel!",
                description=""
            )
        )
    else:
        logger.info(f"Removing homework at {assignment_number}...")
        homework.pop(assignment_number)
    #Create pending embed
    status_embed = Embed(
        title="Status: Skickar via SFTP...",
        description="Läxfilen har laddats ner och uppdaterats i minnet. Skickar den via SFTP...",
        color=Color.dark_orange())
    status_message = await ctx.send(embed=status_embed)
    #Update homework file
    data_handler.upload_homework_file(homework)
    status_embed.title = "Status: Klar!"
    status_embed.description = "✅ Allt klart. Läxfilen har skickats till servern via SFTP."
    await status_message.edit(embed=status_embed)
    #Send confirmation message
    confirmation_embed = Embed(
        title="Klar!",
        description=f"Jag har tagit bort läxan med nummer `{assignment_number}`.",
        color=Color.blue())
    await ctx.send(embed=confirmation_embed)

#Error handler
@bot.event
async def on_command_error(ctx, error):
    '''Handles any errors generated by the bot'''
    irrelevant_errors = [commands.CommandNotFound]
    is_irrelevant_error = [True if isinstance(error, ignored_error) else False for ignored_error in irrelevant_errors]
    logger.info(f"Handling error {error}...")
    if not any(is_irrelevant_error): #If the error is relevant
        error_embed = Embed(
            title="Fel",
            description="Följande fel inträffade:",
            color=Color.red()
        )
        #Generate an error description
        detailed_error_information = f"""
        Feltyp: `{type(error)}`
        Felinformation (traceback): `{error.__traceback__}`.
        Mer information: `{error}`
        """
        error_embed.add_field(name="Detaljerad felinformation",
                              value=detailed_error_information,
                              inline=False)
        await ctx.send(embed=error_embed) #Send error message


bot.run(os.environ["HOMEWORK_BOT_TOKEN"])
