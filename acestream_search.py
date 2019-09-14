#!/usr/bin/env python

import json
import sys
from itertools import count
from datetime import datetime, timedelta
import argparse
import xml.etree.ElementTree as ET
from xml.dom import minidom

if sys.version_info[0] > 2:
    from urllib.request import urlopen, quote

    def u_code(string):
        return string
else:
    from urllib import urlopen, quote

    def u_code(string):
        return string.encode("utf8")

top = ET.Element('tv')


def default_after():
    age = timedelta(days=7)
    now = datetime.now()
    return datetime.strftime(now - age, "%Y-%m-%d %H:%M:%S")


def time_point(point):
    epoch = "1970-01-01 03:00:00"
    isof = "%Y-%m-%d %H:%M:%S"
    epoch = datetime.strptime(epoch, isof)
    try:
        point = datetime.strptime(point, isof)
    except ValueError:
        print("Use 'Y-m-d H:M:S' date time format, for example \"" +
              datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S") +
              '\"')
        exit()
    else:
        return int((point - epoch).total_seconds())


def get_options():
    global args
    parser = argparse.ArgumentParser(
        description="Produce acestream m3u playlist, xml epg or json data.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-q", "--quiet", action="store_false",
                        help="increase output quiet.")
    parser.add_argument("query", nargs='?', type=str, default='',
                        help="Pattern to search tv channels.")
    parser.add_argument("-n", "--name", nargs='+', type=str,
                        help="Exact tv channels to search for, \
                        doesn't effect json output.")
    parser.add_argument("-c", "--category", type=str, default='',
                        help="filter by category.")
    parser.add_argument("-p", "--proxy", type=str, default='localhost:6878',
                        help="proxy host:port to conntect to engine api.")
    parser.add_argument("-t", "--target", type=str, default='localhost:6878',
                        help="target host:port to conntect to engine hls.")
    parser.add_argument("-s", "--page_size", type=int, default=200,
                        help="page size (max 200).")
    parser.add_argument("-g", "--group_by_channels", default=0,
                        action="store_const", const=1,
                        help="group output results by channel.")
    parser.add_argument("-e", "--show_epg", default=0, action="store_const", const=1,
                        help="include EPG in the response.")
    parser.add_argument("-j", "--json", action="store_true",
                        help="json output.")
    parser.add_argument("-x", "--xml_epg", action="store_true",
                        help="make XML EPG.")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="debug mode.")
    parser.add_argument("-a", "--after", type=str, default=default_after(),
                        help="availability updated at.")
    if __name__ == '__main__':
        opts = parser.parse_args()
    else:
        opts = parser.parse_known_args()[0]
    opts.after = time_point(opts.after)
    if opts.show_epg:
        opts.group_by_channels = 1
    if opts.xml_epg:
        opts.show_epg = 1
        opts.group_by_channels = 1
    opts.man = parser.format_help()
    return opts


args = get_options()


def endpoint():
    return 'http://' + args.proxy + '/server/api'


def get_token():
    query = 'method=get_api_access_token'
    try:
        body = urlopen(endpoint() + '?' + query).read().decode()
    except IOError:
        print('Couldn\'t connect to ' + endpoint())
        if args.debug:
            raise
        exit()
    else:
        try:
            response = json.loads(body)
        except ValueError:
            print('Couldn\'t get token from ' + endpoint() + '?' + query)
            if args.debug:
                print(body)
            exit()
        else:
            return response['result']['token']


def build_query(page):
    return 'token=' + get_token() + \
           '&method=search&page=' + str(page) + \
           '&query=' + quote(args.query) + \
           '&category=' + quote(args.category) + \
           '&page_size=' + str(args.page_size) + \
           '&group_by_channels=' + str(args.group_by_channels) + \
           '&show_epg=' + str(args.show_epg)


def fetch_page(query):
    url = endpoint() + '?' + query
    return json.loads(urlopen(url).read().decode('utf8'), encoding='utf8')


def make_playlist(item):
    if item['availability_updated_at'] >= args.after \
            and (not args.name or u_code(item['name']) in args.name):
        title = '#EXTINF:-1'
        if args.show_epg and 'channel_id' in item:
            title += ' tvg-id="' + str(item['channel_id']) + '"'
        title += ',' + item['name']
        if args.quiet:
            if 'categories' in item:
                # title += " " + item['categories'][0]
                categories = ''
                for kind in item['categories']:
                    categories += " " + kind
                    if item['categories'].index(kind) > 0:
                        categories = "," + categories
                title += " [" + categories + " ]"

            dt = datetime.fromtimestamp(item['availability_updated_at'])
            title += " " + dt.isoformat(sep=' ')
            title += " a=" + str(item['availability'])
            if 'bitrate' in item:
                title += " b=" + str(item['bitrate'])
        print(u_code(title))
        print('http://' + args.target + '/ace/manifest.m3u8?infohash=' +
              item['infohash'])


def make_epg(group):
    if 'epg' in group and (not args.name or u_code(group['name']) in args.name):
        start = datetime.fromtimestamp(
            int(group['epg']['start'])).strftime("%Y%m%d%H%M%S")
        stop = datetime.fromtimestamp(
            int(group['epg']['stop'])).strftime("%Y%m%d%H%M%S")
        channel_id = str(group['items'][0]['channel_id'])
        channel = ET.SubElement(top, 'channel')
        channel.set('id', channel_id)
        display = ET.SubElement(channel, 'display-name')
        display.set('lang', 'ru')
        display.text = group['name']
        if 'icon' in group:
            icon = ET.SubElement(channel, 'icon')
            icon.set('src', group['icon'])
        programme = ET.SubElement(top, 'programme')
        programme.set('start', start + " +0300")
        programme.set('stop', stop + " +0300")
        programme.set('channel', channel_id)
        title = ET.SubElement(programme, 'title')
        title.set('lang', 'ru')
        title.text = group['epg']['name']
        if 'description' in group['epg']:
            desc = ET.SubElement(programme, 'desc')
            desc.set('lang', 'ru')
            desc.text = group['epg']['description']


def get_channels():
    page = count()
    channels = []
    while True:
        query = build_query(next(page))
        chunk = fetch_page(query)['result']['results']
        channels += chunk
        if len(chunk) == 0 or not args.group_by_channels and chunk[
                len(chunk)-1]['availability_updated_at'] < args.after:
            break
    return channels


def pretty_xml(top):
    xmlstr = ET.tostring(top)
    xmldoc = minidom.parseString(xmlstr)
    return xmldoc.toprettyxml(indent="    ")


def main():
    channels = get_channels()
    if args.json:
        print(u_code(json.dumps(channels, ensure_ascii=False, indent=4)))
    elif args.xml_epg:
        for group in channels:
            make_epg(group)
        print(u_code(pretty_xml(top)))
    else:
        if args.group_by_channels:
            for group in channels:
                for item in group['items']:
                    make_playlist(item)
        else:
            for item in channels:
                make_playlist(item)


if __name__ == '__main__':
    main()
