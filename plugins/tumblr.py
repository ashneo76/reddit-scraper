from bs4 import BeautifulSoup
from plugins.base_plugin import *


class Tumblr(BasePlugin):
    def execute(self):
        """Executor for this plugin. The entry function by which any plugin must
        operate to handle links.
        """
        if 'tumblr.com' in self.candidate.url.lower():
            img_urls = self.get_tumblr_imgs(self.candidate.url)
            for img_url in img_urls:
                self.current = Download(self.candidate.title,
                                        self.candidate.subreddit,
                                        img_url)

    def get_tumblr_imgs(self, url):
        try:
            resp = requests.get(url)
        except requests.HTTPError, e:
            print 'Error contacting tumblr (%s):' % url
            print e
            return []
        root = BeautifulSoup(resp.text)
        imgs = []

        for iframe in root.find_all('iframe', {'class': 'photoset'}):
            src = iframe.attrs.get('src')

            try:
                resp = requests.get(src)
            except requests.HTTPError, e:
                print 'Error contacting tumblr (%s):' % url
                print e
                return []
            root = BeautifulSoup(resp.text)

            for img in root.find_all({'class': 'photoset_photo'}):
                imgs.append(img.attrs.get('href'))
        return imgs