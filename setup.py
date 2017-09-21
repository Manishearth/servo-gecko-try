from setuptools import setup

setup(
    name='servo_gecko_try',
    version='0.1.0',
    author='The Servo Project Developers',
    url='https://github.com/servo/servo-gecko-try',
    description='A service that lets you make Gecko try pushes out of Servo pull requests',
    packages=['servo_gecko_try'],
    package_data={'': ['run.sh']},
    install_requires=[
        'flask',
    ],
    entry_points={
        'console_scripts': [
            'servo_gecko_try=servo_gecko_try.flask_server:main',
        ],
    },
    zip_safe=False,
)
