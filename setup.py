import os

from setuptools import setup, find_packages


def get_version():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, 'src/darter/version.py')) as f:
        locals = {}
        exec(f.read(), locals)
        return locals['VERSION']
    raise RuntimeError('No version info found.')


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='openstack-darter',
      version=get_version(),
      description=readme(),
      keywords='openstack capacity panel',
      url='',
      author='Marcus Floriano',
      author_email='marcus.floriano@gmail.com',
      license='MIT',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      platforms=[],
      python_requires='>=3',
      install_requires=[
          "click==7",
          "terminaltables==3.1.0",
          "openstacksdk==0.31.2",
          "python-cinderclient==4.2.1",
          "terminaltables==3.1.0",
          "redis==2.10.6",
          "rq==0.10.0",
          "rq-dashboard"
      ],
      setup_requires=['pytest-runner', 'sphinxcontrib-napoleon'],
      tests_require=['pytest', 'pylint'],
      classifiers=[
            # Documents for packaging python softwares
            # https://packaging.python.org/tutorials/distributing-packages/
            # https://pypi.python.org/pypi?%3Aaction=list_classifiers

            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',

            'Environment :: OpenStack',

            # Indicate who your project is intended for
            'Intended Audience :: System Administrators',
            'Topic :: System :: Systems Administration',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: MIT License',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.5',

            'Operating System :: POSIX :: Linux'
        ],
      entry_points={
            'console_scripts': ['openstack-darter=darter:cli'],
      },
      include_package_data=True,
      zip_safe=False)
