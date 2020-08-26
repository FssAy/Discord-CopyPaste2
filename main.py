import discord
import asyncio
from discord.ext import commands
from copypaste import CopyPaste


class BotInstance:
    def __init__(self, loop=None):
        self.loop = loop
        self.prefix = "cp2"
        self.token = "TOKEN"

        self.bot = commands.Bot(command_prefix=self.prefix, loop=self.loop, fetch_offline_members=False)

    async def run(self):

        @self.bot.event
        async def on_message(message):
            if not message.content.lower().startswith(self.prefix):
                return
            elif message.content == self.prefix:
                return
            if message.author == self.bot.user:
                return

            channel = message.channel
            guild = message.guild

            _message = message.content[len(self.prefix):]
            _message = _message.split(' ')
            _message_list = []
            for item in _message:
                if item != "":
                    _message_list.append(item)
            args = _message_list
            command = _message_list[0].lower()
            del _message_list
            del _message

            # --- Commands
            try:

                if command == "copy":
                    if len(args) < 3:
                        await channel.send(f"**ERROR**\nCommand {command} should look like this: `{self.prefix} {command} <GuildID-Original> <GuildID-Target>`")
                        return
                    if len(args[1]) != 18 or len(args[2]) != 18:
                        await channel.send(f"**ERROR**\nInvalid ID!")
                        return
                    try:
                        guild_from = self.bot.get_guild(int(args[1]))
                        guild_to = self.bot.get_guild(int(args[2]))
                    except ValueError:
                        await channel.send(f"**ERROR**\nInvalid ID!")
                        return
                    if guild_from is None or guild_to is None:
                        await channel.send(f"**Error**\nCan't find any guild with this ID!")
                        return

                    msg = await channel.send(f"**Copying...**")
                    await CopyPaste.roles_delete(guild_to)
                    await CopyPaste.channels_delete(guild_to)
                    await CopyPaste.emojis_delete(guild_to)
                    await CopyPaste.roles_create(guild_to, guild_from)
                    await CopyPaste.emojis_create(guild_to, guild_from)
                    await CopyPaste.categories_create(guild_to, guild_from)
                    await CopyPaste.channels_create(guild_to, guild_from)
                    await CopyPaste.members_manage(guild_to, guild_from)
                    await CopyPaste.guild_edit(guild_to, guild_from)
                    CopyPaste.done()
                    await msg.edit(content=f"**DONE!**")
                    return

                if command == "check":
                    await channel.send("**Online!**")
                    return

            except discord.errors.Forbidden:
                error_msg = f"*ERROR**\n Bot is missing permission to execute command ` {command} ` sent by ` **{message.author}#{message.author.discriminator}** (*{message.author.id}*) `\n||{message.jump_url}||"
                try:
                    await channel.send(error_msg)
                except discord.errors.Forbidden:
                    try:
                        await message.author.send(error_msg)
                    except:
                        try:
                            await guild.owner.send(error_msg)
                        except:
                            pass

        @self.bot.event
        async def on_ready():
            print_data = [
                f"╔═══════════════════════════ ONLINE ═══════════════════════════╗",
                f"║ Logged in as: {self.bot.user.name}#{self.bot.user.discriminator} | {self.bot.user.id}",
            ]

            for index in range(len(print_data)):
                if index != 0:
                    print_data[index] += ((len(print_data[0]) - len(print_data[index])-1) * " ") + "║"
            print_data.append(f"╚{'═'*(len(print_data[0])-2)}╝")

            for line in print_data:
                print(line)

        # --- START
        await self.bot.start(self.token, bot=False)


main_loop = asyncio.get_event_loop()
bot_instances = [
    BotInstance(loop=main_loop)
]

for bot_instance in bot_instances:
    main_loop.create_task(bot_instance.run())
main_loop.run_forever()
