'''
Find the rate at an array of desired recoPt cuts (to be pT95)
Authors: T.M.Perry, M.Cepeda
'''
import ROOT
from ROOT import *
from array import array

#gROOT.ProcessLine(".L tdrStyle.C")
LIso=3
LSB=50
ISOTHRESHOLD=0.20
ZEROBIAS_RATE=15000000.00
#ZEROBIAS_RATE=30000000.00
#saveWhere='../plots/Iso40/EG_Iso40_rateVreco'
#saveWhere='../plots/Iso30/EG_Iso30_rateVreco'
#saveWhere='../plots/Iso25/EG_Iso25_rateVreco'
#saveWhere='../plots/Iso20/EG_Iso20_rateVreco'
saveWhere='../plots/Iso15/EG_Iso15_rateVreco'
extraName=''

cIColor=ROOT.EColor.kViolet-7
cRColor=ROOT.EColor.kRed
uIColor=ROOT.EColor.kBlue
uRColor=ROOT.EColor.kGreen+3
cIMarker=24
cRMarker=20
uIMarker=25
uRMarker=21
cISize=1.5
cRSize=1.5
uISize=1.5
uRSize=1.5

## File 
#rate_filename = '../data/EGT_Iso40_Rate.root'
#rate_filename = '../data/EG_Iso30_Rate.root'
#rate_filename = '../data/EGT_Iso25_Rate.root'
#rate_filename = '../data/EGT_Iso20_Rate.root'
rate_filename = '../data/EGT_Iso15_Rate.root'
rate_file = ROOT.TFile(rate_filename)
# L1
rate_rlx_l1g_spot = 'rlxEGUCTRate/Ntuple' # 
rate_iso_l1g_spot = 'isoEGUCTRate/Ntuple' # 
rate_rlx_l1g_eg_ntuple = rate_file.Get(rate_rlx_l1g_spot)
rate_iso_l1g_eg_ntuple = rate_file.Get(rate_iso_l1g_spot)
# Current
rate_rlx_l1_spot = 'rlxEGL1Rate/Ntuple' # 
rate_iso_l1_spot = 'isoEGL1Rate/Ntuple' # 
rate_rlx_l1_eg_ntuple = rate_file.Get(rate_rlx_l1_spot)
rate_iso_l1_eg_ntuple = rate_file.Get(rate_iso_l1_spot)

##### WHICH NTUPLE TO USE ###
#uctNtuple = rate_rlx_l1g_eg_ntuple
#curNtuple = rate_rlx_l1_eg_ntuple
scale = ZEROBIAS_RATE/rate_rlx_l1g_eg_ntuple.GetEntries()
print rate_rlx_l1g_eg_ntuple.GetEntries()
print rate_iso_l1g_eg_ntuple.GetEntries()
print rate_rlx_l1_eg_ntuple.GetEntries()
print rate_iso_l1_eg_ntuple.GetEntries()

log = open(saveWhere+extraName+'.log','w')
log.write('LIso: '+str(LIso)+'\n')
log.write('LSB: '+str(LSB)+'\n')
log.write('ISOTHRESHOLD: '+str(ISOTHRESHOLD)+'\n')
log.write('ZEROBIAS_RATE: '+str(ZEROBIAS_RATE)+'\n')
log.write('Scale: '+str(scale)+'  = total entries / ZEROBIAS_RATE\n\n')

tex = ROOT.TLatex()
tex.SetNDC(True)
tex.SetTextAlign(11)
tex.SetTextSize(0.03)

#### WHICH ISOLATION + ID CUT ON UCT ####
# ID + ISO both with switch at 63GeV
#uctCutString='((pt[0]>=63&&((jetPt[0]-regionPt[0])/regionPt[0]<100))||(pt[0]<63&&((jetPt[0]-pt[0])/pt[0])<'+str(ISOTHRESHOLD)+')&&((!tauVeto[0]&&!mipBit[0])||pt[0]>=63))'

