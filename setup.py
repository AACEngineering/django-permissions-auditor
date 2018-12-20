import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


setup(
    name='django-permissions-auditor',
    version=__import__('permissions_auditor').__version__,
    description='django-easymde is a WYSIWYG markdown editor for Django',
    long_description=README,
    author='AAC Engineering',
    license='MIT',
    packages=find_packages(exclude=['example']),
    include_package_data=True,
    install_requires=[
        'django>=2.1'
        'setuptools'
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking',
    ],
    keywords='django,admin,permissions,audit,auditor',
)
