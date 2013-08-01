'''
Tau Resolution Plots for L1b
Author: T.M.Perry UW Madison
'''
from sys import argv, stdout, stderr
import ROOT
from ROOT import *

##################
# Set Parameters #
##################
saveWhere='../plots/Tau_L1b_resolution_2reg'

#########
# Files #
#########
# Efficiency
eff_ntuple = '../data/TAUefficiency.root'
cur_ntuple = '../data/TAUefficiency.root'
#eff_ntuple = '../data/Laura/uct_tau_efficiency.root'
uct_ntuple_file = ROOT.TFile(eff_ntuple)
cur_ntuple_file = ROOT.TFile(cur_ntuple)
eff_l1b_spot = 'rlxTauEfficiencyStage1B/Ntuple'
eff_cur_spot = 'rlxTauEfficiency/Ntuple'
eff_l1b_tau_ntuple = uct_ntuple_file.Get(eff_l1b_spot)
eff_cur_tau_ntuple = cur_ntuple_file.Get(eff_cur_spot)

#########
# STYLE #
#########
ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

tex = ROOT.TLatex()
tex.SetTextSize(0.03)
tex.SetTextAlign(11)
tex.SetNDC(True)

canvas = ROOT.TCanvas("asdf", "adsf", 800, 800)

l1Four='(max(max(l1g2RegionEt*l1g2RegionPattern,l1g3RegionPattern*l1g3RegionEt),l1g4RegionPattern*l1g4RegionEt) + (!(l1g2RegionPattern))*max(l1gRegionEt,l1gPt))'
l1Three='(max(l1g2RegionEt*l1g2RegionPattern,l1g3RegionPattern*l1g3RegionEt) + (!(l1g2RegionPattern))*max(l1gRegionEt,l1gPt))'
l1Two='((l1g2RegionEt)*l1g2RegionPattern + (!(l1g2RegionPattern))*(l1gRegionEt))'

match = '(l1gMatch)'
#l1pT = '(l1gPt > 40)'
#l1pT = '((l1g2RegionEt > 40))'
#l1pT = '(l1g2RegionPattern*(l1g2RegionEt > 40))'
#l1pT = '(' + l1Two + '> 10)'
#recopt = '(recoPt>0)'
recopT = '(recoPt>40)'
lowPV = '(nPVs < 30)'
hiPV = '(nPVs >= 30)'
#barrel = '(abs(recoEta)<3)'

curMatch = '(l1Match)'
curpT = '(l1Pt > 40)'
#
resCuts=[]
#resCut0='('+match+'&&'+recopT+'&&'+l1pT+'&&'+hiPV+')'
#resCut0='('+match+'&&'+recopT+'&&'+l1pT+'&&'+lowPV+')'
#resCut0='('+match+'&&'+recopT+'&&'+l1pT+')'
resCut0='('+match+'&&'+recopT+')'
#resCut1='('+match+'&&'+recopt+'&&'+barrel+')'

resCuts.append(resCut0)
#resCuts.append(resCut1)

curCut='('+curMatch+'&&'+recopT+')'
#curCut='('+curMatch+'&&'+curpT+'&&'+recopT+')'
#
Xaxes=[]
#axis0='(recoPt-'+l1Two+')/recoPt'
#axis0='(recoPt-'+l1Three+')/recoPt'
axis0='(recoPt-'+l1Two+')/recoPt'
#axis1='(recoPt-max(l1gPt,l1gRegionEt))/recoPt'
#axis2='(recoPt-max(l1gPt,l1g2RegionEt))/recoPt'
#axis3='(recoPt-max(l1gPt,l1g3RegionEt))/recoPt'
#axis4='(recoPt-max(l1gPt,l1g4RegionEt))/recoPt'
#axis5='(recoPt-'+l1Two+')/recoPt'
#axis6='(recoPt-'+l1Three+')/recoPt'
#axis7='(recoPt-'+l1Four+')/recoPt'
axisCur = '(recoPt-l1Pt)/recoPt'

Xaxes.append(axis0)
#Xaxes.append(axis1)
#Xaxes.append(axis2)
#Xaxes.append(axis3)
#Xaxes.append(axis4)
#Xaxes.append(axis5)
#Xaxes.append(axis6)
#Xaxes.append(axis7)

j=0
#for cut,Xaxis in zip(resCuts,Xaxes):
for Xaxis in Xaxes:
 i=0
 for cut in resCuts:
  old = ROOT.TH1F("old","old",50,-2,2)
  new = ROOT.TH1F("new","new",50,-2,2)
 
  eff_cur_tau_ntuple.Draw(axisCur+'>>old',curCut)
#  eff_rlx_tau_ntuple.Draw(Xaxis+'>>old',resCut0)
  eff_l1b_tau_ntuple.Draw(Xaxis+'>>new',cut)
 
  binmin=old.GetXaxis().FindBin(-2)
  binmax=old.GetXaxis().FindBin(2)
 
  old.Scale(1.0/old.Integral(binmin,binmax))
  new.Scale(1.0/new.Integral(binmin,binmax))
#  old.Scale(1.0/old.Integral())
#  new.Scale(1.0/new.Integral())
 
  old.SetMaximum(0.19)
  #old.SetMaximum(1.2*max(old.GetMaximum(),new.GetMaximum()))
  old.GetXaxis().SetTitle('1 - p_{T}^{L1}/p_{T}^{reco}')
  old.SetTitle('')
  old.SetLineColor(ROOT.EColor.kRed)
  old.SetLineWidth(2)
 
  new.SetLineColor(ROOT.EColor.kBlue)
  new.SetLineWidth(2)
 
  leg = ROOT.TLegend(0.65,0.45,0.89,0.7,'','brNDC')
  leg.SetFillColor(ROOT.EColor.kWhite)
  leg.SetBorderSize(0)
  leg.AddEntry(old,'current')
  leg.AddEntry(new,'upgrade')
  
  old.Draw()
  new.Draw('sames')
  leg.Draw()
 
  tex.SetTextAlign(31)
#  tex.DrawLatex(0.89,0.9,'Cut '+str(i))
#  tex.DrawLatex(0.89,0.85,'New Cut: '+cut)
 
  canvas.SaveAs(saveWhere+'.png')
  i+=1
 j+=1
