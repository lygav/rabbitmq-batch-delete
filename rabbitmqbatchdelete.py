import re
from sys import argv
import subprocess

rabbit_username = 'simon'
rabbit_password = 'simon'
host = 'myhost'


def get_queues():
    return subprocess.Popen(['rabbitmqadmin', '-u' + rabbit_username, '-p' + rabbit_password, 'list', 'queues', 'name'],
                            stdout=subprocess.PIPE).communicate()[0]


def delete_queue(name):
    return subprocess.Popen(
        ['rabbitmqadmin', '-V' + host, '-u' + rabbit_username, '-p' + rabbit_password, 'delete', 'queue',
         'name=%s' %  name],
        stdout=subprocess.PIPE).communicate()[0]


try:
    pattern = argv.pop(1)
    compiled = re.compile(r"%s.[^\|]+" % pattern, re.MULTILINE)
    queues = get_queues()
    matches = re.findall(compiled, queues)
    if matches:
        for name in matches:
            print 'deleting ' + name
            print "%s %s" % (delete_queue(name.strip(" \r\n")), name)
    else:
        print "No matches found for pattern " + compiled.pattern
except:
    print "please supply pattern"
