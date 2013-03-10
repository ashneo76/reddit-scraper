#works as of 03-10-13
from base_plugin import BasePlugin


class DirectLinks(BasePlugin):
    def execute(self, candidate):
        """Executor for this plugin. The entry function by which any plugin must
        operate to handle links.
        :param dict candidate: data from a reddit post json
        """
        #This helps handle the new imgur links that are direct links but have
        #  some kind of reddit argument e.g.
        # http://i.imgur.com/nbsQ4SF.jpg#.UTtRkqYGmy0.reddit
        if candidate['data']['url'].startswith('http://i.imgur.com') and \
                candidate['data']['url'].endswith('.reddit'):
            candidate['data']['url'] = candidate['data']['url'].split('#')[0]
        for img_type in ['.jpg', '.jpeg', '.gif', '.bmp', '.png']:
            if candidate['data']['url'].lower().rsplit('?')[0].endswith(
                    img_type):
                self.to_acquire.append({'url': candidate['data']['url']
                    .rsplit('?')[0],
                    'subreddit': candidate['data']['subreddit'],
                    'title': candidate['data']['title']})
                self.handled.append(candidate)
                break