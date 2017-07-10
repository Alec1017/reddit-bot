import bot
import os
import uuid
import unittest
import pytest
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
        '''
        writes some sample data to the file then tries loading it out
        '''
        with open(self.filename, "w") as f:
            f.write("TEST\n")
            f.write("DATA")
        assert bot.load_black_list(self.filename) == ["TEST", "DATA"]

    def testEmptyFile(self):
        '''
        if the file is empty assumes empty list returned
        '''
        open(self.filename, "w").close()

        assert bot.load_black_list(self.filename) == []

    @hypothesis.given(lists(text(printable)))
    def testLotsOfStrings(self, strings):
        '''
        tests a bunch of generated strings
        '''
        with open(self.filename, "w") as f:
            for item in strings:
                #No whitespace on ends
                hypothesis.assume(item.strip() == item)
                #Assume no whitespace in middle of string
                hypothesis.assume(item.split() ==[item])
                f.write(item + "\n")
        assert bot.load_black_list(self.filename) == strings

    def testNonExistantFile(self):
        '''
        makes sure that an IOError is raised when the file does not exist
        '''
        with pytest.raises(IOError):
            bot.load_black_list(self.filename)
