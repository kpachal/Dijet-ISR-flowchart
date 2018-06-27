import glob
import ROOT
import numpy as np
from collections import OrderedDict
from operator import itemgetter

# Tools for making plots
from art.morisot import Morisot
from analysisScripts.searchphase import searchFileData
import analysisScripts.generalfunctions

# File patterns to match. 
# Need to be distinct enough that each matches only the relevant flowchart items.
matchPatterns = ["SearchPhase_dijetgamma_single_trigger_inclusive*_OLD"]

# Location of files
rootFileDir = "/cluster/warehouse/kpachal/DijetISR/Resolved2017/LimitSetting/BayesianFramework/results/flowchart_outputs/"

# Possible functions
allowedFunctions = ["threepar","fourpar","fivepar","UA2"]

def main() :

  # Loop over the files. That way we could do all 4 unblindings at the same time.
  for pattern in matchPatterns :

    print "Beginning flowcharting of files matching",rootFileDir+pattern+"*.root"

    # Collect list of relevant files. Everything will be drawn from these.
    collectFiles = glob.glob(rootFileDir+pattern+"*.root")

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
      #print "Window allowed is",permitWindow

      # Get function
      function = None
      for func in allowedFunctions :
        if func in file :
          function = func 
          continue
      if not function : 
        print "Could not identify function!"
        exit(0)
      #print "Found function",function

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
      #print "Found swiftWindow",swiftWindow

      # Get data
      # Add to dict
      theseData = searchFileData(file,permitWindow)
      if not swiftWindow in optionsDict.keys() : optionsDict[swiftWindow] = {}
      if not function in optionsDict[swiftWindow].keys() :
        optionsDict[swiftWindow][function] = {}
      optionsDict[swiftWindow][function][permitWindow] = theseData

    # Now everything we want is in optionsDict. Begin flowchart.
    # Start: widest window
    gotNominal = None
    print optionsDict.keys()
    for whw in sorted(optionsDict.keys(),reverse=True) :

      materials = optionsDict[whw]
      print "Looking at window size",whw

      # Look at no-window-permitted. Did at least two functions converge?
      converged = didTwoConverge(materials,False)

      # If not, replace this list with window-excluded list instead.
      if len(converged) < 2 :
        print "Only",len(converged),"functions converged!"
        print converged
        print "Switching to fits with permitted windows."
        converged = didTwoConverge(materials,True)

      print "Number of functions converged:", len(converged)
      print "In order of goodness of fit,",converged

      # Now go left or right from convergence boxes. Do right first because easier.
      if len(converged) < 2 :
        print "Need better convergence. Moving down a window size."
        continue

      # So if we are here, we went down enough windows that 2 functions converged.
      # Time to check p-values.





      # END OF WHW LOOP

    # If we looked at all possible windows and gotNominal is null, we failed and go home.
    if gotNominal is None :
      print "We cry and go home!"



def didTwoConverge(materials,doPermitWindow) :

  funcsWhichConverged = {}
  #orderedGoodFuncs = []
  for function in materials.keys() :
    didConverge = True
    data = materials[function][doPermitWindow]
    # Check: is chi2 p-value not inf or nan
    # think this is all we need becasue data object doesn't exist if it barfs on picking things up
    if np.isinf(data.chi2PVal) or np.isnan(data.chi2PVal) :
      didConverge = False

    # Add to dictionary with chi2 p-value (which will identify best one)
    if didConverge :
      funcsWhichConverged[function] = data.chi2PVal

  # Turn dict into list in order.
  # Only issue: random if all p-values zero. Would prefer to prioritise usually good funcs...
  orderedGoodFuncs = OrderedDict(sorted(funcsWhichConverged.items(), key=itemgetter(1), reverse=True))

  return orderedGoodFuncs.keys()


if __name__ == "__main__":
  main()


