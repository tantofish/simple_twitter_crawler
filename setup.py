try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

config = {
    'description': 'crawl twitter practice',
    'author': 'Yu Tu',
    'url': 'https://github.com/tantofish/simple_twitter_crawler',
    'download_url': 'https://github.com/tantofish/simple_twitter_crawler/archive/master.zip',
    'author_email': 'tantofish@gmail.com',
    'version': '0.0.16',
    'install_requires': [
        'nose',
        'lxml',
        'requests',
    ],
    'packages': find_packages(),
    'name': 'twitwi'
}

setup(**config)
