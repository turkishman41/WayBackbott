# HuzunluArtemis - 2021 (Licensed under GPL-v3)

from pyrogram import Client, filters
from pyrogram.types.messages_and_media.message import Message

from HelperFunc.authUserCheck import AuthUserCheck
from HelperFunc.forceSubscribe import ForceSub
from HelperFunc.messageFunc import sendMessage, editMessage
import logging, re
from HelperFunc.wayback import saveWebPage

from config import Config
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


@Client.on_message(filters.text & ~filters.command(Config.ALL_COMMANDS))
async def waybackInstantly(client: Client, message: Message):
    if not await AuthUserCheck(message): return
    if await ForceSub(client, message) == 400: return
    if not Config.AUTO_SAVE_ALL_URLS: return
    url = message.text
    link = None
    try:
        link = re.match(r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*", url)[0]
    except TypeError:
        await sendMessage(message,"🇬🇧 Not a valid link.\n🇹🇷 Geçerli bir link değil.")
        return
    mesaj = await sendMessage(message,"🇬🇧 Wait about 5 minutes. Saving page.\n🇹🇷 5 dakika bekleyin. Sayfa kaydediliyor.")
    retLink = saveWebPage(link)
    if retLink == None:
        await editMessage(mesaj, "🇬🇧 Cannot archieved. Try again later.\n🇹🇷 Arşivlenemedi. Sonra tekrar deneyin.")
        return
    await editMessage(mesaj, f"🇬🇧 Saved webpage. 🇹🇷 Sayfa arşivlendi:\n\n{retLink}")
