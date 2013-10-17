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

binLep  = [binRecoLep,minRecoLep,maxRecoLep]
binTau = [binRecoTau,minRecoTau,maxRecoTau]

baseName = saveWhere+extraName
baseName+='_lepL1%s'%(pTL1LepCut)
baseName+='_tauL1%s'%(pTL1TauCut)
if makeEfficiencyPlot == True: baseName+='_eff'
if makeRatePlot       == True: baseName+='_rate'

## Files ##    ###### MUON FILES NEED TO BE MADE ###
# Lep Efficiency
#lep_eff_name = '../data/TAUefficiency.root'
#lep_eff_rlx_spot = 'rlxTauEfficiencyStage1B/Ntuple'
#lep_eff_iso_spot = 'rlxTauEfficiencyStage1B/Ntuple'
lep_eff_name = '../data/EGefficiency.root'
lep_eff_rlx_spot = 'rlxEGEfficiencyStage1B/Ntuple'
lep_eff_iso_spot = 'rlxEGEfficiencyStage1B/Ntuple'
lep_eff_file = ROOT.TFile(lep_eff_name)
lep_eff_rlx_ntuple = lep_eff_file.Get(lep_eff_rlx_spot)
lep_eff_iso_ntuple = lep_eff_file.Get(lep_eff_iso_spot)

# Tau Efficiency
tau_eff_name = '../data/TAUefficiency.root'
tau_eff_rlx_spot = 'rlxTauEfficiencyStage1B/Ntuple'
tau_eff_iso_spot = 'rlxTauEfficiencyStage1B/Ntuple'

rlxEffTauFriend = 'rlxEffTauFriend'
isoEffTauFriend = 'isoEffTauFriend'
lep_eff_rlx_ntuple.AddFriend(rlxEffTauFriend+"="+tau_eff_rlx_spot,tau_eff_name)
lep_eff_iso_ntuple.AddFriend(isoEffTauFriend+"="+tau_eff_iso_spot,tau_eff_name)

# Lep Rate
lep_rate_name = '../data/UCTrates.root'
lep_rate_rlx_spot = 'rlxEGUCTRateStage1B/Ntuple'
lep_rate_iso_spot = 'rlxEGUCTRateStage1B/Ntuple'
#lep_rate_rlx_spot = 'rlxTauUCTRateStage1B/Ntuple'
#lep_rate_iso_spot = 'rlxTauUCTRateStage1B/Ntuple'
lep_rate_ntuple_file = ROOT.TFile(lep_rate_name)
lep_rate_rlx_ntuple = lep_rate_ntuple_file.Get(lep_rate_rlx_spot)
lep_rate_iso_ntuple = lep_rate_ntuple_file.Get(lep_rate_iso_spot)

# Tau Rate
tau_rate_name = '../data/UCTrates.root'
tau_rate_rlx_spot = 'rlxTauUCTRateStage1B/Ntuple'
tau_rate_iso_spot = 'rlxTauUCTRateStage1B/Ntuple'
#tau_rate_ntuple_file = ROOT.TFile(tau_rate_name)
#tau_rate_rlx_ntuple = tau_rate_ntuple_file.Get(tau_rate_rlx_spot)
#tau_rate_iso_ntuple = tau_rate_ntuple_file.Get(tau_rate_iso_spot)

rlxRateTauFriend = 'rlxRateTauFriend'
isoRateTauFriend = 'isoRateTauFriend'
lep_rate_rlx_ntuple.AddFriend(rlxRateTauFriend+'='+tau_rate_rlx_spot,tau_rate_name)
lep_rate_iso_ntuple.AddFriend(isoRateTauFriend+'='+tau_rate_iso_spot,tau_rate_name)

log = open(baseName+'.log','w')

log.write('Initial Parameters\n')
log.write('==================\n\n')
log.write('ISOTHRESHOLD  : ' + str(ISOTHRESHOLD  ) + '\n') 
log.write('ZEROBIAS_RATE : ' + str(ZEROBIAS_RATE ) + '\n') 
log.write('pTRecoLepCut  : ' + str(pTRecoLepCut  ) + '\n') 
log.write('pTRecoTauCut  : ' + str(pTRecoTauCut  ) + '\n') 
log.write('pTL1LepCut    : ' + str(pTL1LepCut    ) + '\n') 
log.write('pTL1TauCut    : ' + str(pTL1TauCut    ) + '\n') 
log.write('minL1Lep      : ' + str(minRecoLep    ) + '\n') 
log.write('maxL1Lep      : ' + str(maxRecoLep    ) + '\n') 
log.write('binL1Lep      : ' + str(binRecoLep    ) + '\n') 
log.write('minL1Tau      : ' + str(minRecoTau    ) + '\n') 
log.write('maxL1Tau      : ' + str(maxRecoTau    ) + '\n') 
log.write('binL1Tau      : ' + str(binRecoTau    ) + '\n') 
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

