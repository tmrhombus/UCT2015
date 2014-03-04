'''
Makes optionally EG efficiency, rate and resolution plots
Authors: T.M.Perry, E.K.Friis, M.Cepeda, A.G.Levine, N.Woods UW Madison
'''
from sys import argv, stdout, stderr
import ROOT

################
# Choose Plots #
################
efficiencyPlots = True
ratePlots = False

# which curves to draw on rate and efficiency plots
aIso = True    # I region + Iso<ISOTHRESHOLD
aNoIso = True  # N region
aLOne = True     # C current

#rate plot
rateLine = True # line at recoPtVal
rate5k = False
rate10k = False 
rate15k = True 

##################
# Set Parameters #
##################
LIso=3
LSB=50
l1ptVal=20

## 4x4 
#il1ptVal=49
#il1ptVal2=38
#il1ptVal3=33
#nl1ptVal=51
#nl1ptVal2=42
#nl1ptVal3=38

# 2x1 
il1ptVal=42
il1ptVal2=31
il1ptVal3=27
nl1ptVal=44
nl1ptVal2=36
nl1ptVal3=31

cl1ptVal=64
cl1ptVal2=62
cl1ptVal3=58

#l1ptVal=20
#il1ptVal=20
#il1ptVal2=20
#il1ptVal3=20
#nl1ptVal=20
#nl1ptVal2=20
#nl1ptVal3=20
#cl1ptVal=20
#cl1ptVal2=20
#cl1ptVal3=20
rateVal=5000
rateVal2=10000
rateVal3=15000
recoPtVal= 0
ISOTHRESHOLD=0.40
L1_CALIB_FACTOR = 1.0
L1G_CALIB_FACTOR = 1.0
ZEROBIAS_RATE=15000000.00
saveWhere='../plots/Tau_EffAtRate_'

########
# File #
########
#Efficiency
eff_ntuple = '../data/Tau_Efficiency.root'
eff_ntuple_file = ROOT.TFile(eff_ntuple)
# L1 + UCT
eff_rlx_spot = 'rlxTauEfficiency/Ntuple'
eff_iso_spot = 'isoTauEfficiency/Ntuple'
eff_rlx_ntuple = eff_ntuple_file.Get(eff_rlx_spot)
eff_iso_ntuple = eff_ntuple_file.Get(eff_iso_spot)

#Rate
rate_ntuple = '../data/EGT_Iso40_Rate.root'
rate_ntuple_file = ROOT.TFile(rate_ntuple)
# UCT
rate_rlx_UCT_spot = 'rlxTauUCTRate/Ntuple'
rate_iso_UCT_spot = 'isoTauUCTRate/Ntuple'
rate_rlx_UCT_ntuple = rate_ntuple_file.Get(rate_rlx_UCT_spot)
rate_iso_UCT_ntuple = rate_ntuple_file.Get(rate_iso_UCT_spot)
# Current
rate_rlx_L1_spot = 'tauL1Rate/Ntuple'
rate_iso_L1_spot = 'tauL1Rate/Ntuple'
rate_rlx_L1_ntuple = rate_ntuple_file.Get(rate_rlx_L1_spot)
rate_iso_L1_ntuple = rate_ntuple_file.Get(rate_iso_L1_spot)

store = ROOT.TFile(saveWhere+'.root','RECREATE')

name=''
extraName=''
name+=extraName
if aIso: name+='I'
if aNoIso: name+='N'
if aLOne: name+='C'
if rate5k: name+='_rate5k'
if rate10k: name+='_rate10k'
if rate15k: name+='_rate15k'

log = open(saveWhere+name+'_reco'+str(recoPtVal)+'_iso'+str(ISOTHRESHOLD)+'.log','w')
log.write('LIso = '+str(LIso)+'\n')
log.write('LSB = '+str(LSB)+'\n')
log.write('l1ptVal = '+str(l1ptVal)+'\n')
log.write('recoPtVal = '+str(recoPtVal)+'\n')
log.write('ISOTHRESHOLD = '+str(ISOTHRESHOLD)+'\n')
log.write('L1_CALIB_FACTOR = '+str(L1_CALIB_FACTOR)+'\n')
log.write('L1G_CALIB_FACTOR = '+str(L1G_CALIB_FACTOR)+'\n')
log.write('ZEROBIAS_RATE = '+str(ZEROBIAS_RATE)+'\n\n')

