__MODULE__ = "Grup Log"
__HELP__ = """
Bantuan Untuk Sudo

• Perintah: <code>{0}logger</code> [on/off]
• Penjelasan: Aktifkan tag log dan pm log.
"""


from pyrogram.enums import *
from pyrogram.types import *

from ubot import *


@PY.GC()
async def _(client, message):
    log = await get_log(client)
    cek = monggo.get_log_group(client.me.id)
    if not cek:
        return
    user = f"[{message.from_user.first_name} {message.from_user.last_name or ''}](tg://user?id={message.from_user.id})"
    message_link = message.link
    text = f"""
📨 <b>TAGS MESSAGE</b>
• <b>Logs:</b> <code>{client.me.first_name}</code>
• <b>Group:</b> <code>{message.chat.title}</code>
• <b>Dari :</b> <code>{user}</code>
• <b>Pesan:</b> <code>{message.text}</code>

• <b>Tautan Grup:</b> [Disini]({message_link})
"""
    try:
        await client.send_message(
            log.id,
            text,
            disable_web_page_preview=True,
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await client.send_message(
            log.id,
            text,
            disable_web_page_preview=True,
        )


@PY.PC()
async def _(client, message):
    log = await get_log(client)
    cek = monggo.get_log_group(client.me.id)
    if not cek:
        return
    if message.chat.id == 777000:
        return
    async for x in client.search_messages(message.chat.id, limit=1):
        await x.forward(log.id)


@PY.UBOT("logger", sudo=True)
async def _(client, message):
    xx = await message.reply(f"**Processing...**")
    cek = get_arg(message)
    logs = monggo.get_log_group(client.me.id)
    if cek.lower() == "on":
        if not logs:
            monggo.set_log_group(client.me.id, logger=True)
            await create_botlog(client)
            ajg = await get_log(client)
            babi = await client.export_chat_invite_link(int(ajg.id))
            return await xx.edit(f"**Log Group Berhasil Diaktifkan :\n\n{babi}**")
        else:
            return await xx.edit(f"**Log Group Anda Sudah Aktif.**")
    if cek.lower() == "off":
        if logs:
            monggo.del_log_group(client.me.id)
            ajg = await get_log(client)
            await client.delete_supergroup(int(ajg.id))
            return await xx.edit(f"**Log Group Berhasil Dinonaktifkan.**")
        else:
            return await xx.edit(f"**Log Group Anda Sudah Dinonaktifkan.**")
    else:
        return await xx.edit(
            f"**Format yang anda berikan salah. silahkan gunakan <code>{message.text} on/off</code>**"
        )
