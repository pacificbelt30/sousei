import requests
import csv
kamoku = input()
url = 'http://localhost/csv'
param = {'kamoku':kamoku}
r = requests.get(url,param)
print(r.json())
recieved_json = r.json()
risyusya_csv = recieved_json['csv']
kamoku = recieved_json['kamoku']
start_syusseki = recieved_json['start_syusseki']
start_tikoku = recieved_json['start_tikoku']
end_uketuke = recieved_json['end_uketuke']
print(kamoku,start_syusseki,start_tikoku,end_uketuke)
filename = 'risyusya_'+kamoku+'.csv'
risyusya_csv = risyusya_csv.split('\n')
tmp = list()
for i in risyusya_csv:
    tmp.append(i.split(','))

risyusya_csv = tmp
print(tmp)

with open(filename,'w') as f:
    writer = csv.writer(f)
    writer.writerows(risyusya_csv)

class Reciever:
    def __init__(self):
        self.a = 0

