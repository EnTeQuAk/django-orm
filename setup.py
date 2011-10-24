from setuptools import setup, find_packages

description="""
Advanced improvement of postgresql_psycopg2 django-orm 
backend with: connection pool, server-side cursors, native complex types,
hstore and unaccent aggregates.
"""

long_description = """
* **Documentation**: http://readthedocs.org/docs/django-postgresql/en/latest/
* **Project page**: http://www.niwi.be/post/project-django-postgresql/
"""


setup(
    name="django-postgresql",
    #version="1.6",
    version=':versiontools:django_postgresql:',
    url='https://github.com/niwibe/django-postgresql',
    license='BSD',
    platforms=['OS Independent'],
    description = description.strip(),
    long_description = long_description.strip(),
    author = 'Andrei Antoukh',
    author_email = 'niwi@niwi.be',
    maintainer = 'Andrei Antoukh',
    maintainer_email = 'niwi@niwi.be',
    packages = [
        'django_postgresql',
        'django_postgresql.fts',
        'django_postgresql.fields',
        'django_postgresql.hstore',
        'django_postgresql.postgresql_psycopg2',
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
