#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urlparse


class Url:

    @staticmethod
    def url_parse(url):
        return urlparse.urlparse(url)

    @staticmethod
    def url_unparse(data):
        scheme, netloc, url, params, query, fragment = data
        if params:
            url = "%s;%s" % (url, params)
        return urlparse.urlunsplit((scheme, netloc, url, query, fragment))

    @staticmethod
    def qs_parse(qs):
        return dict(urlparse.parse_qsl(qs, keep_blank_values=True))

    @staticmethod
    def build_qs(qs):
        return urllib.urlencode(qs)

    @staticmethod
    def urldecode(qs):
        return urllib.unquote(qs)

    @staticmethod
    def urlencode(qs):
        return urllib.quote(qs)
