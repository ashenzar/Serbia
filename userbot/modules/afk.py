# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
# All Credits to https://t.me/azrim89 for timestamp.

""" Userbot module which contains afk-related commands """

import time as Time

from datetime import datetime
from random import choice, randint

from telethon.events import StopPropagation
from telethon.tl.functions.account import UpdateProfileRequest

from userbot import (AFKREASON, AFK_MEDIA, COUNT_MSG, CMD_HELP, ISAFK, BOTLOG,
                     BOTLOG_CHATID, USERS, PM_AUTO_BAN, bot)
from userbot.events import register

# ========================= CONSTANTS ============================
AFKSTR = [
    "`Estoy ocupado, pero si quieres hablar con alguien habla con tu psicóloga sobre mí.`",
    "Estoy lejos justo ahora. Si necesitas algo deja un mensaje después del tono:\n`beeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeep`!",
    "`Se nota que me extrañas.`",
    "`Espera un segundo a que regrese y si no regreso...,\nespera dos.`",
    "`No estoy aquí justo ahora, así que probablemente estoy en algún otro lugar.`",
    "`Las mejores cosas en la vida son por las que vale la pena esperar...\nRegresaré pronto.`",
    "`Voy a regresar pronto,\nPero si no he regresado pronto,\nRegresaré después.`",
    "`Por si todavía no te has dado cuenta,\nNo estoy aquí.`",
    "`Hola, bienvenido a mi mensaje de AFK, ¿De que manera puedo ignorarte hoy?`",
    "`Estoy lejos sobre 7 reinos y 7 países,\n7 mares y 7 continentes,\n7 montañas y 7 colinas,\n7 planicies y 7 montes,\n7 estanques y 7 lagos,\n7 muelles y 7 prados,\n7 ciudades y 7 vecindades,\n7 palacios y 7 casas...\n\n¡Donde ni siquiera tus mensajes pueden alcanzarme!`",
    "`Estoy lejos del teclado por el momento, pero si gritas lo suficientemente fuerte a tu pantalla. Talvez pueda escucharte.`",
    "`Me fui por aquí\n---->`",
    "`Me fui por aquí\n<----`",
    "`Deja un mensaje y hazme sentir incluso más importante de lo que ya soy.`",
    "`No estoy aquí así que deja de escribirme,\nsi no vas a encontrar el chat lleno de tus propios mensajes.`",
    "`Si estuviera aquí,\nTe diría donde estoy.\n\nPero no estoy aquí,\nAsí que preguntame cuando regrese...`",
    "`¡Estoy lejos!\n¡No sé cuando voy a regresar!\n¡Ojalá dentro de unos minutos!`",
    "`No estoy disponible justo ahora así que deja tu nombre, número y dirección para que pueda ir a acosarte después.`",
    "`No estoy aquí.\nHabla con mi userbot tanto como quieras.`",
    "`¡Apuesto a que estabas esperando un mensaje de AFK!`",
    "`La vida es corta, hay muchas cosas que hacer...\nEstoy lejos haciendo una de ellas.`",
    "`No estoy aquí justo ahora...\npero si estuviera aquí...\n\n¿No sería eso sorprendente?`",
]


global USER_AFK  # pylint:disable=E0602
global afk_time  # pylint:disable=E0602
global afk_start
global afk_end
USER_AFK = {}
afk_time = None
afk_start = {}

# =================================================================
@register(outgoing=True, pattern="^.afk(?: |$)(.*)", disable_errors=True)
async def set_afk(afk_e):
    """ For .afk command, allows you to inform people that you are afk when they message you """
    message = afk_e.text
    string = afk_e.pattern_match.group(1)
    global ISAFK
    global AFKREASON
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    user = await bot.get_me()
    global reason
    USER_AFK = {}
    afk_time = None
    afk_end = {}
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    global image
    if AFK_MEDIA is not None:
        image = f"[‎]({AFK_MEDIA})"
    else:
        image = ""

    if string:
        AFKREASON = string
        afk_r = await afk_e.respond(f"Me voy AFK\
        \nRazón: {AFKREASON}{image}")
    else:
        await afk_e.respond("Me voy AFK")
    if user.last_name:
        await afk_e.client(UpdateProfileRequest(first_name=user.first_name, last_name=user.last_name + " [ AFK ]"))
    else:
        await afk_e.client(UpdateProfileRequest(first_name=user.first_name, last_name=" [ AFK ]"))
    if BOTLOG:
        await afk_e.client.send_message(BOTLOG_CHATID, "#AFK\nTe fuiste AFK.")
    await afk_e.delete()
    ISAFK = True
    afk_time = datetime.now()  # pylint:disable=E0602
    raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(notafk):
    """ This sets your status as not afk automatically when you write something while being afk """
    global ISAFK
    global COUNT_MSG
    global USERS
    global AFKREASON
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    user = await bot.get_me()
    last = user.last_name
    if last and last.endswith(" [ AFK ]"):
        last1 = last[:-8]
    else:
        last1 = ""
    back_alive = datetime.now()
    afk_end = back_alive.replace(microsecond=0)
    if ISAFK:
        ISAFK = False
        await notafk.client(UpdateProfileRequest(first_name=user.first_name, last_name=last1))
        if BOTLOG:
            await notafk.client.send_message(
                BOTLOG_CHATID,
                "Has recibido " + str(COUNT_MSG) + " mensajes de " +
                str(len(USERS)) + " chats mientras estabas fuera.",
            )
            for i in USERS:
                if str(i).isnumeric():
                    name = await notafk.client.get_entity(i)
                    name0 = str(name.first_name)
                    await notafk.client.send_message(
                        BOTLOG_CHATID,
                        "[" + name0 + "](tg://user?id=" + str(i) + ")" +
                        " te envió " + "`" + str(USERS[i]) + "`" + " mensajes.",
                    )
                else:  # anon admin
                    await notafk.client.send_message(
                        BOTLOG_CHATID,
                        "Un admin anónimo en `" + i + "` tw envió " + "`" +
                        str(USERS[i]) + "`" + " mensajes.",
                    )
        COUNT_MSG = 0
        USERS = {}
        AFKREASON = None


