import requests
import re
import mysql.connector
from sklearn import tree
cnx = mysql.connector.connect(user='root', host='127.0.0.1', database='amlak', password = '277353')
cursor = cnx.cursor()
#our table is named : "apartment" :D
page = 1
agahia = []
url_set = set()
while len(agahia) < 2000:
    r = requests.get(f'https://shabesh.com/search/%d8%ae%d8%b1%db%8c%d8%af-%d9%81%d8%b1%d9%88%d8%b4/%d8%a2%d9%be%d8%a7%d8%b1%d8%aa%d9%85%d8%a7%d9%86/%d8%aa%d9%87%d8%b1%d8%a7%d9%86?page={page}')
    text = r.text
    for i in re.findall(r'<a href="(/announce/.*?)"', text):
        url = 'https://shabesh.com' + i
        if url not in url_set:
            agahia.append(i)
            url_set.add(url)
            
    page += 1
agahia = list(map(lambda x : 'https://shabesh.com' + x ,agahia))
n=1
for i in agahia:
    r = requests.get(i)
    text=r.text
    price = re.findall(r'<span class="d-block fw-bold font-20 mt-3">(\d+.*?)\s', text)
    if len(price)==0:
        continue
    price = price[0].replace(",", "")
    metr = re.findall(r'<span class="px-1 font-15">(\d+)', text)
    if len(metr)==0:
        continue
    metr = metr[0]
    bed = re.findall(r'<span class="px-1 ">(\d)\s', text)
    if len(bed)==0:
        continue
    bed = bed[0]
    date = re.findall(r'<span class="px-1 ">(\d{4})<', text)
    if len(date)==0:
        continue
    date = date[0]
    cursor.execute('insert into apartment values (\'%i\',\'%i\',\'%i\',\'%i\')' % (int(price), int(metr) ,int(bed) ,int(date)))
    cnx.commit()
x = []
y = []
cursor.execute("SELECT metr,bed,date FROM apartment")
for i in cursor.fetchall():
    x.append(list(i))
cursor.execute("SELECT price FROM apartment")
for i in cursor.fetchall():
    y.append(list(i))
clf = tree.DecisionTreeClassifier
clf = clf.fit(x,y)
new_data = input('lotfan metrazh va tedad otagh-khaab va saal-e sakht ro bedid')
new_data_list = list(new_data.split(' '))
answer = clf.predict(new_data_list)
print(answer)

