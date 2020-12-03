import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


setup(
    name='django-permissions-auditor',
    version=__import__('permissions_auditor').__version__,
    description='django-permissions-auditor is a tool to audit access control on your django app.',
    long_description=README,
    long_description_content_type='text/markdown',
    author='AAC Engineering',
    url='https://github.com/AACEngineering/django-permissions-auditor',
    license='MIT',
    packages=find_packages(exclude=['example']),
    include_package_data=True,
    python_requires='>=3.5',
    install_requires=[
        'django>=2.1'
        'setuptools'
    ],
    zip_safe=False,
    test_suite='runtests.runtests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking',
    ],
    keywords='django,admin,permissions,audit,auditor',
)
