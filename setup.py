from setuptools import setup

setup(
    name='bitstampy',
    version='0.0.9',
    author='https://github.com/unwitting',
    author_email='jackprestonuk@gmail.com',
    packages=['bitstampy'],
    scripts=['bin/api_runthrough.py'],
    url='https://github.com/unwitting/bitstampy',
    license='LICENSE.txt',
    description='Bitstamp API wrapper for Python',
    long_description=open('README.txt').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP'
    ],
    install_requires=['requests']
)
