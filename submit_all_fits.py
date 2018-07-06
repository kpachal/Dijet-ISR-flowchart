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
#inputDir = "/cluster/warehouse/kpachal/DijetISR/Resolved2017/LimitSetting/inputs/flowchart_tests/"
inputDir = "/cluster/warehouse/kpachal/DijetISR/Resolved2017/LimitSetting/inputs/unblinded_data/"
fitfiles = [
#"dijetgamma_single_trigger_ystar0p75_unblinding_inclusive.root",
#"dijetgamma_single_trigger_ystar0p75_unblinding_nbtag2.root",
"dijetgamma_compound_trigger_ystar0p75_unblinding_inclusive.root",
#"dijetgamma_compound_trigger_ystar0p75_unblinding_nbtag2.root"
]
#fitfiles = ["searchphase.photon_single_inclusiveCATDOGCHECKSat.Gauss_width7.650.gev.SigEvent2600.mjj._ww12.650JUSTABOVE.root"]
#fitfiles = [
#"searchphase.photon_compound_inclusiveCATDOGCHECKSat.Gauss_width7.NOSIGNAL.gev.SigEvent0.mjj._ww9.650.root",
#"searchphase.photon_compound_inclusiveCATDOGCHECKSat.Gauss_width7.650.gev.SigEvent4250.mjj._ww10.650JUSTABOVE.root",
#"searchphase.photon_compound_inclusiveCATDOGCHECKSat.Gauss_width7.650.gev.SigEvent2200.mjj._ww23.650JUSTBELOW.root",
#"dijetgamma_ABCD_compoundtrigger_ystar0p75_15ifbdata_nbtag2.root",
#"dijetgamma_ABCD_compoundtrigger_ystar0p75_15ifbdata_nbtag2_MODIFIED.root",
#"dijetgamma_ABCD_singletrigger_ystar0p75_15ifbdata_nbtag2.root",
#"dijetgamma_ABCD_singletrigger_ystar0p75_15ifbdata_nbtag2_MODIFIED.root",
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass350.SigNum6781.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass1100.SigNum1476.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass750.SigNum2852.mjj_Gauss_sig__smooth.root"
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass1000.SigNum1840.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass1100.SigNum1476.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass350.SigNum6781.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass400.SigNum5915.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass450.SigNum5126.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass550.SigNum4038.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass650.SigNum3446.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass750.SigNum2852.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass850.SigNum2386.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass950.SigNum1921.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass400.SigNum7393.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass400.SigNum8872.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass450.SigNum6408.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass450.SigNum7690.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass600.SigNum4611.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass600.SigNum5533.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass650.SigNum4307.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_compound_inclusive_unblind.Gauss_width10.mass650.SigNum5169.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass1000.SigNum1415.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass1100.SigNum1178.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass200.SigNum11654.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass200.SigNum2913.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass200.SigNum5827.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass200.SigNum8740.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass250.SigNum10722.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass250.SigNum2680.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass250.SigNum5361.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass250.SigNum8041.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass300.SigNum2458.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass300.SigNum4917.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass300.SigNum7376.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass300.SigNum9835.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass350.SigNum2259.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass350.SigNum4509.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass350.SigNum4519.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass350.SigNum6779.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass350.SigNum9039.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass400.SigNum3976.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass450.SigNum3509.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass550.SigNum2827.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass650.SigNum2490.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass750.SigNum2095.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass850.SigNum1754.mjj_Gauss_sig__smooth.root",
#"signalplusbackground.photon_single_inclusive_unblind.Gauss_width10.mass950.SigNum1437.mjj_Gauss_sig__smooth.root"
#]
#fitfiles = ["dijetgamma_HLT_g140_loose_ystar0p75_15ifbdata_inclusive.root"]
#fitfiles = ["dijetgamma_HLT_g75_tight_3j50noL1_L1EM22VHI_ystar0p75_15ifbdata_inclusive.root"]
#fitfiles = ["trijet_HLT_j380_ystar0p75_15ifbdata_inclusive.root"]

extraTags = ["_unblinding_3binUp"]

