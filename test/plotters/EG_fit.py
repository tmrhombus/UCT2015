#!/usr/bin/env python
import ROOT
import random
from ROOT import *
from array import array
eff_file = ROOT.TFile("../data/EG_Iso40_Efficiency.root")
#eff_file = ROOT.TFile("../data/EG_Iso30_Efficiency.root")
#eff_file = ROOT.TFile("../data/EG_Iso25_Efficiency.root")
#eff_file = ROOT.TFile("../data/EG_Iso20_Efficiency.root")
#eff_file = ROOT.TFile("../data/EG_Iso15_Efficiency.root")

eg_rlx_eff_ntuple = eff_file.Get("rlxEGEfficiency/Ntuple")
eg_iso_eff_ntuple = eff_file.Get("isoEGEfficiency/Ntuple")
saveWhere='../plots/Iso40/EG_Iso40_'
#saveWhere='../plots/Iso30/EG_Iso30'
#saveWhere='../plots/Iso25/EG_Iso25'
#saveWhere='../plots/Iso20/EG_Iso20'
#saveWhere='../plots/Iso15/EG_Iso15'
 
canvas = ROOT.TCanvas("asdf", "adsf", 600, 600)
rangeMax=100

def get_pt95(formula):
    for i in range(rangeMax):
        if formula.Eval(i) / formula.GetParameter(0) > 0.95:
            return i
    return rangeMax

def make_turnon(ntuple,l1_cut, color, name, fix_plateau=None,save=False, isIso=False):
    if not isIso:
     ntuple.Draw("recoPt>>denom(20, 0, %i)"%rangeMax, "", "goff")
    if isIso:
     ntuple.Draw("recoPt>>denom(20, 0, %i)"%rangeMax, "(dr03CombinedEt/recoPt)<0.2", "goff")
    ntuple.Draw("recoPt>>num(20, 0, %i)"%rangeMax, l1_cut, "goff")
    denom = ROOT.gDirectory.Get("denom")
    num = ROOT.gDirectory.Get("num")
    graph = ROOT.TGraphAsymmErrors(num, denom)
    graph.SetMarkerColor(color)
    graph.SetMarkerStyle(20)
    formula = ROOT.TF1('fitter' + str(random.randint(0, 1000)),
                       "[0]*(0.5*(tanh([1]*(x-[2]))+1))", 0, rangeMax)
    formula.SetParName(0, 'plateau')
    formula.SetParName(1, 'width')
    formula.SetParName(2, 'threshold')
    formula.SetParameter(0, 0.95)
    formula.SetParLimits(0, 0.1, 1.01)
    if fix_plateau is not None:
        print 'fix plat'
        formula.FixParameter(0, fix_plateau)
    formula.SetParameter(1, 1. / 10)
    formula.SetParameter(2, 30)
    formula.SetLineColor(color)
    graph.Fit(formula)
    # refit, not using the inefficient junk at start of curve
    formula.SetRange(formula.GetParameter(2), rangeMax)
    graph.Fit(formula, "R")
    graph.Draw("ape")
    graph.GetHistogram().SetMaximum(1.1)
    graph.GetHistogram().SetMinimum(0)
    pt95 = get_pt95(formula)
    graph.GetHistogram().GetXaxis().SetTitle('pt95 = %i' % pt95)
    if save==True:
     canvas.SaveAs(saveWhere+name + ".png")
    return graph, formula, pt95

ISOTHRESHOLD=0.20

tex = ROOT.TLatex()
tex.SetNDC(True)
tex.SetTextAlign(11)
tex.SetTextSize(0.03)

isoCut='(l1gPt>=63||(l1gJetPt-l1gPt)/l1gPt<%0.1f)'%(ISOTHRESHOLD)
IDCut='(l1gMatch && dr03CombinedEt<0.2)'
TauCut='(2>1)'
#TauCut='(!l1gTauVeto&&!l1gMIP)'

l1ptVal=array('d',[20,25,30,35,40])#,45])
colors=[ROOT.EColor.kRed,
ROOT.EColor.kOrange,
ROOT.EColor.kYellow,
ROOT.EColor.kGreen,
ROOT.EColor.kBlue,
ROOT.EColor.kViolet]
uct_iso95=array('d',[])
uct_rlx95=array('d',[])
l1_iso95=array('d',[])
l1_rlx95=array('d',[])
for pt,color in zip(l1ptVal,colors):
 l1PtCut = '(l1Pt>%i)'%pt
 l1gPtCut = '(l1gPt>%i)'%pt

 #cutI=isoCut +'&&'+IDCut+'&&'+TauCut+'&&'+l1gPtCut
 cutUCT_I='l1gMatch && (dr03CombinedEt/recoPt)<0.2 && '+l1gPtCut
 cutUCT_R='l1gMatch &&'+l1gPtCut
 cutL1_I='l1Match && (dr03CombinedEt/recoPt)<0.2 && '+l1PtCut
 cutL1_R='l1Match &&  '+l1PtCut
  
 resultUCTIso = make_turnon(eg_iso_eff_ntuple,cutUCT_I,color,'pt%i_UCTIso'%pt,save=True,isIso=True)
 #resultIso = make_turnon(eg_eff_ntuple,cutI,color,'pt%i_Iso'%pt,save=True)
 resultUCTRlx = make_turnon(eg_rlx_eff_ntuple,cutUCT_R,color,'pt%i_UCTRlx'%pt,save=True)
 resultL1Iso  = make_turnon(eg_iso_eff_ntuple,cutL1_I,color,'pt%i_L1Iso'%pt,save=True,isIso=True)
 resultL1Rlx  = make_turnon(eg_rlx_eff_ntuple,cutL1_R,color,'pt%i_L1Rlx'%pt,save=True)
 uct_iso95.append(resultUCTIso[2])
 uct_rlx95.append(resultUCTRlx[2])
 l1_iso95.append(resultL1Iso[2])
 l1_rlx95.append(resultL1Rlx[2])
