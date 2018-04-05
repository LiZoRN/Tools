#!/usr/bin/env python
# -*- coding: utf- -*-
import os
import sys
import platform
import time
from optparse import OptionParser
import logging
import time
from logging.handlers import TimedRotatingFileHandler
import psutil

__all__ = []
__version__ = 1.0
__date__ = '2016-11-18'
__updated__ = '2016-11-18'

class Monitor:
    """Server Monitor"""
    def __init__(self, machine='', user='', password='', is_loop=True, log_path='.', interval=3000):
        self.log_path = os.path.realpath(log_path)
        self.is_loop = is_loop
        self.interval = interval
        self.platform_system = platform.system()
        self.last_status = {}

        LOGGING_DATE_FORMAT	= '%Y-%m-%d %H:%M:%S'
        logging.basicConfig(level=logging.DEBUG, datefmt=LOGGING_DATE_FORMAT)
        self.logger = logging.getLogger('monitor')

        # log file
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)

        #创建TimedRotatingFileHandler对象
        # fh = logging.FileHandler(os.path.join(log_path,'monitor.log'))
        fh = TimedRotatingFileHandler(filename=os.path.join(log_path,'monitor.log'), when="midnight", interval=1, backupCount=2)
        fh.setLevel(logging.DEBUG)
        # log stream
        console = logging.StreamHandler()
        console.setLevel(logging.ERROR)
        # 设置日志格式
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        console.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(console)
        self.logger.debug('System Monitor Start! Looped:%s Interval:%s'%(self.is_loop,self.interval))
    
    def _set_system_info(self,caption,os_architecture,number_of_processes):
        """set last system info"""
        system_info = {}
        system_info['caption'] = caption
        system_info['architecture'] = os_architecture
        system_info['number_of_processes'] = number_of_processes
        self.last_status['os']=system_info

    def _add_cpu_info(self,device_id,device_name,load_percentage):
        """set last cpu info"""
        cpu_info = {}
        cpu_info['device_id'] = device_id
        cpu_info['device_name'] = device_name
        cpu_info['load_percentage'] = load_percentage
        self.last_status['cpu'].append(cpu_info)

    def _add_memory_info(self,total_memory,free_memory):
        """set last memory info"""
        memory_info = {}
        memory_info['total'] = total_memory
        memory_info['free'] = free_memory
        self.last_status['memory'] = memory_info

    def _add_disk_info(self,device, total, free, percent):
        """set last disk info"""
        disk_info = {}
        disk_info['device'] = device
        disk_info['total'] = total
        disk_info['free'] = free
        disk_info['percent'] = percent
        self.last_status['disk'].append(disk_info)

    def _add_network_info(self,ip, net_connects, stats):
        """set last network info"""
        network_info = {}
        network_info['ip'] = ip
        network_info['connects'] = net_connects 
        network_info['stats'] = stats      
        self.last_status['network'].append(network_info)

    def _linux_system(self):
        """get windows operation system info, like version, OS"""
        buff = "\n============system============"
        buff += "\nOS: %s %s" %(platform.uname()[0], platform.machine())
        buff += "\nNumberOfProcesses: %s"%len(psutil.pids())
        self._set_system_info(platform.uname()[0], platform.machine(), len(psutil.pids()))
        return buff

    def operating_system(self):
        """get system info, like version, OS"""
        # self.logger.info("========system========")
        self.last_status['os']=[]
        # if self.platform_system == 'Windows':
        #     return self._win_system()
        # else:
        #     return self._linux_system()

        return self._linux_system()

    def _linux_cpu(self):
        """
            获取linux CPU.
        """
        processor_id = platform.processor()
        processor_name = platform.processor()
        load_percentage = psutil.cpu_percent()
        buff = "\n=============cpu============"

        buff += "\nProcessor ID: %s" % processor_id
        buff += "\nProcess Name: %s" % processor_name
        buff += "\nloadPercentage: %s" % load_percentage
        self._add_cpu_info(processor_id,processor_name,float(load_percentage))
        return buff

    def cpu(self):
        """
            获取CPU 信息.
        """
        # self.logger.info("========CPU========")
        self.last_status['cpu']=[]
        # if self.platform_system == 'Windows':
        #     return self._win_cpu()
        # elif self.platform_system == 'Linux':
        #     return self._linux_cpu()
        return self._linux_cpu()

    def _linux_memory(self):
        """
            获取linux系统内存 信息.
        """
        total_memory = psutil.virtual_memory().total/1024/1024
        available_memory = psutil.virtual_memory().available/1024/1024
        buff = "\n============memory============"
        buff += "\nTotalPhysicalMemory : %sM "%(total_memory)
        buff += "\navailPhysicalMemory : %sM "%(available_memory)

        self._add_memory_info(total_memory, available_memory)
        return buff

    def memory(self):
        """
            获取内存 信息.
        """
        # self.logger.info("\n========memory========")
        self.last_status['memory'] = {}
        # if self.platform_system == 'Windows':
        #     return self._win_memory()
        # else:
        #     return self._linux_memory()
        return self._linux_memory()

    def _linux_disk(self):
        buff = "\n============disk============"
        for disk in psutil.disk_partitions():
            try:
                buff += "\n" + disk.device
                sdiskusage = psutil.disk_usage(disk.mountpoint)
                buff += "\n\ttotal ：%s"%(sdiskusage.total)
                buff += "\n\tfree ：%s"%(sdiskusage.free)
                buff += "\n\tscale ：%.2f%%"%(sdiskusage.percent)
            except:
                self.logger.error("disk error!")
            self._add_disk_info(disk.device, sdiskusage.total, sdiskusage.free, sdiskusage.percent)
        return buff

    def disk(self):
        """
            获取硬盘 信息.
        """
        self.last_status['disk'] = []
        # if self.platform_system == 'Windows':
        #     return self._win_disk()
        # else:
        #     return self._linux_disk()
        return self._linux_disk()

    def _linux_network(self):
        """
            获取linux服务器的MAC和IP地址和TCP连接数
        """
        buff = "\n========network========"
        ipaddress = psutil.net_if_addrs()['WLAN'][0].address
        connects = len(psutil.net_connections())
        net_stats = psutil.net_if_stats()['WLAN'].isup
        buff += "\nip address: %s" % psutil.net_if_addrs()['WLAN'][0].address
        buff += '\nnet connects : %s'%connects
        buff += '\nnet stats : %s'%net_stats
        self._add_network_info(ipaddress, connects, net_stats)
        return buff

    def network(self):
        """
            获取MAC和IP地址和TCP连接数
        """
        self.last_status['network'] = []
        return self._linux_network()

    def start(self):
        """
            start the monitor
        """
        while self.is_loop:
            outstream = self.operating_system()
            outstream += self.cpu()
            outstream += self.disk()
            outstream += self.memory()
            # outstream += self.network()
            self.logger.info(outstream)
            time.sleep(int(self.interval))

def main(argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "v1"
    program_build_date = "%s" %__updated__

    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)

    program_usage = '''monitor [-d \"logpath.\"]  [-t \"interval.\"] [-i \"ip.\"] [-u \"user.\"] [-p \"password.\"] [-m \"mode.\"] '''

    program_longdesc = '''This is a server monitor for CPU, Memory, Disk'''
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
        monitor.start()

    except Exception as identifier:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(identifier) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return False

if __name__ == '__main__': 
    monitor = Monitor()
    monitor.operating_system()
    monitor.cpu()
    monitor.disk()
    monitor.network()