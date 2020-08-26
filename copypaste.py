import discord


def print_log(message):
    print(f'[log] {message}')


def print_warning(message):
    print(f'[WARNING] {message}')


def print_error(message):
    print(f'[ERROR] {message}')


class CopyPaste:
    @staticmethod
    async def roles_delete(guild_to: discord.Guild):
        for role in guild_to.roles:
            try:
                if role.name != "CopyPaste2" and role.name != "@everyone":
                    await role.delete()
                    print_log(f"Role {role.name} has been deleted from {guild_to.name}")
            except discord.Forbidden:
                print_error(f"Can't delete role {role.name} from {guild_to.name} (Forbidden)")
            except discord.HTTPException:
                print_error(f"Can't delete role {role.name} from {guild_to.name}")

    @staticmethod
    async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
        roles = []
        role: discord.Role
        for role in guild_from.roles:
            if role.name != "CopyPaste2" and role.name != "@everyone":
                roles.append(role)
        roles = roles[::-1]
        for role in roles:
            try:
                await guild_to.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    colour=role.colour,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                print_log(f"Role {role.name} has been created in {guild_to.name}")
            except discord.Forbidden:
                print_error(f"Can't create role {role.name} in {guild_to.name} (Forbidden)")
            except discord.HTTPException:
                print_error(f"Can't create role {role.name} in {guild_to.name}")

    @staticmethod
    async def channels_delete(guild_to: discord.Guild):
        for channel in guild_to.channels:
            try:
                await channel.delete()
                print_log(f"Channel {channel.name} has been deleted from {guild_to.name}")
            except discord.Forbidden:
                print_error(f"Can't delete channel {channel.name} from {guild_to.name} (Forbidden)")
            except discord.HTTPException:
                print_error(f"Can't delete channel {channel.name} from {guild_to.name}")

    @staticmethod
    async def categories_create(guild_to: discord.Guild, guild_from: discord.Guild):
        channels = guild_from.categories
        channel: discord.CategoryChannel
        new_channel: discord.CategoryChannel
        for channel in channels:
            try:
                overwrites_to = {}
                for key, value in channel.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                new_channel = await guild_to.create_category(
                    name=channel.name,
                    overwrites=overwrites_to)
                await new_channel.edit(position=channel.position)
                print_log(f"Channel {channel.name} has been created in {guild_to.name}")
            except discord.Forbidden:
                print_error(f"Can't create channel {channel.name} in {guild_to} (Forbidden)")
            except discord.HTTPException:
                print_error(f"Can't create channel {channel.name} in {guild_to}")

    @staticmethod
    async def channels_create(guild_to: discord.Guild, guild_from: discord.Guild):
        channel_text: discord.TextChannel
        channel_voice: discord.VoiceChannel
        category = None
        for channel_text in guild_from.text_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_text.category.name:
                            break
                    except AttributeError:
                        print_warning(f"Channel {channel_text.name} doesn't have any category!")
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_text.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position,
                        topic=channel_text.topic,
                        slowmode_delay=channel_text.slowmode_delay,
                        nsfw=channel_text.nsfw)
                except:
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_log(f"Channel {channel_text.name} has been created in {guild_to.name}")
            except discord.Forbidden:
                print_error(f"Can't create channel {channel_text.name} in {guild_to} (Forbidden)")
            except discord.HTTPException:
                print_error(f"Can't create channel {channel_text.name} in {guild_to}")
            except:
                print_error(f"Can't create channel {channel_text.name} in {guild_to} (Unknown)")

        category = None
        for channel_voice in guild_from.voice_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_voice.category.name:
                            break
                    except AttributeError:
                        print_warning(f"Channel {channel_voice.name} doesn't have any category!")
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_voice.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position,
                        bitrate=channel_voice.bitrate,
                        user_limit=channel_voice.user_limit,
                        )
                except:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_log(f"Channel {channel_voice.name} has been created in {guild_to.name}")
            except discord.Forbidden:
                print_error(f"Can't create channel {channel_voice.name} in {guild_to} (Forbidden)")
            except discord.HTTPException:
                print_error(f"Can't create channel {channel_voice.name} in {guild_to}")
            except:
                print_error(f"Can't create channel {channel_voice.name} in {guild_to} (Unknown)")

    @staticmethod
    async def members_manage(guild_to: discord.Guild, guild_from: discord.Guild):
        member_to: discord.Member
        member_from: discord.Member
        for member_from in guild_from.members:
            if member_from in guild_to.members:
                member_to = guild_to.get_member(member_from.id)
                try:
                    roles = []
                    for role_from in member_from.roles:
                        role_to = discord.utils.get(guild_to.roles, name=role_from.name)
                        if role_to is not None and role_to.name != "@everyone" and role_to.name != "CopyPaste2":
                            roles.append(role_to)
                    for role in roles:
                        await member_to.add_roles(role)
                    print_log(f"Roles for member {member_to.name} has been added in {guild_to.name}")
                except discord.Forbidden:
                    print_error(f"Can't add roles for member {member_to.name} in {guild_to.name} (Forbidden)")
                except discord.HTTPException:
                    print_error(f"Can't add roles for member {member_to.name} in {guild_to.name}")

    @staticmethod
    async def emojis_delete(guild_to: discord.Guild):
        for emoji in guild_to.emojis:
            try:
                await emoji.delete()
                print_log(f"Emoji {emoji.name} has been deleted from {guild_to.name}")
            except discord.Forbidden:
                print_error(f"Can't delete emoji {emoji.name} from {guild_to.name} (Forbidden)")
            except discord.HTTPException:
                print_error(f"Can't delete emoji {emoji.name} from {guild_to.name}")

    @staticmethod
    async def emojis_create(guild_to: discord.Guild, guild_from: discord.Guild):
        emoji: discord.Emoji
        for emoji in guild_from.emojis:
            try:
                emoji_image = await emoji.url.read()
                await guild_to.create_custom_emoji(
                    name=emoji.name,
                    image=emoji_image)
                print_log(f"Emoji {emoji.name} has been created in {guild_to.name}")
            except discord.Forbidden:
                print_error(f"Can't create emoji {emoji.name} in {guild_to.name} (Forbidden)")
            except discord.HTTPException:
                print_error(f"Can't create emoji {emoji.name} in {guild_to.name}")

    @staticmethod
    async def guild_edit(guild_to: discord.Guild, guild_from: discord.Guild):
        print_log(f"Editing {guild_to.name} ...")
        try:
            try:
                icon_image = await guild_from.icon_url.read()
            except discord.errors.DiscordException:
                print_error(f"Can't read icon image from {guild_from.name}")
                icon_image = None
            await guild_to.edit(name=guild_from.name)
            if icon_image is not None:
                try:
                    await guild_to.edit(icon=icon_image)
                    print_log(f"Icon has ben set for {guild_to.name}")
                except:
                    print_error(f"Can't set icon for {guild_to.name}")
        except discord.Forbidden:
            print_error(f"Can't edit {guild_to} (Forbidden)")
        print_log(f"Editing {guild_to.name} done")

    @staticmethod
    def done():
        print_log("DONE!")

