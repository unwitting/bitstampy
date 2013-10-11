from setuptools import setup

setup(
	name = u'bitstampy',
	version = u'0.0.1',
	author = u'https://github.com/unwitting',
	author_email = u'jackprestonuk@gmail.com',
	packages = [u'bitstampy'],
	scripts = [u'bin/api_runthrough.py'],
	url = u'https://github.com/unwitting/bitstampy',
	license = u'LICENSE.txt',
	description = u'Bitstamp API wrapper for Python',
	long_description = open('README.txt').read(),
	classifiers = [
		u'Development Status :: 3 - Alpha',
		u'Intended Audience :: Developers',
		u'License :: OSI Approved :: MIT License',
		u'Natural Language :: English',
		u'Operating System :: OS Independent',
		u'Programming Language :: Python :: 2',
		u'Topic :: Internet :: WWW/HTTP'
	],
	install_requires = [u'requests']
)
