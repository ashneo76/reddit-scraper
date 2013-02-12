from distutils.core import setup

setup(
    name='reddit-scraper',
    version='1.1',
    requires=['pillow>=1.7.8', 'lxml>=3.0.2'],
    url='https://github.com/oscillot/reddit-scraper',
    license='GPL2',
    author='Oscillot',
    author_email='oscillot@trioptimum.com',
    description='Automatically download upvoted wallpapers using cron or jenkins'
)
