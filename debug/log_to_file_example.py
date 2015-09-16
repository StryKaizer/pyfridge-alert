import datetime



#Open Log File
f=open('log.txt','a')
now = datetime.datetime.now()
timestamp = now.strftime("%Y/%m/%d %H:%M")
outvalue = 30.0
outstring = str(timestamp)+"  "+str(outvalue)+" C "+str(outvalue*1.8+32)+" F"+"\n"
f.write(outstring)
f.close()