#extraTags = ["_toys_inputSig650"]
#extraTags = [
#"_toys_noSig",
#"_toys_inputSig650",
#"_toys_verySmallSig650",
#"_ABCD_original",
#"_ABCD_modified",
#"_toys_inputSig350"
#"_toys_inputSig1100_fitTo1400"
#"_toys_inputSig1100_fitTo1500",
#"_toys_inputSig750"
#"_toys_mass1000.SigNum1840",
#"_toys_mass1100.SigNum1476",
#"_toys_mass350.SigNum6781",
#"_toys_mass400.SigNum5915",
#"_toys_mass450.SigNum5126",
#"_toys_mass550.SigNum4038",
#"_toys_mass650.SigNum3446",
#"_toys_mass750.SigNum2852",
#"_toys_mass850.SigNum2386",
#"_toys_mass950.SigNum1921",
#"_toys_mass400.SigNum7393",
#"_toys_mass400.SigNum8872",
#"_toys_mass450.SigNum6408",
#"_toys_mass450.SigNum7690",
#"_toys_mass600.SigNum4611",
#"_toys_mass600.SigNum5533",
#"_toys_mass650.SigNum4307",
#"_toys_mass650.SigNum5169",
#"_toys_mass1000.SigNum1415",
#"_toys_mass1100.SigNum1178",
#"_toys_mass200.SigNum11654",
#"_toys_mass200.SigNum2913",
#"_toys_mass200.SigNum5827",
#"_toys_mass200.SigNum8740",
#"_toys_mass250.SigNum10722",
#"_toys_mass250.SigNum2680",
#"_toys_mass250.SigNum5361",
#"_toys_mass250.SigNum8041",
#"_toys_mass300.SigNum2458",
#"_toys_mass300.SigNum4917",
#"_toys_mass300.SigNum7376",
#"_toys_mass300.SigNum9835",
#"_toys_mass350.SigNum2259",
#"_toys_mass350.SigNum4509",
#"_toys_mass350.SigNum4519",
#"_toys_mass350.SigNum6779",
#"_toys_mass350.SigNum9039",
#"_toys_mass400.SigNum3976",
#"_toys_mass450.SigNum3509",
#"_toys_mass550.SigNum2827",
#"_toys_mass650.SigNum2490",
#"_toys_mass750.SigNum2095",
#"_toys_mass850.SigNum1754",
#"_toys_mass950.SigNum1437",
#]
#extraTags = ["_15ifbData"]

# Tell me about these files
lumi = "full" # or "15fb"
#channel = "dijetgamma_single_trigger"
channel = "dijetgamma_compound_trigger"
#channel = "trijet"
ntag = "inclusive"
#ntag = "nbtag2"

inHistNames = ["background_mjj_var"]
#inHistName = "basicData"
#inHistName = "background_mjj_var"
#inHistName = "mjj_Gauss_sig_350_smoothinjectedToBkg"
#inHistName = "mjj_Gauss_sig_1100_smoothinjectedToBkg"
#inHistNames = ["mjj_Gauss_sig_750_smoothinjectedToBkg"]
#inHistNames = [
#"mjj_Gauss_sig_1000_smoothinjectedToBkg",
#"mjj_Gauss_sig_1100_smoothinjectedToBkg",
#"mjj_Gauss_sig_200_smoothinjectedToBkg",
#"mjj_Gauss_sig_200_smoothinjectedToBkg",
#"mjj_Gauss_sig_200_smoothinjectedToBkg",
#"mjj_Gauss_sig_200_smoothinjectedToBkg",
#"mjj_Gauss_sig_250_smoothinjectedToBkg",
#"mjj_Gauss_sig_250_smoothinjectedToBkg",
#"mjj_Gauss_sig_250_smoothinjectedToBkg",
#"mjj_Gauss_sig_250_smoothinjectedToBkg",
#"mjj_Gauss_sig_300_smoothinjectedToBkg",
#"mjj_Gauss_sig_300_smoothinjectedToBkg",
#"mjj_Gauss_sig_300_smoothinjectedToBkg",
#"mjj_Gauss_sig_300_smoothinjectedToBkg",
#"mjj_Gauss_sig_350_smoothinjectedToBkg",
#"mjj_Gauss_sig_350_smoothinjectedToBkg",
#"mjj_Gauss_sig_350_smoothinjectedToBkg",
#"mjj_Gauss_sig_350_smoothinjectedToBkg",
#"mjj_Gauss_sig_350_smoothinjectedToBkg",
#"mjj_Gauss_sig_400_smoothinjectedToBkg",
#"mjj_Gauss_sig_400_smoothinjectedToBkg",
#"mjj_Gauss_sig_450_smoothinjectedToBkg",
#"mjj_Gauss_sig_450_smoothinjectedToBkg",
#"mjj_Gauss_sig_550_smoothinjectedToBkg",
#"mjj_Gauss_sig_600_smoothinjectedToBkg",
#"mjj_Gauss_sig_600_smoothinjectedToBkg",
#"mjj_Gauss_sig_650_smoothinjectedToBkg",
#"mjj_Gauss_sig_650_smoothinjectedToBkg",
#"mjj_Gauss_sig_750_smoothinjectedToBkg",
#"mjj_Gauss_sig_850_smoothinjectedToBkg",
#"mjj_Gauss_sig_950_smoothinjectedToBkg",
#]

# Other info
#outputDir = "/cluster/warehouse/kpachal/DijetISR/Resolved2017/LimitSetting/BayesianFramework/results/flowchart_outputs/"
outputDir = "/cluster/warehouse/kpachal/DijetISR/Resolved2017/LimitSetting/BayesianFramework/results/search_unblinded_data/"
#doChannels = ["dijetgamma_compound_trigger","dijetgamma_single_trigger"]# "trijet"
doFunctions = ["threepar","fourpar","fivepar","UA2"]

## Set up PBS batch handler
batchmanager = PBSHandler()

minXDict = {"dijetgamma_single_trigger" : 168,
            "dijetgamma_compound_trigger" : 336, # was 300
            "trijet" : 300
           }

maxXForFit = 1201

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
  inHistName = inHistNames[index]

  # Cycle through acceptable functions
  for function in doFunctions :

    inputFile = inputDir+infile

    print "Fitting to",inputFile,"hist",inHistName
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
#    maxWHW = int(math.floor(float(maxBinX-minBinX+1)/2.0))
    maxWHW = 23

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

