from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='driverium',
  version='1.0.0',
  description='Python library that provides functionality for managing and downloading ChromeDriver',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/d3kxrma/captchium',
  project_urls={
      "Source": "https://github.com/d3kxrma/captchium"
  },
  author='dekxrma',
  author_email='qqdjnuxez@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='python, selenium, webdriver, chromedriver',
  packages=find_packages(),
  install_requires=['requests', 'chrome-version', 'tqdm'] 
)