#########
# STYLE #
#########
ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(False)
ROOT.gStyle.SetOptStat(0)

tex = ROOT.TLatex()
tex.SetTextSize(0.07)
tex.SetTextAlign(11)
tex.SetNDC(True)

colorI=ROOT.EColor.kBlue
markerI=20
colorN=ROOT.EColor.kGreen+3
markerN=21
colorC=ROOT.EColor.kRed
markerC=23

canvas = ROOT.TCanvas("asdf", "adsf", 800, 800)

def make_plot(tree, variable, selection, binning, xaxis='', title='',calFactor=1):
 ''' Plot a variable using draw and return the histogram '''
 draw_string = "%s * %0.2f>>htemp(%s)" % (variable,calFactor, ", ".join(str(x) for x in binning))
 print draw_string
 tree.Draw(draw_string, selection, "goff")
 output_histo = ROOT.gDirectory.Get("htemp").Clone()
 output_histo.GetXaxis().SetTitle(xaxis)
 output_histo.SetTitle(title)
 return output_histo

######################################################################
##### EFFICIENCY #####################################################
######################################################################
def make_l1_efficiency(denom, num,color=ROOT.EColor.kBlue,marker=20):
 ''' Make an efficiency graph '''
 eff = ROOT.TGraphAsymmErrors(num, denom)
 eff.SetMarkerStyle(marker)
 eff.SetMarkerColor(color)
 eff.SetMarkerSize(1.5)
 eff.SetLineColor(color)
 return eff

def effi_histo(ntuple,variable,cut,binning,denom,title,leg,color,marker,logg):
 num = make_plot(ntuple,variable,cut,binning)
 efi = make_l1_efficiency(denom,num,color,marker)
 leg.AddEntry(efi,title)
 efi.Draw('pe')
 logg.write(title+'\n')
 logg.write(ntuple.GetDirectory().GetName()+'\n')
 logg.write('Cut: '+cut+'\n\n')
 return efi

def compare_efficiencies(
 variable,
 binning,
 ntuple_rlx,
 ntuple_iso,
 recoPtCut='(2>1)',
 il1gPtCut='(2>1)',il1gPtCut2='(2>1)',il1gPtCut3='(2>1)',
 nl1gPtCut='(2>1)',nl1gPtCut2='(2>1)',nl1gPtCut3='(2>1)',
 cl1PtCut='(2>1)',cl1PtCut2='(2>1)',cl1PtCut3='(2>1)',
 isoCut='(2>1)',aPUCut='(2>1)',bPUCut='(2>1)',extraCut='(2>1)',
 Iso=False,noIso=False,lOne=False,
 legExtra=None,
 setLOG=False
):
 '''
  Returns a (L1, L1G) tuple of TGraphAsymmErrors
 '''

 cutD = recoPtCut+'&&'+extraCut
 denom_rlx = make_plot(
  ntuple_rlx,variable,
  cutD,
  binning
 )
 denom_iso = make_plot(
  ntuple_iso,variable,
  cutD,
  binning
 )

 log.write('_____________________________\n')
 log.write('-------- Efficiency ---------\n\n')
 log.write('File: '+eff_ntuple+'\n')
 log.write('Variable: '+variable+'\n\n')
 log.write('Denominator Tree: '+ntuple_rlx.GetDirectory().GetName()+'\n\n')
 log.write('Denominator Cut: '+cutD+'\n\n')
 
 frame = ROOT.TH1F('frame','frame',*binning)
 canvas.SetLogy(setLOG)
 frame.Draw()
 frame.SetTitle('')
 frame.GetYaxis().SetTitle('Efficiency')
 frame.SetMaximum(1.1)
 if variable is 'nPVs': frame.GetXaxis().SetTitle('Nr. Primary Vertices')
 elif variable is 'recoPt': frame.GetXaxis().SetTitle('p_{T}^{reco} [GeV]')
 else: frame.GetXaxis().SetTitle(variable)
 tex.DrawLatex(0.1,0.91,'Tau Efficiency')
 legend = ROOT.TLegend(0.45,0.35,0.89,0.15,'','brNDC')
 legend.SetFillColor(0)
 legend.SetBorderSize(1)
 if legExtra is not None: legend.SetHeader(legExtra)
 
 color1=ROOT.EColor.kBlue
 marker1=20
 color2=ROOT.EColor.kGreen+3
 marker2=21
 color3=ROOT.EColor.kRed
 marker3=22
 
 tex.SetTextSize(0.04)
 if rate5k:
  tex.DrawLatex(0.15,0.85,'Rate: 5kHz @ L=1e34')
 if rate10k:
  tex.DrawLatex(0.15,0.85,'Rate: 10kHz @ L=1e34')
 if rate15k:
  tex.DrawLatex(0.15,0.85,'Rate: 15kHz @ L=1e34')

