'''
Makes 2D Efficiency and Rate Plots for Lepton and Tau L1 Triggers
Authors: T.M.Perry, A.Levine, M.Cepeda, E.Friis UW Madison
'''
from sys import argv, stdout, stderr
import ROOT
from ROOT import TH1D,TH2D
import simpleMaker as make

## Choose Plots To Draw ##
makeEfficiencyPlot = True
makeRatePlot       = False
combineRateAndEffi = False

## Choose Parameters ##
saveWhere = '../plots/'
extraName = 'lepTau2D'
ISOTHRESHOLD  = 0.20
ZEROBIAS_RATE = 15000000.00
pTRecoLepCut   = 20
pTRecoTauCut  = 20
pTL1LepCut   = 10
pTL1TauCut   = 10
binRecoLep   = 100
minRecoLep   = 15
maxRecoLep   = 115
binRecoTau  = 100
minRecoTau  = 15
maxRecoTau  = 115
canx = 900
cany = 600

binLep = [binRecoLep,minRecoLep,maxRecoLep]
binTau = [binRecoTau,minRecoTau,maxRecoTau]

baseName = saveWhere+extraName
baseName+='_lepL1%s'%(pTL1LepCut)
baseName+='_tauL1%s'%(pTL1TauCut)
if makeEfficiencyPlot == True: baseName+='_eff'
if makeRatePlot       == True: baseName+='_rate'

# Efficiency File #
eff_root_file_name = '../data/TAUefficiency.root'
eff_rlx_spot = 'rlxTauEfficiencyStage1B/Ntuple'
eff_iso_spot = 'isoTauEfficiencyStage1B/Ntuple'
eff_file = ROOT.TFile(eff_root_file_name)
eff_rlx_tree = eff_file.Get(eff_rlx_spot)
eff_iso_tree = eff_file.Get(eff_iso_spot)

# Rate File #
rate_root_file_name = '../data/UCTrates.root'
rate_rlx_spot = 'rlxTauUCTRateStage1B/Ntuple'
rate_iso_spot = 'isoTauUCTRateStage1B/Ntuple'
rate_file = ROOT.TFile(rate_root_file_name)
rate_rlx_tree = rate_file.Get(rate_rlx_spot)
rate_iso_tree = rate_file.Get(rate_iso_spot)

log = open(baseName+'.log','w')

log.write('Initial Parameters\n')
log.write('==================\n\n')
log.write('ISOTHRESHOLD  : ' + str(ISOTHRESHOLD  ) + '\n') 
log.write('ZEROBIAS_RATE : ' + str(ZEROBIAS_RATE ) + '\n') 
log.write('pTRecoLepCut  : ' + str(pTRecoLepCut  ) + '\n') 
log.write('pTRecoTauCut  : ' + str(pTRecoTauCut  ) + '\n') 
log.write('pTL1LepCut    : ' + str(pTL1LepCut    ) + '\n') 
log.write('pTL1TauCut    : ' + str(pTL1TauCut    ) + '\n') 
log.write('binLep        : ' + str(binLep        ) + '\n') 
log.write('binTau        : ' + str(binTau        ) + '\n') 
log.write('Can X         : ' + str(canx          ) + '\n')
log.write('Can Y         : ' + str(cany          ) + '\n\n')

# Style
ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(False)
ROOT.gStyle.SetOptStat(0)

tex = ROOT.TLatex()
tex.SetTextSize(0.07)
tex.SetTextAlign(11)
tex.SetNDC(True)

###  #####################################  ###
# Function to make 2D Lep-Tau Efficiency Plot #
###  #####################################  ###

