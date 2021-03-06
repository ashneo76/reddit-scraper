#Handles getting a single imgur image that isn't a direct link but rather a
# link to its imgur page

#works as of 09-30-13
from bs4 import BeautifulSoup
from plugins.base_plugin import *


class ImgurSingleIndirect(BasePlugin):
    def execute(self):
        """Executor for this plugin. The entry function by which any plugin must
        operate to handle links.
        """
        #prevent this plugin from handling links such as the following:
        #http://i.imgur.com/nbsQ4SF.jpg#.UTtRkqYGmy0.reddit
        if (self.candidate.url.lower().startswith('http://imgur.com/')
            and not self.candidate.url.split('#')[0].lower().startswith(
            'http://imgur.com/a/') and not self.candidate.url.lower()[-4:] in
                ['.jpg', '.bmp', '.png', '.gif']) or \
                (self.candidate.url.lower().startswith('http://i.imgur.com/')
                 and not self.candidate.url.lower()[-4:] in ['.jpg', '.bmp',
                                                             '.png', '.gif']):
            img_url = self.get_imgur_single(self.candidate.url)
            if img_url is not None:
                self.current = Download(self.candidate.title,
                                        self.candidate.subreddit,
                                        img_url)

    def get_imgur_single(self, url):
        """Helper for the imgur single image page function

        :param str url: a url to retrieve and execute the xpath on
        :rtype str: a url that is a direct link to an image
        """
        try:
            resp = requests.get(url)
        except requests.HTTPError, e:
            print 'Error contacting imgur (%s):' % url
            print e
            return []
        root = BeautifulSoup(resp.text)
        al = root.find('head').find_all('link')
        for a in al:
            href = a.attrs.get('href')
            if url.lstrip('http://') in href:
                #Fix The single indirect links that look like this:
                #<link rel="image_src" href="//i.imgur.com/IZZayKa.png" />
                if not href.startswith('http://'):
                    if href.startswith('//'):
                        href = 'http:' + href
                return href