try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='mixpanel-py3',
    version='3.0.3',
    author='Fredrik Svensson',
    author_email='shootoneshot@hotmail.com',
    packages=['mixpanel'],
    url='https://github.com/MyGGaN/mixpanel-python',
    description='Mixpanel library for Python 3',
    long_description="This library wraps Mixpanel's http API in a convenient way.  This is an in-official Mixpanel library for Python 3.",
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
    test_suite='tests'
)