# ID w/o switch + Iso with switch at 63GeV
#uctCutString='((pt[0]>=63&&((jetPt[0]-regionPt[0])/regionPt[0]<100))||(pt[0]<63&&((jetPt[0]-pt[0])/pt[0])<'+str(ISOTHRESHOLD)+')&&((!tauVeto[0]&&!mipBit[0])))'

# Iso w/ switch at 63 + ID w/o switch
#uctCutStringIsoId='(( pt[0]>=63 && (jetPt[0]-regionPt[0])/regionPt[0]<100)||(pt[0]<63&&(jetPt[0]-pt[0])/pt[0]<'+str(ISOTHRESHOLD)+'))&&(!tauVeto[0]&&!mipBit[0])'

# ID w/ switch (No Iso)
#uctCutString='(((!tauVeto[0]&&!mipBit[0])||pt[0]>=63))'

# ID w/o switch (No Iso)
#uctCutStringId='(!tauVeto[0]&&!mipBit[0])'

# No Cut
#uctCutString='(2>1)'

#### CURRENT CUT STRING ###
# No Cut
noCut='(2>1)'
uctCutStringIsoId = noCut
uctCutStringId = noCut
l1CutStringRlx = noCut
l1CutStringIso = noCut 

# values for extrapolation

# Iso15
mUIsoId = 13
bUIsoId = 43.6
## Iso20
#mUIsoId = 1.2
#bUIsoId = 20.8
## Iso25
#mUIsoId = 0.6
#bUIsoId = 27.8
## Iso30
#mUIsoId = 0.8
#bUIsoId = 18.4
## Iso40
#mUIsoId = 0.8
#bUIsoId = 18.8
mUId = 1.1
bUId = 10.6
mCI = 1.1
bCI = 6.2
mCR = 1.2
bCR = 4.8

# y = m x + b
def extrapolate(pT95,m,b):
 L1pT = (pT95-b)/m
 return L1pT

pT95 = array('d',[20,25,30,35,40,45])

uctL1IsoIdPt = array('d',[])
uctL1IdPt = array('d',[])
curIsoL1Pt = array('d',[])
curRlxL1Pt = array('d',[])
for pt in pT95:
 uctL1IsoIdPt.append(int(extrapolate(pt,mUIsoId,bUIsoId)))
 uctL1IdPt.append(int(extrapolate(pt,mUId,bUId)))
 curIsoL1Pt.append(int(extrapolate(pt,mCI,bCI)))
 curRlxL1Pt.append(int(extrapolate(pt,mCR,bCR)))

log.write('pT95 (RECO) Cut:      '+str(pT95)+'\n')
log.write('To have 95% plateau effeciency at [pT95] use L1pT cut at:\n')
log.write('UCT Iso + Id L1Pt:    '+str(uctL1IsoIdPt)+'\n')
log.write('UCT Id (no Iso) L1Pt: '+str(uctL1IdPt)+'\n')
log.write('Current L1Pt:         '+str(curIsoL1Pt)+'\n\n')
log.write('Exrapolated as:\n')
log.write('UCT Iso + Id:     L1pT = (pT95 - '+str(bUIsoId)+')/'+str(mUIsoId)+'\n')
log.write('UCT Id (no Iso):  L1pT = (pT95 - '+str(bUId)+')/'+str(mUId)+'\n')
log.write('Current Iso:      L1pT = (pT95 - '+str(bCI)+')/'+str(mCI)+'\n')
log.write('Current (no Iso): L1pT = (pT95 - '+str(bCR)+')/'+str(mCR)+'\n')

uctIsoIdRate=array('d',[]) 
uctIdRate=array('d',[]) 
curIsoRate=array('d',[])
curRlxRate=array('d',[])
#
log.write('-----------------------\n')
log.write('For UCT:  '+str(rate_iso_l1g_eg_ntuple.GetDirectory().GetName())+'\n\n')
log.write('UCT CutIsoID: '+uctCutStringIsoId+'\n\n')