#print(l1ptVal)
#print(iso95)
#print(non95)
#print(cur95)

nrPts=len(l1ptVal)
xmin=min(l1ptVal)-5
xmax=max(l1ptVal)+10
ymin=min(min(uct_iso95),min(uct_rlx95),min(l1_iso95),min(l1_rlx95))-5
ymax=max(max(uct_iso95),max(uct_rlx95),max(l1_iso95),max(l1_rlx95))+5
uRColor=ROOT.EColor.kGreen+3
uIColor=ROOT.EColor.kBlue
cRColor=ROOT.EColor.kRed
cIColor=ROOT.EColor.kViolet-7
uRMarker=20
uIMarker=21
cRMarker=22
cIMarker=23
uISize=1.5
uRSize=1.5
cISize=1.5
cRSize=1.5

lineFit = ROOT.TF1('lineFit'+str(random.randint(0, 1000)),
   "[0]*x+[1]", 0, rangeMax)
lineFit.SetParName(0,'m')
lineFit.SetParName(1,'b')

can = ROOT.TCanvas('can','can',800,800)
can.SetLogy(False)
frame = TH1F('frame','',1,xmin,xmax)
frame.SetMinimum(ymin)
frame.SetMaximum(ymax)
frame.SetStats(False)
frame.GetXaxis().SetTitle('L1 Cut')
frame.GetYaxis().SetTitle('(RECO) pT95')
frame.SetTitle('')
frame.Draw()

uIgraph=ROOT.TGraph(nrPts,l1ptVal,uct_iso95)
uIgraph.SetMarkerColor(uIColor)
uIgraph.SetMarkerStyle(uIMarker)
uIgraph.SetMarkerSize(uISize)
lineFit.SetLineColor(uIColor)
uIgraph.Fit(lineFit)
uIgraph.Draw('P')
tex.DrawLatex(0.5,0.3,'UCT Iso: pT95 = %0.01f L1 + %0.1f'
  %(lineFit.GetParameter(0),lineFit.GetParameter(1)))

uRgraph=ROOT.TGraph(nrPts,l1ptVal,uct_rlx95)
uRgraph.SetMarkerColor(uRColor)
uRgraph.SetMarkerStyle(uRMarker)
uRgraph.SetMarkerSize(uRSize)
lineFit.SetLineColor(uRColor)
uRgraph.Fit(lineFit)
uRgraph.Draw('P')
tex.DrawLatex(0.5,0.25,'UCT Rlx: pT95 = %0.01f L1 + %0.1f'
  %(lineFit.GetParameter(0),lineFit.GetParameter(1)))
uRgraph.Draw('P')

cIgraph=ROOT.TGraph(nrPts,l1ptVal,l1_iso95)
cIgraph.SetMarkerColor(cIColor)
cIgraph.SetMarkerStyle(cIMarker)
cIgraph.SetMarkerSize(cISize)
lineFit.SetLineColor(cIColor)
cIgraph.Fit(lineFit)
cIgraph.Draw('P')
tex.DrawLatex(0.5,0.2,'Current Iso: pT95 = %0.01f L1 + %0.1f'
  %(lineFit.GetParameter(0),lineFit.GetParameter(1)))
cIgraph.Draw('P')

cRgraph=ROOT.TGraph(nrPts,l1ptVal,l1_rlx95)
cRgraph.SetMarkerColor(cRColor)
cRgraph.SetMarkerStyle(cRMarker)
cRgraph.SetMarkerSize(cRSize)
lineFit.SetLineColor(cRColor)
cRgraph.Fit(lineFit)
cRgraph.Draw('P')
tex.DrawLatex(0.5,0.15,'Current Rlx: pT95 = %0.01f L1 + %0.1f'
  %(lineFit.GetParameter(0),lineFit.GetParameter(1)))
cRgraph.Draw('P')

legend = ROOT.TLegend(0.11,0.5,0.4,0.89,'','brNDC')
legend.SetFillColor(ROOT.EColor.kWhite)
legend.SetBorderSize(0)
legend.AddEntry(uIgraph,'UCT Iso','P')
legend.AddEntry(uRgraph,'UCT Rlx','P')
legend.AddEntry(cIgraph,'Current Iso','P')
legend.AddEntry(cRgraph,'Current Rlx','P')
legend.Draw()

save=raw_input('press enter to finish, type save to save\n')
if save=='save':
 can.SaveAs(saveWhere+'fits.png')
