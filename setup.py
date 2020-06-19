import os
import setuptools
try:
    # pip >=20
    from pip._internal.network.session import PipSession
    from pip._internal.req import parse_requirements
except ImportError:
    try:
        # 10.0.0 <= pip <= 19.3.1
        from pip._internal.download import PipSession
        from pip._internal.req import parse_requirements
    except ImportError:
        # pip <= 9.0.3
        from pip.download import PipSession
        from pip.req import parse_requirements


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()


setuptools.setup(
    name='steamfiles',
    version='0.1.4',
    url='https://github.com/leovp/steamfiles',
    license='MIT',

    author='Leonid Runyshkin',
    author_email='runyshkin@gmail.com',

    keywords='steam files valve format parse appinfo vdf acf manifest',
    description='Python library for parsing the most common Steam file formats.',
    long_description=read('README.rst'),

    include_package_data=True,
    package_data={'': ['README.rst', 'LICENSE']},

    platforms=['any'],
    packages=setuptools.find_packages(exclude=['tests']),

    install_requires=[
        str(req.req) for req in parse_requirements('requirements.txt',
                                                   session=PipSession())
        ],

    tests_require=[
        str(req.req) for req in parse_requirements('requirements_test.txt',
                                                   session=PipSession())
        ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
