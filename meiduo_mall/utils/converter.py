from django.urls import converters


class UsernameConverter:
    regex = '[a-zA-z0-9_-]{5,20}'

    def to_python(self, value):
        return value


class UUIDConverter:
    regex = '[\\w-]+'

    def to_python(self, value):
        return value
