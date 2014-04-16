'''
Makes 2D Efficiency and Rate Plots for Lepton and Tau L1 Triggers
Authors: T.M.Perry, A.Levine, M.Cepeda, E.Friis UW Madison
'''
from sys import argv, stdout, stderr
import ROOT
from ROOT import TH1D,TH2D
import simpleMaker as make

## Choose Plots To Draw ##
makeEfficiencyPlot = False
makeRatePlot       = True
combineRateAndEffi = False
doIso              = False

if combineRateAndEffi: 
 makeEfficiencyPlot = True
 makeRatePlot       = True

## Choose Parameters ##
saveWhere = '../plots/XX_'
extraName = 'muTau2D'
ISOTHRESHOLD  = 0.20
ZEROBIAS_RATE = 15000000.00
pTRecoLepCut   = 15
pTRecoTauCut  = 20
pTL1LepCut   = 15
pTL1TauCut   = 20

binRecoLep   = 5
minRecoLep   = 15
maxRecoLep   = 115

binRecoTau  = 5
minRecoTau  = 15
maxRecoTau  = 115

canx = 900
cany = 600

binLep = [binRecoLep,minRecoLep,maxRecoLep]
binTau = [binRecoTau,minRecoTau,maxRecoTau]

baseName = saveWhere+extraName
baseName+='_lepL1%s'%(pTL1LepCut)
baseName+='_tauL1%s'%(pTL1TauCut)
if doIso: baseName+='_iso'
#if makeEfficiencyPlot : baseName+='_eff'
#if makeRatePlot : baseName+='_rate'

# Efficiency File #
eff_root_file_name = '../data/uctEfficiencyMuJetSkim.root'
eff_rlx_spot = 'Efficiency2D/Ntuple'
eff_iso_spot = 'Efficiency2D/Ntuple'
eff_file = ROOT.TFile(eff_root_file_name)
eff_rlx_tree = eff_file.Get(eff_rlx_spot)
eff_iso_tree = eff_file.Get(eff_iso_spot)

# Rate File #
rate_root_file_name = '../data/uctRateMuJetSkim.root'
rate_rlx_spot = 'Rate2D/Ntuple'
rate_iso_spot = 'Rate2D/Ntuple'
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
 effHisto.GetXaxis().SetTitle('p_{T}^{#tau}')
 effHisto.GetYaxis().SetTitle('p_{T}^{#mu}')
 r3 = raw_input("Efficiency Plot: type save to save\n")
 if r3 == 'save': can.SaveAs(baseName+'_effic.png')
 
 return effHisto

###                               ###
# Call the Efficiency Plot Function #
###                               ###
if makeEfficiencyPlot:

 # define cuts
 recoLepCut  = 'ptMu>='+str(pTRecoLepCut)
 recoTauCut  = 'ptTau>='+str(pTRecoTauCut)
 l1LepCut    = 'ptL1Mu>='+str(pTL1LepCut)
 l1TauCut    = 'ptL1Tau>='+str(pTL1TauCut)
 matchLep    = 'matchL1Mu'
 matchTau    = 'matchL1Tau'

 region = '((l1g2RegionEt)*l1g2RegionPattern+(!(l1g2RegionPattern))*(l1gRegionEt))'
 isoLepCut   = '((l1gJetPt-'+region+')/'+region+' <'+str(ISOTHRESHOLD)+')'
 isoTauCut   = '((l1gJetPt-'+region+')/'+region+' <'+str(ISOTHRESHOLD)+')'
 otherLepCut = '(2>1)'
 otherTauCut = '(2>1)'

 # denominator cuts
 cutDLep = [recoLepCut]
 cutDTau = [recoTauCut]
 # numerator cuts
 cutNLep = [recoLepCut,l1LepCut,matchLep,otherLepCut]
 cutNTau = [recoTauCut,l1TauCut,matchTau,otherTauCut]
 if doIso:
  cutNLep.append(isoLepCut)
  cutNTau.append(isoTauCut)
 
 eff = efficiencyTwoD(
  tree  = eff_rlx_tree,
  axisVarLep='ptMu',
  axisVarTau='ptTau',
  binsLep  = binLep,
  binsTau = binTau,
  cutLepD = cutDLep,
  cutTauD = cutDTau,
  cutLepN = cutNLep,
  cutTauN = cutNTau,
 )
 eff.SetName('eff')

###  #######################  ###
# Function to make 2D Rate plot #
###  #######################  ###

