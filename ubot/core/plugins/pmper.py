from pyrogram import *
from pyrogram.types import *

from ubot import *

PM_GUARD_WARNS_DB = {}
PM_GUARD_MSGS_DB = {}

flood = {}
flood2 = {}

DEFAULT_TEXT = """
I am {} maintains this Chat Room . Don't spam or You will be auto blocked.
"""

PM_WARN = """
Security Message <b>{}</b> . You have <code>{}/{}</code> warnings !!

<b>{}</b>
"""

LIMIT = 5


async def permitpm(client, message):
    user_id = client.me.id
    babi = await message.reply("`Processing...`")
    bacot = get_arg(message)
    if not bacot:
        return await babi.edit(f"`Gunakan Format : `{0}pmpermit on or off`.`")
    is_already = monggo.get_var(user_id, "ANTI_PM")
    if bacot.lower() == "on":
        if is_already:
            return await babi.edit("`PMPermit Sudah DiHidupkan.`")
        monggo.set_var(user_id, "ANTI_PM", True)
        await babi.edit("`PMPermit Berhasil DiHidupkan.`")
    elif bacot.lower() == "off":
        if not is_already:
            return await babi.edit("`PMPermit Sudah DiMatikan.`")
        monggo.set_var(user_id, "ANTI_PM", False)
        await babi.edit("`PMPermit Berhasil DiMatikan.`")
    else:
        await babi.edit(f"`Gunakan Format : `{0}pmpermit on or off`.`")


