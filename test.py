import unittest

from __init__ import (validateString, validateRequiredString, validateText, validateRequiredText,
    validateEmail, validateRequiredEmail, validateUrl, validateRequiredUrl, validateChoices,
    validateBool, validateInt, validateFloat, validateDateTime, validateDate, validateTime)


class TestValidators(unittest.TestCase):

    def testValidateString(self):
        # non-unicode characters should fail
        valid, value = validateString('\xaa')
        self.assertFalse(valid)

        # non-ascii string should pass
        valid, value = validateString(u'\xaa')
        self.assertTrue(valid)

        # whitespace should be stripped
        valid, value = validateString('  test    ')
        self.assertTrue(valid)
        self.assertEqual(value, 'test')

        # beyond max length should fail
        valid, value = validateString('a' * 501)
        self.assertFalse(valid)

        # having newlines should fail
        valid, value = validateString('test with\ninner newline')
        self.assertFalse(valid)

        # having carriage return should fail
        valid, value = validateString('test with\rinner carriage return')
        self.assertFalse(valid)

        # empty string should pass
        valid, value = validateString('')
        self.assertTrue(valid)

    def testValidateRequiredString(self):
        # empty string should fail
        valid, value = validateRequiredString('')
        self.assertFalse(valid)

        # that includes spaces because they'll be stripped
        valid, value = validateRequiredString('    ')
        self.assertFalse(valid)

        # string with something should pass
        valid, value = validateRequiredString('test')
        self.assertTrue(valid)

    def testValidateText(self):
        # newlines should be allowed
        valid, value = validateText('foo\r\nbar')
        self.assertTrue(valid)

        # larger than normal string length should be allowed
        valid, value = validateText('a' * 501)
        self.assertTrue(valid)

    def testValidateRequiredText(self):
        # empty string should fail
        valid, value = validateRequiredText('')
        self.assertFalse(valid)

        # that includes spaces because they'll be stripped
        valid, value = validateRequiredText('    ')
        self.assertFalse(valid)

        # string with something should pass
        valid, value = validateRequiredText('test')
        self.assertTrue(valid)

    def testValidateEmail(self):
        # empty string should pass
        valid, value = validateUrl('')
        self.assertTrue(valid)

        # no at sign should fail
        valid, value = validateEmail('example.com')
        self.assertFalse(valid)

        # invalid username should fail
        valid, value = validateEmail('t(es>t@example.com')
        self.assertFalse(valid)

        # invalid domain should fail
        valid, value = validateEmail('test@example')
        self.assertFalse(valid)

        # valid should pass
        valid, value = validateEmail('test@example.com')
        self.assertTrue(valid)
        # confirm it hasn't been modified
        self.assertEqual(value, 'test@example.com')

    def testValidateRequiredEmail(self):
        # empty string should fail
        valid, value = validateRequiredEmail('')
        self.assertFalse(valid)

        # string with something should pass
        valid, value = validateRequiredEmail('test@example.com')
        self.assertTrue(valid)

    def testValidateUrl(self):
        # empty string should pass
        valid, value = validateUrl('')
        self.assertTrue(valid)

        # no host should fail
        valid, value = validateUrl('http://')
        self.assertFalse(valid)

        # scheme and host should pass
        valid, value = validateUrl('http://example.com')
        self.assertTrue(valid)

        # scheme should be added if not present
        valid, value = validateUrl('example.com')
        self.assertTrue(valid)
        self.assertEqual(value, 'http://example.com')

        # adding a path should pass
        valid, value = validateUrl('http://example.com/path')
        self.assertTrue(valid)

        # adding a query string should pass
        valid, value = validateUrl('http://example.com/path?key=value')
        self.assertTrue(valid)

    def testValidateRequiredUrl(self):
        # empty string should fail
        valid, value = validateRequiredUrl('')
        self.assertFalse(valid)

        # string with something should pass
        valid, value = validateRequiredUrl('http://example.com')
        self.assertTrue(valid)

    def testValidateChoices(self):
        # should fail if it's not in list
        valid, value = validateChoices('test', [])
        self.assertFalse(valid)

        # should pass if it is
        valid, value = validateChoices('test', ['test'])
        self.assertTrue(valid)

    def testValidateBool(self):

        # "on" should return True as that's what the GAE request returns for checkboxes
        valid, value = validateBool('on')
        self.assertTrue(valid)
        self.assertTrue(value)

        # empty string should return False
        valid, value = validateBool('')
        self.assertTrue(valid)
        self.assertFalse(value)

        # None should return False
        valid, value = validateBool(None)
        self.assertTrue(valid)
        self.assertFalse(value)

    def testValidateInt(self):
        # not a number should fail
        valid, value = validateInt('None')
        self.assertFalse(valid)

        # below the minimum should fail
        valid, value = validateInt(str(-2**64))
        self.assertFalse(valid)

        # above the maximum should fail
        valid, value = validateInt(str(2**64))
        self.assertFalse(valid)

        # valid should pass
        valid, value = validateInt('08')
        self.assertTrue(valid)
        # confirm base 10
        self.assertEqual(value, 8)

    def testValidateFloat(self):
        # not a number should fail
        valid, value = validateFloat('None')
        self.assertFalse(valid)

        # below the minimum should fail
        valid, value = validateFloat(str(-2**64))
        self.assertFalse(valid)

        # above the maximum should fail
        valid, value = validateFloat(str(2**64))
        self.assertFalse(valid)

        # valid integer should pass (implied float)
        valid, value = validateFloat('08')
        self.assertTrue(valid)
        # confirm base 10
        self.assertEqual(value, 8.0)

        # actual float with decimals should pass
        valid, value = validateFloat('3.14159')
        self.assertTrue(valid)
        self.assertEqual(value, 3.14159)

    def testValidateDateTime(self):
        # not a date time should fail
        valid, value = validateDateTime('None')
        self.assertFalse(valid)

        # valid date should pass
        valid, value = validateDateTime('3000-01-20T13:45')
        self.assertTrue(valid)

        # and have the seconds be zero
        self.assertEqual(value.second, 0)
        self.assertEqual(value.microsecond, 0)

        # a past date should fail
        valid, value = validateDateTime('1970-01-20T13:45')
        self.assertFalse(valid)

    def testValidateDate(self):
        # not a date should fail
        valid, value = validateDate('None')
        self.assertFalse(valid)

        # valid date should pass
        valid, value = validateDate('3000-01-20')
        self.assertTrue(valid)

        # a past date should fail
        valid, value = validateDate('1970-01-20')
        self.assertFalse(valid)

    def testValidateTime(self):
        # not a time should fail
        valid, value = validateTime('None')
        self.assertFalse(valid)

        # valid date should pass
        valid, value = validateTime('13:45')
        self.assertTrue(valid)

        # and have the seconds should be zero
        self.assertEqual(value.second, 0)
        self.assertEqual(value.microsecond, 0)


if __name__ == '__main__':
    unittest.main()
