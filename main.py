from operator import itemgetter, attrgetter
import datetime
import unittest


class TestBasicSchedules(unittest.TestCase):

    def test_print_slot(self):
        startTime = datetime.datetime(100,1,1,8,00,00)
        s = SlotSchedule(startTime.strftime("%I:%M %p") ,{'title':'Writing Fast Tests Against Enterprise Rails','time':60})
        self.assertEqual(s.__str__(), '08:00 AM Writing Fast Tests Against Enterprise Rails 60min\n')

    def test_find_longest_talk(self):
        c = ConferenceScheduler(2,180,240,True)
        slots = [{'title':'Writing Fast Tests Against Enterprise Rails','time':60}]
        res = c.find_first_slot(slots,120)
        self.assertEqual(res,{'title':'Writing Fast Tests Against Enterprise Rails','time':60})

    def test_find_no_talk(self):
        c = ConferenceScheduler(2,180,240,True)
        slots = [{'title':'Writing Fast Tests Against Enterprise Rails','time':60}]
        res = c.find_first_slot(slots,10)
        self.assertEqual(res,None)

    def test_find_talk_that_fits_in_window(self):
        c = ConferenceScheduler(2,180,240,True)
        slots = [{'title':'Writing Fast Tests Against Enterprise Rails','time':60},{'title':'Writing Fast Tests Against Enterprise Rails','time':5}]
        res = c.find_first_slot(slots,10)
        self.assertEqual(res,{'title':'Writing Fast Tests Against Enterprise Rails','time':5})



class SlotSchedule:
    """ 
        Slot schedule represents a talk slot
    """
    def __init__(self,time,raw_schedule):
        self.slot_time = time
        self.slot_title = raw_schedule['title']
        self.slot_duration = raw_schedule['time']

    def __str__(self):
        return '%s %s %dmin\n' % (self.slot_time,self.slot_title,self.slot_duration)


class ConferenceScheduler:
    """ConferenceScheduler sets up tracks to effeciently plan a conference """

    def __init__(self,number_of_tracks,morning_track_size,afternoon_track_size,show_remainder):
        """ 
            Morning and afternoon track sizes are defined in minutes
        """
        self.number_of_tracks = number_of_tracks
        self.morning_track_size = morning_track_size
        self.afternoon_track_size = afternoon_track_size
        self.show_remainder = show_remainder
        self.slots = []
        self.load_raw_schedules()

    def find_first_slot(self,sl,remainder):
        """ 
        find_first_slot searches through the list of remaining 
        talks and finds one that will fit in a track
        """
        for ts in sl:
            if remainder - ts['time'] >= 0:
                return ts

    def processSlot(self,slotTime,slots,startTime):
        while slotTime > 0:
            f = self.find_first_slot(slots,slotTime)
            if f:
                slots = [x for x in slots if x != f]
                slots = sorted(slots,key=itemgetter('time'),reverse=True)
                s = SlotSchedule(startTime.strftime("%I:%M %p") ,f)
                startTime = startTime + datetime.timedelta(seconds=60*f['time'])            
                self.final_schedules += s.__str__()
                slotTime -= f['time']
            else:
                break
        return startTime,slots


    def load_raw_schedules(self):
        with open('data.txt') as f:
            data = f.readlines()

            for d in data:
                parts = d.split()
                time = parts[-1]
                if time == "lightning":
                    time = "5min"
                time = time.replace('min','')
                self.slots.append({'title':' '.join(parts[:-1]),'time':int(time)})

            self.slots = sorted(self.slots,key=itemgetter('time'),reverse=True)


    def __str__(self):
        return self.final_schedules

    def calculate_schedules(self):
        self.final_schedules = ''
        if self.number_of_tracks < 1:
            print('Invalid track count provided')
            return

        for i in range(1,self.number_of_tracks+1):
            self.final_schedules += 'Track %d:\n' % (i)
            startTime = datetime.datetime(100,1,1,9,00,00)
            (startTime,self.slots) = self.processSlot(self.morning_track_size,self.slots,startTime)

            self.final_schedules += '%s Lunch\n' % (startTime.strftime("%I:%M %p"))
            startTime = startTime + datetime.timedelta(seconds=60*60)            

            (startTime,self.slots) = self.processSlot(self.afternoon_track_size,self.slots,startTime)

            self.final_schedules += '%s Networking Event\n' % (startTime.strftime("%I:%M %p"))

        if self.show_remainder:
            self.final_schedules += 'Remainder\n'
            self.final_schedules += self.slots.__str__()


if __name__ == '__main__':
    c = ConferenceScheduler(2,180,240,False)
    c.calculate_schedules()
    print(c)