def efficiencyTwoD(
 tree = None,
 axisVarLep = 'l1gPt',
 axisVarTau = 'l1gPt',
 binsLep = [10,15,115],
 binsTau = [10,20,120],
 cutLepD = '[(2>1)]',
 cutTauD = '[(2>1)]',
 cutLepN = '[(2>1)]',
 cutTauN = '[(2>1)]'
 ):
 ''' makes a 2D efficiency plot '''

 log.write('EFFICIENCY PLOT\n')
 log.write('===============\n\n')
 log.write('File: '+eff_root_file_name+'\n')
 log.write('Tree: '+tree.GetDirectory().GetName()+'\n\n')
 
 can = ROOT.TCanvas("can", "can", canx, cany)

 effHisto = TH2D("effHisto","LepTau Trigger Efficiency",
  binsLep[0],binsLep[1],binsLep[2],
  binsTau[0],binsTau[1],binsTau[2])

 denom = TH2D("denom","Denominator",
  binsLep[0],binsLep[1],binsLep[2],
  binsTau[0],binsTau[1],binsTau[2])
 numer = TH2D("numer","Numerator",
  binsLep[0],binsLep[1],binsLep[2],
  binsTau[0],binsTau[1],binsTau[2])
 
 log.write('  DENOMINATOR\n')
 denom = make.hist2D(
  tree,axisVarLep,axisVarTau,
  cutLepD,cutTauD,binsLep,binsTau,logg=log
 )

 denom.Draw('COLZ')
 denom.SetName('denom')
 r1 = raw_input("Denominator Plot: type save to save\n")
 if r1 == 'save': can.SaveAs(baseName+'_denom.png')

 log.write('  NUMERATOR\n')
 numer = make.hist2D(
  tree,axisVarLep,axisVarTau,
  cutLepN,cutTauN,binsLep,binsTau,logg=log
 )
 numer.SetName('numer')
 numer.Draw('COLZ')
 r2 = raw_input("Numerator Plot: type save to save\n")
 if r2 == 'save': can.SaveAs(baseName+'_numer.png')
 
 effHisto = numer.Clone()
 effHisto.SetName('effHisto')
 effHisto.Divide(denom)
 effHisto.Draw("COLZ")
 r3 = raw_input("Efficiency Plot: type save to save\n")
 if r3 == 'save': can.SaveAs(baseName+'_effic.png')
 
 return effHisto

###                               ###
# Call the Efficiency Plot Function #
###                               ###
if makeEfficiencyPlot:

 # define cuts
 recoLepCut  = 'recoPt>='+str(pTRecoLepCut)
 recoTauCut  = 'recoPt>='+str(pTRecoTauCut)
 l1LepCut    = 'l1gJetPt>='+str(pTL1LepCut)
 l1TauCut    = 'l1gPt>='+str(pTL1TauCut)
 isoLepCut   = '(2>1)'
 isoTauCut   = '(2>1)'
 otherLepCut = '(2>1)'
 otherTauCut = '(2>1)'

 # denominator cuts
 cutDLep = [recoLepCut]
 cutDTau = [recoTauCut]
 # numerator cuts
 cutNLep = [recoLepCut,l1LepCut,isoLepCut,otherLepCut]
 cutNTau = [recoTauCut,l1TauCut,isoTauCut,otherTauCut]
 
 region = '((l1g2RegionEt)*l1g2RegionPattern+(!(l1g2RegionPattern))*(l1gRegionEt))'
 eff = efficiencyTwoD(
  tree  = eff_rlx_tree,
  axisVarLep='l1gJetPt',
  axisVarTau='recoPt',
  binsLep  = binLep,
  binsTau = binTau,
  cutLepD = cutDLep,
  cutTauD = cutDTau,
  cutLepN = cutNLep,
  cutTauN = cutNTau,
 )

###  #######################  ###
# Function to make 2D Rate plot #
###  #######################  ###
#
#def rate2D(
#
#)


# lepBins = []
# for abin in range(binsLep[1],binsLep[2],binsLep[0]):
#  lepBins.append(abin)
# #print(lepBins)
# 
# for i in range(len(lepBins)-1):
#  lepCutA = '%s>=%s' %(axisVar,lepBins[i])
#  lepCutB = '%s<%s' %(axisVar,lepBins[i+1])
#  #print(lepCutA)
#  #print(lepCutB)
#  cutNLep.append(lepCutA)
#  cutNLep.append(lepCutB)
#  #print(cutNLep)
#  cutNLep.pop()
#  cutNLep.pop()
#
# for lepCutVal in range(binsLep[1],binsLep[2],binsLep[0]):
#  cutNLep.append(axisVar+'>%s'%(lepCutVal))
#  print(cutNLep)
#  
#  numRow = TH1D("numRow","numRow",binsTau)
#
#  for tauCutVal in range(binsTau[1],binsTau[2],binsTau[0]):
#   cutNTau.append(axisVar+'>%s'%(tauCutVal))
#   print(cutNTau)
#   cutNTau.pop()
#
#  cutNLep.pop()



log.close()

