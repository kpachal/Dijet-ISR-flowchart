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
matchPatterns = [
"SearchPhase_dijetgamma_single_trigger_inclusive_*unblinding",
"SearchPhase_dijetgamma_single_trigger_nbtag2_*unblinding",
"SearchPhase_dijetgamma_compound_trigger_inclusive_*unblinding_2binUp",
"SearchPhase_dijetgamma_compound_trigger_nbtag2_*unblinding"
]

#matchPatterns = [
#"SearchPhase_dijetgamma_single_trigger_inclusive*_inputSig650",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*toys_noSig",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*toys_inputSig650",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*toys_verySmallSig650",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*15ifbData",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*15ifbData",
#"SearchPhase_trijet_inclusive_*15ifbData",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*ABCD_original",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*ABCD_modified",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*ABCD_original",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*ABCD_modified",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*toys_inputSig350",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*toys_inputSig1100",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*_toys_inputSig1100_fitTo1400",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*_toys_inputSig1100_fitTo1500",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*toys_inputSig750"
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*mass1000.SigNum1840",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*mass1100.SigNum1476",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*mass350.SigNum6781",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*mass400.SigNum5915",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*mass400.SigNum7393",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*mass400.SigNum8872",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*mass450.SigNum5126",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*mass450.SigNum6408",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*mass450.SigNum7690",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*mass550.SigNum4038",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*mass650.SigNum3446",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*mass650.SigNum4307",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*mass650.SigNum5169",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*mass750.SigNum2852",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*mass850.SigNum2386",
#"SearchPhase_dijetgamma_compound_trigger_inclusive_*mass950.SigNum1921",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass1000.SigNum1415",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass1100.SigNum1178",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass200.SigNum11654",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass200.SigNum2913",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass200.SigNum5827",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass200.SigNum8740",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass250.SigNum10722",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass250.SigNum2680",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass250.SigNum5361",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass250.SigNum8041",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass300.SigNum2458",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass300.SigNum4917",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass300.SigNum7376",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass300.SigNum9835",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass350.SigNum2259",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass350.SigNum4509",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass350.SigNum4519",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass350.SigNum6779",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass350.SigNum9039",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass400.SigNum3976",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass450.SigNum3509",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass550.SigNum2827",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass650.SigNum2490",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass750.SigNum2095",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass850.SigNum1754",
#"SearchPhase_dijetgamma_single_trigger_inclusive_*mass950.SigNum1437"
#]

plotExtensions = [
"_single_trigger_inclusive_unblinding",
"_single_trigger_nbtag2_unblinding",
"_compound_trigger_inclusive_unblinding",
"_compound_trigger_nbtag2_unblinding"
]

