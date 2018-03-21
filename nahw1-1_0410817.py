# -- coding: utf-8 --
import sys
import requests
import pytesseract
import argparse
import getpass
from pyquery import PyQuery as pq
import pandas as pds
from lxml import html
from io import BytesIO
from PIL import Image
from prettytable import PrettyTable

# Input username
parser = argparse.ArgumentParser(description = "Web crawler for NCTU class schedule")
parser.add_argument('username', type=str, help="username of NCTU portal")
args = parser.parse_args()

# Input password
pw = getpass.getpass("Please input your password:")

# s is NCTU portal login page
s = requests.Session()
r = s.get('https://portal.nctu.edu.tw/portal/login.php')
pic_r = s.get('https://portal.nctu.edu.tw/captcha/pic.php', cookies = r.cookies)
img = Image.open(BytesIO(pic_r.content))
img.save('t.png')
captcha = pytesseract.image_to_string(img)
# print(captcha)

while (1):
    # rs is captcha update page
    rs = requests.Session()
    pic_s = rs.get('https://portal.nctu.edu.tw/captcha/claviska-simple-php-captcha/pic.php', cookies = r.cookies)
    im = Image.open(BytesIO(pic_s.content)).convert('1')
    im.save('t1.png')
    captcha = pytesseract.image_to_string(im)
    captcha.strip( '\ ' )
    captcha.strip()
    captcha.strip('‘')
    #print(captcha)
    try:
        int(captcha)
        if len(captcha) == 4:
            payload ={'username' : args.username, 'Submit2': 'Login', 'pwdtype' : 'static', 'password' : pw, 'seccode' : captcha}
            r = s.post('https://portal.nctu.edu.tw/portal/chkpas.php', data = payload)
            if int(r.headers['Cteonnt-Length']) == 143:
                r = s.get('https://portal.nctu.edu.tw/portal/login.php')
                continue
            r = s.get('https://portal.nctu.edu.tw/portal/relay.php?D=cos', cookies = r.cookies)
            break
    except:
        pass


if (int(r.headers['Cteonnt-Length']) == 138):
    sys.exit("Login error")

# Dealing with URL redirection
payload.clear()
tree = html.fromstring(r.content)
form = pq(r.text)
tag = form("input")
for i in tag:
    payload.update({pq(i).attr('id') : pq(i).attr('value')})
# print(payload)
r = s.post('https://course.nctu.edu.tw/jwt.asp',data = payload)
r = s.post('https://course.nctu.edu.tw/adSchedule.asp',cookies = r.cookies)

# Put timetable in the prettytable
tt = pds.read_html(r.content)
tt[0].replace(tt[0][1][0], '', inplace = True)
value = tt[0].values
pt = PrettyTable()
pt.field_names = value[1]
for i in range(2, 18):
    pt.add_row(value[i])
print(pt)
