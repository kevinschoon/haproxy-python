__author__ = 'kevinschoon@gmail.com'
"""
This tool parses the "keyword" sections copied from HAProxy's configuration file....it is a far from an ideal solution.
"""

# TODO: Import configuration keys programmatically.

import re

global_config = {
    '1.5': """
     * Process management and security
   - ca-base
   - chroot
   - crt-base
   - daemon
   - gid
   - group
   - log
   - log-send-hostname
   - nbproc
   - pidfile
   - uid
   - ulimit-n
   - user
   - stats
   - ssl-server-verify
   - node
   - description
   - unix-bind

 * Performance tuning
   - max-spread-checks
   - maxconn
   - maxconnrate
   - maxcomprate
   - maxcompcpuusage
   - maxpipes
   - maxsessrate
   - maxsslconn
   - maxsslrate
   - noepoll
   - nokqueue
   - nopoll
   - nosplice
   - nogetaddrinfo
   - spread-checks
   - tune.bufsize
   - tune.chksize
   - tune.comp.maxlevel
   - tune.http.cookielen
   - tune.http.maxhdr
   - tune.idletimer
   - tune.maxaccept
   - tune.maxpollevents
   - tune.maxrewrite
   - tune.pipesize
   - tune.rcvbuf.client
   - tune.rcvbuf.server
   - tune.sndbuf.client
   - tune.sndbuf.server
   - tune.ssl.cachesize
   - tune.ssl.lifetime
   - tune.ssl.force-private-cache
   - tune.ssl.maxrecord
   - tune.ssl.default-dh-param
   - tune.zlib.memlevel
   - tune.zlib.windowsize

 * Debugging
   - debug
   - quiet
   """
}


