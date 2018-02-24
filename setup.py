from setuptools import setup

setup(
  name = 'greedypacker',
  packages = ['greedypacker'],
  version = '0.4',
  description = 'A two dimensional binpacking library',
  author = 'Solomon Bothwell',
  author_email = 'ssbothwell@gmail.com',
  license = 'Apache2',
  url = 'https://github.com/ssbothwell/BinPack',
  install_requires = [ 'sortedcontainers'],
  download_url = 'https://github.com/ssbothwell/greedypacker/archive/v0.4.tar.gz',
  keywords = ['binpacking', 'algorithm', 'greedy', 'library'],
  classifiers = [],
  python_requires='>=3',
)
