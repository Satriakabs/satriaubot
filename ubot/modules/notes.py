import os

from pyrogram import errors
from pyrogram.types import *
from telegraph import upload_file

from ubot import (PY, Emo, ReplyCheck, Types, bot, build_keyboard,
                  get_note_type, monggo, parse_button, ubot)

# TODO: Add buttons support in some types
# TODO: Add group notes, but whats for? since only you can get notes

__MODULE__ = "Notes"
__HELP__ = """Bantuan Untuk Notes


• Perintah: <code>{0}save</code> [nama catatan] [balas pesan]
• Penjelasan: Untuk menyimpan catatan.

• Perintah: <code>{0}get</code> [nama catatan]
• Penjelasan: Untuk mengambil catatan.

• Perintah: <code>{0}rm</code> [nama catatan]
• Penjelasan: Untuk menghapus catatan.

• Perintah: <code>{0}notes</code>
• Penjelasan: Untuk melihat semua catatan.

• Button Format :
<code>[Teks](buttonurl://google.com)</code>
<code>[Teks 2](buttonurl://google.com:same)</code>
"""


def kontol_siapa(xi, tipe):
    return f"ubot/resources/{xi}.{tipe}"


@PY.UBOT("save", sudo=True)
async def save_note(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    gua = client.me.id
    cek = message.reply_to_message
    note_name, text, data_type, content = get_note_type(message)
    xx = await message.reply(f"{emo.proses} <b>Processing...</b>")
    if not note_name:
        return await xx.edit(
            f"{emo.gagal} <b>Gunakan format :</b> <code>save</code> [nama catatan] [balas ke pesan]."
        )

    if data_type == Types.TEXT:
        teks, _ = parse_button(text)
        if not teks:
            return await xx.edit(f"{emo.gagal} <b>Teks tidak dapat kosong.</b>")
        monggo.save_note(client.me.id, note_name, text, data_type, content)
    elif data_type in [Types.PHOTO, Types.VIDEO]:
        teks, _ = parse_button(text)
        file_type = "jpg" if data_type == Types.PHOTO else "mp4"
        xo = kontol_siapa(gua, file_type)
        mek = await client.download_media(cek, xo)
        xo_url = upload_file(mek)
        mmk = f"https://telegra.ph/{xo_url[0]}"
        monggo.save_note(client.me.id, note_name, text, data_type, mmk)
        os.remove(xo)
    await xx.edit(
        f"{emo.sukses} <b>Catatan <code>{note_name}</code> berhasil disimpan.</b>"
    )


@PY.UBOT("get", sudo=True)
async def get_note(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    xx = await message.reply(f"{emo.proses} <b>Processing...</b>")
    note = None
    if len(message.text.split()) >= 2:
        note = message.text.split()[1]
    else:
        await xx.edit(f"{emo.gagal} <b>Give me a note tag!</b>")

    getnotes = monggo.get_note(client.me.id, note)
    teks = None
    if not getnotes:
        return await xx.edit(f"{emo.gagal} <b>This note does not exist!</b>")

    if getnotes["type"] == Types.TEXT:
        teks, button = parse_button(getnotes.get("value"))
        button = build_keyboard(button)
        if button:
            button = InlineKeyboardMarkup(button)
        else:
            button = None
        if button:
            try:
                inlineresult = await client.get_inline_bot_results(
                    bot.me.username, f"get_note_ {note}"
                )
                await message.delete()
                await client.send_inline_bot_result(
                    message.chat.id,
                    inlineresult.query_id,
                    inlineresult.results[0].id,
                    reply_to_message_id=ReplyCheck(message),
                )
            except Exception as e:
                return await xx.edit(f"Error {e}")
        else:
            await message.reply(teks)

    elif getnotes["type"] == Types.PHOTO:
        teks, button = parse_button(getnotes.get("value"))
        button = build_keyboard(button)
        if button:
            button = InlineKeyboardMarkup(button)
        else:
            button = None
        if button:
            try:
                inlineresult = await client.get_inline_bot_results(
                    bot.me.username, f"get_note_ {note}"
                )
                await message.delete()
                await client.send_inline_bot_result(
                    message.chat.id,
                    inlineresult.query_id,
                    inlineresult.results[0].id,
                    reply_to_message_id=ReplyCheck(message),
                )
            except Exception as e:
                return await xx.edit(f"Error {e}")
        else:
            await client.send_photo(
                message.chat.id,
                getnotes["file"],
                caption=getnotes["value"],
                reply_to_message_id=ReplyCheck(message),
            )
    elif getnotes["type"] == Types.VIDEO:
        teks, button = parse_button(getnotes.get("value"))
        button = build_keyboard(button)
        if button:
            button = InlineKeyboardMarkup(button)
        else:
            button = None
        if button:
            try:
                inlineresult = await client.get_inline_bot_results(
                    bot.me.username, f"get_note_ {note}"
                )
                await message.delete()
                await client.send_inline_bot_result(
                    message.chat.id,
                    inlineresult.query_id,
                    inlineresult.results[0].id,
                    reply_to_message_id=ReplyCheck(message),
                )
            except Exception as e:
                return await xx.edit(f"Error {e}")
        else:
            await client.send_video(
                message.chat.id,
                getnotes["file"],
                caption=getnotes["value"],
                reply_to_message_id=ReplyCheck(message),
            )
    elif getnotes["type"] == Types.STICKER:
        await client.send_sticker(
            message.chat.id, getnotes["file"], reply_to_message_id=ReplyCheck(message)
        )
    elif getnotes["type"] == Types.VOICE:
        await client.send_voice(
            message.chat.id,
            getnotes["file"],
            caption=getnotes["value"],
            reply_to_message_id=ReplyCheck(message),
        )
    elif getnotes["type"] == Types.VIDEO_NOTE:
        await client.send_video_note(
            message.chat.id,
            getnotes["file"],
            # caption=getnotes["value"],
            reply_to_message_id=ReplyCheck(message),
        )
    elif getnotes["type"] == Types.ANIMATED_STICKER:
        await client.send_sticker(
            message.chat.id,
            getnotes["file"],
            # caption=getnotes["value"],
            reply_to_message_id=ReplyCheck(message),
        )
    else:
        if getnotes.get("value"):
            teks, button = parse_button(getnotes.get("value"))
            button = build_keyboard(button)
            if button:
                button = InlineKeyboardMarkup(button)
            else:
                button = None
        else:
            teks = None
            button = None
        if button:
            try:
                inlineresult = await client.get_inline_bot_results(
                    bot.me.username, f"get_note_ {note}"
                )
            except errors.exceptions.bad_request_400.BotInlineDisabled:
                await message.edit(
                    "Your bot inline isn't available!\nCheck your bot for more information!"
                )
                return
            try:
                await message.delete()
                await client.send_inline_bot_result(
                    message.chat.id,
                    inlineresult.query_id,
                    inlineresult.results[0].id,
                    reply_to_message_id=ReplyCheck(message),
                )
            except IndexError:
                await message.edit(
                    "An error has accured! Check your assistant for more information!"
                )
                return
        else:
            await client.send_media_group(
                message.chat.id,
                getnotes["file"],
                caption=teks,
                reply_to_message_id=ReplyCheck(message),
            )
    await xx.delete()


@PY.UBOT("notes", sudo=True)
async def local_notes(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    xx = await message.reply(f"{emo.proses} <b>Processing...</b>")
    getnotes = monggo.get_all_notes(client.me.id)
    if not getnotes:
        await xx.edit(f"{emo.gagal} <b>There are no notes in local notes!</b>")
        return
    rply = f"{emo.alive} <b>Local notes:</b>\n"
    for x in getnotes:
        if len(rply) >= 1800:
            await xx.edit(rply)
            rply = f"{emo.alive} <b>Local notes:</b>\n"
        rply += f"{emo.sukses} <code>{x}</code>\n"

    await xx.edit(rply)


@PY.UBOT("rm", sudo=True)
async def clear_note(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    xx = await message.reply(f"{emo.proses} <b>Processing...</b>")
    if len(message.text.split()) <= 1:
        return await xx.edit(f"{emo.gagal} <b>What do you want to clear?</b>")

    note = message.text.split()[1]
    getnote = monggo.rm_note(client.me.id, note)
    if not getnote:
        return await xx.edit(f"{emo.gagal} <b>This note does not exist!</b>")
    else:
        return await xx.edit(f"{emo.sukses} <b>Deleted note <code>{note}</code>!</b>")


@PY.INLINE("^get_note_")
async def catet(client, inline_query):
    for x in ubot._ubot:
        x.me.id
    q = inline_query.query.split(None, 1)
    notetag = q[1]
    inline_query.from_user.id
    noteval = monggo.get_note(inline_query.from_user.id, notetag)
    if not noteval:
        return
    note, button = parse_button(noteval.get("value"))
    button = build_keyboard(button)
    if noteval["type"] in [Types.PHOTO, Types.VIDEO]:
        file_type = "jpg" if noteval["type"] == Types.PHOTO else "mp4"
        biji = noteval.get("file")

        if noteval["type"] == Types.PHOTO:
            await client.answer_inline_query(
                inline_query.id,
                cache_time=0,
                results=[
                    InlineQueryResultPhoto(
                        title="Note Photo",
                        photo_url=biji,
                        caption=note,
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                ],
            )
        elif noteval["type"] == Types.VIDEO:
            await client.answer_inline_query(
                inline_query.id,
                cache_time=0,
                results=[
                    InlineQueryResultVideo(
                        title="Note Video",
                        video_url=biji,
                        caption=note,
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                ],
            )
    elif noteval["type"] == Types.TEXT:
        await client.answer_inline_query(
            inline_query.id,
            cache_time=0,
            results=[
                InlineQueryResultArticle(
                    title="Tombol Notes!",
                    input_message_content=InputTextMessageContent(note),
                    reply_markup=InlineKeyboardMarkup(button),
                )
            ],
        )
