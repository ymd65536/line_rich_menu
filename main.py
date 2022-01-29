import os
from dotenv import load_dotenv
from linebot import LineBotApi
from linebot.models import RichMenu
from linebot.models import RichMenuSize
from linebot.models import RichMenuArea
from linebot.models import RichMenuBounds
from linebot.models import MessageAction

load_dotenv()
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
line_bot = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

if __name__ == '__main__':

    print('register richmenu')

    # リッチメニューの作成
    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=2500, height=843),
        selected=False,
        name="start_menu",
        chat_bar_text="メニューを開く",
        areas=[RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=2500, height=843),
            action=MessageAction(label='message', text='start'))]
    )
    rich_menu_id = line_bot.create_rich_menu(rich_menu=rich_menu_to_create)

    # リッチメニュー用の画像をアップロード
    image_path= "./img/menu.png"
 
    with open(image_path, 'rb') as f:
        line_bot.set_rich_menu_image(rich_menu_id, "image/jpeg", f)

    line_bot.set_default_rich_menu(rich_menu_id)
    print('Done!')