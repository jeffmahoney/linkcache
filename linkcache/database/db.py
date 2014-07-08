class LinkDb:
    def __init__(self, config):
        assert type(config) is dict

    def update(self, id, field, value):
        pass

    def set_title(self, id, title):
        self.update(id, 'title', title)

    def clear_title(self, id):
        self.set_title(id, '')

    def set_description(self, id, desc):
        self.update(id, 'description', desc)

    def set_flags(self, id, flags):
        self.update(id, 'flags', flags)

    def set_content_type(self, id, content_type):
        self.update(id, 'type', content_type)

    def set_url_alive(self, id, alive=1):
        self.update(id, 'alive', alive)

    def set_url_dead(self, id):
        self.set_url_alive(id, 0)

    def fetch_by_field(self, field, id, channel):
        pass

    def fetch_by_url(self, url, channel=""):
        return self.fetch_by_field("url", url, channel)

    def fetch_by_id(self, id, channel=""):
        return self.fetch_by_field("id", id, channel)

    def fetch_by_shorturl(self, shorturl, channel=""):
        return self.fetch_by_field("id", shorturl, channel)

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
