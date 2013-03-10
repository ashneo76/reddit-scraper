#Handles getting a single imgur image that isn't a direct link but rather a
# link to its imgur page

#works as of 02-23-13

import urllib
import urllib2
from lxml import etree
from base_plugin import BasePlugin


class ImgurSingleIndirect(BasePlugin):
    def execute(self, candidate):
        """Executor for this plugin. The entry function by which any plugin must
        operate to handle links.
        :param dict candidate: data from a reddit post json
        """
        if (candidate['data']['url'].lower().startswith('http://imgur.com/')
            and not candidate['data']['url'].lower().startswith(
            'http://imgur.com/a/') and not candidate['data']['url'].lower()[
                -4:] in ['.jpg', '.bmp', '.png', '.gif']) or \
                (candidate['data']['url'].lower().startswith('http://i.imgur'
                                                             '.com/') and not
                    candidate['data']['url'].lower()[-4:] in ['.jpg', '.bmp',
                                                              '.png', '.gif']):
            img = self.get_imgur_single(candidate['data']['url'])
            #This handles the links that come down with extensions like
            # `jpg?1` that have been showing up lately. Regular links
            # should be unaffected by this. This is done here so that the
            #  list of handled links is still accurate.
            self.to_acquire.append({'url': img.split('?')[0],
                               'subreddit': candidate['data']['subreddit'],
                               'title': candidate['data']['title']})
            self.handled.append(candidate)

    def get_imgur_single(self, url):
        """Helper for the imgur single image page function

        :param str url: a url to retrieve and execute the xpath on
        :rtype str: a url that is a direct link to an image
        """
        try:
            resp = urllib.urlopen(url)
        except urllib2.HTTPError, e:
            print 'Error contacting imgur (%s):' % url
            print e
            return []
        tree = etree.HTML(resp.read())
        al = tree.findall('.//head/link')
        for a in al:
            href = a.attrib['href']
            if url.lstrip('http://') in href:
                return href