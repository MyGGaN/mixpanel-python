try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='mixpanel-py3',
    version='3.0.0',
    author='Fredrik Svensson',
    author_email='shootoneshot@hotmail.com',
    packages=['mixpanel'],
    url='https://github.com/MyGGaN/mixpanel-python',
    description='Mixpanel library for Python3.3',
    long_description="This library allows for server-side integration of Mixpanel. This is an inofficial Mixpanel library for Python3.3.",
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
    test_suite='tests'
)
