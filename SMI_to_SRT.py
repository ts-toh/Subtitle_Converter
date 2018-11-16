#!/usr/local/bin/python3

#-*- coding: utf-8 -*-
import os, re, sys

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

    return h+':'+m+':'+s+','+r

def myDecode(string):
    try:
        return string.decode('cp949')
    except:
        try:
            return string.decode('utf-8')
        except:
            return string.decode('utf-16','ignore')
            
def convert(path, option=None):
    ls = os.listdir(path)

    for i in range(len(ls)):
        if option == '-r' and os.path.isdir(path+ls[i]):
            convert(path+ls[i]+"/")

        if re.search('.*smi',ls[i]) != None:
            print(ls[i], end='')
            smi_file = open(path + ls[i], 'br')
            srt_file = open(path + ls[i][:-3] + 'srt', 'bw')
            
            data = smi_file.readlines()
            line = 0
            count = 1

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
                        srt_file.write((str(count)+'\n').encode())
                        srt_file.write((numToTime(startNum)+' --> '+numToTime(endNum)+'\n').encode())
                        tmp = tmp.replace('\n','').replace('<br>','\n')
                        tmp = re.sub(r'.*<P', '<P', tmp)
                        tmp = re.sub(r'\n\n| \n', '\n', tmp)
                        tmp = re.sub(r'<b>|</b>|&nbsp;', '', tmp)
                        tmp = tmp[:-1]
                        srt_file.write((tmp + '\n\n').encode())
                        count +=1
                    line = p
                else:
                    line += 1

            smi_file.close()
            srt_file.close()
            print(' ---> '+ls[i][:-3]+'srt')
            
if __name__ == '__main__':
    if len(sys.argv) == 1:
        convert('./')
    elif len(sys.argv) == 2:
        convert(sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[2] == '-r':
        convert(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python3 SMI_to_SRT.py [TargetPath] [-r]")

    print("Complete!")
