import gzip
from collections import defaultdict
from datetime import datetime


def parse(path):
    g = gzip.open(path, 'r')
    for l in g:
        yield eval(l)
counter = 10000

print("beginning")
countU = defaultdict(lambda: 0)
countP = defaultdict(lambda: 0)
line = 0

dataset_name = 'steam'
f = open(dataset_name + '_reviews' + '.txt', 'w')
for l in parse(dataset_name + '_reviews' + '.json.gz'):
    line += 1
    #if line > counter:
    #    break
    # products = str(l['products'])
    # hours = str(l['hours'])
    f.write(u' '.join([l['username'], l['product_id'], l['date'],l['text']]).encode('utf-8').strip() + ' \n')
    username = l['username']
    product_id = l['product_id']
    date = l['date']
    countU[username] += 1
    countP[product_id] += 1
f.close()

print("middle")

usermap = dict()
usernum = 0
itemmap = dict()
itemnum = 0
line = 0 
User = dict()

for l in parse(dataset_name + '_reviews' + '.json.gz'):
    #if line > counter:
    #    break
    line += 1
    product_id = l['product_id']
    username = l['username']
    date = l['date']
    # if countU[username] < 5 or countP[product_id] < 5:
        # continue


    if username in usermap:
        userid = usermap[username]
    else:
        usernum += 1
        userid = usernum
        usermap[username] = userid
        User[userid] = []
    if product_id in itemmap:
        itemid = itemmap[product_id]
    else:
        itemnum += 1
        itemid = itemnum
        itemmap[product_id] = itemid
    User[userid].append([date, itemid, line])
# sort reviews in User according to time
print("end")

for userid in User.keys():
    User[userid].sort(key=lambda x: x[0])

print usernum, itemnum

f = open('Steam2.txt', 'w')
for user in User.keys():
    for i in User[user]:
        f.write('%d %d %d\n' % (user, i[1], i[2]))
f.close()