for pt in uctL1IsoIdPt:
 uIsoIdNr = rate_iso_l1g_eg_ntuple.GetEntries(uctCutStringIsoId+'&&(pt[0]>'+str(pt)+')')
 uIsoIdRate = uIsoIdNr*scale
 uctIsoIdRate.append(int(uIsoIdRate))
 log.write('At pT = '+str(pt)+'\n')
 log.write('Rate Iso + Id = '+str(uIsoIdRate)+'\n\n')

# 
log.write('-----------------------\n')
log.write('For UCT:  '+str(rate_rlx_l1g_eg_ntuple.GetDirectory().GetName())+'\n\n')
log.write('UCT CutID: '+uctCutStringId+'\n\n')

for pt in uctL1IdPt:
 uIdNr = rate_rlx_l1g_eg_ntuple.GetEntries(uctCutStringId+'&&(pt[0]>'+str(pt)+')')
 uIdRate = uIdNr*scale
 uctIdRate.append(int(uIdRate))
 log.write('At pT = '+str(pt)+'\n')
 log.write('Rate Id (no Iso) = '+str(uIdRate)+'\n\n')

#
log.write('-----------------------\n')
log.write('For Current Iso:  '+str(rate_iso_l1_eg_ntuple.GetDirectory().GetName())+'\n\n')
log.write('Current Iso Cut: '+l1CutStringIso+'\n\n')
#log.write('Current Cut: '+curCutString+'\n\n')

for pt in curIsoL1Pt:
 cINr = rate_iso_l1_eg_ntuple.GetEntries(l1CutStringIso+'&&(pt[0]>'+str(pt)+')')
 cIRate = cINr*scale
 curIsoRate.append(int(cIRate))
 log.write('At pT = '+str(pt)+'\n')
 log.write('Rate = '+str(cIRate)+'\n\n')

#
log.write('-----------------------\n')
log.write('For Current Rlx:  '+str(rate_rlx_l1_eg_ntuple.GetDirectory().GetName())+'\n\n')
log.write('Current Rlx Cut: '+l1CutStringRlx+'\n\n')
#log.write('Current Cut: '+curCutString+'\n\n')

for pt in curRlxL1Pt:
 cRNr = rate_rlx_l1_eg_ntuple.GetEntries(l1CutStringRlx+'&&(pt[0]>'+str(pt)+')')
 cRRate = cRNr*scale
 curRlxRate.append(int(cRRate))
 log.write('At pT = '+str(pt)+'\n')
 log.write('Rate = '+str(cIRate)+'\n\n')


### PLOT reco pT (pT95) vs rate at L1 cut to make pT95 fall at 95% efficiency ###
can = ROOT.TCanvas('can','can',800,800)
can.SetLogy(True)

xmin = min(pT95)-5
xmax = max(pT95)+5
ymax = 2E7
#ymax = max(max(uctIsoIdRate),max(uctIdRate),max(curIsoRate),max(curRlxRate))*3
nrPts = len(pT95)

frame = TH1F('frame','',1,xmin,xmax)
frame.SetMaximum(ymax)
frame.SetMinimum(100)
frame.SetStats(False)
frame.GetXaxis().SetTitle('L1 Threshold [GeV]')
frame.GetYaxis().SetTitleOffset(1.3)
frame.GetYaxis().SetTitle('Rate [Hz]')
frame.SetTitle('')

curRlxGraph = ROOT.TGraph(nrPts,pT95,curRlxRate)
curRlxGraph.SetLineColor(ROOT.EColor.kBlack)
curRlxGraph.SetMarkerColor(cRColor)
curRlxGraph.SetLineWidth(2)
curRlxGraph.SetMarkerStyle(cRMarker)
curRlxGraph.SetMarkerSize(cRSize)
curRlxGraph.Draw('P')
labCR0=ROOT.TText(pT95[0],curRlxRate[0]/1.7,'%0.f' %curRlxL1Pt[0])
labCR0.SetTextSize(0.03)
labCR1=ROOT.TText(pT95[1],curRlxRate[1]/1.7,'%0.f' %curRlxL1Pt[1])
labCR1.SetTextSize(0.03)
labCR2=ROOT.TText(pT95[2],curRlxRate[2]/1.7,'%0.f' %curRlxL1Pt[2])
labCR2.SetTextSize(0.03)
labCR3=ROOT.TText(pT95[3],curRlxRate[3]/1.7,'%0.f' %curRlxL1Pt[3])
labCR3.SetTextSize(0.03)
labCR4=ROOT.TText(pT95[4],curRlxRate[4]/1.7,'%0.f' %curRlxL1Pt[4])
labCR4.SetTextSize(0.03)
labCR5=ROOT.TText(pT95[5],curRlxRate[5]/1.7,'%0.f' %curRlxL1Pt[5])
labCR5.SetTextSize(0.03)

curIsoGraph = ROOT.TGraph(nrPts,pT95,curIsoRate)
curIsoGraph.SetLineColor(ROOT.EColor.kBlack)
curIsoGraph.SetMarkerColor(cIColor)
curIsoGraph.SetLineWidth(2)
curIsoGraph.SetMarkerStyle(cIMarker)
curIsoGraph.SetMarkerSize(cISize)
curIsoGraph.Draw('P')
labC0=ROOT.TText(pT95[0],curIsoRate[0]/1.7,'%0.f' %curIsoL1Pt[0])
labC0.SetTextSize(0.03)
labC1=ROOT.TText(pT95[1],curIsoRate[1]/1.7,'%0.f' %curIsoL1Pt[1])
labC1.SetTextSize(0.03)
labC2=ROOT.TText(pT95[2],curIsoRate[2]/1.7,'%0.f' %curIsoL1Pt[2])
labC2.SetTextSize(0.03)
labC3=ROOT.TText(pT95[3],curIsoRate[3]/1.7,'%0.f' %curIsoL1Pt[3])
labC3.SetTextSize(0.03)
labC4=ROOT.TText(pT95[4],curIsoRate[4]/1.7,'%0.f' %curIsoL1Pt[4])
labC4.SetTextSize(0.03)
labC5=ROOT.TText(pT95[5],curIsoRate[5]/1.7,'%0.f' %curIsoL1Pt[5])
labC5.SetTextSize(0.03)

uctIsoIdGraph = ROOT.TGraph(nrPts,pT95,uctIsoIdRate)
uctIsoIdGraph.SetLineColor(ROOT.EColor.kBlack)
uctIsoIdGraph.SetMarkerColor(uIColor)
uctIsoIdGraph.SetLineWidth(2)
uctIsoIdGraph.SetMarkerStyle(uIMarker)
uctIsoIdGraph.SetMarkerSize(uISize)
uctIsoIdGraph.Draw('P')
labUID0=ROOT.TText(pT95[0],uctIsoIdRate[0]/1.5,'%0.f' %uctL1IsoIdPt[0])
labUID0.SetTextSize(0.03)
labUID1=ROOT.TText(pT95[1],uctIsoIdRate[1]/1.5,'%0.f' %uctL1IsoIdPt[1])
labUID1.SetTextSize(0.03)
labUID2=ROOT.TText(pT95[2],uctIsoIdRate[2]/1.5,'%0.f' %uctL1IsoIdPt[2])
labUID2.SetTextSize(0.03)
labUID3=ROOT.TText(pT95[3],uctIsoIdRate[3]/1.5,'%0.f' %uctL1IsoIdPt[3])
labUID3.SetTextSize(0.03)
labUID4=ROOT.TText(pT95[4],uctIsoIdRate[4]/1.5,'%0.f' %uctL1IsoIdPt[4])
labUID4.SetTextSize(0.03)
labUID5=ROOT.TText(pT95[5],uctIsoIdRate[5]/1.5,'%0.f' %uctL1IsoIdPt[5])
labUID5.SetTextSize(0.03)


uctIdGraph = ROOT.TGraph(nrPts,pT95,uctIdRate)
uctIdGraph.SetLineColor(ROOT.EColor.kBlack)
uctIdGraph.SetMarkerColor(uRColor)
uctIdGraph.SetLineWidth(2)
uctIdGraph.SetMarkerStyle(uRMarker)
uctIdGraph.SetMarkerSize(uRSize)
uctIdGraph.Draw('P')
labUD0=ROOT.TText(pT95[0],uctIdRate[0]*1.5,'%0.f' %uctL1IdPt[0])
labUD0.SetTextSize(0.03)
labUD1=ROOT.TText(pT95[1],uctIdRate[1]*1.5,'%0.f' %uctL1IdPt[1])
labUD1.SetTextSize(0.03)
labUD2=ROOT.TText(pT95[2],uctIdRate[2]*1.5,'%0.f' %uctL1IdPt[2])
labUD2.SetTextSize(0.03)
labUD3=ROOT.TText(pT95[3],uctIdRate[3]*1.5,'%0.f' %uctL1IdPt[3])
labUD3.SetTextSize(0.03)
labUD4=ROOT.TText(pT95[4],uctIdRate[4]*1.5,'%0.f' %uctL1IdPt[4])
labUD4.SetTextSize(0.03)
labUD5=ROOT.TText(pT95[5],uctIdRate[5]*1.5,'%0.f' %uctL1IdPt[5])
labUD5.SetTextSize(0.03)

legend = ROOT.TLegend(0.6,0.7,0.89,0.89,'','brNDC')
legend.SetFillColor(ROOT.EColor.kWhite)
legend.SetBorderSize(0)
legend.AddEntry(curRlxGraph,'Current Rlx EG','P')
legend.AddEntry(curIsoGraph,'Current Iso EG','P')
legend.AddEntry(uctIdGraph,'Upgrade Rlx EG','P')
legend.AddEntry(uctIsoIdGraph,'Upgrade Iso EG','P')
#legend.SetTextFont(62)
#legend.AddEntry(uctIsoIdGraph,'UCT: Region + ID + Iso < 0.2','P')
#legend.AddEntry(uctIdGraph,'UCT: Region + ID (no Iso)','P')
#legend.AddEntry(curIsoGraph,'Current (no Iso)','P')

frame.Draw()
curRlxGraph.Draw('LP')
curIsoGraph.Draw('LP')
uctIsoIdGraph.Draw('LP')
uctIdGraph.Draw('LP')
#labUID0.Draw()
#labUID1.Draw()
#labUID2.Draw()
#labUID3.Draw()
#labUID4.Draw()
#labUID5.Draw()
#labUD0.Draw()
#labUD1.Draw()
#labUD2.Draw()
#labUD3.Draw()
#labUD4.Draw()
#labUD5.Draw()
#labC0.Draw()
#labC1.Draw()
#labC2.Draw()
#labC3.Draw()
#labC4.Draw()
#labC5.Draw()
legend.Draw()

tex.SetTextFont(42)
tex.SetLineWidth(2)
tex.SetTextSize(0.04)
tex.SetTextAlign(31) # align right
tex.DrawLatex(0.9,0.91,'#sqrt{s} = 8 TeV')
tex.SetTextAlign(11) # align left
tex.DrawLatex(0.1,0.91,'CMS Preliminary 2012')
tex.SetTextAlign(13)
tex.DrawLatex(0.1,0.89,'L=2E34 cm^{-2}s^{-1}')

# From Andres 
#tex.SetTextFont(42)
#tex.SetLineWidth(2)
#tex.SetTextSize(0.04)
#tex.SetTextAlign(31) # align right
#tex.DrawLatex(0.9,0.96,'#sqrt{s} = 8 TeV')
#tex.SetTextAlign(11) # align left
#tex.DrawLatex(0.18,0.96,'CMS 2012')
#tex.DrawLatex(0.18,0.91,'L=2E34 cm^{-2}s^{-1}')

# removed for TDR plots
#tex.SetTextAlign(11)
#tex.SetTextSize(0.05)
#tex.DrawLatex(0.1,0.91,'EG Rate v Reco. p_{T} Cut')
#tex.SetTextAlign(13)
#tex.SetTextSize(0.03)
#tex.DrawLatex(0.1,0.89,'CMS Preliminary')
#tex.SetTextAlign(11)
##tex.DrawLatex(0.1,0.4,'Rate at p_{T} necessary to reach\n 95% of plateau efficiency corresponding to L1 p_{T} cut')
save2 = raw_input ('Press Enter to Exit (type save to save)\n')
if save2 == 'save':
 can.SaveAs(saveWhere+'_pT95_L1rate.png')
 #can.SaveAs(saveWhere+'_pT95_L1rate.pdf')


