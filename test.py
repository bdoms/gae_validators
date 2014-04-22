import unittest

from __init__ import validateString, validateRequiredString, validateText, validateEmail
from __init__ import validateBool, validateInt, validateDate


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
        valid, value = validateText('\r\n')
        self.assertTrue(valid)

        # larger than normal string length should be allowed
        valid, value = validateText('a' * 501)
        self.assertTrue(valid)

    def testValidateEmail(self):
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

    def testValidateDate(self):
        # not a date should fail
        valid, value = validateDate('None')
        self.assertFalse(valid)

        # valid date should pass
        valid, value = validateDate('01/01/1970')
        self.assertTrue(valid)
        # and have the time component stripped
        self.assertEqual(value.hour, 0)
        self.assertEqual(value.minute, 0)
        self.assertEqual(value.second, 0)
        self.assertEqual(value.microsecond, 0)

        # a future date should fail
        valid, value = validateDate('01/01/3000')
        self.assertFalse(valid)


if __name__ == '__main__':
    unittest.main()