@register(incoming=True, disable_edited=True)
async def mention_afk(mention):
    """This function takes care of notifying the people who mention you that you are AFK."""
    global COUNT_MSG
    global USERS
    global ISAFK
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    afk_since = "un momento"
    if ISAFK and mention.message.mentioned:
        now = datetime.now()
        datime_since_afk = now - afk_time  # pylint:disable=E0602
        time = float(datime_since_afk.seconds)
        days = time // (24 * 3600)
        time %= 24 * 3600
        hours = time // 3600
        time %= 3600
        minutes = time // 60
        time %= 60
        seconds = time
        if days == 1:
            afk_since = "un día"
        elif days > 1:
            if days > 6:
                date = now + \
                    datetime.timedelta(
                        days=-days, hours=-hours, minutes=-minutes)
                afk_since = date.strftime("%A, %Y %B %m, %H:%I")
            else:
                wday = now + datetime.timedelta(days=-days)
                afk_since = wday.strftime('%A')
        elif hours > 1:
            afk_since = f"`{int(hours)}h{int(minutes)}m`"
        elif minutes > 0:
            afk_since = f"`{int(minutes)}m{int(seconds)}s`"
        else:
            afk_since = f"`{int(seconds)}s`"

        is_bot = False
        if (sender := await mention.get_sender()):
            is_bot = sender.bot
            if is_bot: return  # ignore bot

        chat_obj = await mention.client.get_entity(mention.chat_id)
        chat_title = chat_obj.title

        if mention.sender_id not in USERS or chat_title not in USERS:
            if AFKREASON:
                msg = await mention.reply(f"Estoy AFK desde hace {afk_since}\
                        \nRazón: {AFKREASON}{image}")
            else:
                msg = await mention.reply(str(choice(AFKSTR)))

            Time.sleep(10)
            await msg.delete()

            if mention.sender_id is not None:
                USERS.update({mention.sender_id: 1})
            else:
                USERS.update({chat_title: 1})
        else:
            if AFKREASON:
                msg = await mention.reply(f"Sigo AFK desde hace {afk_since}\
                        \nRazón: {AFKREASON}{image}")
            else:
                msg = await mention.reply(str(choice(AFKSTR)))

            Time.sleep(10)
            await msg.delete()

            if mention.sender_id is not None:
                USERS[mention.sender_id] += 1
            else:
                USERS[chat_title] += 1
        COUNT_MSG += 1

@register(incoming=True, disable_errors=True)
async def afk_on_pm(sender):
    """ Function which informs people that you are AFK in PM """
    global ISAFK
    global USERS
    global COUNT_MSG
    global COUNT_MSG
    global USERS
    global ISAFK
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    user = await bot.get_me()
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    afk_since = "un momento"
    if sender.is_private and sender.sender_id != 777000 and not (
            await sender.get_sender()).bot:
        if PM_AUTO_BAN:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import is_approved
                apprv = is_approved(sender.sender_id)
            except AttributeError:
                apprv = True
        else:
            apprv = True
        if apprv and ISAFK:
            now = datetime.now()
            datime_since_afk = now - afk_time  # pylint:disable=E0602
            time = float(datime_since_afk.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            if days == 1:
                afk_since = "un día"
            elif days > 1:
                if days > 6:
                    date = now + \
                        datetime.timedelta(
                            days=-days, hours=-hours, minutes=-minutes)
                    afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    afk_since = wday.strftime('%A')
            elif hours > 1:
                afk_since = f"`{int(hours)}h {int(minutes)}m`"
            elif minutes > 0:
                afk_since = f"`{int(minutes)}m {int(seconds)}s`"
            else:
                afk_since = f"`{int(seconds)}s`"
            if sender.sender_id not in USERS:
                if AFKREASON:
                    msg = await sender.reply(f"Estoy AFK desde hace {afk_since}\
                        \nRazón: {AFKREASON}{image}")
                else:
                    msg = await sender.reply(str(choice(AFKSTR)))

                Time.sleep(10)
                await msg.delete()

                USERS.update({sender.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif apprv and sender.sender_id in USERS:
                if AFKREASON:
                    msg = await sender.reply(f"Sigo AFK desde hace {afk_since}\
                        \nRazón: {AFKREASON}{image}")
                else:
                    msg = await sender.reply(str(choice(AFKSTR)))

                Time.sleep(10)
                await msg.delete()

                USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                COUNT_MSG = COUNT_MSG + 1


CMD_HELP.update({
    "afk":
    "`.afk` [Optional Reason]\
\nUsage: Sets you as afk.\nReplies to anyone who tags/PM's \
you telling them that you are AFK(reason).\n\nSwitches off AFK when you type back anything, anywhere.\
"
})
