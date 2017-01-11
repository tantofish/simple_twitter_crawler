try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'crawl twitter practice',
    'author': 'Yu Tu',
    'url': 'TBD',
    'download_url': 'TBD',
    'author_email': 'Tantofish@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['twitwi'],
    'scripts': [],
    'name': 'twitwi'
}

setup(**config)