#plotExtensions = [
#"_single_trigger_inclusive_toys_inputSig650",
#"_compound_trigger_inclusive_toys_noSig",
#"_compound_trigger_inclusive_toys_inputSig650",
#"_compound_trigger_inclusive_toys_verySmallSig650",
#"_single_trigger_inclusive_15ifbData",
#"_compound_trigger_inclusive_15ifbData",
#"_trijet_inclusive_15ifbData",
#"_single_trigger_inclusive_ABCD_original",
#"_single_trigger_inclusive_ABCD_modified",
#"_compound_trigger_inclusive_ABCD_original",
#"_compound_trigger_inclusive_ABCD_modified",
#"_compound_trigger_inclusive_toys_inputSig350"
#"_compound_trigger_inclusive_toys_inputSig1100",
#"_compound_trigger_inclusive_toys_inputSig1100_fitTo1400",
#"_compound_trigger_inclusive_toys_inputSig1100_fitTo1500"
#"_compound_trigger_inclusive_toys_inputSig750"
#"_compound_trigger_inclusive_mass1000.SigNum1840",
#"_compound_trigger_inclusive_mass1100.SigNum1476",
#"_compound_trigger_inclusive_mass350.SigNum6781",
#"_compound_trigger_inclusive_mass400.SigNum5915",
#"_compound_trigger_inclusive_mass400.SigNum7393",
#"_compound_trigger_inclusive_mass400.SigNum8872",
#"_compound_trigger_inclusive_mass450.SigNum5126",
#"_compound_trigger_inclusive_mass450.SigNum6408",
#"_compound_trigger_inclusive_mass450.SigNum7690",
#"_compound_trigger_inclusive_mass550.SigNum4038",
#"_compound_trigger_inclusive_mass650.SigNum3446",
#"_compound_trigger_inclusive_mass650.SigNum4307",
#"_compound_trigger_inclusive_mass650.SigNum5169",
#"_compound_trigger_inclusive_mass750.SigNum2852",
#"_compound_trigger_inclusive_mass850.SigNum2386",
#"_compound_trigger_inclusive_mass950.SigNum1921",
#"_single_trigger_inclusive_mass1000.SigNum1415",
#"_single_trigger_inclusive_mass1100.SigNum1178",
#"_single_trigger_inclusive_mass200.SigNum11654",
#"_single_trigger_inclusive_mass200.SigNum2913",
#"_single_trigger_inclusive_mass200.SigNum5827",
#"_single_trigger_inclusive_mass200.SigNum8740",
#"_single_trigger_inclusive_mass250.SigNum10722",
#"_single_trigger_inclusive_mass250.SigNum2680",
#"_single_trigger_inclusive_mass250.SigNum5361",
#"_single_trigger_inclusive_mass250.SigNum8041",
#"_single_trigger_inclusive_mass300.SigNum2458",
#"_single_trigger_inclusive_mass300.SigNum4917",
#"_single_trigger_inclusive_mass300.SigNum7376",
#"_single_trigger_inclusive_mass300.SigNum9835",
#"_single_trigger_inclusive_mass350.SigNum2259",
#"_single_trigger_inclusive_mass350.SigNum4509",
#"_single_trigger_inclusive_mass350.SigNum4519",
#"_single_trigger_inclusive_mass350.SigNum6779",
#"_single_trigger_inclusive_mass350.SigNum9039",
#"_single_trigger_inclusive_mass400.SigNum3976",
#"_single_trigger_inclusive_mass450.SigNum3509",
#"_single_trigger_inclusive_mass550.SigNum2827",
#"_single_trigger_inclusive_mass650.SigNum2490",
#"_single_trigger_inclusive_mass750.SigNum2095",
#"_single_trigger_inclusive_mass850.SigNum1754",
#"_single_trigger_inclusive_mass950.SigNum1437"
#]

binExtensions = ["","_1binUp","_2binUp"]

# Location of files
#rootFileDir = "/cluster/warehouse/kpachal/DijetISR/Resolved2017/LimitSetting/BayesianFramework/results/flowchart_outputs/"
rootFileDir = "/cluster/warehouse/kpachal/DijetISR/Resolved2017/LimitSetting/BayesianFramework/results/search_unblinded_data/"

#plotDir = "flowchart_plots/"
plotDir = "unblinded_data_plots/"

# Possible functions
allowedFunctions = ["threepar","fourpar","fivepar","UA2"]

# Point of narrowest possible window
smallestWHW = 15

# Make plots of result
doPlots = True
doDetailedPlots = True

# Make a painter
myPainter = Morisot()
myPainter.setColourPalette("Teals")
myPainter.setLabelType(2)
myPainter.setEPS(True)

def main() :

  # Loop over the files. That way we could do all 4 unblindings at the same time.
  index = -1
  for pattern in matchPatterns :
  
    index = index +1

    print "\n\nBeginning flowcharting of files matching",rootFileDir+pattern+"*.root"

    # Collect list of relevant files. Everything will be drawn from these.
    collectFiles = glob.glob(rootFileDir+pattern+"*.root")
    if len(collectFiles) < 1 :
      print "No files found matching pattern",pattern,"!"
      continue

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
        # FIXME: for getting rid of global
        continue
        swiftWindow = 1000
      elif "whw" in file :
        tokens = file.split("_")
        relevant = [token for token in tokens if "whw" in token]
        if len(relevant) > 1 : print "????"
        windowSize = relevant[0].replace("whw","")
        swiftWindow = eval(windowSize)
        # FIXME
        #if swiftWindow > 22 :
          #continue
      if not swiftWindow :
        print "Could not identify swift window!"
        exit(0)
      #print "Found swiftWindow",swiftWindow

      # Get data
      # Add to dict
      try :
        theseData = searchFileData(file,permitWindow)
      except ValueError :
        print "No data created!"
        continue
      if not swiftWindow in optionsDict.keys() : optionsDict[swiftWindow] = {}
      if not function in optionsDict[swiftWindow].keys() :
        optionsDict[swiftWindow][function] = {}
      optionsDict[swiftWindow][function][permitWindow] = theseData
      if doDetailedPlots :
        windowPhrase = "permitWindow" if permitWindow else "noPermitWindow"
        plotTag = "_{0}_whw{1}_{2}".format(function,swiftWindow,windowPhrase)
        theseData.makeSearchPhasePlots(myPainter,theseData.fitLow,theseData.fitHigh,0,plotDir+"/detailedPlots/",plotTag+plotExtensions[index])

    # Put these here instead of inside the loop
    # if you want to allow cross-window-width solutions
    #gotNominal = None
    #gotAlternate = None
    #gotPossibleSignal = False
    #gotLimitCase = False

    # Now everything we want is in optionsDict. Begin flowchart.
    # Start: widest window
    for whw in sorted(optionsDict.keys(),reverse=True) :
    
      gotNominal = None
      gotAlternate = None
      gotPossibleSignal = False
      gotLimitCase = False

      # This is our stopping criterion
      if whw < smallestWHW :
        break

      materials = optionsDict[whw]
      print "Looking at window size",whw
      print materials

      # Look at no-window-permitted. Did at least two functions converge?
      useWindowPermission = False
      converged = didTwoConverge(materials,False)

      # This was the top green box I am convinced we don't need
