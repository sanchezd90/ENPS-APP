import datetime

now=datetime.datetime.now()
print(now.strftime('%H:%M'))
dead = now+datetime.timedelta(minutes=20)
timeUp=str(dead.hour)+":"+str(dead.minute)
