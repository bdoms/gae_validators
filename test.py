import unittest

from gae_validators import (PY3, validateString, validateRequiredString, validateText,
    validateRequiredText, validateEmail, validateRequiredEmail, validatePhone,
    validateRequiredPhone, validateUrl, validateRequiredUrl, validateChoices,
    validateRequiredChoices, validateBool, validateInt, validateRequiredInt, validateFloat,
    validateRequiredFloat, validateDateTime, validateRequiredDateTime, validateDate,
    validateRequiredDate, validateTime, validateRequiredTime)


class TestValidators(unittest.TestCase):

    def testValidateString(self):
        if PY3:
            # check for invalid unicode string
            valid, value = validateString('\udcc3')
            self.assertFalse(valid)

            # handle bad byte string
            valid, value = validateString(b'\xff')
            self.assertFalse(valid)
        else:
            # non-ascii characters in an ascii string should fail
            valid, value = validateString('\xaa')
            self.assertFalse(valid)

            # check for invalid unicode string
            valid, value = validateString(u'\u0411', encoding='iso-8859-15')
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

        # none should pass as empty string
        valid, value = validateString(None)
        self.assertTrue(valid)
        self.assertEqual(value, '')

        # inner spaces should be condensed
        valid, value = validateString('test  with   inner     spaces')
        self.assertTrue(valid)
        self.assertEqual(value, 'test with inner spaces')

        # spaces should be converted
        valid, value = validateString(u'test\xa0with\x20unicode\u2000spaces')
        self.assertTrue(valid)
        self.assertEqual(value, 'test with unicode spaces')

        # spaces that need to be converted should also be condensed
        valid, value = validateString(u'test\xa0\x20with inner\x20\xa0unicode\u2000 \u3000spaces')
        self.assertTrue(valid)
        self.assertEqual(value, 'test with inner unicode spaces')

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

        # enforce a higher minimum length
        valid, value = validateRequiredString('foo', min_length=6)
        self.assertFalse(valid)

        valid, value = validateRequiredString('foobar', min_length=6)
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

        # enforce a higher minimum length
        valid, value = validateRequiredText('foo', min_length=6)
        self.assertFalse(valid)

        valid, value = validateRequiredText('foobar', min_length=6)
        self.assertTrue(valid)

    def testValidateEmail(self):
        # empty string should pass
        valid, value = validateEmail('')
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

    def testValidatePhone(self):
        # empty string should pass
        valid, value = validatePhone('')
        self.assertTrue(valid)

        # not enough digits should fail
        valid, value = validatePhone('this is not a phone number')
        self.assertFalse(valid)

        # too many digits should fail
        valid, value = validatePhone('12345678901234567890')
        self.assertFalse(valid)

        # valid without country code should pass
        valid, value = validatePhone('555-555-5555')
        self.assertTrue(valid)
        self.assertEqual(value, '+15555555555')

        # valid with country code should pass
        valid, value = validatePhone('+1 555 555 5555')
        self.assertTrue(valid)
        self.assertEqual(value, '+15555555555')

        # looking for extension but no extension separator
        valid, value = validatePhone('555-555-5555', extension_separators=('ext'))
        self.assertTrue(valid)
        self.assertEqual(value, '+15555555555')

        # looking for extension but none provided
        valid, value = validatePhone('555-555-5555 ext', extension_separators=('ext'))
        self.assertTrue(valid)
        self.assertEqual(value, '+15555555555')

        valid, value = validatePhone('555-555-5555 ext here', extension_separators=('ext'))
        self.assertTrue(valid)
        self.assertEqual(value, '+15555555555')

        # looking for extension but it's too long
        valid, value = validatePhone('555-555-5555 ext 123-456-7890',
            extension_separators=('ext'), extension_max_length=9)
        self.assertTrue(valid)
        self.assertEqual(value, '+15555555555')

        # valid extension
        valid, value = validatePhone('555-555-5555 ext 123-456-789',
            extension_separators=('ext'), extension_max_length=9)
        self.assertTrue(valid)
        self.assertEqual(value, '+15555555555;ext=123456789')

    def testValidateRequiredPhone(self):
        # empty string should fail
        valid, value = validateRequiredPhone('')
        self.assertFalse(valid)

        # string with something should pass
        valid, value = validateRequiredPhone('(555) 555-5555')
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
        # should pass if there's nothing
        valid, value = validateChoices('', [])
        self.assertTrue(valid)

        # should fail if it's not in list
        valid, value = validateChoices('test', [])
        self.assertFalse(valid)

        # should pass if it is
        valid, value = validateChoices('test', ['test'])
        self.assertTrue(valid)

    def testValidateRequiredChoices(self):
        # should fail if there's nothing
        valid, value = validateRequiredChoices('', [])
        self.assertFalse(valid)

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
        # empty should pass
        valid, value = validateInt('')
        self.assertTrue(valid)

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

    def testValidateRequiredInt(self):
        # empty should fail
        valid, value = validateRequiredInt('')
        self.assertFalse(valid)

    def testValidateFloat(self):
        # empty should pass
        valid, value = validateFloat('')
        self.assertTrue(valid)

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

    def testValidateRequiredFloat(self):
        # empty should fail
        valid, value = validateRequiredFloat('')
        self.assertFalse(valid)

    def testValidateDateTime(self):
        # empty should pass
        valid, value = validateDateTime('')
        self.assertTrue(valid)

        # not a date time should fail
        valid, value = validateDateTime('None')
        self.assertFalse(valid)

        # valid date should pass
        valid, value = validateDateTime('3000-01-20T13:45')
        self.assertTrue(valid)

        # and have the seconds be zero
        self.assertEqual(value.second, 0)
        self.assertEqual(value.microsecond, 0)

        # a future date should pass if it has to be in the future
        valid, value = validateDateTime('3000-01-20T13:45', future_only=True)
        self.assertTrue(valid)

        # but fail if it has to be in the past
        valid, value = validateDateTime('3000-01-20T13:45', past_only=True)
        self.assertFalse(valid)

        # a past date should pass if it has to be in the past
        valid, value = validateDateTime('1970-01-20T13:45', past_only=True)
        self.assertTrue(valid)

        # but fail if it has to be in the future
        valid, value = validateDateTime('1970-01-20T13:45', future_only=True)
        self.assertFalse(valid)

    def testValidateRequiredDateTime(self):
        # empty should fail
        valid, value = validateRequiredDateTime('')
        self.assertFalse(valid)

    def testValidateDate(self):
        # empty shoulf pass
        valid, value = validateDate('')
        self.assertTrue(valid)

        # not a date should fail
        valid, value = validateDate('None')
        self.assertFalse(valid)

        # valid date should pass
        valid, value = validateDate('3000-01-20')
        self.assertTrue(valid)

        # a future date should pass if it has to be in the future
        valid, value = validateDateTime('3000-01-20T13:45', future_only=True)
        self.assertTrue(valid)

        # but fail if it has to be in the past
        valid, value = validateDateTime('3000-01-20T13:45', past_only=True)
        self.assertFalse(valid)

        # a past date should pass if it has to be in the past
        valid, value = validateDate('1970-01-20', past_only=True)
        self.assertTrue(valid)

        # but fail if it has to be in the future
        valid, value = validateDate('1970-01-20', future_only=True)
        self.assertFalse(valid)

    def testValidateRequiredDate(self):
        # empty shoulf pass
        valid, value = validateRequiredDate('')
        self.assertFalse(valid)

    def testValidateTime(self):
        # emoty should pass
        valid, value = validateTime('')
        self.assertTrue(valid)

        # not a time should fail
        valid, value = validateTime('None')
        self.assertFalse(valid)

        # valid date should pass
        valid, value = validateTime('13:45')
        self.assertTrue(valid)

        # and have the seconds should be zero
        self.assertEqual(value.second, 0)
        self.assertEqual(value.microsecond, 0)

    def testValidateRequiredTime(self):
        # emoty should fail
        valid, value = validateRequiredTime('')
        self.assertFalse(valid)


if __name__ == '__main__':
    unittest.main()
