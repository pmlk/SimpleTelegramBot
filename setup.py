from setuptools import setup

setup(
    name='SimpleTelegramBot',
    packages=['bot', 'utils'],
    version='0.0.0',
    include_package_data=True,
    install_requires=[
        'requests',
        'urllib3',
    ],
)
