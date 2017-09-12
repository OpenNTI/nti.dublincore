import codecs
from setuptools import setup, find_packages

entry_points = {
    'console_scripts': [
    ],
}

TESTS_REQUIRE = [
    'nti.testing',
    'zope.dottedname',
    'zope.testrunner',
]


def _read(fname):
    with codecs.open(fname, encoding='utf-8') as f:
        return f.read()


setup(
    name='nti.dublincore',
    version=_read('version.txt').strip(),
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="NTI Dublincore",
    long_description=(_read('README.rst') + '\n\n' + _read("CHANGES.rst")),
    license='Apache',
    keywords='dublincore',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    url="https://github.com/NextThought/nti.dublincore",
    zip_safe=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    namespace_packages=['nti'],
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'setuptools',
        'nti.base',
        'nti.externalization',
        'nti.schema',
        'nti.zodb',
        'persistent',
        'zope.component',
        'zope.deferredimport',
        'zope.deprecation',
        'zope.dublincore',
        'zope.interface',
        'zope.mimetype',
        'zope.security',
    ],
    extras_require={
        'test': TESTS_REQUIRE,
    },
    entry_points=entry_points,
)
