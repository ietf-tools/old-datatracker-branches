import sys
from ietf.utils import TestCase
from django.test.client import Client
from ietf.meeting.models  import TimeSlot, Session, Schedule, ScheduledSession
from ietf.meeting.models  import Constraint
from ietf.group.models    import Group
from ietf.name.models     import ConstraintName
from settings import BADNESS_CONFLICT_1,BADNESS_CONFLICT_2,BADNESS_CONFLICT_3,BADNESS_UNPLACED,BADNESS_TOOSMALL_50,BADNESS_TOOSMALL_100,BADNESS_TOOBIG,BADNESS_MUCHTOOBIG
from settings import BADNESS_CALC_LOG
from ietf.meeting.placement import CurrentScheduleState

class PlacementTestCase(TestCase):
    # See ietf.utils.test_utils.TestCase for the use of perma_fixtures vs. fixtures
    perma_fixtures = [ 'names.xml',  # ietf/names/fixtures/names.xml for MeetingTypeName, and TimeSlotTypeName
                 'meeting83.json',
                 'constraint83.json',
                 'workinggroups.json',
                 'groupgroup.json',
                 'person.json', 'users.json' ]

    def test_calculatePlacedSession1(self):
        """
        calculate the fitness for a session that has been placed (stock placement)
        """
        schedule = Schedule.objects.get(pk=24)
        mtg = schedule.meeting
        assignments = schedule.group_mapping
        dtnrg = mtg.session_set.get(group__acronym = 'dtnrg')
        self.assertNotEqual(dtnrg, None)
        self.assertNotEqual(assignments[dtnrg.group], [])
        badness = dtnrg.badness(assignments)
        self.assertEqual(badness, BADNESS_TOOBIG+BADNESS_CONFLICT_2*2)

    def test_calculatePlacedSession2(self):
        """
        calculate the fitness for a session that has been placed.
        """

        # do some setup of these slots
        schedule = Schedule.objects.get(pk=103)
        mtg = schedule.meeting
        ipsecme = mtg.session_set.get(group__acronym = 'ipsecme')
        websec  = mtg.session_set.get(group__acronym = 'websec')
        slot1   = schedule.scheduledsession_set.get(timeslot__id = 2373) # 2012-03-26 13:00 location_id=212 (242AB)
        slot2   = schedule.scheduledsession_set.get(timeslot__id = 2376) # 2012-03-26 13:00 location_id=213 (Maillot)
        slot1.session = ipsecme
        slot1.save()
        slot2.session = websec
        slot2.save()

        # now calculate badness
        assignments = schedule.group_mapping
        self.assertNotEqual(ipsecme, None)
        self.assertTrue(len(assignments[ipsecme.group]) > 0)
        badness = ipsecme.badness(assignments)
        self.assertEqual(badness, BADNESS_CONFLICT_3+BADNESS_TOOBIG)

    def test_calculateBadnessMtg83(self):
        """
        calculate the fitness for a session that has been placed.
        """

        # do some setup of these slots
        schedule = Schedule.objects.get(pk=24)
        self.assertEqual(schedule.calc_badness(), 15081200)

    def dump_placer_slots(self, placer1):
        """
        This is a helper/debug routine for use in badness optimization
        """
        i1 = placer1.timeslots.iterkeys()
        slotnum=0
        total  =0
        for tsk in i1:
            ts = placer1.timeslots[tsk]
            print "rc,%u, %s, %u,,,,recalc" % (slotnum, ts.daytime, ts.calc_badness(placer1))
            slotnum += 1
            total   += ts.calc_badness(placer1)

        for sess,fs in placer1.sessions.iteritems():
            if fs is None:
                print "rc,,,,%s,none" % (sess.short_name)
            elif fs.scheduleslot is None:
                print "rc,,,,%s,%s,none" % (sess.short_name, fs)
            else:
                print "rc,,,,%s,,%u" % (fs.scheduleslot.daytime,fs.session.calc_badness(placer1))

    def test_calculateBadnessViaScheduledStateMtg83(self):
        """
        calculate the fitness for a session that has been placed, using the placer
        state system.  This will calculate the badness for each column, saving the
        results for faster recalculation.
        """

        # do some setup of these slots
        schedule = Schedule.objects.get(pk=24)
        placer1 = CurrentScheduleState(schedule)

        #self.dump_placer_slots(placer1)
        #import pdb; pdb.set_trace()

        # calculate placement new way.
        b1 = placer1.calc_badness(None, None)

        #from settings import BADNESS_CALC_LOG
        #BADNESS_CALC_LOG = 1
        # badness calculation by the old way fails to count four groups that have
        # two sessions properly,     200 * 4 = 800.
        b2 = schedule.calc_badness1(placer1) + 800
        b3 = schedule.calc_badness()         + 800
        #print "rc,b1: %u b2: %u b3: %u" % (b1, b2, b3)
        self.assertEqual(b1, 3082000)
        self.assertEqual(b2, 3082000)
        self.assertEqual(b3, 15082000)   # this does not exclude non-session items!

    def test_calculateBadnessMtg83unplaced(self):
        """
        calculate the fitness for a session that has been placed.
        """

        # do some setup of these slots
        schedule = Schedule.objects.get(pk=103)
        self.assertEqual(schedule.calc_badness(), 137001000)

    def test_calculateUnPlacedSession(self):
        """
        calculate the fitness for a session that has not been placed
        """
        schedule = Schedule.objects.get(pk=103)
        mtg = schedule.meeting
        assignments = schedule.group_mapping
        pkix = mtg.session_set.get(group__acronym = 'pkix')
        self.assertNotEqual(pkix, None)
        self.assertTrue(len(assignments[pkix.group]) == 0)
        badness = pkix.badness(assignments)
        self.assertEqual(badness, BADNESS_UNPLACED)

    def test_startPlacementSession(self):
        """
        kicks starts the placement process.
        There are 149 timeslots total.
        Says useable (empty) QS: 127.
        There are 149-127 = 22 timeslots with placements, but it's 8 unique session
                               requests, because in this dataset, two session were
                               scheduled into two timeslots.
        There are 145 session requests total.
        So there are 145-8           = 133 unplaced sessions.
        So there should be 149 + 133 = 282 slots total - 8 = 273
        And then 12 non-sessions agenda items were excluded to take 273=>261.
        """
        sched1  = Schedule.objects.get(pk=103)
        placer1 = CurrentScheduleState(sched1)
        self.assertEqual(placer1.total_slots, 261) #, "total slots calculation")

    def test_currentScheduleStateIndex(self):
        sched1  = Schedule.objects.get(pk=103)
        placer1 = CurrentScheduleState(sched1)
        placer1.current_assignments["hello"] = "there"
        self.assertEqual(placer1["hello"], "there")
        placer1.tempdict["hello"] = "goodbye"
        self.assertEqual(placer1["hello"], "goodbye")

    def test_probcalculation(self):
        sched1  = Schedule.objects.get(pk=103)
        placer1 = CurrentScheduleState(sched1)
        placer1.temperature = 1000000
        prob = placer1.calc_probability(1000)
        self.assertTrue(prob < 0.5, "prob: %.2f" % (prob))
        prob = placer1.calc_probability(-1000)
        self.assertTrue(prob > 0.5, "prob: %.2f" % (prob))

