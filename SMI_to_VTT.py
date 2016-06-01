#-*- coding: utf-8 -*-
import os, re

def numToTime(num):
    
    time = int(num)

    r = str(time % 1000)
    s = int(time / 1000)
    m = int(s / 60)
    s = str(s % 60)
    h = str(int(m / 60))
    m = str(m % 60)

    while(len(r) < 3):
        r = '0'+r
    while(len(s) < 2):
        s = '0'+s
    while(len(m) < 2):
        m = '0'+m
    while(len(h) < 2):
        h = '0'+h

    return h+':'+m+':'+s+'.'+r

def myDecode(string):
    try:
        return string.decode('cp949')
    except:
        try:
            return string.decode('utf-8')
        except:
            print("EUC-KR 또는 UTF-8 인코딩 방식의 파일만 변환이 가능합니다.")
            exit(0)

ls = os.listdir('./')

for i in range(len(ls)):
    if re.search('.*smi',ls[i]) != None:
        print(ls[i], end='')
        smi_file = open(ls[i], 'br')
        vtt_file = open(ls[i][:-3] + 'vtt', 'bw')
        vtt_file.write(b'WEBVTT\n\n')
        
        data = smi_file.readlines()
        line = 0
            
        while(line < len(data)):
            if re.search('sync start=[0-9]+', myDecode(data[line]).lower()):
                startNum = re.search('[0-9]+', myDecode(data[line])).group(0)
                tmp = ''
                p = line+1
                while p < len(data) and not(re.search('sync start=[0-9]+>',myDecode(data[p]).lower())):
                        tmp += myDecode(data[p])
                        p += 1
                if p >= len(data): break;
                endNum = re.search('[0-9]+',myDecode(data[p])).group(0)
                if tmp != '':
                    vtt_file.write((numToTime(startNum)+' --> '+numToTime(endNum)+'\n').encode())
                    tmp = tmp.replace('\n','').replace('<br>','\n')
                    tmp = re.sub(r'.*<P', '<P', tmp)
                    tmp = re.sub(r'\n\n| \n', '\n', tmp)
                    tmp = re.sub(r'<b>|</b>|&nbsp;', '', tmp)
                    tmp = tmp[:-1]
                    vtt_file.write((tmp + '\n\n').encode())
                line = p
            else:
                line += 1

        smi_file.close()
        vtt_file.close()
        print(' ---> '+ls[i][:-3]+'vtt')

print("Complete!")

