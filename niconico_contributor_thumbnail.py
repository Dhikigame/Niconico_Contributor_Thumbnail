# coding:utf-8
import sqlite3
from contextlib import closing
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import urllib
import requests
from bs4 import BeautifulSoup


def contributor_name_conv(contributor_name : str):

    print("Contributor Name: " + contributor_name)

    # 名前にファイル名として使えない文字列が含まれていたら覗く
    if '/' in contributor_name:
        contributor_name = contributor_name.replace('/', '')
    if '¥' in contributor_name:
        contributor_name = contributor_name.replace('¥', '')
    if ':' in contributor_name:
        contributor_name = contributor_name.replace(':', '')
    if '*' in contributor_name:
        contributor_name = contributor_name.replace('*', '')
    if '?' in contributor_name:
        contributor_name = contributor_name.replace('?', '')
    if '”' in contributor_name:
        contributor_name = contributor_name.replace('”', '')
    if '<' in contributor_name:
        contributor_name = contributor_name.replace('<', '')
    if '>' in contributor_name:
        contributor_name = contributor_name.replace('>', '')
    if '|' in contributor_name:
        contributor_name = contributor_name.replace('|', '')
    if '.' in contributor_name:
        contributor_name = contributor_name.replace('.', '')

    print("Contributor Name conv: " + contributor_name)

    return contributor_name



if __name__ == "__main__":

    print("データベースのある場所を入力してください(例：./test.db)")
    database = input()
    print("""投稿者のサムネイルを取得したいテーブルを入力してください(例：best100)
    ※カラム名：contributor_idがあるテーブルが対象です""")
    table = input()

    db = sqlite3.connect(database)
    
    with closing(db) as con:
        c = con.cursor()
        cursor = db.cursor()
        sql = "select contributor_id from " + table + " ORDER BY total DESC"
        cursor.execute(sql)
        contributor_ids = cursor.fetchall()
        contributor_id_list= []
        for contributor_id in contributor_ids:
            contributor_id_list.append(contributor_id[-1])
        print("【Contributor ID List】")
        print(contributor_id_list)

    contributor_name_list = []
    contributor_thumbnail_list = []
    rank = 1
    for contributor_id in contributor_id_list:
        response = urllib.request.urlopen('https://www.nicovideo.jp/user/' + str(contributor_id))
        content = response.read()
        soup = BeautifulSoup(content, "html.parser")

        print("【RANK" + str(rank) + "】")
        print("【HTML Parse】")
        meta_name = soup.find("meta", attrs={'property': 'profile:username'})
        if meta_name == None:
            rank += 1
            continue
        contributor_name = meta_name.get('content')
        print("・Contributor Name")
        print(contributor_name)
        meta_thumbnail = soup.find("meta", attrs={'property': 'og:image'})
        contributor_thumbnail = meta_thumbnail.get('content')
        print("・Contributor Thumbnail")
        print(contributor_thumbnail)

        contributor_name_list.append(contributor_name)
        contributor_thumbnail_list.append(contributor_thumbnail)

        rank += 1


    print("【Contributor Name List】")
    print(contributor_name_list)
    print("【Contributor Thumbnail List】")
    print(contributor_thumbnail_list)

    print("【Contributor Thumbnail Download】")
    image_target_pass = []
    for i in range(len(contributor_name_list)):
        contributor_name = contributor_name_conv(str(contributor_name_list[i]))
        image_target_pass.append("./downloadimage/" + contributor_name + ".jpg")
        response = requests.get(contributor_thumbnail_list[i])
        image = response.content
        # 画像ダウンロード
        with open(image_target_pass[i], "wb") as download_dir:
            download_dir.write(image)
            print("ダウンロード：" + image_target_pass[i])
    
    print("【Contributor Thumbnail Download END】")
