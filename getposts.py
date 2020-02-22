import json
import basic
import sys
import random
import time
import requests
from bs4 import BeautifulSoup

#VARIABEL
sql = "SELECT shortcode FROM ig_read_json WHERE params_query = '"
sql_update = "UPDATE ig_read_json SET has_processed = 1 WHERE shortcode = '"
urltemplate = "https://www.instagram.com/p/"
url = urltemplate
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) Gecko/20100101 Firefox/70.0"

#FUNGSI
def get_ig(url,user_agent):

    try:
        response = requests.get(url,headers={'User-Agent':user_agent})
        response.raise_for_status()
    except requests.HTTPError:
        raise requests.HTTPError('Dari IG, kode non 200')
    except requests.RequestException:
        raise requests.RequestException
    else:
        return response.text

def extract_json_data(html):
    soup = BeautifulSoup(html,'html.parser')
    body = soup.find('body')
    script_tag = body.find('script')
    raw_string = script_tag.text.strip().replace('window._sharedData =','').replace(';','')
    return json.loads(raw_string)


if __name__ == '__main__':
    _tag = sys.argv[1]
    _rec_num = sys.argv[2]

    #QUERY
    basic.cursor.execute(sql + _tag + "' AND has_processed = 0 ORDER BY id ASC LIMIT "+str(_rec_num))
    records = basic.cursor.fetchall()

    if len(records) == 0:
        print("Tag:"+_tag+" sudah SELESAI atau tidak ADA")
    else:
        #PROSES
        for row in records:

            url = url + row[0]
            print("Mulai membuka URL",url)
            acak = random.randint(23, 67)
            print("Pause script selama " + str(acak) + " detik")
            time.sleep(acak)

            #buka url
            html_ig = get_ig(url, user_agent)

            #extract
            myjson = extract_json_data(html_ig)

            #save file
            fileJson = row[0]+".json"
            with open("posts/"+fileJson, 'w') as outfile:
                json.dump(myjson, outfile)

            #update table
            try:
                basic.cursor.execute(sql_update + row[0]+"'")
                basic.cnx.commit()
                print("File posts/" + row[0] + ".json Berhasil disimpan!")
                #reset url value
                url = urltemplate
                print("=======================================================")
            except basic.Error as e:
                basic.cnx.rollback()
                print("Error MySQL di bagian Save file Name baru:", e)



