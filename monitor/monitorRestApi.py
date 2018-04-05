#!/usr/bin/env python
# -*- coding: utf- -*-
import os
import sys
from monitor import Monitor
from optparse import OptionParser
import threading

from flask import Flask, jsonify, make_response, render_template
from flask_cors import CORS

__all__ = []
__version__ = 1.0
__date__ = '2016-11-18'
__updated__ = '2016-11-18'

threads = []
program_name = os.path.basename(sys.argv[0])
program_version = "v1"
program_build_date = "%s" %__updated__

program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)

program_usage = '''monitorRestApi [-d \"logpath.\"]  [-t \"interval.\"] [-i \"ip.\"] [-u \"user.\"] [-p \"password.\"] [-m \"mode.\"] '''

program_longdesc = '''This is a server monitor for CPU, Memory, Disk and support rest api'''
program_license = "Copyright 2016 Ningbo Saturn"

argv = sys.argv[1:]

try:
    # setup option parser
    parser = OptionParser(version=program_version_string, \
                        epilog=program_longdesc, \
                        description=program_license, \
                        usage=program_usage)

    parser.add_option("-d", "--dir", dest="logpath",help="target dir for log file.")
    parser.add_option("-t", "--interval", dest="interval", default=300, help="monitor interval (seconds), default 5m")
    parser.add_option("-l", "--loop", dest="loop", default=True, help="monitor loop mode. default is: True")
    # set defaults
    parser.set_defaults(logpath=os.path.split(os.path.realpath(__file__))[0])

    # process options
    (opts, args) = parser.parse_args(argv)

    monitor = Monitor(log_path=opts.logpath, is_loop=opts.loop, interval=opts.interval)
    threads.append(threading.Thread(target=monitor.start))

except Exception as identifier:
    indent = len(program_name) * " "
    sys.stderr.write(program_name + ": " + repr(identifier) + "\n")
    sys.stderr.write(indent + "  for help use --help")


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/monitor/api/v1.0/system', methods=['GET'])
def get_system():
    return jsonify({'os': monitor.last_status['os']})

@app.route('/monitor/api/v1.0/cpu', methods=['GET'])
def get_cpu():
    return jsonify({'cpu': monitor.last_status['cpu']})

@app.route('/monitor/api/v1.0/disk', methods=['GET'])
def get_disk():
    return jsonify({'disk': monitor.last_status['disk']})

@app.route('/monitor/api/v1.0/network', methods=['GET'])
def get_network():
    return jsonify({'network': monitor.last_status['network']})

@app.route('/monitor/api/v1.0/memory', methods=['GET'])
def get_memory():
    return jsonify({'memory': monitor.last_status['memory']})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Support'}), 404)

def main(argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "v1"
    program_build_date = "%s" %__updated__

    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)

    program_usage = '''monitorRestApi [-d \"logpath.\"]  [-t \"interval.\"] [-i \"ip.\"] [-u \"user.\"] [-p \"password.\"] [-m \"mode.\"] '''

    program_longdesc = '''This is a server monitor for CPU, Memory, Disk and support rest api'''
    program_license = "Copyright 2016 Ningbo Saturn"

    if argv is None:
        argv = sys.argv[1:]

    try:
        # setup option parser
        parser = OptionParser(version=program_version_string, \
                            epilog=program_longdesc, \
                            description=program_license, \
                            usage=program_usage)

        parser.add_option("-d", "--dir", dest="logpath",help="target dir for log file.")
        parser.add_option("-t", "--interval", dest="interval", default=300, help="monitor interval (seconds), default 5m")
        parser.add_option("-l", "--loop", dest="loop", default=True, help="monitor loop mode. default is: True")
        # set defaults
        parser.set_defaults(logpath=os.path.split(os.path.realpath(__file__))[0])

        # process options
        (opts, args) = parser.parse_args(argv)

        monitor = Monitor(log_path=opts.logpath, is_loop=opts.loop, interval=opts.interval)
        threads.append(threading.Thread(target=monitor.start))

    except Exception as identifier:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(identifier) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return False

if __name__ == '__main__':
    try:
        main()
        for t in threads:
            t.setDaemon(True)
            t.start()
        app.run(debug=True,host='0.0.0.0')
    except Exception as identifier:
        for t in threads:
            t.stop()

        