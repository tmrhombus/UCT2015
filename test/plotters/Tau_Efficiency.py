'''
Makes Tau efficiency plots
Authors: T.M.Perry, E.K.Friis, M.Cepeda, A.G.Levine, N.Woods UW Madison
'''
from sys import argv, stdout, stderr
import ROOT

efficiencyPlots=True
# which curves to draw on rate and efficiency plots
drawUCTIso = False
drawUCTRlx = False
drawUCTIso_byhand = False
drawL1Iso = False
drawL1Rlx = True

##################
# Set Parameters #
##################
LIso=3
LSB=50
l1ptVal=20
recoPtVal=0
ISOTHRESHOLD=0.40
L1_CALIB_FACTOR = 1.0
L1G_CALIB_FACTOR = 1.0
ZEROBIAS_RATE=15000000.00
saveWhere='../plots/Tau_L1_Efficiency'

########
# File #
########
#Efficiency
eff_ntuple = '../data/Tau_Efficiency.root'
eff_ntuple_file = ROOT.TFile(eff_ntuple)
# L1
eff_rlx_spot = 'rlxTauEfficiency/Ntuple'
eff_iso_spot = 'isoTauEfficiency/Ntuple'
eff_rlx_eg_ntuple = eff_ntuple_file.Get(eff_rlx_spot)
eff_iso_eg_ntuple = eff_ntuple_file.Get(eff_iso_spot)

#To Be Made
store = ROOT.TFile(saveWhere+'.root','RECREATE')

name=''
if drawUCTIso or drawUCTRlx or drawUCTIso_byhand: name+='_UCT_'
if drawUCTRlx: name+='R'
if drawUCTIso: name+='I'
if drawUCTIso_byhand: name+='Ibh'+str(int(ISOTHRESHOLD * 10))
name+='_'

if drawL1Iso or drawL1Rlx: name+= 'L1_'
if drawL1Rlx: name+='R'
if drawL1Iso: name+='I'

extraName=''
name+=extraName

log = open(saveWhere+name+extraName+'.log','w')
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
#ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

tex = ROOT.TLatex()
tex.SetTextSize(0.07)
tex.SetTextAlign(11)
tex.SetNDC(True)

colorUR=ROOT.EColor.kGreen+3
markerUR=25
#markerUR=21
colorUI=ROOT.EColor.kCyan+3
markerUI=25
colorUIbh=ROOT.EColor.kBlack
#colorUIbh=ROOT.EColor.kGreen+3
#colorUIbh=ROOT.EColor.kBlue
colorUIbh=ROOT.EColor.kRed
#colorUIbh=ROOT.EColor.kViolet-7
markerUIbh=25
#markerUIbh=22
colorCR=ROOT.EColor.kViolet-7
markerCR=20
colorCI=ROOT.EColor.kRed
markerCI=24

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
 leg.AddEntry(efi,title,'pe')
 efi.Draw('pe')
 logg.write('---------------------------------\n')
 logg.write(title+'\n\n')
 logg.write('Tree: '+ntuple.GetDirectory().GetName()+'\n\n')
 logg.write('Cut: '+cut+'\n\n')
 return efi

def compare_efficiencies(
 variable,
 binning,
 ntuple_rlx=None,
 ntuple_iso=None,
 recoPtCut='(2>1)',l1PtCut='(2>1)',l1gPtCut='(2>1)',
 isoCut='(2>1)',extraCut='(2>1)',
 drawUCTIso_=False,
 drawUCTRlx_=False,
 drawUCTIso_byhand_=False,
 drawL1Iso_=False,
 drawL1Rlx_=False,
 legExtra='',
 setLOG=False
):
 ''' 
  Returns a (L1, L1G) tuple of TGraphAsymmErrors
 '''

 cutD_rlx = recoPtCut+'&&'+extraCut
 denom_rlx = make_plot(
  ntuple_rlx,variable,
  cutD_rlx,
  binning
 )
 cutD_iso = cutD_rlx #+ '&& (dr03CombinedEt/recoPt)<0.2'
 denom_iso = make_plot(
  ntuple_iso,variable,
  cutD_iso,
  binning
 )
 
 log.write('_____________________________\n')
 log.write('-------- Efficiency ---------\n\n')
 log.write('Variable: '+variable+'\n\n')
 log.write('Denominator Tree: '+ntuple_rlx.GetDirectory().GetName()+'\n')
 #log.write('Denominator Cut: '+cutD+'\n\n')
 
 frame = ROOT.TH1F('frame','frame',*binning)
 canvas.SetLogy(setLOG)
 frame.Draw()
 frame.SetTitle('')
 frame.GetYaxis().SetTitle('Efficiency')
 frame.SetMaximum(1.1)
 if variable is 'nPVs': frame.GetXaxis().SetTitle('Nr. Primary Vertices')
 else: frame.GetXaxis().SetTitle(variable)
 tex.DrawLatex(0.1,0.91,'Tau '+variable+' Efficiency')
 tex.SetTextSize(0.03)
 tex.DrawLatex(0.1,0.87,'CMS Preliminary')
 tex.SetTextSize(0.07)
 #legend = ROOT.TLegend(0.15,0.35,0.69,0.55,'','brNDC')
 legend = ROOT.TLegend(0.35,0.35,0.89,0.55,'','brNDC')
 legend.SetFillColor(0)
 legend.SetBorderSize(0)
 legend.SetHeader(legExtra)
 
 info ='_'+variable 
 if variable=='nPVs': info+=str(recoPtVal)

