import ROOT
import sys, os
import glob
import math
import subprocess
from condor_files import CondorHandler
from pbs_files import PBSHandler

## What do you want to do?
doSWIFTFits = True
doGlobalFits = True
useBatch = True

# File you want to test on
inputDir = "/cluster/warehouse/kpachal/DijetISR/Resolved2017/LimitSetting/inputs/flowchart_tests/"
#fitfiles = ["searchphase.photon_single_inclusiveCATDOGCHECKSat.Gauss_width7.650.gev.SigEvent2600.mjj._ww12.650JUSTABOVE.root"]
fitfiles = [
#"searchphase.photon_compound_inclusiveCATDOGCHECKSat.Gauss_width7.NOSIGNAL.gev.SigEvent0.mjj._ww9.650.root",
#"searchphase.photon_compound_inclusiveCATDOGCHECKSat.Gauss_width7.650.gev.SigEvent4250.mjj._ww10.650JUSTABOVE.root",
"searchphase.photon_compound_inclusiveCATDOGCHECKSat.Gauss_width7.650.gev.SigEvent2200.mjj._ww23.650JUSTBELOW.root"
]
#fitfiles = ["dijetgamma_HLT_g140_loose_ystar0p75_15ifbdata_inclusive.root"]
#fitfiles = ["dijetgamma_HLT_g75_tight_3j50noL1_L1EM22VHI_ystar0p75_15ifbdata_inclusive.root"]
#fitfiles = ["trijet_HLT_j380_ystar0p75_15ifbdata_inclusive.root"]
#extraTags = ["_toys_inputSig650"]
extraTags = [
#"_toys_noSig",
#"_toys_inputSig650"
"_toys_verySmallSig650"
]
#extraTags = ["_15ifbData"]

# Tell me about these files
lumi = "full" # or 15fb
#channel = "dijetgamma_single_trigger"
channel = "dijetgamma_compound_trigger"
#channel = "trijet"
ntag = "inclusive"
inHistName = "basicData"
#inHistName = "background_mjj_var"

# Other info
outputDir = "/cluster/warehouse/kpachal/DijetISR/Resolved2017/LimitSetting/BayesianFramework/results/flowchart_outputs/"
#doChannels = ["dijetgamma_compound_trigger","dijetgamma_single_trigger"]# "trijet"
doFunctions = ["threepar","fourpar","fivepar","UA2"]

## Set up PBS batch handler
batchmanager = PBSHandler()

minXDict = {"dijetgamma_single_trigger" : 168,
            "dijetgamma_compound_trigger" : 300,
            "trijet" : 300
           }

maxXForFit = 1200

minWHW = 9

functionLoopDict = {
  "fivepar" : {
    "functioncode" : 7,
    "npar" : 5
  },
  "fourpar" : {
    "functioncode" : 4,
    "npar" : 4
  },
  "UA2" : {
    "functioncode" : 1,
    "npar" : 4
  },
  "threepar" : {
    "functioncode" : 9,
    "npar" : 3
  }
}

# Dictionary of good start parameters.
# Based on fits to MC with equivalent luminosities of 
# 79.826 dijetgamma
# 79.521 trijet
if "full" in lumi :
  from start_pars_80fb import startParDict
else :
  from start_pars_15fb import startParDict

templateConfig = os.path.realpath("../../source/Bayesian/configurations/DijetISR_Configs/Step1_SearchPhase_Swift_template.config")
newConfigDir = os.path.realpath("./configs/")

