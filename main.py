# 参考：https://qiita.com/uezo/items/2dd9db3046ef7b28ed2e
import os
import requests
import json

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
LINE_USER_ID = os.getenv('LINE_USER_ID', None)

if __name__ == '__main__':
    print('register richmenu')

    # チャネルアクセストークンの設定
    # ベアラー
    headers = {"Authorization": "Bearer {%s}" % LINE_CHANNEL_ACCESS_TOKEN}

    # リッチメニューの名前を設定
    rich_menu_name = "start_menu"

    # チャットバーのテキスト
    chat_bar_name = "メニューを開く"

    # 範囲は画像と同じ大きさに設定
    x = 0
    y = 0
    width = 2500
    height = 843
    bounds={"x":x,"y":y,"width":width,"height":height}

    # 画像サイズの指定
    size = {"width":width, "height": height}

    # リッチメニューのアクションタイプ
    action = {"type": "message"}
    action["text"] = "start"
    areas = []
    areas.append({"bounds": bounds, "action": action})

    # 画像パス
    image_path= "./img/menu.png"

    # 送信データの作成
    send_dic = {"size":size,"selected":True,"name":rich_menu_name,"chatBarText":chat_bar_name,"areas":areas}
    send_json = json.dumps(send_dic)

    # リッチメニューの登録
    register_url = "https://api.line.me/v2/bot/richmenu"
    res = requests.post(register_url, headers=dict(headers, **{"Content-Type": "application/json"}), data=send_json,verify=True).json()
    rich_menu_id = res["richMenuId"]

    # 取得したリッチメニューIDを元に画像をアップロード
    upload_url = "https://api-data.line.me/v2/bot/richmenu/%s/content" % rich_menu_id
    image_file = open(image_path,"rb")
    requests.post(upload_url, headers=dict(headers, **{"Content-Type": "image/jpeg"}), data=image_file, verify=True)

    # 特定のユーザIDにリッチメニューを登録
    apply_url = "https://api.line.me/v2/bot/user/%s/richmenu/%s" % (LINE_USER_ID,rich_menu_id)
    requests.post(apply_url, headers=headers, verify=True)

    # リッチメニューの設定をチェック
    applied_url = "https://api.line.me/v2/bot/user/%s/richmenu" % LINE_USER_ID
    res = requests.get(applied_url, headers=headers, verify=True).json()

    if not res["richMenuId"] == "":
        print("リッチメニューが設定されています。")