keyword_matrices = {
    '1.5': """
     keyword                              defaults   frontend   listen    backend
------------------------------------+----------+----------+---------+---------
acl                                       -          X         X         X
appsession                                -          -         X         X
backlog                                   X          X         X         -
balance                                   X          -         X         X
bind                                      -          X         X         -
bind-process                              X          X         X         X
block                                     -          X         X         X
capture cookie                            -          X         X         -
capture request header                    -          X         X         -
capture response header                   -          X         X         -
clitimeout                  (deprecated)  X          X         X         -
compression                               X          X         X         X
contimeout                  (deprecated)  X          -         X         X
cookie                                    X          -         X         X
default-server                            X          -         X         X
default_backend                           X          X         X         -
description                               -          X         X         X
disabled                                  X          X         X         X
dispatch                                  -          -         X         X
enabled                                   X          X         X         X
errorfile                                 X          X         X         X
errorloc                                  X          X         X         X
errorloc302                               X          X         X         X
-- keyword -------------------------- defaults - frontend - listen -- backend -
errorloc303                               X          X         X         X
force-persist                             -          X         X         X
fullconn                                  X          -         X         X
grace                                     X          X         X         X
hash-type                                 X          -         X         X
http-check disable-on-404                 X          -         X         X
http-check expect                         -          -         X         X
http-check send-state                     X          -         X         X
http-request                              -          X         X         X
http-response                             -          X         X         X
http-send-name-header                     -          -         X         X
id                                        -          X         X         X
ignore-persist                            -          X         X         X
log                                  (*)  X          X         X         X
log-format                                X          X         X         -
max-keep-alive-queue                      X          -         X         X
maxconn                                   X          X         X         -
mode                                      X          X         X         X
monitor fail                              -          X         X         -
monitor-net                               X          X         X         -
monitor-uri                               X          X         X         -
option abortonclose                  (*)  X          -         X         X
option accept-invalid-http-request   (*)  X          X         X         -
option accept-invalid-http-response  (*)  X          -         X         X
option allbackups                    (*)  X          -         X         X
option checkcache                    (*)  X          -         X         X
option clitcpka                      (*)  X          X         X         -
option contstats                     (*)  X          X         X         -
option dontlog-normal                (*)  X          X         X         -
option dontlognull                   (*)  X          X         X         -
option forceclose                    (*)  X          X         X         X
-- keyword -------------------------- defaults - frontend - listen -- backend -
option forwardfor                         X          X         X         X
option http-ignore-probes            (*)  X          X         X         -
option http-keep-alive               (*)  X          X         X         X
option http-no-delay                 (*)  X          X         X         X
option http-pretend-keepalive        (*)  X          X         X         X
option http-server-close             (*)  X          X         X         X
option http-tunnel                   (*)  X          X         X         X
option http-use-proxy-header         (*)  X          X         X         -
option httpchk                            X          -         X         X
option httpclose                     (*)  X          X         X         X
option httplog                            X          X         X         X
option http_proxy                    (*)  X          X         X         X
option independent-streams           (*)  X          X         X         X
option ldap-check                         X          -         X         X
option log-health-checks             (*)  X          -         X         X
option log-separate-errors           (*)  X          X         X         -
option logasap                       (*)  X          X         X         -
option mysql-check                        X          -         X         X
option pgsql-check                        X          -         X         X
option nolinger                      (*)  X          X         X         X
option originalto                         X          X         X         X
option persist                       (*)  X          -         X         X
option redispatch                    (*)  X          -         X         X
option redis-check                        X          -         X         X
option smtpchk                            X          -         X         X
option socket-stats                  (*)  X          X         X         -
option splice-auto                   (*)  X          X         X         X
option splice-request                (*)  X          X         X         X
option splice-response               (*)  X          X         X         X
option srvtcpka                      (*)  X          -         X         X
option ssl-hello-chk                      X          -         X         X
-- keyword -------------------------- defaults - frontend - listen -- backend -
option tcp-check                          X          -         X         X
option tcp-smart-accept              (*)  X          X         X         -
option tcp-smart-connect             (*)  X          -         X         X
option tcpka                              X          X         X         X
option tcplog                             X          X         X         X
option transparent                   (*)  X          -         X         X
persist rdp-cookie                        X          -         X         X
rate-limit sessions                       X          X         X         -
redirect                                  -          X         X         X
redisp                      (deprecated)  X          -         X         X
redispatch                  (deprecated)  X          -         X         X
reqadd                                    -          X         X         X
reqallow                                  -          X         X         X
reqdel                                    -          X         X         X
reqdeny                                   -          X         X         X
reqiallow                                 -          X         X         X
reqidel                                   -          X         X         X
reqideny                                  -          X         X         X
reqipass                                  -          X         X         X
reqirep                                   -          X         X         X
reqisetbe                                 -          X         X         X
reqitarpit                                -          X         X         X
reqpass                                   -          X         X         X
reqrep                                    -          X         X         X
-- keyword -------------------------- defaults - frontend - listen -- backend -
reqsetbe                                  -          X         X         X
reqtarpit                                 -          X         X         X
retries                                   X          -         X         X
rspadd                                    -          X         X         X
rspdel                                    -          X         X         X
rspdeny                                   -          X         X         X
rspidel                                   -          X         X         X
rspideny                                  -          X         X         X
rspirep                                   -          X         X         X
rsprep                                    -          X         X         X
server                                    -          -         X         X
source                                    X          -         X         X
srvtimeout                  (deprecated)  X          -         X         X
stats admin                               -          -         X         X
stats auth                                X          -         X         X
stats enable                              X          -         X         X
stats hide-version                        X          -         X         X
stats http-request                        -          -         X         X
stats realm                               X          -         X         X
stats refresh                             X          -         X         X
stats scope                               X          -         X         X
stats show-desc                           X          -         X         X
stats show-legends                        X          -         X         X
stats show-node                           X          -         X         X
stats uri                                 X          -         X         X
-- keyword -------------------------- defaults - frontend - listen -- backend -
stick match                               -          -         X         X
stick on                                  -          -         X         X
stick store-request                       -          -         X         X
stick store-response                      -          -         X         X
stick-table                               -          -         X         X
tcp-check connect                         -          -         X         X
tcp-check expect                          -          -         X         X
tcp-check send                            -          -         X         X
tcp-check send-binary                     -          -         X         X
tcp-request connection                    -          X         X         -
tcp-request content                       -          X         X         X
tcp-request inspect-delay                 -          X         X         X
tcp-response content                      -          -         X         X
tcp-response inspect-delay                -          -         X         X
timeout check                             X          -         X         X
timeout client                            X          X         X         -
timeout client-fin                        X          X         X         -
timeout clitimeout          (deprecated)  X          X         X         -
timeout connect                           X          -         X         X
timeout contimeout          (deprecated)  X          -         X         X
timeout http-keep-alive                   X          X         X         X
timeout http-request                      X          X         X         X
timeout queue                             X          -         X         X
timeout server                            X          -         X         X
timeout server-fin                        X          -         X         X
timeout srvtimeout          (deprecated)  X          -         X         X
timeout tarpit                            X          X         X         X
timeout tunnel                            X          -         X         X
transparent                 (deprecated)  X          -         X         X
unique-id-format                          X          X         X         -
unique-id-header                          X          X         X         -
use_backend                               -          X         X         -
use-server                                -          -         X         X
------------------------------------+----------+----------+---------+---------
 keyword                              defaults   frontend   listen    backend
"""
}


def get_config_options(key):
    global_pattern = r'\s*-\s(?P<keyword>.[a-z][a-z0-9\-\+\_\.]*)'
    keyword_pattern = r'^(%s%s)(%s)' % (
        '([a-z][a-z0-9\-\+_\.]*[a-z0-9\-\+_)])',  # keyword
        '( [a-z0-9\-_]+)*',                  # subkeywords
        '(\([^ ]*\))?'
    )  # Thanks https://github.com/cbonte/haproxy-dconv/blob/master/parser/keyword.py#L8-L12
    keyword_section_pattern = r'(?P<defaults>[X-])\s*(?P<frontend>[X-])\s*(?P<listen>[X-])\s*(?P<backend>[X-])$'
    keyword_sections = ['defaults', 'listen', 'frontend', 'backend']
    config = dict()

    for line in keyword_matrices[key].split('\n'):
        keyword_match = re.match(keyword_pattern, line)
        section_match = re.search(keyword_section_pattern, line)
        for section in keyword_sections:
            if section not in config:
                config[section] = list()
            if section_match:
                if section_match.groupdict()[section] == 'X':
                    if keyword_match:
                        config[section].append(keyword_match.group(0))

    for line in global_config[key].split('\n'):
        key_match = re.match(global_pattern, line)
        if key_match:
            if 'global' not in config:
                config['global'] = list()
            config['global'].append(key_match.groupdict()['keyword'])

    return config