async def approve(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    babi = await message.reply(f"{emo.proses} <b>Processing...</b>")
    chat_type = message.chat.type
    getc_pm_warns = monggo.get_var(client.me.id, "PM_LIMIT")
    pm_text = monggo.get_var(client.me.id, "PM_TEXT")
    custom_pm_txt = pm_text if pm_text else DEFAULT_TEXT
    custom_pm_warns = getc_pm_warns if getc_pm_warns else LIMIT
    if chat_type == "me":
        return await babi.edit(f"{emo.gagal} <b>Apakah anda sudah gila ?</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        if not message.reply_to_message:
            return await babi.edit(
                f"{emo.gagal} <b>Balas ke pesan pengguna, untuk disetujui.</b>"
            )
        dia = message.reply_to_message.from_user.id
    elif chat_type == enums.ChatType.PRIVATE:
        dia = message.chat.id
    else:
        return
    ok_tak = monggo.dicek_pc(dia)
    if ok_tak:
        return await babi.edit(f"{emo.sukses} <b>Pengguna ini sudah disetujui.</b>")

    teks, button = parse_button(custom_pm_txt)
    button = build_keyboard(button)
    if button:
        button = InlineKeyboardMarkup(button)
    else:
        button = None
    if button:
        async for m in client.get_chat_history(dia, limit=custom_pm_warns):
            if m.reply_markup:
                await m.delete()
    else:
        try:
            await client.delete_messages("me", message_ids=flood2[dia])
        except KeyError:
            pass
        # if dia in flood:
        # try:
        # await client.delete_messages(
        # chat_id, message_ids=flood2[dia])
        # except BaseException:
        # pass
    monggo.oke_pc(dia)
    await babi.edit(
        f"{emo.sukses} <b>Baiklah, pengguna ini disetujui untuk mengirim pesan.</b>"
    )


async def disapprove(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    babi = await message.reply(f"{emo.proses} <b>Processing...</b>")
    await asyncio.sleep(2)
    rep = message.reply_to_message
    chat_type = message.chat.type
    if chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        if not rep:
            return await babi.edit(
                f"{emo.gagal} <b>Balas ke pesan pengguna, untuk ditolak.</b>"
            )
        message.reply_to_message.from_user.id
    elif chat_type == enums.ChatType.PRIVATE:
        user_id = message.chat.id
    else:
        return
    ok_tak = monggo.dicek_pc(user_id)
    if not ok_tak:
        return await babi.edit(
            f"{emo.gagal} <b>Pengguna ini memang belum disetujui untuk mengirim pesan.</b>"
        )
    monggo.tolak_pc(user_id)
    await babi.edit(
        f"{emo.sukses} <b>Baiklah, pengguna ini ditolak untuk mengirim pesan.</b>"
    )


async def get_msg(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    jing = await message.reply(f"{emo.proses} <b>Processing...</b>")
    if len(message.command) < 2:
        return await jing.edit(
            f"{emo.gagal} <b>Tidak ada variabel tersebut !! Variabel : <code>pmpic</code>, <code>pmtext</code>, <code>pmlimit</code>.</b>"
        )
    command, variable = message.command[:2]
    if variable.lower() == "pmtext":
        bb = monggo.get_var(client.me.id, "PM_TEXT")
        cc = bb if bb else DEFAULT_TEXT
        teks, button = parse_button(cc)
        button = build_keyboard(button)
        if button:
            button = InlineKeyboardMarkup(button)
        else:
            button = None
        if button:
            try:
                x = await client.get_inline_bot_results(
                    bot.me.username, f"get_teks_but {message.chat.id}"
                )
                await client.send_inline_bot_result(
                    message.chat.id,
                    x.query_id,
                    x.results[0].id,
                    reply_to_message_id=ReplyCheck(message),
                )
                await jing.delete()
            except Exception as e:
                await jing.edit(f"Error {e}")
        else:
            await jing.edit(
                f"{emo.sukses} <b>Ini PM Text anda :\n<code>{bb}</code></b>"
            )
    elif variable.lower() == "pmlimit":
        bb = monggo.get_var(client.me.id, "PM_LIMIT")
        await jing.edit(f"{emo.sukses} <b>Ini PM Limit anda :\n<code>{bb}</code></b>")
    elif variable.lower() == "pmpic":
        bb = monggo.get_var(client.me.id, "PM_PIC")
        await jing.edit(f"{emo.sukses} <b>Ini PM Pic anda :\n<code>{bb}</code></b>")
    else:
        await jing.edit(
            f"{emo.gagal} <b>Tidak ada variabel tersebut !! Variabel : <code>pmpic</code>, <code>pmtext</code>, <code>pmlimit</code>.</b>"
        )


async def geteksbut(client, iq):
    gw = iq.from_user.id
    getpm_txt = monggo.get_var(gw, "PM_TEXT")
    pm_text = getpm_txt if getpm_txt else DEFAULT_TEXT
    teks, button = parse_button(pm_text)
    button = build_keyboard(button)
    duar = [
        (
            InlineQueryResultArticle(
                title="Tombol Teks PM!",
                input_message_content=InputTextMessageContent(getpm_txt),
                reply_markup=InlineKeyboardMarkup(button),
            )
        )
    ]
    await client.answer_inline_query(iq.id, cache_time=0, results=duar)


async def set_msg(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    babi = await message.reply(f"{emo.proses} <b>Processing...</b>")
    await asyncio.sleep(2)
    user_id = client.me.id
    r_msg = message.reply_to_message
    args_txt = get_arg(message)
    if r_msg:
        if r_msg.text:
            pm_txt = r_msg.text
        else:
            return await babi.edit(
                f"{emo.gagal} <b>Silakan balas ke pesan untuk dijadikan teks PMPermit !</b>"
            )
    elif args_txt:
        pm_txt = args_txt
    else:
        return await babi.edit(
            f"{emo.gagal} <b>Silakan balas ke pesan atau berikan pesan untuk dijadikan teks PMPermit !\nContoh :<code>{message.text} Halo saya anuan.</code></b>"
        )
    teks, _ = parse_button(pm_txt)
    monggo.set_var(user_id, "PM_TEXT", pm_txt)
    await babi.edit(
        f"{emo.sukses} <b>Pesan PMPemit berhasil diatur menjadi : <code>{pm_txt}</code>.</b>"
    )


async def set_limit(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    babi = await message.reply(f"{emo.proses} <b>Processing...</b>")
    await asyncio.sleep(2)
    user_id = client.me.id
    args_txt = get_arg(message)
    if args_txt:
        if args_txt.isnumeric():
            pm_warns = int(args_txt)
        else:
            return await babi.edit(
                f"{emo.gagal} <b>Silakan berikan untuk angka limit !</b>"
            )
    else:
        return await babi.edit(
            f"{emo.gagal} <b>Silakan berikan pesan untuk dijadikan angka limit !\nContoh :<code> {message.text}setlimit 5.</code></b>"
        )
    monggo.set_var(user_id, "PM_LIMIT", pm_warns)
    await babi.edit(
        f"{emo.sukses} <b>Pesan Limit berhasil diatur menjadi : <code>{args_txt}</code>.</b>"
    )


async def handle_pmpermit(client, message):
    user_id = client.me.id
    siapa = message.from_user.id
    biji = message.from_user.mention
    chat_id = message.chat.id
    in_user = message.from_user
    fsdj = monggo.dicek_pc(chat_id)
    is_pm_guard_enabled = monggo.get_var(user_id, "ANTI_PM")
    getc_pm_txt = monggo.get_var(user_id, "PM_TEXT")
    getc_pm_warns = monggo.get_var(user_id, "PM_LIMIT")
    master = await client.get_me()
    custom_pm_txt = getc_pm_txt if getc_pm_txt else DEFAULT_TEXT
    custom_pm_warns = getc_pm_warns if getc_pm_warns else LIMIT
    if not is_pm_guard_enabled:
        return

    if fsdj:
        return

    if in_user.is_fake or in_user.is_scam:
        await message.reply("**Sepertinya anda mencurigakan...**")
        return await client.block_user(in_user.id)
    if in_user.is_support or in_user.is_verified or in_user.is_self:
        return
    if siapa in DEVS:
        try:
            monggo.oke_pc(chat_id)
            await client.send_message(
                chat_id,
                f"<b>Menerima Pesan Dari {biji} !!\nTerdeteksi Founder Dari {bot.me.first_name}.</b>",
                parse_mode=enums.ParseMode.HTML,
            )
        except BaseException:
            pass
        return
    teks, button = parse_button(custom_pm_txt)
    button = build_keyboard(button)
    if button:
        button = InlineKeyboardMarkup(button)
    else:
        button = None
    if button:
        try:
            x = await client.get_inline_bot_results(
                bot.me.username, f"ambil_tombolpc {chat_id}"
            )
            await client.send_inline_bot_result(
                message.chat.id,
                x.query_id,
                x.results[0].id,
                reply_to_message_id=ReplyCheck(message),
            )
        except Exception as e:
            return await eor(message, f"Error {e}")
    else:
        gmbr = monggo.get_var(user_id, "PM_PIC")
        if gmbr:
            kok_poto = (
                message.reply_video if gmbr.endswith(".mp4") else message.reply_photo
            )
            if in_user.id in flood:
                try:
                    if chat_id in flood2:
                        await client.delete_messages(
                            chat_id, message_ids=flood2[chat_id]
                        )
                except BaseException:
                    pass
                flood[in_user.id] += 1
                if flood[in_user.id] >= custom_pm_warns:
                    del flood[in_user.id]
                    await message.reply(
                        f"{emo.gagal} <b>Saya sudah memberi tahu `{custom_pm_warns}` peringatan\nTunggu tuan saya menyetujui pesan anda, atau anda akan diblokir !</b>"
                    )
                    return await client.block_user(in_user.id)
                else:
                    rplied_msg = await kok_poto(
                        gmbr,
                        caption=PM_WARN.format(
                            master.first_name,
                            flood[in_user.id],
                            custom_pm_warns,
                            custom_pm_txt.format(bot.me.first_name),
                        ),
                    )
            else:
                flood[in_user.id] = 1
                rplied_msg = await kok_poto(
                    gmbr,
                    caption=PM_WARN.format(
                        master.first_name,
                        flood[in_user.id],
                        custom_pm_warns,
                        custom_pm_txt.format(bot.me.first_name),
                    ),
                )
            flood2[chat_id] = rplied_msg.id
        else:
            if in_user.id in flood:
                try:
                    if chat_id in flood2:
                        await client.delete_messages(
                            chat_id, message_ids=flood2[chat_id]
                        )
                except BaseException:
                    pass
                flood[in_user.id] += 1
                if flood[in_user.id] >= custom_pm_warns:
                    del flood[in_user.id]
                    await message.reply(
                        f"{emo.gagal} <b>Saya sudah memberi tahu `{custom_pm_warns}` peringatan\nTunggu tuan saya menyetujui pesan anda, atau anda akan diblokir !</b>"
                    )
                    return await client.block_user(in_user.id)
                else:
                    rplied_msg = await message.reply(
                        PM_WARN.format(
                            master.first_name,
                            flood[in_user.id],
                            custom_pm_warns,
                            custom_pm_txt.format(bot.me.first_name),
                        ),
                    )
            else:
                flood[in_user.id] = 1
                rplied_msg = await message.reply(
                    PM_WARN.format(
                        master.first_name,
                        flood[in_user.id],
                        custom_pm_warns,
                        custom_pm_txt.format(bot.me.first_name),
                    ),
                )
            flood2[chat_id] = rplied_msg.id


async def pc_inline(client, iq):
    org = iq.query.split()
    gw = iq.from_user.id
    getpm_txt = monggo.get_var(gw, "PM_TEXT")
    getpm_warns = monggo.get_var(gw, "PM_LIMIT")
    pm_warns = getpm_warns if getpm_warns else LIMIT
    pm_text = getpm_txt if getpm_txt else DEFAULT_TEXT
    teks, button = parse_button(pm_text)
    button = build_keyboard(button)
    kiki = None
    for ki in ubot._ubot:
        if ki.me.id == gw:
            if int(org[1]) in flood2:
                flood2[int(org[1])] += 1
            else:
                flood2[int(org[1])] = 1
            async for m in ki.get_chat_history(int(org[1]), limit=pm_warns):
                if m.reply_markup:
                    await m.delete()
            kiki = PM_WARN.format(
                ki.me.first_name,
                flood2[int(org[1])],
                pm_warns,
                teks.format(bot.me.first_name),
            )
            if flood2[int(org[1])] > pm_warns:
                await ki.send_message(int(org[1]), "Spam Terdeteksi !!! Blokir.")
                del flood2[int(org[1])]
                await ki.block_user(int(org[1]))
                return
            lah = monggo.get_var(gw, "PM_PIC")

            if lah:
                filem = (
                    InlineQueryResultVideo
                    if lah.endswith(".mp4")
                    else InlineQueryResultPhoto
                )
                url_ling = (
                    {"video_url": lah, "thumb_url": lah}
                    if lah.endswith(".mp4")
                    else {"photo_url": lah}
                )
                duar = [
                    filem(
                        **url_ling,
                        title="PIC Buttons !",
                        caption=kiki,
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                ]
            else:
                duar = [
                    (
                        InlineQueryResultArticle(
                            title="Tombol PM!",
                            input_message_content=InputTextMessageContent(kiki),
                            reply_markup=InlineKeyboardMarkup(button),
                        )
                    )
                ]
            await client.answer_inline_query(iq.id, cache_time=0, results=duar)