def rate2D(
 tree = None,
 axisVarLep='ptMu',
 axisVarTau='ptTau',
 binsLep = [10,10,100], 
 binsTau = [10,10,100],
 cutLepR = ['(2>1)'], 
 cutTauR = ['(2>1)'] 
):

 log.write('RATE PLOT\n')
 log.write('=========\n\n')
 log.write('File: '+rate_root_file_name+'\n')
 log.write('Tree: '+tree.GetDirectory().GetName()+'\n\n')
 #log.write('X axis: %s\n'%(axisVarTau))
 #log.write('Y axis: %s\n'%(axisVarLep))

 can = ROOT.TCanvas("can", "can", canx, cany)

 preRateHisto = TH2D("preRateHisto","Events At pT Levels",
  binsLep[0],binsLep[1],binsLep[2],
  binsTau[0],binsTau[1],binsTau[2])
 rateHisto = TH2D("rateHisto","Integrated Rate",
  binsLep[0],binsLep[1],binsLep[2],
  binsTau[0],binsTau[1],binsTau[2])

 preRateHisto = make.hist2D(tree,axisVarLep,axisVarTau,cutLepR,cutTauR,binsLep,binsTau,logg=log)
 preRateHisto.SetName('preRateHisto')
 preRateHisto.Draw('text')
 #preRateHisto.Draw('colz')
 r4 = raw_input('Pre Rate Plot: type save to save\n')
 if r4 == 'save': can.SaveAs(baseName+'_preRate.png') 

 rateHisto = preRateHisto.Clone()
 rateHisto.SetName('rateHisto')
 for i in range(binsLep[0]):
  #binL = binsLep[0]-i
  binL = binsLep[0]-i-1 #to test handling of overflows
  for j in range(binsTau[0]):
   #print('i=%s'%(i))
   #print('j=%s'%(j))
   #binT = binsTau[0]-j
   binT = binsTau[0]-j-1 #to test handling of overflows
   #print('(%s,%s)'%(binT,binL))
   this  = rateHisto.GetBinContent(binT,binL)
   right = rateHisto.GetBinContent(binT+1,binL)
   up    = rateHisto.GetBinContent(binT,binL+1)
   diag  = rateHisto.GetBinContent(binT+1,binL+1)
   #print('%s, %s, %s, %s'%(this,right,up,diag))
   newEntry = this+right+up-diag
   if i==0 and j==0: newEntry = this+right+up+diag
   if i==0 and j!=0: newEntry = this+right+up
   if i!=0 and j==0: newEntry = this+right+up
   #print(newEntry)
   #print('')
   rateHisto.SetBinContent(binT,binL,newEntry)
 rateHisto.GetXaxis().SetTitle('p_{T}^{#tau}')
 rateHisto.GetYaxis().SetTitle('p_{T}^{#mu}')
 rateHisto.Draw('text')
 #rateHisto.Draw('colz')
 r5 = raw_input('Rate Plot: type save to save\n')
 if r5 == 'save': can.SaveAs(baseName+'_rate.png')
 return rateHisto

if makeRatePlot:
 region = 'max((region2Disc.patternPass[0]*(region2Disc.totalEt[0])+((!region2Disc.patternPass[0])*(regionPt[0]))), pt[0])'
 # define cuts
 isoLepCut   = '((jetPt[0] - '+region+')/'+region+'<'+str(ISOTHRESHOLD)+')'
 isoTauCut   = '((jetPt[0] - '+region+')/'+region+'<'+str(ISOTHRESHOLD)+')'
 otherLepCut = '(2>1)'
 otherTauCut = '(2>1)'

 cutRLep = [otherLepCut]
 cutRTau = [otherTauCut]
 if doIso:
  cutRLep.append(isoLepCut)
  cutRTau.append(isoTauCut)

 rate = rate2D(
  tree = rate_rlx_tree,
  axisVarLep='ptMu',
  axisVarTau='ptTau',
  binsLep  = binLep,
  binsTau = binTau,
  cutLepR = cutRLep,
  cutTauR = cutRTau,
 )
 rate.SetName('rate')

if combineRateAndEffi:
 
 can = ROOT.TCanvas("can", "can", canx, cany)
 
 eff.Draw("colz")
 rate.Draw("cont3, sames")

 r6 = raw_input('Combined Plot: type save to save\n')
 if r6=='save': can.SaveAs(baseName+'_combined.png')

log.close()

