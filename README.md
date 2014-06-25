mixpanel-py3
============
This library allows for server-side integration of Mixpanel.
This is an in-official Mixpanel library for Python3.
Its major version number reflects the Mixpanel API version.

Features over the official client
---------------------------------
* Support for Python3
* Optional async consumer using tornado's AsyncHTTPClient
* Convenient method to generate tracking URLs, useful for email tracking

Installation
------------
This library can be installed via PyPI:

    pip install mixpanel-py3

Getting Started
---------------
Typical usage usually looks like this:

    from mixpanel import Mixpanel

    mp = Mixpanel(YOUR_TOKEN)

    # tracks an event with certain properties
    mp.track('button clicked', {'color': 'green', 'size': 'large'})

    # sends an update to a user profile
    mp.people_set(USER_ID, {'$first_name': 'Graham', 'favorite color': 'red'})

You can use an instance of the Mixpanel class for sending all of your events and people updates.

Issues
------
If you find any issues please file those on [GitHub](https://github.com/MyGGaN/mixpanel-python/issues) preferably with a pull request.

Contribute
----------
If you have improved code, tests, documentation or added a feature, please open a pull request and share your work.

Additional Information
----------------------
[mixpanel-py](https://github.com/mixpanel/mixpanel-python) Official client for Python2.

[Tornado](http://www.tornadoweb.org/en/stable/) I/O-loop based web framework.
