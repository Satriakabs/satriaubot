from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ubot import *


class MSG:
    def EXPIRED_MSG_BOT(X):
        return f"""
<b>❏ Announcement</b>
<b>├ Account :</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>├ ID:</b> <code>{X.me.id}</code>
<b>╰ Active Time Expired</b>
"""

    def START(message):
        if not message.from_user.id == USER_ID:
            msg = f"""
<b>👋 Hello {message.from_user.first_name} !! Is there anything I can help ?

If you have already made a payment, please click the Create Userbot button.</b>
"""
        else:
            msg = f"""
🧑‍💻 Developer <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>

✅ Gunakan Dengan Bijak !!!
"""
        return msg

    def TEXT_PAYMENT(harga, total, bulan):
        return f"""
<b>Please Make Payment First</b>

<b>Monthly Price: {harga}.000</b>

<b>💳 Payment method:</b>
 <b>├──• Dana </b>
 <b>├─• <code>085718366690</code></b>


<b>🔖 Total price: Rp {total}.000</b>
<b>🗓️ Total Month: {bulan}</b> 

<b>✅ Click the button below to send proof of payment</b>
"""

    async def USERBOT(count):
        expired_date = monggo.get_expired_date(ubot._ubot[int(count)].me.id)
        return f"""
<b>❏ Userbot To</b> <code>{int(count) + 1}/{len(ubot._ubot)}</code>
<b> ├ Account:</b> <a href=tg://user?id={ubot._ubot[int(count)].me.id}>{ubot._ubot[int(count)].me.first_name} {ubot._ubot[int(count)].me.last_name or ''}</a> 
<b> ├ ID:</b> <code>{ubot._ubot[int(count)].me.id}</code>
<b> ╰ Expired</b> <code>{expired_date.strftime('%d-%m-%Y')}</code>
"""

    def POLICY():
        return """
↪️ Return Policy

After making payment, if you have not received/
receive benefits from the purchase,
You can exercise your right to replacement within 2 days of purchase. However, if
You have used/received one of the benefits of
purchase, including access to userbot creation features, then
You are no longer entitled to a refund.

🆘 Support
To get support, you can:
• Contact the admin below
• Support @KynanSupport on Telegram
⚠️ DO NOT contact Telegram Support or Bot Support to request te support
👉🏻 Press the Continue button to confirm that you have
read and accept these terms and continue
purchase. If not, press the Cancel button.
"""


async def sending_user(user_id):
    await bot.send_message(
        user_id,
        "Please Re-Create Your Userbot",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Create a Userbot",
                        callback_data="bahan",
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )
