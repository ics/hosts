#!venv/bin/python

import argparse
import urllib.request

BAD = (
    'http://winhelp2002.mvps.org/hosts.txt',
    'http://someonewhocares.org/hosts/hosts',
    'http://www.malwaredomainlist.com/hostslist/hosts.txt',
    'http://www.hostsfile.org/Downloads/hosts.txt'
)
ADS = (
    'http://adaway.org/hosts.txt',
    'http://hosts-file.net/ad_servers.txt',
    'http://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext',
    'http://adblock.gjtech.net/?format=unix-hosts',
    'https://jansal.googlecode.com/svn/trunk/adblock/hosts'
)


def uniquify(seq):
    keys = {}
    for e in seq:
        keys[e] = 1
    return keys.keys()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='HOSTS',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-o', '--output', dest='output', default='hosts'
    )
    parser.add_argument('--ads', dest='ads', action='store_true')
    parser.set_defaults(ads=False)

    args = parser.parse_args()

    if args.ads is True:
        BAD += ADS

    entries = []
    for line in BAD:
        print('[+] Downloading ' + line)
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10')]
        try:
            entries += opener.open(line).readlines()
        except IOError as e:
            print('[-]' + str(e))

    with open(args.output, mode='wt', encoding='utf-8') as out:
        print('[+] Writing new file...')
        out.write('\n'.join(uniquify(l.decode('utf-8').strip() for l in entries
                                   if not l.decode('utf-8').startswith('#'))))
