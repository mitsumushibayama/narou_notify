import requests
from bs4 import BeautifulSoup
import re

def main():

    #通知用LINE Notifyの設定
    notify_url = 'https://notify-api.line.me/api/notify'
    notify_token = 'ここにトークンを貼る'
    headers = {"Authorization" : "Bearer "+ notify_token}

    #前回のプログラム実行時に保存された最新話の確認
    f = open('/path/to/text', 'r')
    previous_chapter_number = f.readline()
    f.close()

    #小説の最新話の話数を取得する
    res = requests.get('https://api.syosetu.com/novelapi/api/?of=ga&ncode=小説コード')
    soup = BeautifulSoup(res.text, 'html.parser')
    text = soup.get_text()
    current_chapter = re.search('general_all_no: [0-9]+', text)
    current_chapter_text = current_chapter.group()
    current_chapter_num_search = re.search('[0-9]+', current_chapter_text)
    current_chapter_number = current_chapter_num_search.group()

    #保存された話数とサイトから取得した話数が異なっていれば更新されたと判断する
    if current_chapter_number != previous_chapter_number:
        message = '最新話'+current_chapter_number+'が更新されました'
        payload = {"message" : message}
        requests.post(notify_url, headers = headers, params = payload)

        message2 = 'https://ncode.syosetu.com/小説コード/'
        payload = {"message" : message2}
        requests.post(notify_url, headers = headers, params = payload)

        #保存する話数を更新
        f = open('/path/to/text','w')
        f.write(current_chapter_number)
        f.close()

if __name__ ==  '__main__' :
    main()

