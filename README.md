Copyright &copy; 2014-2020, [Brendan Doms](http://www.bdoms.com/)  
Licensed under the [MIT license](http://www.opensource.org/licenses/MIT)

# GAE Validators

GAE Validators provides user input validation methods with smart defaults for the Google App Engine datastore.

## Build Status

![Python 2 Tests](https://api.cirrus-ci.com/github/bdoms/gae_validators.svg?task=python2_tests)
![Python 3 Tests](https://api.cirrus-ci.com/github/bdoms/gae_validators.svg?task=python3_tests)
![Flake8 Linter](https://api.cirrus-ci.com/github/bdoms/gae_validators.svg?task=flake8)
![Build Package](https://api.cirrus-ci.com/github/bdoms/gae_validators.svg?task=build_package)

## How It Works

Each validator is simply a method that receives string input and returns a tuple of `(valid, value)` back.
`valid` is simply a boolean of whether the input passed validation or not.
`value` is a coerced, potentially optimized version of the input.
For example, strings have outer whitespace stripped, while integers, booleans, and dates are all returned as their respective type.

Some validators have additional parameters to help configure how validation should be done.
By default, these are all defined to match the restrictions of the
[GAE properties](https://cloud.google.com/appengine/docs/python/datastore/typesandpropertyclasses).
In theory you could support any datastore backend simply by changing the configuration parameters.

## Example Use

The normal flow of a program would be to get some user input from a form, pull it out of the request, and validate it.
If validation passes for all the fields, then update the datastore, if not, then return helpful errors to the user.
For example:


```python
from gae_validators import validateEmail

class ExampleHandler(webapp2.RequestHandler):

    def post(self):

        form_email = self.request.get("email")

        is_valid, validated_email = validateEmail(form_email)

        if is_valid:
            user.email = validated_email
            user.put()
        else:
            self.redirect("/user/update?errors=email")
```

## Available Validators

Here are all the function signatures with their default configuration values:

```python
validateString(source, max_length=500, newlines=False, encoding='utf-8', condense=True, convert_spaces=True)
# condense turns multiple spaces in a row into a single space, e.g. "foo   bar" becomes "foo bar"
# convert_spaces turns unicode spaces into normal ASCII spaces

validateRequiredString(source, min_length=1, max_length=500, newlines=False, encoding='utf-8', condense=True, convert_spaces=True)
# same as above execpt that a string below the min_length will fail

validateText(source, max_length=ONE_MB, newlines=True, encoding='utf-8', condense=True, convert_spaces=True)
# the major default difference with text is allowing newlines, and a much larger max_length
# ONE_MB is defined as 2 ** 20

validateRequiredText(source, min_length=1, max_length=ONE_MB, newlines=True, encoding='utf-8', condense=True, convert_spaces=True)

validateEmail(source)

validateRequiredEmail(source)

validatePhone(source)
# returns the number in a good approximation of E.164 format
# this should work exactly for numbers with country code 1 (US and Canada)
# however it will not be correct in all cases for all countries
# you'll need a different solution if you want full international support

validateRequiredPhone(source)

validateUrl(source)
# only http and https schemes are supported

validateRequiredUrl(source)

validateChoices(source, choices)
# choices should be an iterable

validateRequiredChoices(source, choices)

validateBool(source)
# any value can be truthy or falsy
# so there is no required version of validateBool, and it will never return an invalid result

validateInt(source, min_amount=-INT_SIZE, max_amount=INT_SIZE - 1)
# INT_SIZE is defined as a 64 bit signed integer, which means 2 ** 63

validateRequiredInt(source, min_amount=-INT_SIZE, max_amount=INT_SIZE - 1)

validateFloat(source, min_amount=-INT_SIZE, max_amount=INT_SIZE - 1)

validateRequiredFloat(source, min_amount=-INT_SIZE, max_amount=INT_SIZE - 1)

validateDateTime(source, date_format="%Y-%m-%dT%H:%M", future_only=False, past_only=False)

validateRequiredDateTime(source, date_format="%Y-%m-%dT%H:%M", future_only=False, past_only=False)

validateDate(source, date_format="%Y-%m-%d", future_only=False, past_only=False)

validateRequiredDate(source, date_format="%Y-%m-%d", future_only=False, past_only=False)

validateTime(source, time_format="%H:%M")

validateRequiredTime(source, time_format="%H:%M")
```
