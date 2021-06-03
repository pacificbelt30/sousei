# -*- coding: utf-8 -*-
import csv
def csv_reader(filename):
    try:
        with open(filename,'r',encoding='utf-8') as csvfile: #読み込むcsvファイルに適宜変更
            reader = csv.reader(csvfile)
            header = next(reader)
            csvdata = list()
            for s in reader:
                csvdata.append(s)
            return csvdata
    except:
        import traceback
        traceback.print_exc()
        return ''

#print('risyusya-F2.csv')
#data = csv_reader(input())
#data = csv_reader('risyusya-F2.csv')
#print([s for s in data])
