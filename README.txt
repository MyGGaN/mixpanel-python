mixpanel-python
===============
This is an inofficial Mixpanel Python3.3 library. This library allows for server-side integration of Mixpanel.

Features
--------
* Support for Python3.3
* Async support using tornados AsyncHTTPClient

Installation
------------
This Python3.3 library can not be installed via PyPi jet. Please clone the repo.


Getting Started
---------------
Typical usage usually looks like this:

    from mixpanel import Mixpanel

    mp = Mixpanel(YOUR_TOKEN)

    # tracks an event with certain properties
    mp.track('button clicked', {'color' : 'blue', 'size': 'large'})

    # sends an update to a user profile
    mp.people_set(USER_ID, {'$first_name' : 'Amy', 'favorite color': 'red'})

You can use an instance of the Mixpanel class for sending all of your events and people updates.

Additional Information
----------------------
[Help Docs](https://www.mixpanel.com/help/reference/python)

[Full Documentation](http://mixpanel.github.io/mixpanel-python/)

[mixpanel-python-asyc](https://github.com/jessepollak/mixpanel-python-async) a third party tool for sending data asynchronously from the tracking python process.