#      if len(converged) < 2 :
#        print "Only",len(converged),"functions converged!"
#        print converged
#        print "Switching to fits with permitted windows."
#        useWindowPermission = True
#        converged = didTwoConverge(materials,True)

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
        # below: was useWindowPermission
        if materials[function][False].chi2PVal > 0.05 :
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
        gotAlternate = [alternateFunction,whw]
        
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
          print "Found nominal p-value",nomData.bumpHunterPVal,"and alternate p-value",alternateData.bumpHunterPVal
          print "One of our BH p-values is less than 0.01 and the other is not. "
          print "Is this signal?"
          # Go down a window and take another look
          continue
        
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
          # below: was useWindowPermission
          if materials[function][False].bumpHunterPVal > 0.01 :
            nBHOK = nBHOK + 1
            
        # If BH p-values are OK (> 0.01)
        print "Number of OK BH values:",nBHOK
#        if nBHOK > 1 :  # Decided that if only one function thinks it's a signal, it's not a signal.
        if nBHOK > 0 :
          
          # We have some functions with OK bump hunter p-values but not enough
          # with OK chi2 p-values.
          # Looks like a bad background but not like a signal.
          # We should go down to a smaller window.
          print "BH p-values are OK. Go to a smaller window."
          continue
        
        # If we made it here we have no more than 1 decent chi2 or bh p-value.
        # This could be signal or it could be a bad background.
        # We should look at it with a window permitted.
        print "In the ambiguous case. Could be signal or background."
        windowPermittedData = {}
        nBHOK_Outside = 0
        nChi2OK_Outside = 0
        nBothGood_Outside = 0
        for function in converged :
          if not True in materials[function].keys() :
            continue
          smallDict = {}
          smallDict["chi2All"] = materials[function][True].chi2PVal
          smallDict["BHAll"] = materials[function][True].bumpHunterPVal
          smallDict["didExcludeWindow"] = materials[function][True].excludeWindow
          if materials[function][True].excludeWindow :
            smallDict["chi2Out"] = materials[function][True].Chi2PValRemainder
            smallDict["BHOut"] = materials[function][True].BHPValRemainder
          else :
            print "BHAll is",smallDict["BHAll"]
            print "For no-window, was",materials[function][False].bumpHunterPVal
            print "This behaviour is weird. Skip this function."
            continue
          
          # Compare window locations. For a real signal, should have some overlap between the
          # window it decided to include and where it thinks the bumpiest bit is later.
          print "Bottom and top edges of window excluded are",materials[function][True].bottomWindowEdge,materials[function][True].topWindowEdge
          print "Bottom and top edge of biggest bump are",materials[function][True].bumpLowEdge,materials[function][True].bumpHighEdge
          isBumpSane = doTheyOverlap([materials[function][True].bottomWindowEdge,materials[function][True].topWindowEdge],
                                     [materials[function][True].bumpLowEdge,materials[function][True].bumpHighEdge])
          smallDict["isBumpSane"] = isBumpSane
          print "Concluded that these overlap?",isBumpSane
          
          if smallDict["chi2Out"] > 0.05 : nChi2OK_Outside = nChi2OK_Outside + 1
          if smallDict["BHOut"] > 0.01 : nBHOK_Outside = nBHOK_Outside + 1
          if smallDict["chi2Out"] > 0.05 and smallDict["BHOut"] > 0.01 and isBumpSane :
            smallDict["bothOutsideGood"] = True
            nBothGood_Outside = nBothGood_Outside + 1
          else :
            smallDict["bothOutsideGood"] = False

          windowPermittedData[function] = smallDict
        
        print windowPermittedData
        
        # Check BH and chi2 p-values outside.
        # Happy if there are two functions for which chi2out and BHout are both OK.
        # Medium happy if there is one.
        if nBothGood_Outside < 1 :

          # Bad background case. Time to go to a smaller window.
          print "Decided it is bad background, since window exclusion doesn't help."
          continue
        
        # Now we are in an acceptable case.
        # Sort results by outside-window chi2 p-value.
        # My python isn't good enough to do this automatically.
        funcsByChi2Out = getFuncsByChi2Out(windowPermittedData)

        # Let's see how many we got.
        passingFuncs = [func for func in funcsByChi2Out if windowPermittedData[func]["bothOutsideGood"]]
        
        print "The following functions had good bumphunter and chi2 p-values outside an excluded window (decreasing goodness order):"
        print passingFuncs
        
        # Can't have zero, we already checked that case.
        # And nominal is definitely first.
        gotNominal = [passingFuncs[0],whw]
        
        # If we have two good ones, we can stop here.
        if len(passingFuncs) > 1 :
          print "We found a signal! And we have a good background estimate and an alternate."
          gotPossibleSignal = True
          gotAlternate = [passingFuncs[1],whw]
          # Stop looping, we are done.
          break
        
        # If we only found 1, we might want to keep going.
        # Making this a separate case so we can iterate later if we need to.
        else :
          print "Only one good function, though we have a signal-like case. Let's try one window smaller ..."
          continue

      # END OF WHW LOOP

    # If we looked at all possible windows and gotNominal is null, we failed and go home.
    if gotNominal is None :
      print "We cry and go home!"
      continue

    # Otherwise, we reached a better conclusion.
    print "Nominal background is",gotNominal[0],"at window half-width",gotNominal[1]
    nominalData = optionsDict[gotNominal[1]][gotNominal[0]][True]
    print "Alternate background is",gotAlternate[0],"at window half-width",gotAlternate[1]
    alternateData = optionsDict[gotAlternate[1]][gotAlternate[0]][True]

    if gotPossibleSignal :
      print "We think we found a signal! Our total BumpHunter p-value (analysis result) is",nominalData.bumpHunterPVal
      if not nominalData.excludeWindow :
        print "Uh oh major bug!!!"
        exit(0)
      print "We excluded a window from",nominalData.bottomWindowEdge,"to",nominalData.topWindowEdge
      print "Outside the window, we had chi2 pvalue",nominalData.Chi2PValRemainder,"and BH pvalue",nominalData.BHPValRemainder
    else :
      print "We do not see evidence of a signal. Our global bump-hunter p-value is",nominalData.bumpHunterPVal

    # Make plots if permitted
    if doPlots :
      nominalData.makeSearchPhasePlots(myPainter,nominalData.fitLow,nominalData.fitHigh,0,plotDir,"_nominal"+plotExtensions[index])
      alternateData.makeSearchPhasePlots(myPainter,alternateData.fitLow,alternateData.fitHigh,0,plotDir,"_alternate"+plotExtensions[index])

