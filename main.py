from scheduler import *

if __name__ == '__main__':
    c = ConferenceScheduler(2,180,240,False)
    c.calculate_schedules()
    print(c)
