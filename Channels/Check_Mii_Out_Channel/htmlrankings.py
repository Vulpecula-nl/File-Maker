import base64
import MySQLdb
import os
import subprocess
from json import load
from datetime import datetime

with open("/var/rc24/File-Maker/Tools/CMOC/config.json", "r") as f:
        config = load(f)

date = str(datetime.today().strftime("%B %d, %Y"))

beginning = "<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\n<link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css\">\n<link href=\"/css/style.css\" rel=\"Stylesheet\" type=\"text/css\" />\n<link href=\"/css/ctmkf.css\" rel=\"Stylesheet\" type=\"text/css\" />\n<title>Mii Artisan Rankings</title>\n<link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/apple-touch-icon.png\">\n<link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/favicon-32x32.png\">\n<link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/favicon-16x16.png\">\n<link rel=\"manifest\" href=\"/site.webmanifest\">\n<link rel=\"mask-icon\" href=\"/safari-pinned-tab.svg\" color=\"#89c0ca\">\n<meta name=\"msapplication-TileColor\" content=\"#2d89ef\">\n<meta name=\"theme-color\" content=\"#ffffff\">\n</head>\n<body class=\"center\">\n\n<h2><img src=\"/images/rankings.png\" id=\"icon\"> Mii Artisan Rankings</h2>\n<h4>" + date + "</h4>\n<p>Only the top 300 Mii Artisans are shown. Click on a Mii to download it.</p>\n<table class=\"striped\" align=\"center\">\n"

db = MySQLdb.connect('localhost', config['dbuser'], config['dbpass'], 'cmoc', use_unicode=True, charset='utf8mb4')
cursor = db.cursor()

cursor.execute('SELECT craftsno,miidata,nickname,votes FROM artisan WHERE votes >= 3 AND craftsno != 100000993 ORDER BY votes DESC LIMIT 300')
list = cursor.fetchall()

month = int(datetime.now().month)
day = int(datetime.now().day)

tables = beginning + "\t<tr>\n\t\t<th>Rank</th>\n\t\t<th>Mii</th>\n\t\t<th>Artisan</th>\n\t\t<th>Votes</th>\n\t</tr>\n"

for i in range(len(list)):
	mii_filename = "/var/www/wapp.wii.com/miicontest/public_html/render/crafts-{}.mii".format(list[i][0])
	if not os.path.exists(mii_filename):
		with open(mii_filename, "wb") as f:
			f.write(base64.b64decode(list[i][1])[:-2])
	if int(list[i][3]) >= 1000:
		master = "<img src=\"/images/master.png\" /><br>"
	else:
		master = ""
	tables += "\t<tr>\n"
	tables += "\t\t<td>{}</td>\n".format(i + 1)
	tables += "\t\t<td>{}</td>\n".format("<a href=\"/render/crafts-{}.mii\"><img width=\"75\" src=\"/render/crafts-{}.mii.png\"/></a>".format(list[i][0], list[i][0]))
	tables += "\t\t<td>{}</td>\n".format(master + list[i][2])
	tables += "\t\t<td>{}</td>\n".format(list[i][3])
	tables += "\t</tr>\n"
	#tables += str('\n' + list[i][0] + '' + str(list[i][1]))

tables += "\n</table>\n</body>\n</html>"

with open('/var/www/wapp.wii.com/miicontest/public_html/rankings.html', 'w') as file:
	file.write(tables)
