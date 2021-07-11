import schedule
import time

def job():
    exec(open("stonkbot.py").read())
    # print("Joker is the best villian of all time")

schedule.every(20).seconds.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
