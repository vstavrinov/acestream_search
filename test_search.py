# coding=utf8
import sys
import json
import re
import unittest
from . import acestream_search
channel = 'НТВ'
if sys.version_info[0] > 2:
    def u_code(string):
        return string
else:
    def u_code(string):
        return string.encode("utf8")


def probe(args):
    for chunk in acestream_search.main(acestream_search.args):
        return chunk


class TestQuery(unittest.TestCase):
    def test_query(self):
        acestream_search.args = acestream_search.get_options()
        acestream_search.args.query = channel
        re.match('#EXTINF:-1,' + channel +
                 '.*\n.*/ace/manifest.m3u8\\?infohash=[0-9a-f]+',
                 probe(acestream_search.args))

    def test_epg(self):
        acestream_search.args = acestream_search.get_options()
        acestream_search.args.query = channel
        acestream_search.args.show_epg = 1
        acestream_search.args.group_by_channels = 1
        re.match('#EXTINF:-1 tvg-id="[0-9]+",' + channel +
                 '.*\n.*/ace/manifest.m3u8\\?infohash=[0-9a-f]+',
                 probe(acestream_search.args))

    def test_xml(self):
        acestream_search.args = acestream_search.get_options()
        acestream_search.args.query = channel
        acestream_search.args.xml_epg = 1
        acestream_search.args.show_epg = 1
        acestream_search.args.group_by_channels = 1
        re.match(' +<channel id="[0-9]+">\\n +<display-name lang="ru">'
                 + channel, probe(acestream_search.args))

    def test_json(self):
        acestream_search.args = acestream_search.get_options()
        acestream_search.args.query = channel
        acestream_search.args.json = 1
        item = json.loads(probe(acestream_search.args), encoding='utf8')[0]
        self.assertTrue(channel in u_code(item['name']) and
                        re.match('[0-9a-f]+', item['infohash']))

    def test_name(self):
        acestream_search.args = acestream_search.get_options()
        acestream_search.args.name = channel
        re.match('#EXTINF:-1,' + '"' + channel + '"' +
                 '.*\n.*/ace/manifest.m3u8\\?infohash=[0-9a-f]+',
                 probe(acestream_search.args))
