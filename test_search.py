# coding=utf8
import unittest
import sys
if sys.version_info[0] > 2:
    from io import StringIO
    from acestream_search import acestream_search
else:
    from cStringIO import StringIO
    import acestream_search

channel = 'НТВ'
acestream_search.args.query = channel


def probe(args):
    stdout = sys.stdout
    stream = StringIO()
    sys.stdout = stream
    acestream_search.main()
    sys.stdout = stdout
    return stream.getvalue()


class TestQuery(unittest.TestCase):
    def test_query(self):
        self.assertIn('#EXTINF', probe(acestream_search.args))


class TestEPG(unittest.TestCase):
    def test_epg(self):
        acestream_search.args.group_by_channels = 1
        acestream_search.args.show_epg = 1
        self.assertIn(' tvg-id="', probe(acestream_search.args))


class TestXML(unittest.TestCase):
    def test_xml(self):
        acestream_search.args.xml_epg = True
        acestream_search.args.group_by_channels = 1
        acestream_search.args.show_epg = 1
        self.assertIn('<channel id="', probe(acestream_search.args))


class TestJson(unittest.TestCase):
    def test_json(self):
        acestream_search.args.json = True
        self.assertIn('"name": "' + channel, probe(acestream_search.args))
