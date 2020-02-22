# import requests
# from requests.exceptions import HTTPError
import basic
import urllib
from urllib.request import urlopen
import urllib.request
import sys
import json
import time
import random


#1. VARIABEL
url = "https://www.instagram.com/explore/tags/"
# url = "https://api.github.com/"
#italy/?__a=1"
url_max = "&max_id="
fileJson = end_cursor = ""
new_num = num = acak = 0
has_next_page = True
is_next_page = True
loop_num = 1

sql = "SELECT id,crawl_json_file,end_cursor FROM ig_crawl_files WHERE params_query = '"
# ORDER BY created_at DESC
sql_file = "INSERT INTO ig_crawl_files(params_query,crawl_json_file,end_cursor)VALUES(%s,%s,%s)"

#3. MAIN
if __name__ == '__main__':
    _tag = sys.argv[1]
    url = url + _tag + "/?__a=1"

    #a. mulai proses looping
    while has_next_page == True:
        print("LOOP KE-",str(loop_num))

        #b. query
        basic.cursor.execute(sql + _tag + "' ORDER BY created_at DESC")
        records = basic.cursor.fetchall()
        num = len(records)

        # c. create filename json baru
        if num == 0:
            fileJson = _tag + "_IG.json"
        else:
            if records[0][2] == "none":
                has_next_page = False
                print("WARNING:")
                print("1. File sudah ada.")
                print("2. File "+records[0][1]+" sudah final.")
                print("Proses berhenti di loop ke-",str(loop_num))
                break
            else:
                print("INFO:")
                print("1. File sudah ada.")
                print("2. File "+records[0][1]+" adalah file terakhir")
                print("End cursor =",records[0][2])

                new_num = num + 1
                url = url + "&max_id=" + records[0][2]
                fileJson = _tag + "_IG_" + str(new_num) + ".json"


        # d. get json

        if loop_num > 1:
            acak = random.randint(27, 47)
            print("PAUSE PROGRAM SELAMA " + str(acak) + " detik")
            time.sleep(acak)

        try:
            req = urllib.request.Request(url,
                                        data=None,
                                         headers={
                                             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) Gecko/20100101 Firefox/70.0'
                            }
                    )
            # res = urlopen(url)
            res = urllib.request.urlopen(req)
            data = json.loads(res.read())

            # e. get cursor dan next page boolean
            is_next_page = data["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["has_next_page"]
            end_cursor = data["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["end_cursor"]
            print("has next page", is_next_page)
            print("end cursor", end_cursor)

            # f. simpan file
            with open(fileJson, 'w') as outfile:
                json.dump(data, outfile)

            # g. save filename to db
            if is_next_page == False and end_cursor is None:
                has_next_page = False
                print("stop at loop num", loop_num)
                end_cursor = "none"

            _tuple = (_tag, fileJson, end_cursor)
            try:
                basic.cursor.execute(sql_file, _tuple)
                basic.cnx.commit()
                print("file baru " + fileJson + " berhasil disimpan")
            except basic.Error as e:
                basic.cnx.rollback()
                print("Error MySQL di bagian Save file Name baru:", e)

        except urllib.error.HTTPError as http_err:
            has_next_page = False
            print(f'HTTP Error di bagian file json baru: {http_err}')

        if loop_num >=10:
            has_next_page = False
        else:
            loop_num += 1
        print("=============================================================================")

