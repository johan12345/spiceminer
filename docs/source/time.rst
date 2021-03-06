Time
****


spiceminer ships its own time implementation to allow custom features and more
consistency than the standart datetime module.

Differences to datetime
=======================

It's a float:
    That means it can be used in range functions that support floats like
    ``numpy.arange`` or ``numpy.linspace``.

    It also supports all arithmetical operations, allowing much simpler
    calculations like ``Time(2015) + 20`` to add 20 seconds instead of having to
    generate a new object explicitly. It also has constants for minute, hour,
    and day to simpliefy use in range functions. For example
    ``numpy.arange(Time(2000), Time(2001), Time.DAY)`` produces an array with
    each entry representing a day in the year 2000.
Day of year:
    Time has constructor and attribute for handling day of year instead of
    handling month, day, hour, etc. seperately.
No timezones:
    You don't have to handle conversion to UTC and timezone related weirdness.

API
===

.. module:: spiceminer

.. autoclass:: Time
   :members:
