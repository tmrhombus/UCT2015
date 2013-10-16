'''
Makes 2D Efficiency and Rate Plots for Muon and Tau L1 Triggers
Authors: T.M.Perry, A.Levine, M.Cepeda, E.Friis UW Madison
'''
from sys import argv, stdout, stderr
import ROOT
from ROOT import TH1D,TH2D
import simpleMaker as make

## Choose Plots To Draw ##
makeEfficiencyPlot = False
makeRatePlot       = False
combineRateAndEffi = False

## Choose Parameters ##
saveWhere = '../plots/'
extraName = 'muTau2D'
ISOTHRESHOLD  = 0.20
ZEROBIAS_RATE = 15000000.00
pTRecoMuCut   = 20
pTRecoTauCut  = 20
binRecoMu   = 10
minRecoMu   = 15
maxRecoMu   = 115
binRecoTau  = 10
minRecoTau  = 15
maxRecoTau  = 115
canx = 900
cany = 600

binMu  = [binRecoMu,minRecoMu,maxRecoMu]
binTau = [binRecoTau,minRecoTau,maxRecoTau]

baseName = saveWhere+extraName
if makeEfficiencyPlot == True: baseName+='_eff'
if makeRatePlot       == True: baseName+='_rate'

## Files ##    ###### MUON FILES NEED TO BE MADE ###
# Mu Efficiency
#mu_eff_name = '../data/TAUefficiency.root'
#mu_eff_rlx_spot = 'rlxTauEfficiencyStage1B/Ntuple'
#mu_eff_iso_spot = 'rlxTauEfficiencyStage1B/Ntuple'
mu_eff_name = '../data/EGefficiency.root'
mu_eff_rlx_spot = 'rlxEGEfficiencyStage1B/Ntuple'
mu_eff_iso_spot = 'rlxEGEfficiencyStage1B/Ntuple'
mu_eff_file = ROOT.TFile(mu_eff_name)
mu_eff_rlx_ntuple = mu_eff_file.Get(mu_eff_rlx_spot)
mu_eff_iso_ntuple = mu_eff_file.Get(mu_eff_iso_spot)

## Tau Efficiency
tau_eff_name = '../data/TAUefficiency.root'
tau_eff_rlx_spot = 'rlxTauEfficiencyStage1B/Ntuple'
tau_eff_iso_spot = 'rlxTauEfficiencyStage1B/Ntuple'
#tau_eff_file = ROOT.TFile(tau_eff_name)
#tau_eff_rlx_ntuple = tau_eff_file.Get(tau_eff_rlx_spot)
#tau_eff_iso_ntuple = tau_eff_file.Get(tau_eff_iso_spot)

rlxEffTauFriend = 'rlxEffTauFriend'
isoEffTauFriend = 'isoEffTauFriend'
mu_eff_rlx_ntuple.AddFriend(rlxEffTauFriend+"="+tau_eff_rlx_spot,tau_eff_name)
mu_eff_iso_ntuple.AddFriend(isoEffTauFriend+"="+tau_eff_iso_spot,tau_eff_name)

# Mu Rate
mu_rate_name = '../data/UCTrates.root'
mu_rate_ntuple_file = ROOT.TFile(mu_rate_name)
mu_rate_rlx_spot = 'rlxTauUCTRateStage1B/Ntuple'
mu_rate_iso_spot = 'rlxTauUCTRateStage1B/Ntuple'
mu_rate_rlx_ntuple = mu_rate_ntuple_file.Get(mu_rate_rlx_spot)
mu_rate_iso_ntuple = mu_rate_ntuple_file.Get(mu_rate_iso_spot)

# Tau Rate
tau_rate_name = '../data/UCTrates.root'
tau_rate_ntuple_file = ROOT.TFile(tau_rate_name)
tau_rate_rlx_spot = 'rlxTauUCTRateStage1B/Ntuple'
tau_rate_iso_spot = 'rlxTauUCTRateStage1B/Ntuple'
tau_rate_rlx_ntuple = tau_rate_ntuple_file.Get(tau_rate_rlx_spot)
tau_rate_iso_ntuple = tau_rate_ntuple_file.Get(tau_rate_iso_spot)

mu_rate_rlx_ntuple.AddFriend(tau_rate_rlx_spot,tau_rate_name)
mu_rate_iso_ntuple.AddFriend(tau_rate_iso_spot,tau_rate_name)

log = open(baseName+'.log','w')

log.write('ISOTHRESHOLD  : ' + str(ISOTHRESHOLD ) + '\n') 
log.write('ZEROBIAS_RATE : ' + str(ZEROBIAS_RATE) + '\n') 
log.write('pTRecoMuCut   : ' + str(pTRecoMuCut  ) + '\n') 
log.write('pTRecoTauCut  : ' + str(pTRecoTauCut ) + '\n') 
log.write('minL1Mu       : ' + str(minRecoMu    ) + '\n') 
log.write('maxL1Mu       : ' + str(maxRecoMu    ) + '\n') 
log.write('binL1Mu       : ' + str(binRecoMu    ) + '\n') 
log.write('minL1Tau      : ' + str(minRecoTau   ) + '\n') 
log.write('maxL1Tau      : ' + str(maxRecoTau   ) + '\n') 
log.write('binL1Tau      : ' + str(binRecoTau   ) + '\n') 
log.write('Can X         : ' + str(canx         ) + '\n')
log.write('Can Y         : ' + str(cany         ) + '\n\n')

# Style
ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(False)
ROOT.gStyle.SetOptStat(0)

tex = ROOT.TLatex()
tex.SetTextSize(0.07)
tex.SetTextAlign(11)
tex.SetNDC(True)

###                            ###
# Make 2D Mu-Tau Efficiency Plot #
###                            ###

def efficiencyTwoD(
 ntupleMu = None,
 effTauFriend = None,
 axisVar = 'l1gPt',
 recoMuCut='(2>1)',
 recoTauCut='(2>1)',
 isoMuCut='(2>1)',
 isoTauCut='(2>1)',
 binsMu=[10,15,115],
 binsTau=[10,20,120]):
 ''' Loops over making 1D histograms to form a 2D efficiency plot'''
 
 can = ROOT.TCanvas("can", "can", canx, cany)

 effHisto = TH2D("effHisto","MuTau Trigger Efficiency",
  binsMu[0],binsMu[1],binsMu[2],
  binsTau[0],binsTau[1],binsTau[2])

 denom = TH2D("denom","Denominator",
  binsMu[0],binsMu[1],binsMu[2],
  binsTau[0],binsTau[1],binsTau[2])
 numer = TH2D("numer","Numerator",
  binsMu[0],binsMu[1],binsMu[2],
  binsTau[0],binsTau[1],binsTau[2])
 
 cutDMu  = [recoMuCut]
 cutNMu  = [recoMuCut]
 cutDTau = [recoTauCut]
 cutNTau = [recoTauCut]
 log.write('Cut D Mu:  '+str(cutDMu )+'\n')
 log.write('Cut D Tau: '+str(cutDTau)+'\n')
 den = make.hist2Dfriend(
  ntupleMu,effTauFriend,axisVar,axisVar,cutDMu,cutDTau,[1,0.,999.],[1,0.,999.]
 )
 sf = den.GetBinContent(1,1)
 for i in range(binsTau[0]):
  for j in range(binsMu[0]):
   denom.SetBinContent(i+1,j+1,sf)
 print(sf)
 denom.Draw('COLZ')
 denom.SetName('denom')
 can.SaveAs(baseName+'_denom.png')
 #raw_input("do you like the denominator plot?")

 numer = make.hist2Dfriend(
  ntupleMu,effTauFriend,axisVar,axisVar,cutDMu,cutDTau,binsMu,binsTau
 )
 numer.SetName('numer')
 numer.Draw('COLZ')
 can.SaveAs(baseName+'_numer.png')
 #raw_input("do you like the numerator plot?")
 
 effHisto = numer.Clone()
 effHisto.SetName('effHisto')
 effHisto.Divide(denom)
 effHisto.Draw("COLZ")
 can.SaveAs(baseName+'_effic.png')
 #raw_input("do you like the efficiency plot?")
 
# muBins = []
# for abin in range(binsMu[1],binsMu[2],binsMu[0]):
#  muBins.append(abin)
# #print(muBins)
# 
# for i in range(len(muBins)-1):
#  muCutA = '%s>=%s' %(axisVar,muBins[i])
#  muCutB = '%s<%s' %(axisVar,muBins[i+1])
#  #print(muCutA)
#  #print(muCutB)
#  cutNMu.append(muCutA)
#  cutNMu.append(muCutB)
#  #print(cutNMu)
#  cutNMu.pop()
#  cutNMu.pop()
#
# for muCutVal in range(binsMu[1],binsMu[2],binsMu[0]):
#  cutNMu.append(axisVar+'>%s'%(muCutVal))
#  print(cutNMu)
#  
#  numRow = TH1D("numRow","numRow",binsTau)
#
#  for tauCutVal in range(binsTau[1],binsTau[2],binsTau[0]):
#   cutNTau.append(axisVar+'>%s'%(tauCutVal))
#   print(cutNTau)
#   cutNTau.pop()
#
#  cutNMu.pop()
 return effHisto


eff = efficiencyTwoD(
 ntupleMu  = mu_eff_rlx_ntuple,
 effTauFriend = rlxEffTauFriend,
 axisVar='l1gPt',
 recoMuCut  = 'recoPt>='+str(pTRecoMuCut ),
 recoTauCut = 'recoPt>='+str(pTRecoTauCut),
 isoMuCut  = '(2>1)',
 isoTauCut = '(2>1)',
 binsMu  = binMu,
 binsTau = binTau
)

eff.Draw()

log.close()

