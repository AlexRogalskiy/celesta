# coding=UTF-8

from java.sql import Timestamp
from java.time import LocalDateTime

from celestaunit.internal_celesta_unit import CelestaUnit
from aggregate._aggregate_orm import countConditionLessCursor, countGetDateCondCursor\
    , viewCountCondLessCursor, viewCountGetDateCondCursor, tableSumOneFieldCursor\
    , viewSumOneFieldCursor, sumFieldAndNumberCursor, viewSumTwoNumbersCursor\
    , tableSumTwoFieldsCursor, viewSumTwoFieldsCursor, tableMinMaxCursor\
    , viewMinOneFieldCursor, viewMaxOneFieldCursor, viewMinTwoFieldsCursor, viewMaxTwoFieldsCursor\
    , tableGroupByCursor, viewGroupByAggregateCursor, viewGroupByCursor, viewCountMinMaxCursor

class TestAggregate(CelestaUnit):

    def test_count_without_condition(self):
        tableCursor = countConditionLessCursor(self.context)
        tableCursor.deleteAll()

        viewCursor = viewCountCondLessCursor(self.context)
        self.assertEqual(1, viewCursor.count())
        viewCursor.first()
        self.assertEqual(0, viewCursor.c)

        tableCursor.insert()
        tableCursor.clear()
        tableCursor.insert()

        self.assertEqual(1, viewCursor.count())
        viewCursor.first()
        self.assertEqual(2, viewCursor.c)


    def test_count_with_getdate_condition(self):
        tableCursor = countGetDateCondCursor(self.context)
        tableCursor.deleteAll()

        viewCursor = viewCountGetDateCondCursor(self.context)
        viewCursor.first()
        self.assertEqual(0, viewCursor.c)

        tableCursor.insert()
        tableCursor.clear()
        tableCursor.date = Timestamp.valueOf(LocalDateTime.now().minusSeconds(1))
        tableCursor.insert()

        viewCursor.first()
        self.assertEqual(0, viewCursor.c)

        tableCursor.clear()
        tableCursor.date = Timestamp.valueOf(LocalDateTime.now().plusDays(1))
        tableCursor.insert()

        viewCursor.first()
        self.assertEqual(1, viewCursor.c)


    def test_sum_one_field(self):
        tableOneFieldCursor = tableSumOneFieldCursor(self.context)
        tableOneFieldCursor.deleteAll()

        viewOneFieldCursor = viewSumOneFieldCursor(self.context)
        viewOneFieldAndNumberCursor= sumFieldAndNumberCursor(self.context)
        viewTwoNumbersCursor = viewSumTwoNumbersCursor(self.context)

        self.assertEqual(1, viewOneFieldCursor.count())
        self.assertEqual(1, viewOneFieldAndNumberCursor.count())
        self.assertEqual(1, viewTwoNumbersCursor.count())

        viewOneFieldCursor.first()
        viewOneFieldAndNumberCursor.first()
        viewTwoNumbersCursor.first()
        self.assertEqual(None, viewOneFieldCursor.s)
        self.assertEqual(None, viewOneFieldAndNumberCursor.s)
        self.assertEqual(None, viewTwoNumbersCursor.s)

        tableOneFieldCursor.f = 4
        tableOneFieldCursor.insert()

        viewOneFieldCursor.first()
        viewOneFieldAndNumberCursor.first()
        viewTwoNumbersCursor.first()
        self.assertEqual(4, viewOneFieldCursor.s)
        self.assertEqual(5, viewOneFieldAndNumberCursor.s)
        self.assertEqual(3, viewTwoNumbersCursor.s)


    def test_sum_two_fields(self):
        tableTwoFieldsCursor = tableSumTwoFieldsCursor(self.context)
        tableTwoFieldsCursor.deleteAll()

        viewTwoFieldsCursor = viewSumTwoFieldsCursor(self.context)

        self.assertEqual(1, viewTwoFieldsCursor.count())

        viewTwoFieldsCursor.first()
        self.assertEqual(None, viewTwoFieldsCursor.s)

        tableTwoFieldsCursor.f1 = 2
        tableTwoFieldsCursor.insert()
        tableTwoFieldsCursor.clear()

        viewTwoFieldsCursor.first()
        self.assertEqual(None, viewTwoFieldsCursor.s)

        tableTwoFieldsCursor.f2 = 2
        tableTwoFieldsCursor.insert()
        tableTwoFieldsCursor.clear()

        viewTwoFieldsCursor.first()
        self.assertEqual(None, viewTwoFieldsCursor.s)

        tableTwoFieldsCursor.f1 = 2
        tableTwoFieldsCursor.f2 = 3
        tableTwoFieldsCursor.insert()
        tableTwoFieldsCursor.clear()

        viewTwoFieldsCursor.first()
        self.assertEqual(5, viewTwoFieldsCursor.s)


    def test_min_and_max_one_field(self):
      tableCur = tableMinMaxCursor(self.context)
      tableCur.deleteAll()

      viewMinOneFieldCur = viewMinOneFieldCursor(self.context)
      viewMaxOneFieldCur = viewMaxOneFieldCursor(self.context)
      viewMinTwoFieldsCur = viewMinTwoFieldsCursor(self.context)
      viewMaxTwoFieldsCur = viewMaxTwoFieldsCursor(self.context)
      viewCountMinMaxCur = viewCountMinMaxCursor(self.context)

      viewMinOneFieldCur.first()
      viewMaxOneFieldCur.first()
      viewMinTwoFieldsCur.first()
      viewMaxTwoFieldsCur.first()
      viewCountMinMaxCur.first()
      self.assertEqual(1, viewMinOneFieldCur.count())
      self.assertEqual(1, viewMaxOneFieldCur.count())
      self.assertEqual(1, viewMinTwoFieldsCur.count())
      self.assertEqual(1, viewMaxTwoFieldsCur.count())
      self.assertEqual(1, viewCountMinMaxCur.count())
      self.assertEqual(None, viewMinOneFieldCur.m)
      self.assertEqual(None, viewMaxOneFieldCur.m)
      self.assertEqual(None, viewMinTwoFieldsCur.m)
      self.assertEqual(None, viewMaxTwoFieldsCur.m)
      self.assertEqual(0, viewCountMinMaxCur.countv)
      self.assertEqual(None, viewCountMinMaxCur.maxv)
      self.assertEqual(None, viewCountMinMaxCur.minv)

      tableCur.f1 = 1
      tableCur.f2 = 5
      tableCur.insert()
      tableCur.clear()

      tableCur.f1 = 5
      tableCur.f2 = 2
      tableCur.insert()
      tableCur.clear()

      viewMinOneFieldCur.first()
      viewMaxOneFieldCur.first()
      viewMinTwoFieldsCur.first()
      viewMaxTwoFieldsCur.first()
      viewCountMinMaxCur.first()

      self.assertEqual(1, viewMinOneFieldCur.m)
      self.assertEqual(5, viewMaxOneFieldCur.m)
      self.assertEqual(6, viewMinTwoFieldsCur.m)
      self.assertEqual(7, viewMaxTwoFieldsCur.m)
      self.assertEqual(2, viewCountMinMaxCur.countv)
      self.assertEqual(5, viewCountMinMaxCur.maxv)
      self.assertEqual(2, viewCountMinMaxCur.minv)


def testGroupBy(self):
        tableCursor = tableGroupByCursor(self.context)
        tableCursor.deleteAll()

        viewGroupByCur = viewGroupByCursor(self.context)
        viewAggregateCursor = viewGroupByAggregateCursor(self.context)

        self.assertEqual(0, viewAggregateCursor.count())

        name1 = "A"
        name2 = "B"

        tableCursor.name = name1
        tableCursor.cost = 100
        tableCursor.insert()
        tableCursor.clear()

        viewGroupByCur.first()
        self.assertEqual(name1, viewGroupByCur.name)
        self.assertEqual(100, viewGroupByCur.cost)

        tableCursor.name = name1
        tableCursor.cost = 150
        tableCursor.insert()
        tableCursor.clear()
        tableCursor.name = name2
        tableCursor.cost = 50
        tableCursor.insert()
        tableCursor.clear()

        self.assertEqual(2, viewAggregateCursor.count())
        viewAggregateCursor.first()
        self.assertEqual(name1, viewAggregateCursor.name)
        self.assertEqual(250, viewAggregateCursor.s)

        viewAggregateCursor.next()
        self.assertEqual(name2, viewAggregateCursor.name)
        self.assertEqual(50, viewAggregateCursor.s)