###                                        ###
# Function to make 2D Lep-Tau Efficiency Plot #
###                                        ###

def efficiencyTwoD(
 ntupleLep = None,
 effTauFriend = None,
 axisVarLep = 'l1gPt',
 axisVarTau = 'l1gPt',
 recoLepCut='(2>1)',
 recoTauCut='(2>1)',
 l1LepCut='(2>1)',
 l1TauCut='(2>1)',
 isoLepCut='(2>1)',
 isoTauCut='(2>1)',
 region = 'l1gRegionEt',
 binsLep=[10,15,115],
 binsTau=[10,20,120]
 ):
 ''' makes a 2D efficiency plot'''
 
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
 
 cutDLep  = [recoLepCut]
 cutNLep  = [recoLepCut]
 cutDTau = [recoTauCut]
 cutNTau = [recoTauCut]
 #log.write('Cut D Lep: '+str(cutDLep)+'\n')
 #log.write('Cut D Tau: '+str(cutDTau)+'\n')
 #den = make.hist2Dfriend(
 # ntupleLep,effTauFriend,axisVarLep,axisVarTau,cutDLep,cutDTau,[1,0.,999.],[1,0.,999.]
 #)
 #sf = den.GetBinContent(1,1)
 #for i in range(binsTau[0]):
 # for j in range(binsLep[0]):
 #  denom.SetBinContent(i+1,j+1,sf)
 #print(sf)
 
 log.write('  DENOMINATOR\n')
 denom = make.hist2Dfriend(
  ntupleLep,effTauFriend,axisVarLep,axisVarTau,cutDLep,cutDTau,binsLep,binsTau,logg=log
 )

 denom.Draw('COLZ')
 denom.SetName('denom')
 r1 = raw_input("Denominator Plot: type save to save\n")
 if r1 == 'save': can.SaveAs(baseName+'_denom.png')

 log.write('  NUMERATOR\n')
 cutNLep.append('l1gMatch')
 cutNLep.append(l1LepCut)
 cutNTau.append('l1gMatch')
 cutNTau.append(l1TauCut)
 #numer = make.hist2DfriendNum(
 # ntupleLep,effTauFriend,axisVarLep,'((rlxEffTauFriend.l1g2RegionEt)*rlxEffTauFriend.l1g2RegionPattern+(!(rlxEffTauFriend.l1g2RegionPattern))*(rlxEffTauFriend.l1gRegionEt))',cutNLep,cutNTau,binsLep,binsTau,logg=log
 #)
 numer = make.hist2Dfriend(
  ntupleLep,effTauFriend,axisVarLep,axisVarTau,cutNLep,cutNTau,binsLep,binsTau,logg=log
 )
 #numer = make.hist2Dfriend(
 # ntupleLep,effTauFriend,axisVarLep,region,cutNLep,cutNTau,binsLep,binsTau,logg=log
 #)
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
 eff = efficiencyTwoD(
  ntupleLep  = lep_eff_rlx_ntuple,
  effTauFriend = rlxEffTauFriend,
  axisVarLep='recoPt',
  axisVarTau='recoPt',
  #axisVarLep='l1gPt',
  #axisVarTau='l1gPt',
  recoLepCut = 'recoPt>='+str(pTRecoLepCut),
  recoTauCut = 'recoPt>='+str(pTRecoTauCut),
  l1LepCut = 'l1gPt>='+str(pTL1LepCut),
  l1TauCut = 'l1gPt>='+str(pTL1TauCut),
  isoLepCut  = '(2>1)',
  isoTauCut = '(2>1)',
  region = '((l1g2RegionEt)*l1g2RegionPattern+(!(l1g2RegionPattern))*(l1gRegionEt))',
  binsLep  = binLep,
  binsTau = binTau
 )

###                           ###
# Function to make 2D Rate plot #
###                           ###
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

