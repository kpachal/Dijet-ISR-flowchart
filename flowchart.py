import glob
import ROOT

# Tools for making plots
from art.morisot import Morisot
from analysisScripts.searchphase import searchFileData
import analysisScripts.generalfunctions

# File patterns to match. 
# Need to be distinct enough that each matches only the relevant flowchart items.
matchPatterns = ["SearchPhase_dijetgamma_single_trigger_inclusive*_inputSig650"]

# Location of files
rootFileDir = "/cluster/warehouse/kpachal/DijetISR/Resolved2017/LimitSetting/BayesianFramework/results/flowchart_outputs/"

# Possible functions
allowedFunctions = ["threepar","fourpar","fivepar","UA2"]

# Loop over them. That way we could do all 4 unblindings at the same time.
for pattern in matchPatterns :

  print "Beginning flowcharting of files matching",rootFileDir+pattern+"*.root"

  # Collect list of relevant files. Everything will be drawn from these.
  collectFiles = glob.glob(rootFileDir+pattern+"*.root")
  print collectFiles

  # Get their data and organise it into a dictionary
  optionsDict = {
  }
  for file in collectFiles :

    # Get info about file for referencing it

    permitWindow = None
    if "permitWindow" in file :
      permitWindow = True
    elif "noPermitWindow" in file :
      permitWindow = False
    else :
      print "Could not determine if window is allowed!"
      exit(0)
    print "Window allowed is",permitWindow

    # Get function
    function = None
    for func in allowedFunctions :
      if func in file :
        function = func 
        continue
    if not function : 
      print "Could not identify function!"
      exit(0)
    print "Found function",function

    # Get range of swift fit
    swiftWindow = None
    if "global" in file :
      swiftWindow = 1000
    elif "whw" in file :
      tokens = file.split("_")
      relevant = [token for token in tokens if "whw" in token]
      if len(relevant) > 1 : print "????"
      windowSize = relevant[0].replace("whw","")
      swiftWindow = eval(windowSize)
    if not swiftWindow :
      print "Could not identify swift window!"
      exit(0)
    print "Found swiftWindow",swiftWindow

    # Get data
    # Add to dict
    theseData = searchFileData(file,permitWindow)
    if not swiftWindow in optionsDict.keys() : optionsDict[swiftWindow] = {}
    if not function in optionsDict[swiftWindow].keys() :
      optionsDict[swiftWindow][function] = {}
    optionsDict[swiftWindow][function][permitWindow] = theseData

    print optionsDict

# Start: widest window


