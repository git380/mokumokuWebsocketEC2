from flask import Flask, request
from flask_cors import CORS

import json

app = Flask(__name__)
CORS(app)


@app.route('/make_chat', methods=['POST'])
def receive_json():
    # POSTリクエストからJSONデータを取得
    data = request.get_json()

    uuid = data[0]
    chat_name = data[1]
    chat_date = data[2]
    # JSONのチャット履歴を追加
    with open('json/group_info.json', 'r', encoding='utf-8') as json_file_r:
        group_info = json.load(json_file_r)
    # JSONチャット履歴を辞書に追加(キーはStringに変換)
    group_info[uuid] = [{}, chat_name, chat_date]
    # チャット履歴をJSONで保存
    with open('json/group_info.json', 'w', encoding='utf-8') as json_file_w:
        json.dump(group_info, json_file_w, ensure_ascii=False, indent=4)
    return ''


@app.route('/load', methods=['POST'])
def load():
    # JSONのチャット履歴を追加
    with open(f'json/{request.data.decode('utf-8')}.json', 'r', encoding='utf-8') as json_file_r:
        return json_file_r.read()


@app.route('/reset_chat', methods=['POST'])
def reset_chat():
    # 元チャットデータ
    with open('json/chat_history.json', 'r', encoding='utf-8') as json_data:
        chat_history = json.load(json_data)

    # 元チャット履歴
    with open('json/chat_history_log.json', 'r', encoding='utf-8') as json_data:
        chat_history_log = json.load(json_data)

    # チャットデータをチャット履歴に追加
    chat_history_log.update(chat_history)

    # 新チャット履歴出力
    with open('json/chat_history_log.json', 'w') as json_data:
        json.dump(chat_history_log, json_data, indent=4)

    # 元チャットデータ削除
    with open('json/chat_history.json', 'w') as json_data:
        json.dump({}, json_data, indent=4)

    ##################

    # 元グループデータ
    with open('json/group_info.json', 'r', encoding='utf-8') as json_data:
        group_info = json.load(json_data)

    # 元グループ履歴
    with open('json/group_info_log.json', 'r', encoding='utf-8') as json_data:
        group_info_log = json.load(json_data)

    # ステータス情報削除
    for uuid, info in group_info.items():
        # group_infoに名前がない場合保存しない
        if uuid in chat_history:
            for key, name in info[0].items():
                info[0][key] = name[0]
            group_info_log[uuid] = info

    # 新グループデータ出力
    with open('json/group_info_log.json', 'w') as json_data:
        json.dump(group_info_log, json_data, indent=4)

    # 元グループデータ削除
    with open('json/group_info.json', 'w') as json_data:
        json.dump({}, json_data, indent=4)
    return ''


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
