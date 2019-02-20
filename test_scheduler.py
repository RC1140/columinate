import unittest
import datetime
from scheduler import *

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


if __name__ == '__main__':
    unittest.main()
