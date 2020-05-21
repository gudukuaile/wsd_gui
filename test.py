from datetime import datetime
import time

d1 = datetime.now()
time.sleep(3)
d2 = datetime.now()

d = d2-d1
print(type(d))
print(dir(d))
print(d.seconds)