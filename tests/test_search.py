# coding=utf8
import json
import re
import unittest

from acestream_search.acestream_search import main, get_options

channel = 'НТВ'
m3u_re = re.compile('#EXTM3U#EXTINF:-1,[0-9]+\\. ' + channel +
                    '.*\n.*/ace/getstream\\?infohash=[0-9a-f]+')


def probe(args):
    out = ''
    for page in main(args):
        for chunk in page:
            out += chunk
    return out


class TestQuery(unittest.TestCase):
    def test_query(self):
        opts = {'query': channel}
        args = get_options(opts)
        self.assertIsNotNone(m3u_re.match(probe(args)))

    def test_name(self):
        opts = {'query': channel}
        opts['name'] = [channel]
        args = get_options(opts)
        self.assertIsNotNone(m3u_re.match(probe(args)))

    def test_group(self):
        opts = {'query': channel}
        opts['group_by_channels'] = 1
        args = get_options(opts)
        self.assertIsNotNone(m3u_re.match(probe(args)))

    def test_epg(self):
        opts = {'query': channel}
        opts['name'] = [channel]
        opts['show_epg'] = 1
        args = get_options(opts)
        self.assertIsNotNone(re.match('#EXTM3U#EXTINF:-1 tvg-id="[0-9]+",[0-9]+\\. ' + channel +
                             '.*\n.*/ace/getstream\\?infohash=[0-9a-f]+',
                                      probe(args)))

    def test_xml(self):
        opts = {'query': channel}
        opts['xml_epg'] = 1
        args = get_options(opts)
        self.assertIsNotNone(re.search(' +<channel id="[0-9]+">\n +<display-name lang="ru">'
                             + channel, probe(args)))

    def test_json(self):
        opts = {'query': channel}
        opts['json'] = 1
        args = get_options(opts)
        item = json.loads(probe(args))[0]['items'][0]
        self.assertTrue(channel in item['name'] and
                        re.match('[0-9a-f]+', item['infohash']))
