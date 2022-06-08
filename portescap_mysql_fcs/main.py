
from gen_functions import job

if __name__ == '__main__':
    # try:
    training_data = job()
#
#
# import datetime
#
# import schedule
# import time
#
#
# # Functions setup
# def sudo_placement():
#     print("Get ready for Sudo Placement at Geeksforgeeks")
#
#
# def good_luck():
#     print("Good Luck for Test")
#
#
# def work():
#     print("Study and work hard")
#
#
# def bedtime():
#     print("It is bed time go rest")
#
#
# def geeks():
#     # print("Start")
#     print("geeks start", datetime.datetime.now())
#     time.sleep(2)
#     print("geeks end", datetime.datetime.now())
#     print("Shaurya says Geeksforgeeks")
#
#
# # Task scheduling
# # After every 10mins geeks() is called.
# schedule.every(1).seconds.do(geeks)
#
# while True:
#     # Checks whether a scheduled task
#     # is pending to run or not
#     print("While start",datetime.datetime.now())
#     schedule.run_pending()
#     time.sleep(0.5)
#     print("While end", datetime.datetime.now())