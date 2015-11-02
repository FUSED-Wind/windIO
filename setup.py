from setuptools import setup

setup(name='windIO',
      version='0.1',
      description='A simple python package to read and write wind energy related input/output files',
      url='https://github.com/rethore/windIO',
      author='Pierre-Elouan Rethore',
      author_email='pire@dtu.dk',
      license='Apache 2.0',
      packages=['windIO'],
      install_requires=[
        'pyyaml',
        'numpy',
      ],
      zip_safe=False)
