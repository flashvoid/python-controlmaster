#!/usr/bin/env python
import sys
import os
import string
import random
import subprocess
import thread
import time
import signal

class controlmaster():
  host = ''
  status = ''
  master_socket = ''
  controldir = ''
  debug = False
  masterpid = 0
  cmdpid = 0
  def __init__(self,hostname,master_socket='',debug=False):
    self.ifdebug("in init")
    self.host = hostname
    self.check_control_dir()
    self.stdout = ''
    self.stderr = ''
    if master_socket=='':
      rnd=''.join(random.choice(string.letters) for i in xrange(10))
      self.master_socket = self.controldir + '/' + rnd
    else:
      self.master_socket = self.controldir + '/' + master_socket
    self.debug=debug

  def ifdebug(self,args):
    if self.debug:
      print(args)

  def cmd(self,args):
    self.ifdebug("in cmd: executing %s" % args)
    try:
      p = subprocess.Popen(args,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      self.cmdpid=p.pid
      retcode = p.wait()
      self.stdout = p.communicate()[0]
      if retcode < 0:
        print("in cmd: Child was terminated ", -retcode, file=sys.stderr)
    except OSError as e:
      print("in cmd: Execution failed: ", e, file=sys.stderr)
    return retcode

  def checkauth(self):
    self.ifdebug("in checkauth")
    if not os.path.exists(self.master_socket):
      self.ifdebug("in checkauth: FAIL: NOFILE")
      return False
    status = self.cmd(['ssh','-S',self.master_socket,'-O','check','go'])
    if status != 0:
      self.ifdebug("in checkauth: FAIL: NOCONN")
      return False
    return True

  def connect(self):
    self.ifdebug("in connect")
    if self.checkauth(): return True
    thread.start_new_thread(self.cmd, ((['ssh', '-fNMS', self.master_socket, self.host]),))
    print("connecting", self.host)
    for i in range(0,10):
      if self.checkauth(): 
        self.masterpid = self.cmdpid
        print("Success")
        return True
      print(".")
      sys.stdout.flush()
      time.sleep(1)
    print("Fail")
    self.masterpid = self.cmdpid
    print("masterpid = %s" % self.masterpid)
    if self.masterpid > 0:
      try:
        os.kill(self.masterpid,signal.SIGTERM)
      except OSError:
        pass
    return False


  def disconnect(self):
    self.ifdebug("in disconnect")
    if not self.checkauth(): return True
    status = self.cmd(['ssh','-S',self.master_socket,'-O', 'exit', 'go'])
    if status == 0: 
      return True
    else:
      print("in disconnect: Fail : %s" % status)
      return False

  def put(self,src,dst):
    if not self.checkauth(): return False
    self.ifdebug("in put")
    status = self.cmd(['scp','-o controlpath='+self.master_socket,src,'go:'+dst])
    if status == 0: 
      return True
    else:
      print("in put: Fail : %s" % status)
      return False

  def get(self,src,dst):
    if not self.checkauth(): return False
    self.ifdebug("in get")
    status = self.cmd(['scp','-o controlpath='+self.master_socket,'go:'+src,dst])
    if status == 0: 
      return True
    else:
      print("in get: Fail : %s" % status)
      return False

  def rput(self):
    if not self.checkauth(): return False
    self.ifdebug("in rput")
    status = self.cmd(['scp','-r','-o controlpath='+self.master_socket,src,'go:'+dst])
    if status == 0: 
      return True
    else:
      print("in rput: Fail : %s" % status)
      return False

  def rget(self):
    if not self.checkauth(): return False
    self.ifdebug("in rget"  )
    status = self.cmd(['scp','-r','-o controlpath='+self.master_socket,'go:'+src,dst])
    if status == 0: 
      return True
    else:
      print("in rget: Fail : %s" % status)
      return False
 
  def exe(self,command):
    self.ifdebug("in exe")
    if not self.checkauth(): return False
    status = self.cmd(['ssh','-S',self.master_socket,'go',command])
    if status == 0: 
      print(self.stdout)
      return status
    else:
      print("in exe: Fail : %s" % status)
      return False

  def check_control_dir(self,
                        controldir=os.environ['HOME']+"/.controlmaster"):
    self.ifdebug("in check_control_dir : controldir = %s" % controldir)
    if not os.path.isdir(controldir):
      os.makedirs(controldir)
    self.controldir = controldir

  def create_master_socket(self):
    self.ifdebug("in create_master_socket")


if __name__ == '__main__':
  if len(sys.argv)>1:
    host=sys.argv[1] 
  if len(sys.argv)>2:
    debug=sys.argv[2] 
  else:
    debug=False
  ssh = controlmaster(host,debug=debug)
  ssh.connect()
  ssh.exe('uptime')
  ssh.disconnect()
