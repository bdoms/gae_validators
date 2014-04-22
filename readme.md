Copyright &copy; 2014, [Brendan Doms](http://www.bdoms.com/)  
Licensed under the [MIT license](http://www.opensource.org/licenses/MIT)

# GAE Validators

GAE Validators provides user input validation methods for the Google App Engine datastore.

## How It Works

Each validator is simply a method that receives input and returns a tuple of `(valid, value)` back.
`valid` is simply a boolean of whether the input passed validation or not.
`value` is a coerced, potentially optimized version of the input.
For example, strings have outer whitespace stripped, while integers, booleans, and dates are all returned as their respective type.

Some validators have additional parameters to help configure how validation should be done.
By default, these are all defined to match the restrictions of the
[GAE properties](https://developers.google.com/appengine/docs/python/datastore/typesandpropertyclasses).
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
validateString(source, max_length=500, newlines=False)

validateRequiredString(source, max_length=500, newlines=False)
# same as above execpt that an empty string will fail

validateText(source, max_length=ONE_MB, newlines=True)
# ONE_MB is defined as 2 ** 20

validateEmail(source)

validateBool(source)

validateInt(source, min_amount=-INT_SIZE, max_amount=INT_SIZE - 1)
# INT_SIZE is defined as a 64 bit signed integer, which means 2 ** 63

validateDate(source, date_format="%m/%d/%Y", keep_time=False, future_only=True)
```