#
#### PLOT offline pT vs Rate ###
#can2 = ROOT.TCanvas('can2','can2',800,800)
#can2.SetLogy(True)
#
#xmin = min(min(uctL1IsoIdPt),min(uctL1IdPt),min(curIsoL1Pt))-5
#xmax = max(max(uctL1IsoIdPt),max(uctL1IdPt),max(curIsoL1Pt))+5
#ymax = max(max(uctIsoIdRate),max(uctIdRate),max(curIsoRate))*3
#nrPts = len(pT95)
#
#frame2 = TH1F('frame2','',1,xmin,xmax)
#frame2.SetMaximum(ymax)
#frame2.SetMinimum(100)
#frame2.SetStats(False)
#frame2.GetXaxis().SetTitle('Online p_{T} [GeV]')
#frame2.GetYaxis().SetTitle('Hz (8Tev, 1e34)')
#frame2.SetTitle('')
#
#uctIsoIdGraph2 = ROOT.TGraph(nrPts,uctL1IsoIdPt,uctIsoIdRate)
#uctIsoIdGraph2.SetLineColor(ROOT.EColor.kBlack)
#uctIsoIdGraph2.SetMarkerColor(uIColor)
#uctIsoIdGraph2.SetLineWidth(2)
#uctIsoIdGraph2.SetMarkerStyle(uIMarker)
#uctIsoIdGraph2.SetMarkerSize(uISize)
#uctIsoIdGraph2.Draw('P')
#
#uctIdGraph2 = ROOT.TGraph(nrPts,uctL1IdPt,uctIdRate)
#uctIdGraph2.SetLineColor(ROOT.EColor.kBlack)
#uctIdGraph2.SetMarkerColor(uRColor)
#uctIdGraph2.SetLineWidth(2)
#uctIdGraph2.SetMarkerStyle(uRMarker)
#uctIdGraph2.SetMarkerSize(uRSize)
#uctIdGraph2.Draw('P')
#
#curIsoGraph2 = ROOT.TGraph(nrPts,curIsoL1Pt,curIsoRate)
#curIsoGraph2.SetLineColor(ROOT.EColor.kBlack)
#curIsoGraph2.SetMarkerColor(cIColor)
#curIsoGraph2.SetLineWidth(2)
#curIsoGraph2.SetMarkerStyle(cIMarker)
#curIsoGraph2.SetMarkerSize(cSize)
#curIsoGraph2.Draw('P')
#
#legend2 = ROOT.TLegend(0.6,0.7,0.89,0.89,'','brNDC')
#legend2.SetFillColor(ROOT.EColor.kWhite)
#legend2.SetBorderSize(0)
#legend2.AddEntry(uctIsoIdGraph2,'UCT: Region + ID + Iso < 0.2','P')
#legend2.AddEntry(uctIdGraph2,'UCT: Region + ID (no Iso)','P')
#legend2.AddEntry(curIsoGraph2,'Current (no Iso)','P')
#
#frame2.Draw()
#curIsoGraph2.Draw('LP')
#uctIsoIdGraph2.Draw('LP')
#uctIdGraph2.Draw('LP')
#legend2.Draw()
#
#tex.SetTextAlign(11)
#tex.SetTextSize(0.07)
#tex.DrawLatex(0.1,0.91,'EG Rate v p_{T}')
#tex.SetTextAlign(31)
#tex.SetTextSize(0.03)
#tex.DrawLatex(0.9,0.91,'CMS Preliminary')
#
#save = raw_input ('Press Enter for reco (pT95) v Rate (type save to save)\n')
#if save == 'save':
# can2.SaveAs(saveWhere+'_L1_Rate.png')