# Cycle through files I want to test on
index = -1
for infile in fitfiles :

  index = index + 1
  extraTag = extraTags[index]

  # Cycle through acceptable functions
  for function in doFunctions :

    inputFile = inputDir+infile

    print "Fitting to",inputFile
    openFile = ROOT.TFile.Open(inputFile,"READ")
    inHist = openFile.Get(inHistName)
    inHist.SetDirectory(0)
    openFile.Close()

    # Min x for fit by channel, max defined at top
    simplechannel = channel.split("_")[0]
    minXForFit = minXDict[channel]
    minBinX = inHist.FindBin(minXForFit)+1

    maxBinX = inHist.FindBin(maxXForFit)-1

    # Max x available defined by last bin with > 1 event in histogram.
    maxXAvailable = 7000
    maxBinAvailable = inHist.GetNbinsX()
    for bin in range(inHist.GetNbinsX(), 1, -1) :
      if inHist.GetBinContent(bin) > 1.0 :
        maxXAvailable = inHist.GetBinLowEdge(bin+1)+1
        maxBinAvailable = bin
        break

    # Min window width set at top. Max window width = half the distance between lowest and highest bins.
    maxWHW = int(math.floor(float(maxBinX-minBinX+1)/2.0))

    # Get start parameters I can trust
    fitSettings = functionLoopDict[function]
    startPars = startParDict[function][simplechannel][ntag]

    ## Cycle through available SWIFT fit options and generate configurations for each
    for whw in [0]+range(minWHW,maxWHW+1) :

      if whw > 0 :
        if not doSWIFTFits :
          continue
        else :
          extension = "whw{0}".format(whw)
          print "setting extension",extension

      if whw < 1 :
        if not doGlobalFits :
          continue
        else :
          extension = "global"

      # Need 2 configs for each: window exclusion permitted and window exclusion not permitted
      for doWindow in [True,False] :
        windowExt = ""
        if doWindow : 
          windowExt = "_permitWindow"
        else :
          windowExt = "_noPermitWindow"

        newConfig = newConfigDir+"/Step1_SearchPhase_Swift_{0}_{1}_{2}_{3}{4}{5}.config".format(channel,ntag,function,extension,windowExt,extraTag)
        outputFile = outputDir+"SearchPhase_{0}_{1}_{2}_{3}{4}{5}.root".format(channel,ntag,function,extension,windowExt,extraTag)
        outputLog = "logs/SearchPhase_{0}_{1}_{2}_{3}{4}{5}.txt".format(channel,ntag,function,extension,windowExt,extraTag)
        with open(templateConfig,'r') as readConf :
          with open(newConfig,'w') as writeConf :

            for line in readConf :
              if "inputFileName" in line :
                line = "inputFileName {0}\n".format(inputFile)
              elif "outputFileName" in line :
                line = "outputFileName {0}\n".format(outputFile)
              elif "dataHist" in line :
                line = "dataHist {0}\n".format(inHistName)
              elif "permitWindow" in line :
                line = "permitWindow	{0}"
                if doWindow :
                  line = line.format("true")
                else :
                  line = line.format("false")
              elif "minXForFit" in line :
                line = "minXForFit {0}\n".format(minXForFit)
              elif "maxXForFit" in line :
                line = "maxXForFit {0}\n".format(maxXForFit)
              elif "nPseudoExpFit" in line :
                line = "nPseudoExpFit    1\n"
              elif "functionCode" in line :
                line = "functionCode {0}\n".format(fitSettings["functioncode"])
              elif "nParameters" in line :
                line = "nParameters {0}\n".format(fitSettings["npar"])
              if whw > 0 :
                if "swift_minXAvailable" in line :
                  line = "swift_minXAvailable {0}\n".format(minXForFit)
                elif "swift_maxXAvailable" in line :
                  line = "swift_maxXAvailable {0}\n".format(maxXAvailable)
                elif "swift_nBinsLeft" in line :
                  line = "swift_nBinsLeft {0}\n".format(whw)
                elif "swift_nBinsRight" in line :
                  line = "swift_nBinsRight {0}\n".format(whw)
              else :
                if "doSwift" in line :
                  line = "doSwift False\n"
              # Want to keep the right number of parameters
              if "parameter1" in line :
                line = ""
                for par in sorted(startPars.keys()) :
                  line = line + "{0} {1}\n".format(par,startPars[par])
              elif "parameter" in line :
                continue
              writeConf.write(line)

        # Run the search
        if not useBatch :
          command = "SearchPhase --config {0} > {1}".format(newConfig,outputLog)
          print command
          subprocess.call(command,shell=True)
        else :
          print "Passing config name",newConfig
          batchmanager.send_job(newConfig)

