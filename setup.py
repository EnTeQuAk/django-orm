from setuptools import setup, find_packages

description="""
Advanced improvement of django-orm with a lot of third-party plugins for use different parts of databases are
not covered by the standard orm. 
"""

long_description = """
Currently the only supported what was django-postgresql. 
But I'm working for some features available for all supported backends (postgresql, sqlite,
mysql), as orm connection-pool and low-level cache.

If you want to know in detail what it offers for each database, check the documentation.

* **Documentation**: http://readthedocs.org/docs/django-orm/en/latest/
* **Project page**: http://www.niwi.be/post/project-django-orm/
"""


setup(
    name="django-orm",
    version=':versiontools:django_orm:',
    url='https://github.com/niwibe/django-orm',
    license='BSD',
    platforms=['OS Independent'],
    description = description.strip(),
    long_description = long_description.strip(),
    author = 'Andrei Antoukh',
    author_email = 'niwi@niwi.be',
    maintainer = 'Andrei Antoukh',
    maintainer_email = 'niwi@niwi.be',
    packages = [
        'django_orm.postgresql',
        'django_orm.cache',
        'django_orm.mysql',
        'django_orm.fields',
        'django_orm.sqlite3',
        'django_orm.postgresql.fts',
        'django_orm.postgresql.fields',
        'django_orm.postgresql.hstore',
        'django_orm.postgresql.geometric',
        'django_orm.backends',
        'django_orm.backends.postgresql_psycopg2',
        'django_orm.backends.mysql',
        'django_orm.backends.sqlite3',
        'django_orm.gis',
    ],
    include_package_data = True,
    install_requires=[
        'distribute',
        'psycopg2>=2.4'
    ],
    setup_requires = [
        'versiontools >= 1.8',
    ],
    zip_safe = False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