# Current Relaxed
 if drawL1Rlx_:
  cut_L1_rlx=recoPtCut+'&&'+l1PtCut+'&& l1Match'
  h_L1_rlx=effi_histo(ntuple_rlx,variable,cut_L1_rlx,binning,denom_rlx,
  'L1: Rlx',legend,
  colorCR,markerCR,log)
  h_L1_rlx.SetName('h_L1_rlx')
  h_L1_rlx.Write()
# Current With Isolation
 if drawL1Iso_:
  cut_L1_iso=recoPtCut+'&&'+l1PtCut+'&& l1Match'# && (dr03CombinedEt/recoPt)<0.2'
  h_L1_iso=effi_histo(ntuple_iso,variable,cut_L1_iso,binning,denom_iso,
  'L1: Iso',legend,
  colorCI,markerCI,log)
  h_L1_iso.SetName('h_L1_iso')
  h_L1_iso.Write()
# UCT Relaxed
 if drawUCTRlx_:
  cut_uctR=recoPtCut+'&&'+l1gPtCut+'&&l1gMatch'
  h_UCT_rlx=effi_histo(ntuple_rlx,variable,cut_uctR,binning,denom_rlx,
  'UCT: Rlx',legend,
   colorUR,markerUR,log)
  h_UCT_rlx.SetName('h_UCT_rlx')
  h_UCT_rlx.Write()
# UCT Rlx + Isolation by hand
 if drawUCTIso_byhand_:
  cut_UCT_isoByHand=recoPtCut+'&&'+l1gPtCut+'&&'+isoCut+'&& l1gMatch' # && (dr03CombinedEt/recoPt)<0.2'
  h_UCT_isoByHand=effi_histo(ntuple_rlx,variable,cut_UCT_isoByHand,binning,denom_iso,
  'UCT: Iso < %0.1f'%(ISOTHRESHOLD),legend,
  #'UCT: Rlx + IsoByHand<%0.1f'%(ISOTHRESHOLD),legend,
  colorUIbh,markerUIbh,log)
  h_UCT_isoByHand.SetName('h_UCT_isoByHand')
  h_UCT_isoByHand.Write()
# UCT Isolated
 if drawUCTIso_:
  cut_uctI=recoPtCut+'&&'+l1gPtCut+'&&l1gMatch '#&& (dr03CombinedEt/recoPt)<0.2'
  h_UCT_iso=effi_histo(ntuple_iso,variable,cut_uctI,binning,denom_iso,
  'UCT: Iso',legend,
   colorUI,markerUI,log)
  h_UCT_iso.SetName('h_UCT_iso')
  h_UCT_iso.Write()

 legend.Draw()
 save=raw_input("Type save to save as "+saveWhere+name+info+".png (enter to continue):\n")
 if save=="save": canvas.SaveAs(saveWhere+name+info+'.png')
 #canvas.SaveAs(saveWhere+name+info+'.png')
######################################################################
##### EFFICIENCY #####################################################
######################################################################


######################################################################
###### DRAW PLOTS ####################################################
######################################################################

####################
# Efficiency Plots #
####################
if efficiencyPlots == True:
 #binPt = [10,40,80] #l120
 binPt = [40,0,200]
 binVert=[10,0,35]
 binJetPt=[40,0,70]

# variable,
# binning,
# ntuple_rlx=None,
# ntuple_iso=None,
# recoPtCut='(2>1)',l1PtCut='(2>1)',l1gPtCut='(2>1)',
# isoCut='(2>1)',extraCut='(2>1)',
# drawUCTIso_=False,
# drawUCTRlx_=False,
# drawUCTIso_byhand_=False,
# drawL1Iso_=False,
# drawL1Rlx_=False
# legExtra='',
# setLOG=False

 compare_efficiencies(
  'recoPt',
  binPt,
  eff_rlx_eg_ntuple, eff_iso_eg_ntuple,
  recoPtCut = '(recoPt >= '+str(recoPtVal)+')',
  #l1PtCut = '(l1Pt >= '+str(l1ptVal)+')',
  l1gPtCut = '(l1gRegionEt >= '+str(l1ptVal)+')',
  #l1gPtCut = '(l1gPt >= '+str(l1ptVal)+')',
  # 12x12-4x4 
  isoCut='(l1gPt>=60||(l1gJetPt-l1gRegionEt)/l1gRegionEt<'+str(ISOTHRESHOLD)+')',
  # 12x12 - 2x1
  #isoCut='(l1gPt[0]>=60||(l1gJetPt[0]-l1gPt[0])/l1gPt[0]<'+str(ISOTHRESHOLD)+')',
  drawUCTIso_=drawUCTIso,
  drawUCTRlx_=drawUCTRlx,
  drawUCTIso_byhand_=drawUCTIso_byhand,
  drawL1Iso_=drawL1Iso,
  drawL1Rlx_=drawL1Rlx,
  #legExtra = 'Tau 4x4'
 )
 
# compare_efficiencies(
#  'nPVs',
#  binVert,
#  eff_rlx_eg_ntuple, eff_iso_eg_ntuple,
#  recoPtCut = '(recoPt >= '+str(recoPtVal)+')',
#  l1PtCut = '(l1Pt >= '+str(l1ptVal)+')',
#  l1gPtCut = '(l1gPt >= '+str(l1ptVal)+')',
#  isoCut='(l1gPt>=60||(l1gJetPt-l1gPt)/l1gPt<'+str(ISOTHRESHOLD)+')',
#  drawUCTIso_=drawUCTIso,
#  drawUCTRlx_=drawUCTRlx,
#  drawUCTIso_byhand_=drawUCTIso_byhand,
#  drawL1Iso_=drawL1Iso,
#  drawL1Rlx_=drawL1Rlx,
#  legExtra='Reco Pt > '+str(recoPtVal)
#)
