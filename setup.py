import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',

    'psycopg2',
    'dogpile.cache',

    # testing
    'nose',
    'coverage',
    'unittest2',
    'mock',
    ]

setup(name='turnabout',
      version='0.0',
      description='turnabout',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='turnabout',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = turnabout:main
      [console_scripts]
      initialize_turnabout_db = turnabout.scripts.initializedb:main
      """,
      )
