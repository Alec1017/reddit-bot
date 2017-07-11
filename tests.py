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
        black_list = ['TEST', 'DATA']
        bot.save_black_list(self.filename, black_list)
        assert bot.load_black_list(self.filename) == black_list

    def testEmptyFile(self):
        '''
        if the file is empty assumes empty list returned
        '''
        open(self.filename, "w").close()

        assert bot.load_black_list(self.filename) == []

    def testAppendBlackList(self):
        '''
        test the ability to append an item to the black_list
        '''
        black_list = ['SOME', 'EXAMPLE', 'STRINGS']
        for item in black_list:
            bot.append_to_black_list(self.filename, item)
        assert bot.load_black_list(self.filename) == black_list


    def testNonExistentFile(self):
        '''
        makes sure that an IOError is raised when the file does not exist
        '''
        with pytest.raises(IOError):
            bot.load_black_list(self.filename)


# Remove the file if it's there, if it's not, we don't care.
def maybeRemoveFile(path):
    try:
        os.remove(path)
    except OSError:
        pass # we expect that call to fail if the test didnt make a file

class HypothesisTestBlackList(unittest.TestCase):
    '''
    Test suite formulated for the hypothesis framework.
    '''
    def execute_example(self, f):
        '''
        This is the handler that will run the below function.
        This class should be used for any Hypothesis test that needs a temporary
        file to work off of via the self.filename.
        '''

        # Generate a unique filename
        self.filename = str(uuid.uuid4())

        # Try to run the test
        try:
            result = f()
        except Exception:
            # If the test fails, try to delete the file if it was created
            maybeRemoveFile(self.filename)
            # Raise the exception to signal the test failed
            raise

        # If it is a success, try to delete the file if it was created
        maybeRemoveFile(self.filename)

        # Return the result of the test
        return result

    @hypothesis.given(lists(text(printable)))
    def testLotsOfStrings(self, strings):
        '''
        tests a bunch of generated strings
        '''
        # Assume the list is non-empty.
        hypothesis.assume(len(strings) > 0)

        # Fetch the given filename.
        filename = self.filename

        for ID in strings:
            # No whitespace on ends
            hypothesis.assume(ID.strip() == ID)
            # Assume no whitespace in middle of string
            hypothesis.assume(ID.split() == [ID])
            # Append the black id to the black_list file
            bot.append_to_black_list(filename, ID)

        # Verify that the loaded data matches the input data
        assert bot.load_black_list(filename) == strings
