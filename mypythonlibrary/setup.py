from setuptools import find_packages, setup

setup(
  name = 'monitorlib',
  packages = find_packages(include=['monitorlib']),
  version = '0.1.26',
  description = 'Library for Monitor0',
  author = 'JMBR',
  license = 'MIT',
  install_requires = ['pandas'],
  setup_requires = ['pytest-runner'],
  tests_require = ['pytest'],
  test_suite = 'tests',
)

