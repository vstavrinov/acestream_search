import unittest
import sys
if sys.version_info[0] > 2:
    from io import StringIO
    from acestream_search.acestream_search import main
else:
    from cStringIO import StringIO
    from acestream_search import main

channel = 'Amedia'


def probe(test):
    stdout = sys.stdout
    stream = StringIO()
    sys.stdout = stream
    main(test)
    sys.stdout = stdout
    return stream.getvalue()


class TestQuery(unittest.TestCase):
    def test_query(self):
        test = {'query': channel}
        self.assertIn('#EXTINF', probe(test))


class TestEPG(unittest.TestCase):
    def test_epg(self):
        test = {'query': channel, 'group_by_channels': 1, 'show_epg': 1}
        self.assertIn(' tvg-id="', probe(test))


class TestXML(unittest.TestCase):
    def test_xml(self):
        test = {'query': channel, 'xml_epg': 1, 'group_by_channels': 1, 'show_epg': 1}
        self.assertIn('<channel id="', probe(test))


class TestJson(unittest.TestCase):
    def test_json(self):
        test = {'query': channel, 'json': True}
        self.assertIn('"name": "' + channel, probe(test))
