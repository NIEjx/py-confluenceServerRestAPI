import os
import datetime

# 並列処理時に各処理のログ出力用
def mpprint(*values:object):
    print('[', os.getpid(), ']', ''.join(values))

def saveTextFile(content, fileName):
    with open(fileName,'w',encoding='utf-8') as file:
        file.write(content)

def saveBinaryFile(content, fileName):
    with open(fileName,'wb') as file:
        file.write(content)

def cvtTimeDelta(delta:datetime.timedelta):
    rtn = ""
    if delta.days != 0:
        if rtn != "":
            rtn = rtn + " "
        rtn = rtn + str(delta.days) + "D" 
    if delta.seconds > 3599:
        hours = int(delta.seconds/3600)
        if rtn != "":
            rtn = rtn + " "
        rtn = rtn + str(hours) + "hr"
    if delta.seconds > 59:
        minutes = int((delta.seconds - int(delta.seconds/3600)*3600)/60)
        if minutes != 0:
            if rtn != "":
                rtn = rtn + " "
            rtn = rtn + str(minutes) + "min"
    if delta.seconds % 60 != 0:
        seconds = delta.seconds % 60
        if rtn != "":
            rtn = rtn + " "
        rtn = rtn + str(seconds) + "s"
    return rtn