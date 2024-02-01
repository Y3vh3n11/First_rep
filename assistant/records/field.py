import re
from datetime import datetime, date

class Field:
    """ This class accepts the value value, checks
      it using the is_value method, and if the value
      passes the check, the value is written to the
      _value class field. """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self.is_valid(value):
            self._value = value

    def is_valid(self, value):
        """ This method performs a value check, and
        if the check is successful, returns True, and
        if not, throws an exception of type ValueError """
        return True

class Name(Field):
    def is_valid(self, value: str):
        if value.isalpha():
            return True
        raise ValueError('Incorrect name format')


class Phone(Field):
    def is_valid(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Incorrect phone number")
        return True


class Address(Field):
    def is_valid(self, value):
        if not 0 < len(value) <= 100:
            raise ValueError("Address is too long. 100 symbols max")
        if not re.search(
            r"^[a-zA-Z0-9 .,_-]*$",
            value
        ):
            raise ValueError(
                "Incorrect character used. Accepted characters: "
                "capital and small letters, digits, period(.), "
                "hyphen(-), underscore(_), comma(,) and space."
            )
        return True

class Date(Field):
    def is_valid(self, value):
        try:
            birthday = datetime.strptime(value, "%Y-%m-%d").date()
            if date.today() < birthday:
                raise ValueError
            return True
        except ValueError:
            raise ValueError("Incorrect date of birth")


class EmailAddress(Field):
    def is_valid(self, value):
        if re.search(
            r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$",
            value
        ):
            return True
        raise ValueError("Incorrect e-mail format")


# The tag should not be too long.
# Hereby established the rule for tag length: 25 symbol max.
# Next characters are accepted: capital and small letters, digits,
# period(.), hyphen(-), underscore(_), comma(,) and space.
class Tag(Field):
    def is_valid(self, value):
        if not 0 < len(value) <= 25:
            raise ValueError("Tag is too long. 25 symbols max")
        if not re.search(
            r"^[a-zA-Z0-9 .,_-]*$",
            value
        ):
            raise ValueError(
                "Incorrect character used. Accepted characters: "
                "capital and small letters, digits, period(.), "
                "hyphen(-), underscore(_), comma(,) and space."
            )
        return True

class Text(Field):
    MAX_LENGTH = 250

    def is_valid(self, value):
        if len(value) > self.MAX_LENGTH:
            raise ValueError(
                "Text exceeds the maximum length of {} characters.".format(
                    self.MAX_LENGTH))
        return True


class Title(Field):
    MAX_LENGTH = 15

    def is_valid(self, value):
        if len(value) > self.MAX_LENGTH:
            raise ValueError(
                "Title exceeds the maximum length of {} characters.".format(
                    self.MAX_LENGTH))
        return True
