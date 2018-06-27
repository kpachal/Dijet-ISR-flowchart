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
matchPatterns = ["SearchPhase_dijetgamma_single_trigger_inclusive*_inputSig650"]

# Location of files
rootFileDir = "/cluster/warehouse/kpachal/DijetISR/Resolved2017/LimitSetting/BayesianFramework/results/flowchart_outputs/"

# Possible functions
allowedFunctions = ["threepar","fourpar","fivepar","UA2"]

# Point of narrowest possible window
smallestWHW = 14

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
    gotPossibleSignal = False
    gotLimitCase = False
    print optionsDict.keys()
    for whw in sorted(optionsDict.keys(),reverse=True) :

      # This is our stopping criterion
      if whw < smallestWHW :
        break

      materials = optionsDict[whw]
      print "Looking at window size",whw

      # Look at no-window-permitted. Did at least two functions converge?
      useWindowPermission = False
      converged = didTwoConverge(materials,False)

      # If not, replace this list with window-excluded list instead.
      if len(converged) < 2 :
        print "Only",len(converged),"functions converged!"
        print converged
        print "Switching to fits with permitted windows."
        useWindowPermission = True
        converged = didTwoConverge(materials,True)

      print "Number of functions converged:", len(converged)
      print "In order of goodness of fit,",converged

      # Now go left or right from convergence boxes. Do right first because easier.
      if len(converged) < 2 :
        print "Need better convergence. Moving down a window size."
        continue

      # So if we are here, we went down enough windows that 2 functions converged.
      # Time to check p-values.
      
      # 1: do we have two functions with chi2 p-value > 0.0?
      nChi2OK = 0
      for function in converged :
        if materials[function][useWindowPermission].chi2PVal > 0.05 :
          nChi2OK = nChi2OK + 1

      # Is it a simple background?
      print "Number of good chi2 results:", nChi2OK
      if nChi2OK > 1 :
        
        # Good!
        # Go down from central diamond.
        print "Chi2 pvalues are good. Going downwards."
        
        # Have enough info to determine nominal and alternate fits.
        nomFunction = converged[0]
        alternateFunction = converged[1]
        gotNominal = [nomFunction,whw]
        
        # Now we look at permitting-window fits to check the BumpHunter p-values.
        nomData = materials[nomFunction][True]
        alternateData = materials[alternateFunction][True]
        
        # If BH p-values < 0.01, looks like signal!
        if nomData.bumpHunterPVal < 0.01 and alternateData.bumpHunterPVal < 0.01 :
          print "Both BH p-values are less than 0.01, this looks like signal!"
          gotPossibleSignal = True
          # Stop looping, we are done.
          break
        
        # If only one is, looks weird. Investigate.
        elif nomData.bumpHunterPVal < 0.01 or alternateData.bumpHunterPVal < 0.01 :
          print "One of our BH p-values is less than 0.01 and the other is not. "
          print "Is this signal?"
          break
        
        # Otherwise, looks like limit setting case.
        else :
          print "Both bump hunter p-values are > 0.01. This is a background with no signal."
          gotLimitCase = True
          break

      else :
      
        # Uh oh! Ambiguous background.
        # Go left from central diamond.
        print "Chi2 pvalues are bad. Going left."

        # Check bumphunter p-values. Do we have any two which are > 0?
        nBHOK = 0
        for function in converged :
          if materials[function][useWindowPermission].bumpHunterPVal > 0.01 :
            nBHOK = nBHOK + 1
            
        # If BH p-values are OK (> 0.01)
        if nBHOK > 1 :
          
          # We have some functions with OK bump hunter p-values but not enough
          # with OK chi2 p-values.
          # Looks like a bad background but not like a signal.
          # We should go down to a smaller window.
          continue
        
        # If we made it here we have no more than 1 decent chi2 or bh p-value.
        # This could be signal or it could be a bad background.
        # We should look at it with a window permitted.
        windowPermittedData = {}
        for function in converged :
          smallDict = {}
          windowPermittedData[function] = {}
          


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