def didTwoConverge(materials,doPermitWindow) :

  funcsWhichConverged = {}
  #orderedGoodFuncs = []
  for function in materials.keys() :
    didConverge = True
    if not doPermitWindow in materials[function].keys() :
      didConverge = False
    
    else :
      data = materials[function][doPermitWindow]

      # Check: is chi2 p-value not inf or nan
      # think this is all we need becasue data object doesn't exist if it barfs on picking things up
      if np.isinf(data.chi2PVal) or np.isnan(data.chi2PVal) :
        didConverge = False
      
      # Check: do we have any 20s in the residual? This shouldn't happen in real life.
      for bin in range(1,data.residualHist.GetNbinsX()+1) :
        if data.residualHist.GetBinContent(bin) > 19.5 :
          didConverge = False

    # Add to dictionary with chi2 p-value (which will identify best one)
    if didConverge :
      funcsWhichConverged[function] = data.chi2PVal

  # Turn dict into list in order.
  # Only issue: random if all p-values zero. Would prefer to prioritise usually good funcs...
  print funcsWhichConverged
  orderedGoodFuncs = OrderedDict(sorted(funcsWhichConverged.items(), key=itemgetter(1), reverse=True))

  return orderedGoodFuncs.keys()

def getFuncsByChi2Out(dictOfInfo) :

  smallDict = {}
  for func in dictOfInfo.keys() :
    smallDict[func] = dictOfInfo[func]["chi2Out"]
  orderedSmallDict = OrderedDict(sorted(smallDict.items(),key=itemgetter(1),reverse=True))

  return orderedSmallDict.keys()

def doTheyOverlap(range1,range2) :
  overlap = False
  range1 = sorted(range1)
  range2 = sorted(range2)
  if range1[1] > range2[0] and range1[0] < range2[1] :
    overlap = True
  return overlap

if __name__ == "__main__":
  main()


