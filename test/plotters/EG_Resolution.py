'''
Makes optionally EG efficiency, rate and resolution plots
Authors: T.M.Perry, E.K.Friis, M.Cepeda, A.G.Levine, N.Woods UW Madison
'''
from sys import argv, stdout, stderr
import ROOT

resolutionPlots=True
resL1 = True
resReco = True
# which curves to draw on rate and efficiency plots
drawUCTIso = True
drawUCTRlx = True
drawUCTIso_byhand = False
drawL1Iso = True
drawL1Rlx = True

##################
# Set Parameters #
##################
LIso=3
LSB=50
l1ptVal=20
recoPtVal=0
ISOTHRESHOLD=0.20
L1_CALIB_FACTOR = 1.0
L1G_CALIB_FACTOR = 1.0
ZEROBIAS_RATE=15000000.00
saveWhere='../plots/EG_Resolution'

########
# File #
########
#Efficiency
eff_ntuple = '../data/EG_Efficiency.root'
eff_ntuple_file = ROOT.TFile(eff_ntuple)
# L1
eff_rlx_spot = 'rlxEGEfficiency/Ntuple'
eff_iso_spot = 'isoEGEfficiency/Ntuple'
eff_rlx_eg_ntuple = eff_ntuple_file.Get(eff_rlx_spot)
eff_iso_eg_ntuple = eff_ntuple_file.Get(eff_iso_spot)

#To Be Made
store = ROOT.TFile(saveWhere+'.root','RECREATE')

name=''
if drawUCTIso or drawUCTRlx or drawUCTIso_byhand: name+='_UCT_'
if drawUCTRlx: name+='R'
if drawUCTIso: name+='I'
if drawUCTIso_byhand: name+='Ibh'
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
markerUR=21
colorUI=ROOT.EColor.kBlue
markerUI=25
colorUIbh=ROOT.EColor.kBlack
markerUIbh=22
colorCR=ROOT.EColor.kRed
markerCR=20
colorCI=ROOT.EColor.kViolet-7
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
##### RESOLUTION #####################################################
######################################################################
def make_res_pt(
Relaxed=True,recoPt="recoPt",l1Pt="l1Pt",uctPt="l1gPt",binning=[100,-2,2],cutRecoPt="(2>1)",cutL1Pt="(2>1)",cutExtra="(2>1)",filename='',setLOG=False):
 '''
 makes resolution plot
 '''
 if Relaxed:
  ntuple = eff_rlx_eg_ntuple
  colorUCT=colorUR
  colorL1 =colorCR
  matchUCT = "(l1gMatch)"
  matchL1  = "(l1Match)"
  name_UCT = "UCT Rlx"
  name_L1  = "L1 Rlx"
  filename+= "_Rlx"
 else:
  ntuple = eff_iso_eg_ntuple
  colorUCT=colorUI
  colorL1 =colorCI
  matchUCT = "(l1gMatch && (dr03CombinedEt/recoPt)<0.2)"
  matchL1  = "(l1Match  && (dr03CombinedEt/recoPt)<0.2)"
  name_UCT = "UCT Iso"
  name_L1  = "L1 Iso"
  filename+= "_Iso"

 cuts = '('+cutRecoPt+'&&'+cutL1Pt+'&&'+cutExtra+')'
 cutUCT = "("+cuts+"&&"+matchUCT+")"
 cutL1  = "("+cuts+"&&"+matchL1 +")"
 canvas.SetLogy(setLOG)

 h_UCT = make_plot(ntuple,"((%s - %s)/%s)"%(recoPt,uctPt,recoPt),cutUCT,binning)
 h_UCT.SetName("h_UCT")
 h_UCT.Scale(1./h_UCT.Integral())
 h_UCT.SetLineColor(colorUCT)
 h_UCT.SetTitle("Resolution")
 h_UCT.GetXaxis().SetTitle("1-p_{T}^{trig}/p_{T}^{reco}")
 
 h_L1 = make_plot(ntuple,"((%s - %s)/%s)"%(recoPt,l1Pt,recoPt),cutL1,binning)
 h_L1.SetName("h_L1")
 h_L1.SetLineColor(colorL1)
 h_L1.Scale(1./h_L1.Integral())

 legend = ROOT.TLegend(0.6,0.7,0.89,0.89,'','brNDC')
 legend.SetFillColor(ROOT.EColor.kWhite)
 legend.SetBorderSize(0)
 legend.AddEntry(h_UCT,name_UCT)
 legend.AddEntry(h_L1,name_L1)
 
 h_UCT.SetMaximum(1.1*max(h_UCT.GetMaximum(),h_L1.GetMaximum()))
 h_UCT.Draw()
 h_L1.Draw('sames')
 legend.Draw()
 tex.SetTextSize(0.03)
 tex.DrawLatex(0.1,0.87,'CMS Preliminary')

 canvas.SaveAs(saveWhere+filename+'.png')

####      ####
# Make Plots #
####      ####
binPt=[100,-0.5,1.5]
make_res_pt(Relaxed=True,binning=binPt)
make_res_pt(Relaxed=False,binning=binPt)

