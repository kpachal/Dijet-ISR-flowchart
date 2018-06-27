# For setting up submission scripts for a pbs batch
import os
import subprocess

class PBSHandler(object) :

  def __init__(self) :

    self.commandTemplate = "SearchPhase --config {0}"
    self.basepath = os.getcwd().replace("run/flowchart","")
    print "Base path is",self.basepath
    return
  
  def make_bash_file(self, config) :

    thisCommand = self.commandTemplate.format(config)
    tags = config.split("/")[-1]
    tags = tags.replace(".config","").replace("Step1_SearchPhase_","")
    batchtempname = "batch/submitScript_{0}.sh".format(tags)

    with open(batchtempname,'write') as out :
      out.write("#!/bin/sh -v\n")
      out.write("shopt -s expand_aliases\n")
      out.write("source ~/.bash_profile\n")
      out.write("cd {0}\n".format(self.basepath))
      out.write("setupATLAS\n")
      out.write("asetup --restore\n")
      out.write("cd run/flowchart\n")
      out.write("source ../../build/x86_64-slc6-gcc62-opt/setup.sh\n")
      out.write("SearchPhase --config {0}\n".format(config))
    
    modcommand = "chmod 744 {0}".format(batchtempname)

    return batchtempname

  def send_job(self,config) :

    bashfile = self.make_bash_file(config)
    subprocess.call("qsub {0}".format(bashfile),shell=True)
