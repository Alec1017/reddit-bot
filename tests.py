import bot
import os
import uuid
import unittest
import hypothesis
from hypothesis.strategies import lists, text
from string import printable

class TestBlackListLoading(unittest.TestCase):
    def setUp(self):
        '''
        creates a black_list file with a uuid for a name and a
        uuid for a name
        '''
        self.filename = str(uuid.uuid4())

    def tearDown(self):
        try:
            os.remove(self.filename)
        except OSError:
            pass # we expect that call to fail if the test didnt make a file

    def testSimpleLoading(self):
        with open(self.filename, "w") as f:
            f.write("TEST\n")
            f.write("DATA")
        assert bot.load_black_list(self.filename) == ["TEST", "DATA"]

    @hypothesis.given(lists(text(printable)))
    def testLotsOfStrings(self, strings):
        with open(self.filename, "w") as f:
            for item in strings:
                #No whitespace on ends
                hypothesis.assume(item.strip() == item)
                #Assume no whitespace in middle of string
                hypothesis.assume(item.split() ==[item])
                f.write(str(item) + "\n")
        assert bot.load_black_list(self.filename) == strings