# UCT Isolated
#ntuple with Region and Isolation
 if Iso:
  if rate5k:
   cutI=recoPtCut+'&&'+extraCut+'&&'+isoCut +'&&'+il1gPtCut+'&&l1gMatch'
   print(ntuple_rlx.GetDirectory().GetName())
   print(variable)
   print(cutI)
   #l1g=effi_histo(ntuple_rlx,variable,cutI,binning,denom_iso,
   l1g=effi_histo(ntuple_rlx,variable,cutI,binning,denom_rlx,
    'Region + Isolation, L1pT > %0.f'%(il1ptVal),legend,
    color1,marker1,log)
   l1g.SetName('l1g')
   l1g.Write()

  if rate10k:
   cutI2=recoPtCut+'&&'+extraCut+'&&'+isoCut +'&&'+il1gPtCut2+'&&l1gMatch'
   #l1g2=effi_histo(ntuple_rlx,variable,cutI2,binning,denom_iso,
   l1g2=effi_histo(ntuple_rlx,variable,cutI2,binning,denom_rlx,
    'Region + Isolation, L1pT > %0.f'%(il1ptVal2),legend,
    color1,marker2,log)
   l1g2.SetName('l1g2')
   l1g2.Write()

  if rate15k:
   cutI3=recoPtCut+'&&'+extraCut+'&&'+isoCut +'&&'+il1gPtCut3+'&&l1gMatch'
   #l1g3=effi_histo(ntuple_rlx,variable,cutI3,binning,denom_iso,
   l1g3=effi_histo(ntuple_rlx,variable,cutI3,binning,denom_rlx,
    'Region + Isolation, L1pT > %0.f'%(il1ptVal3),legend,
    color1,marker3,log)
   l1g3.SetName('l1g3')
   l1g3.Write()

# UCT Relaxed
#ntuple with Region and without Isolation
 if noIso:
  if rate5k:
   cutN=recoPtCut+'&&'+extraCut+'&&'+nl1gPtCut+'&& l1gMatch'
   l1g_noiso=effi_histo(ntuple_rlx,variable,cutN,binning,denom_rlx,
    'Region, L1pT > %0.f'%(nl1ptVal),legend,
    color2,marker1,log) 
   l1g_noiso.SetName('l1g_noiso')
   l1g_noiso.Write()

  if rate10k:
   cutN2=recoPtCut+'&&'+extraCut+'&&'+nl1gPtCut2+'&& l1gMatch'
   l1g_noiso2=effi_histo(ntuple_rlx,variable,cutN2,binning,denom_rlx,
    'Region, L1pT > %0.f'%(nl1ptVal2),legend,
    color2,marker2,log) 
   l1g_noiso2.SetName('l1g_noiso2')
   l1g_noiso2.Write()

  if rate15k:
   cutN3=recoPtCut+'&&'+extraCut+'&&'+nl1gPtCut3+'&& l1gMatch'
   l1g_noiso3=effi_histo(ntuple_rlx,variable,cutN3,binning,denom_rlx,
    'Region, L1pT > %0.f'%(nl1ptVal3),legend,
    color2,marker3,log) 
   l1g_noiso3.SetName('l1g_noiso3')
   l1g_noiso3.Write()

