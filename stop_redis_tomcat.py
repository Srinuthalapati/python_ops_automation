#! /usr/bin/env python
# -*- coding: utf-8 -*-

#Importing modules
import shutil
import os, sys
import shlex, subprocess
import popen2
import shutil
import re

# Defining function to check whether a process is running or not
def process_exists(proc_name):
    ps = subprocess.Popen("ps ax -o pid= -o args= ", shell=True, stdout=subprocess.PIPE)
    ps_pid = ps.pid
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()

    for line in output.split("\n"):
        res = re.findall("(\d+) (.*)", line)
        if res:
            pid = int(res[0][0])
            if proc_name in res[0][1] and pid != os.getpid() and pid != ps_pid:
                return True
    return False

# Stopping tomcat process if it exists 	
if process_exists("tomcat"):
    print "stopping tomcat"
    p = subprocess.Popen('service tomcat stop;pkill -9 -f tomcat', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print line,
    p.wait()

# Flush the cache and stop redis service if it exists
if process_exists("redis"):
    print "stopping Redis and clearing the cache"
    p = subprocess.Popen('redis-cli flushall;service redis stop', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print line,
    p.wait()

# Stopping redis-sentinel service if it exists	
if process_exists("redis-sentinel"):
    print "stopping redis-sentinel running"
    p = subprocess.Popen('service redis-sentinel stop', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print line,
    p.wait()

# Remove redis package if installed
print os.system('if yum list installed "redis" >/dev/null 2>&1; then yum -y remove redis;fi')

#Remove all redis logs and config files
os.system('rm -rf /var/log/redis; rm -rf /etc/redis*')