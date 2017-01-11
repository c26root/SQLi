#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import requests


class SQLMapApi:

    """SQLMAP API"""

    def __init__(self, host, port, admin_id='', timeout=2):
        self.host = host
        self.port = port
        self.url = 'http://{}:{}'.format(host, int(port))
        self.timeout = timeout
        self.admin_id = admin_id
        self.headers = {
            'Content-Type': 'application/json',
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
        }
        if not self.admin_id:
            print 'admin_id error or empty'
            exit()

    def get_info(self):
        """ api host port url info
        {
          "url": "http://localhost:8775", 
          "host": "localhost", 
          "port": 8775
        }

        """
        return json.dumps({'host': self.host, 'port': self.port, 'url': self.url}, indent=2)

    def admin_list(self):
        """
        List task pull
        """
        url = '{}/admin/{}/list'.format(self.url, self.admin_id)
        try:
            r = self.http_get(url)
            return r.json()
        except Exception as e:
            print str(e)
            return {}

    def admin_flush(self):
        """
        Flush task spool (delete all tasks)
        """
        url = '{}/admin/{}/flush'.format(self.url, self.admin_id)
        try:
            r = self.http_get(url)
            return r.json()
        except Exception as e:
            print str(e)
            return {}

    def task_new(self):
        url = '{}/task/new'.format(self.url)
        try:
            r = self.http_get(url)
            return r.json().get('taskid')
        except Exception as e:
            print str(e)
            return {}

    def task_delete(self, taskid):
        url = '{}/task/{}/delete'.format(self.url, taskid)
        try:
            r = self.http_get(url)
            return r.json()
        except Exception as e:
            print str(e)
            return {}

    def option_list(self, taskid):
        """
        List options for a certain task ID
        """
        url = '{}/option/{}/list'.format(self.url, taskid)
        try:
            r = self.http_get(url)
            return r.json()
        except Exception as e:
            print str(e)
            return {}

    def option_get(self, taskid):
        """
        Get the value of an option (command line switch) for a certain task ID
        """
        url = '{}/option/{}/get'.format(self.url, taskid)
        try:
            r = self.http_post(url)
            return r.json()
        except Exception as e:
            print str(e)
            return {}

    def option_set(self, taskid, options={}):
        """
        Set an option (command line switch) for a certain task ID
        """
        url = '{}/option/{}/set'.format(self.url, taskid)
        try:
            r = self.http_post(url, json=options)
            return r.json()
        except Exception as e:
            print str(e)
            return {}

    def scan_start(self, taskid, options={}):
        """
        Launch a scan
        """
        url = '{}/scan/{}/start'.format(self.url, taskid)
        try:
            r = self.http_post(url, json=options)
            return r.json()
        except Exception as e:
            print str(e)
            return {}

    def scan_stop(self, taskid):
        """
        Stop a scan
        """
        url = '{}/scan/{}/stop'.format(self.url, taskid)
        try:
            r = self.http_get(url)
            return r.json()
        except Exception as e:
            print str(e)
            return {}

    def scan_kill(self, taskid):
        """
        Kill a scan
        """
        url = '{}/scan/{}/kill'.format(self.url, taskid)
        try:
            r = self.http_get(url)
            return r.json()
        except Exception as e:
            print str(e)
            return {}
            return {}

    def scan_status(self, taskid):
        """
        Returns status of a scan
        """
        url = '{}/scan/{}/status'.format(self.url, taskid)
        try:
            r = self.http_get(url)
            return r.json()
        except Exception as e:
            print str(e)
            return {}

    def scan_data(self, taskid):
        """
        Retrieve the data of a scan
        """
        url = '{}/scan/{}/data'.format(self.url, taskid)
        try:
            r = self.http_get(url)
            return r.json()
        except Exception as e:
            print str(e)
            return {}

    def scan_log_limit(self, taskid, start, end):
        """
        Retrieve a subset of log messages
        """
        pass

    def scan_log(self, taksid):
        """
        Retrieve the log messages
        """
        url = '{}/scan/{}/log'.format(self.url, taskid)
        try:
            r = self.http_get(url)
            return r.json()
        except Exception as e:
            print str(e)
            return {}

    def download(self, taskid):
        """
        Download a certain file from the file system
        """
        pass

    """HTTP GET"""

    def http_get(self, url, params={}, headers={}):
        headers = headers or self.headers
        try:
            print '[GET]', url
            r = requests.get(
                url, params=params, headers=headers, timeout=self.timeout)
            return r
        except Exception as e:
            print '[ERROR]', str(e)
            return requests.Request()
        finally:
            print

    """HTTP POST"""

    def http_post(self, url, params={}, data={}, json={}, headers={}):
        headers = headers or self.headers
        try:
            print '[POST]', url
            r = requests.post(
                url, params=params, data=data, json=json, headers=headers, timeout=self.timeout)
            return r
        except Exception as e:
            print '[ERROR]', str(e)
            return requests.Request()
        finally:
            print

if __name__ == '__main__':
    pass
    # api = SQLMapApi(host, port)