# C
#Current trigger
 if lOne:
  if rate5k:
   cutC=recoPtCut+'&&'+extraCut+'&&'+cl1PtCut+'&&l1Match'
   #l1=effi_histo(ntuple_iso,variable,cutC,binning,denom_iso,
   l1=effi_histo(ntuple_iso,variable,cutC,binning,denom_rlx,
    'Current, L1pT > %0.f'%(cl1ptVal),legend,
   color3,marker1,log)
   l1.SetName('l1')
   l1.Write()
 
  if rate10k:
   cutC2=recoPtCut+'&&'+extraCut+'&&'+cl1PtCut2+'&&l1Match'
   #l12=effi_histo(ntuple_iso,variable,cutC2,binning,denom_iso,
   l12=effi_histo(ntuple_iso,variable,cutC2,binning,denom_rlx,
    'Current, L1pT > %0.f'%(cl1ptVal2),legend,
   color3,marker2,log)
   l12.SetName('l12')
   l12.Write()

  if rate15k:
   cutC3=recoPtCut+'&&'+extraCut+'&&'+cl1PtCut3+'&&l1Match'
   #l13=effi_histo(ntuple_iso,variable,cutC3,binning,denom_iso,
   l13=effi_histo(ntuple_iso,variable,cutC3,binning,denom_rlx,
    'Current, L1pT > %0.f'%(cl1ptVal3),legend,
   color3,marker3,log)
   l13.SetName('l13')
   l13.Write()
 
 legend.Draw()
 info = '_EFF_'+variable+'_reco'+str(recoPtVal)+'_l1'+str(l1ptVal)
 saveEff = raw_input("type 'save' to save:\n")
 if saveEff == 'save':
  canvas.SaveAs(saveWhere+name+info+'.png')
######################################################################
##### EFFICIENCY #####################################################
######################################################################

######################################################################
##### RATE ###########################################################
######################################################################
def make_l1_rate(pt, color=ROOT.EColor.kBlack, marker=20):
 ''' Make a rate plot out of L1Extra Pts '''
 numBins = pt.GetXaxis().GetNbins()
 rate = pt.Clone()
 for i in range(1, numBins+1):
  rate.SetBinContent(i, pt.Integral(i, numBins))
 rate.SetLineColor(color)
 rate.SetMarkerStyle(marker)
 rate.SetMarkerColor(color)
 return rate

def rate_histo(ntuple,cut,binning,calibfactor,scale,color,marker,leg,title,logg,line,ptLine,ptLine2,ptLine3,w,s,rateLine=False,xaxis='pt[0]'):
 pt = make_plot(ntuple,xaxis,cut,binning,'','',calibfactor)
 rate = make_l1_rate(pt,color,marker)
 rate.Scale(scale)
 rate.Draw('phsame')
 leg.AddEntry(rate,title,'pe')
 maxx = rate.GetMaximum()
 bs=float((binning[2]-binning[1]))/float(binning[0])
 binn=None
 print('Cut: %s'%cut)
 for a in range(0,binning[0]):
  if rate.GetBinContent(a) <= ptLine and binn==None: 
   binn=a
 vert=None
 hor=None
 if binn != None:
  rateVal=binning[1]-bs+float(binn)*bs
 else:
  rateVal=binning[1]
 print('Rate: %0.f'%ptLine)
 print('L1pT: %0.f\n'%rateVal)
 hor=ROOT.TLine(binning[1],ptLine,rateVal,ptLine)
 hor.SetLineWidth(w)
 hor.SetLineStyle(s)   
 vert=ROOT.TLine(rateVal,0,rateVal,ptLine)
 vert.SetLineWidth(w)
 vert.SetLineStyle(s)
 if rateLine is True:
  vert.Draw()
  hor.Draw()

 binn2=None
 for a in range(0,binning[0]):
  if rate.GetBinContent(a) <= ptLine2 and binn2==None: 
   binn2=a
 vert2=None
 hor2=None
 rateVal2=binning[1]-bs+float(binn2)*bs
 print('Rate: %0.f'%ptLine2)
 print('L1pT: %0.f\n'%rateVal2)
 hor2=ROOT.TLine(binning[1],ptLine2,rateVal2,ptLine2)
 hor2.SetLineWidth(1)
 hor2.SetLineStyle(1)   
 vert2=ROOT.TLine(rateVal2,0,rateVal2,ptLine2)
 vert2.SetLineWidth(1)
 vert2.SetLineStyle(1)
 if rateLine is True:
  vert2.Draw()
  hor2.Draw()

 binn3=None
 for a in range(0,binning[0]):
  if rate.GetBinContent(a) <= ptLine3 and binn3==None: 
   binn3=a
 vert3=None
 hor3=None
 rateVal3=binning[1]-bs+float(binn3)*bs
 print('Rate: %0.f'%ptLine3)
 print('L1pT: %0.f\n'%rateVal3)
 hor3=ROOT.TLine(binning[1],ptLine3,rateVal3,ptLine3)
 hor3.SetLineWidth(2)
 hor3.SetLineStyle(2)   
 vert3=ROOT.TLine(rateVal3,0,rateVal3,ptLine3)
 vert3.SetLineWidth(2)
 vert3.SetLineStyle(2)
 if rateLine is True:
  vert3.Draw()
  hor3.Draw()

 logg.write('---------------------------------\n')
 logg.write(title+'\n')
 logg.write('---------------------------------\n')
 logg.write('Cut: '+cut+'\n\n')
 logg.write('At pT = '+str(ptLine)+', Rate = '+str(rateVal)+'\n\n')
 return rate,maxx,vert,hor,vert2,hor2,vert3,hor3

l1Region2 = 'pt[0]'
#l1Region2 = 'regionPt[0]'
def make_rate_plot(
 l1_ntuple,
 uct_iso_ntuple,
 uct_rlx_ntuple,
 binning,
 filename='',
 setLOG=True,
 isoCut='(2>1)',puACut='(2>1)',puBCut='(2>1)',extraCut='(2>1)',
 ptLine=20,
 ptLine2=20,
 ptLine3=20,
 Iso=False,noIso=False,lOne=False,
 line=False
 ):

 info = '_RATE'
 scale = ZEROBIAS_RATE/uct_iso_ntuple.GetEntries()
 print l1_ntuple.GetEntries()
 print uct_iso_ntuple.GetEntries()
 print uct_rlx_ntuple.GetEntries()
 
 canvas.SetLogy(setLOG)
 frame = ROOT.TH1F('frame','frame',*binning)
 frame.Draw()
 frame.SetTitle('')
 frame.GetYaxis().SetTitle('Hz (8TeV,1E34)')
 frame.GetXaxis().SetTitle('p_{T}^{L1}')
 frame.SetMaximum(10000000)
 frame.SetMinimum(100)
 tex.DrawLatex(0.1,0.91,'Tau Rate')
 legend = ROOT.TLegend(0.5,0.7,0.89,0.89,'','brNDC')
 legend.SetFillColor(0)
 legend.SetBorderSize(0)

 # line (a=width b=style)
 aI=3
 bI=3
 aN=3
 bN=3
 aC=3
 bC=3

 log.write('----------------\n')
 log.write('----- Rate -----\n\n')
 log.write('File : '+rate_ntuple+'\n')

 maxI = 1
 maxN = 1
 maxC = 1
# I
# Isolated
 if Iso:
  cutI=isoCut+'&&'+extraCut
  l1gRate,maxI,vertI,horI,vert2I,hor2I,vert3I,hor3I = rate_histo(
   uct_rlx_ntuple,cutI,binning,L1G_CALIB_FACTOR,
   scale,colorI,markerI,legend,
   'UCT Iso <'+str(ISOTHRESHOLD),
   log,line,ptLine,ptLine2,ptLine3,aI,bI,rateLine=line,xaxis=l1Region2)
  info+='_iso_'+str(ISOTHRESHOLD)
# Non Isolated
 if noIso:
  cutN=extraCut
  l1gNoIsoRate,maxN,vertN,horN,vert2N,hor2N,vert3N,hor3N = rate_histo(
   uct_rlx_ntuple,cutN,binning,L1G_CALIB_FACTOR,
   scale,colorN,markerN,legend,
   'UCT Rlx',
   log,line,ptLine,ptLine2,ptLine3,aN,bN,rateLine=line,xaxis=l1Region2)
# Current
 if lOne:
  l1Rate,maxC,vertC,horC,vert2C,hor2C,vert3C,hor3C = rate_histo(
   l1_ntuple,extraCut,binning,L1G_CALIB_FACTOR,
   scale,colorC,markerC,legend,
   'Current', 
   log,line,ptLine,ptLine2,ptLine3,aC,bC,rateLine=line,xaxis='pt[0]')

 frame.SetMaximum(3E6)
 #frame.SetMaximum(5*max(maxI,maxN,maxC))
 legend.Draw()
 save = raw_input("Type 'save' to save:\n")
 if save == 'save':
  canvas.SaveAs(saveWhere+name+info+'.png')
