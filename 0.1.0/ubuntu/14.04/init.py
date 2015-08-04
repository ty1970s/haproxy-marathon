#!/usr/bin/python -u

"""Generate HAProxy configuration (using Marathon as a data source)"""

import json
import logging
import os
import re
import subprocess
import sys
import time

import jinja2
import kazoo.client


def main():

    logging.basicConfig()

    zk = kazoo.client.KazooClient(hosts=os.getenv('ZK', 'localhost:2181'), read_only=True)
    zk.start()

    #
    zk.ensure_path("/haproxy")
    try:
        zk.create("/haproxy/config", "")
    except kazoo.exceptions.NodeExistsError:
        pass

    #
    marathon = os.getenv('MARATHON', '127.0.0.1:8080')

    while True:
        apps = []

        p = subprocess.Popen(["curl", "-fsS", "http://%s/v2/apps" % marathon], stdout=subprocess.PIPE)
        assert p.wait() == 0

        appIds = [app['id'] for app in json.load(p.stdout)['apps']]

        for appId in appIds:
            p = subprocess.Popen(["curl", "-fsS", "http://%s/v2/apps%s" % (marathon, appId)], stdout=subprocess.PIPE)
            assert p.wait() == 0

            app = json.load(p.stdout)['app']

            if not 'portMappings' in app['container']['docker']:
                continue

            apps.append(app)

        #
        def regex_replace(string, pattern, repl):
            return re.sub(pattern, repl, string)

        environment = jinja2.Environment()
        environment.filters['regex_replace'] = regex_replace

        with open('/haproxy.cfg.j2') as f:
            x = f.read()
        template = environment.from_string(x)

        haproxy_cfg = template.render(apps=apps)
        haproxy_cfg = re.sub(r'\n{2,}', '\n\n', haproxy_cfg).rstrip() + '\n'

        data, stat = zk.get("/haproxy/config")

        if haproxy_cfg != data:
            print >>sys.stderr, "set"
            zk.set("/haproxy/config", haproxy_cfg.encode('utf-8'))
        time.sleep(10)


if __name__ == '__main__':
    main()
