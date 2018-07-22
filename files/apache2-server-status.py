#!/usr/bin/env python

import argparse
import base64
import json
import urllib2
import sys

# Map of apache worker status use in scoreboard
apache_worker_status_map = {
    '_': 'waiting',
    'S': 'starting',
    'R': 'reading',
    'W': 'sending',
    'K': 'keepalive',
    'D': 'dns',
    'C': 'closing',
    'L': 'logging',
    'G': 'gracefully',
    'I': 'idle',
    '.': 'free'
}

# List of float items to format in json
apache_float_keys = [
    'BytesPerReq', 'ReqPerSec', 'BytesPerSec'
]


class ApacheException(Exception):
    """Basic exception for Apache status communication
    """
    pass


def apacheStatus(request, timeout):
    """Fetch apache status from http url
    """
    try:
        answer = urllib2.urlopen(request, timeout=timeout)
    except (urllib2.HTTPError, urllib2.URLError) as e:
        raise ApacheException(str(e))
    status = answer.read()
    answer.close()
    return status


# RETRIEVE INFORMATIONS
if __name__ == '__main__':
    # Create parser
    parser = argparse.ArgumentParser(description=('Command line utility to query stats '
                                                  'from apache status virtual host'))
    parser.add_argument('-P', '--port', action='store', type=int,
                        dest='port', default=80,
                        help='The port on which to call web endpoint')
    parser.add_argument('-u', '--url', action='store', default='/apache-status',
                        dest='url',
                        help='The url on which to call web endpoint')
    parser.add_argument('-l', '--login', action='store', dest='login',
                        help='optional username')
    parser.add_argument('-p', '--password', action='store', dest='password',
                        help='optional password')
    parser.add_argument('-t', '--timeout', action='store', dest='timeout',
                        default=1, help='timeout in seconds')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                        default=False, help='Enable output of errors')

    args = parser.parse_args()
    if args.verbose:
        print(str(vars(args)))

    content = dict(error=None)

    # prepare request
    url = 'http://localhost:{port}{url}?auto'.format(**vars(args))
    if args.verbose:
        print('call url ' + url)
    request = urllib2.Request(url)
    if hasattr(args, 'username') and hasattr(args, 'password'):
        if args.verbose:
            sys.stdout.write('using basic auth')
        base64string = base64.b64encode('{}:{}'.format(args.username, args.password)).strip()
        request.add_header("Authorization", "Basic {}".format(base64string))

    # execute query for status1
    try:
        status = apacheStatus(request, args.timeout)
    except ApacheException as e:
        content['error'] = str(e)
        print(json.dumps(content))
        sys.exit(1)

    # parse status datas
    if args.verbose:
        print('status:')
        print(status)

    lines = status.splitlines()
    for line in lines:
        parts = line.split(':')
        parts = map(lambda x: x.strip(), parts)
        if len(parts) == 2:
            content[parts[0]] = parts[1]

    # parse scoreboard worker status
    if 'Scoreboard' not in content:
        content['error'] = 'Unable to find Scoreboard item in server status result'
        print(json.dumps(content))
        sys.exit(1)

    scoreboard = content['Scoreboard']
    worker_count_per_status = dict()

    # add up worker per status
    for worker_status in scoreboard:
        if worker_status not in worker_count_per_status:
            worker_count_per_status[worker_status] = 0
        worker_count_per_status[worker_status] += 1

    content['workers'] = dict(map(lambda x: (x, 0), apache_worker_status_map.values()))
    content['workers']['total'] = len(scoreboard)
    for key in worker_count_per_status:
        # handle missing mapping
        if key not in apache_worker_status_map:
            msg = "worker status '{}' is not in mapping".format(key)
            if 'error' in content:
                content['error'] += ',' + msg
            else:
                content['error'] = msg
            continue
        content['workers'][apache_worker_status_map[key]] = worker_count_per_status[key]

    # format float key correctly
    for item in apache_float_keys:
        try:
            content[item] = float(content[item])
        except ValueError:
            msg = "unable to format value '{}' of key {} as float".format(content[item], item)
            if 'error' in content:
                content['error'] += ',' + msg
            else:
                content['error'] = msg
            continue

    # OUTPUT
    print(json.dumps(content))
    sys.exit(0)