######################################################################
##### RATE ###########################################################
######################################################################

######################################################################
###### DRAW PLOTS ####################################################
######################################################################
####################
# Efficiency Plots #
####################
if efficiencyPlots == True:

 binPt = [40,0,200]
 binPV = [12,0,35]

 l1Two='l1gPt'
 #l1Two='l1gRegionEt'
 compare_efficiencies(
  'recoPt',
  binPt,
  eff_rlx_ntuple, eff_iso_ntuple,
  recoPtCut = '(recoPt >= '+str(recoPtVal)+')',
  il1gPtCut =  '('+l1Two+' >= '+str(il1ptVal)+')',
  il1gPtCut2 = '('+l1Two+' >= '+str(il1ptVal2)+')',
  il1gPtCut3 = '('+l1Two+' >= '+str(il1ptVal3)+')',
  nl1gPtCut =  '('+l1Two+' >= '+str(nl1ptVal)+')',
  nl1gPtCut2 = '('+l1Two+' >= '+str(nl1ptVal2)+')',
  nl1gPtCut3 = '('+l1Two+' >= '+str(nl1ptVal3)+')',
  cl1PtCut = '(l1Pt >= '+str(cl1ptVal)+')',
  cl1PtCut2 = '(l1Pt >= '+str(cl1ptVal2)+')',
  cl1PtCut3 = '(l1Pt >= '+str(cl1ptVal3)+')',
 isoCut='(l1gPt>=60||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD)+')',
  Iso=aIso,
  noIso=aNoIso,
  lOne=aLOne,
 )
 
# compare_efficiencies(
#  'nPVs',
#  binPV,
#  eff_rlx_tau_ntuple, eff_iso_tau_ntuple,
#  recoPtCut = '(recoPt >= '+str(recoPtVal)+')',
#  il1gPtCut =  '('+l1Two+' > '+str(il1ptVal)+')',
#  il1gPtCut2 = '('+l1Two+' > '+str(il1ptVal2)+')',
#  il1gPtCut3 = '('+l1Two+' > '+str(il1ptVal3)+')',
#  nl1gPtCut =  '('+l1Two+' > '+str(nl1ptVal)+')',
#  nl1gPtCut2 = '('+l1Two+' > '+str(nl1ptVal2)+')',
#  nl1gPtCut3 = '('+l1Two+' > '+str(nl1ptVal3)+')',
#  cl1PtCut = '(l1Pt >= '+str(cl1ptVal)+')',
#  cl1PtCut2 = '(l1Pt >= '+str(cl1ptVal2)+')',
#  cl1PtCut3 = '(l1Pt >= '+str(cl1ptVal3)+')',
#  isoCut='((l1gJetPt-'+l1Two+')/'+l1Two+' <'+str(ISOTHRESHOLD)+')',
#  Iso=aIso,
#  noIso=aNoIso,
#  lOne=aLOne,
#  legExtra = 'p_{T}^{reco} > '+str(recoPtVal)
# )
 
##############
# Rate Plots #
##############
if ratePlots == True:
 #binRate = [12,25,85]
 binRate = [36,0,80]

 make_rate_plot(
  rate_rlx_L1_ntuple,
  rate_iso_UCT_ntuple,
  rate_rlx_UCT_ntuple,
  binRate,
  filename='',
  setLOG=True,
  isoCut='(( pt[0]>=63 && (jetPt[0]-regionPt[0])/regionPt[0]<100)||(pt[0]<63&&(jetPt[0]-regionPt[0])/regionPt[0]<'+str(ISOTHRESHOLD)+'))',
  #isoCut='((jetPt[0] - '+l1Region2+')/'+l1Region2+'<'+str(ISOTHRESHOLD)+')',
  Iso=aIso,
  noIso=aNoIso,
  lOne=aLOne,
  line = rateLine,
  ptLine=rateVal,
  ptLine2=rateVal2,
  ptLine3=rateVal3,
 )
