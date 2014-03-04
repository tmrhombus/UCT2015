'''
Makes optionally EG efficiency, rate and resolution plots
Authors: T.M.Perry, E.K.Friis, M.Cepeda, A.G.Levine, N.Woods UW Madison
'''
from sys import argv, stdout, stderr
import ROOT

ratePlots = True
asFrequency = False # y-axis as frequency or nr. events
# which curves to draw on rate and efficiency plots
drawUCTIso = True
drawUCTRlx = False
drawUCTIso_byhand = False
drawL1Iso = False
drawL1Rlx = False

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
#saveWhere='../plots/Iso40/EG_Iso40_Rate'
saveWhere='../plots/Iso30/EG_Iso30_Rate'
#saveWhere='../plots/Iso25/EG_Iso25_Rate'
#saveWhere='../plots/Iso20/EG_Iso20_Rate'
if not asFrequency: saveWhere+='_Evts'

#rate plot
rateLine = True # line at recoPtVal

########
# File #
########
#Rate
#rate_ntuple = '../data/EGT_Iso40_Rate.root'
rate_ntuple = '../data/EG_Iso30_Rate.root'
#rate_ntuple = '../data/EGT_Iso25_Rate.root'
#rate_ntuple = '../data/EGT_Iso20_Rate.root'
rate_ntuple_file = ROOT.TFile(rate_ntuple)
# L1
rate_rlx_UCT_spot = 'rlxEGUCTRate/Ntuple'
rate_iso_UCT_spot = 'isoEGUCTRate/Ntuple'
rate_rlx_UCT_ntuple = rate_ntuple_file.Get(rate_rlx_UCT_spot)
rate_iso_UCT_ntuple = rate_ntuple_file.Get(rate_iso_UCT_spot)
# Current
rate_rlx_L1_spot = 'rlxEGL1Rate/Ntuple'
rate_iso_L1_spot = 'isoEGL1Rate/Ntuple'
rate_rlx_L1_ntuple = rate_ntuple_file.Get(rate_rlx_L1_spot)
rate_iso_L1_ntuple = rate_ntuple_file.Get(rate_iso_L1_spot)

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

colorUR=ROOT.EColor.kBlack
markerUR=22
#colorUR=ROOT.EColor.kGreen+3
#markerUR=21
#colorUI=ROOT.EColor.kGreen+3
colorUI=ROOT.EColor.kBlue
#colorUI=ROOT.EColor.kRed
#colorUI=ROOT.EColor.kViolet-7
markerUI=21
#markerUI=25
colorUIbh=ROOT.EColor.kBlack
markerUIbh=22
colorCR=ROOT.EColor.kRed
markerCR=20
colorCI=ROOT.EColor.kViolet-7
markerCI=24

print("about to make canvas")
canvas = ROOT.TCanvas("asdf", "adsf", 800, 800)
print("made canvas")

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
##### RATES ##########################################################
######################################################################
def make_l1_rate(pt, color=ROOT.EColor.kBlack, marker=20):
 ''' Make a rate plot out of L1Extra Pts '''
 numBins = pt.GetXaxis().GetNbins()
 rate = pt.Clone()
 for i in range(1,numBins):
  rate.SetBinContent(i,pt.Integral(i,numBins))
 rate.SetLineColor(color)
 rate.SetMarkerStyle(marker)
 rate.SetMarkerColor(color)
 return rate

def rate_histo(ntuple,cut,binning,calibfactor,scale,color,marker,leg,title,logg,line,ptLine,w,s):
 pt = make_plot(ntuple,'pt[0]',cut,binning,'','',calibfactor)
 rate = make_l1_rate(pt,color,marker)
 rate.Scale(scale)
 rate.Draw('phsame')
 leg.AddEntry(rate,title,'P')
 maxx = rate.GetMaximum()
 binn = rate.GetXaxis().FindBin(ptLine)
 rateVal = rate.GetBinContent(binn)
 vert=None
 hor=None
 if line==True:
  vert=ROOT.TLine(ptLine,0,ptLine,rateVal)
  vert.SetLineWidth(w)
  vert.SetLineStyle(s)
  hor=ROOT.TLine(binning[1],rateVal,ptLine,rateVal)
  hor.SetLineWidth(w)
  hor.SetLineStyle(s)   
  vert.Draw()
  hor.Draw()
 logg.write('---------------------------------\n')
 logg.write(title+'\n\n')
 logg.write('Tree: '+ntuple.GetDirectory().GetName()+'\n\n')
 logg.write('Cut: '+cut+'\n\n')
 logg.write('At pT = '+str(ptLine)+', Rate = '+str(rateVal)+'\n\n')
 return rate,maxx,vert,hor

def make_rate_plot(
 binning,
 ntuple_UCT_rlx=None,
 ntuple_UCT_iso=None,
 ntuple_L1_rlx =None,
 ntuple_L1_iso =None,
 filename='',
 setLOG=True,
 isoCut='(2>1)',extraCut='(2>1)',
 drawUCTIso_=False,
 drawUCTRlx_=False,
 drawUCTIso_byhand_=False,
 drawL1Iso_=False,
 drawL1Rlx_=False,
 line=False,
 ptLine=20
 ):

 info = ''
 #scale = 2589270./1754889. #for Iso < 0.3
 scale = 1.
 if asFrequency: scale = ZEROBIAS_RATE/ntuple_UCT_rlx.GetEntries()
 print(ntuple_UCT_rlx.GetEntries())
 print(ntuple_UCT_iso.GetEntries())
 print(ntuple_L1_rlx.GetEntries())
 print(ntuple_L1_iso.GetEntries())
 
 canvas.SetLogy(setLOG)
 frame = ROOT.TH1F('frame','frame',*binning)
 frame.Draw()
 frame.SetTitle('')
 if asFrequency: frame.GetYaxis().SetTitle('Hz (8TeV,1E34)')
 else: frame.GetYaxis().SetTitle('Nr. Events / %s GeV'%((binning[2]-binning[1])/binning[0]))
 frame.GetXaxis().SetTitle('p_{T}')
 tex.DrawLatex(0.1,0.91,'EG Rate')
 tex.SetTextSize(0.03)
 tex.SetTextAlign(31)
 tex.DrawLatex(0.9,0.91,'CMS Preliminary')
 tex.SetTextSize(0.07)
 tex.SetTextAlign(11)
 legend = ROOT.TLegend(0.6,0.7,0.89,0.89,'','brNDC')
 legend.SetFillColor(0)
 legend.SetBorderSize(0)

 # line (a=width b=style)
 aUR=3
 bUR=3
 aUI=3
 bUI=3
 aUIbh=3
 bUIbh=3
 aCR=3
 bCR=3
 aCI=3
 bCI=3

 log.write('________________\n')
 log.write('----- Rate -----\n\n')
 log.write('File : '+rate_ntuple+'\n')

 max_UCT_rlx=1
 max_UCT_iso=1
 max_UCT_isoByHand=1
 max_L1_rlx=1
 max_L1_iso=1

# Current Relaxed
 if drawL1Rlx_:
  cut_L1_rlx=extraCut
  h_L1_rlx,max_L1_rlx,vert_L1_rlx,hor_L1_rlx = rate_histo(
   ntuple_L1_rlx,cut_L1_rlx,binning,L1G_CALIB_FACTOR,
   scale,colorCR,markerCR,legend,
   'L1: Rlx',
   log,line,ptLine,aCR,bCR)
# Current Isolated 
 if drawL1Iso_:
  cut_L1_iso=extraCut
  h_L1_iso,max_L1_iso,vert_L1_iso,hor_L1_iso = rate_histo(
   ntuple_L1_iso,cut_L1_iso,binning,L1G_CALIB_FACTOR,
   scale,colorCI,markerCI,legend,
   'L1: Iso',
   log,line,ptLine,aCI,bCI)
# UCT Relaxed
 if drawUCTRlx_:
  cut_UCT_rlx=extraCut
  h_UCT_rlx,max_UCT_rlx,vert_UCT_rlx,hor_UCT_rlx = rate_histo(
   ntuple_UCT_rlx,cut_UCT_rlx,binning,L1G_CALIB_FACTOR,
   scale,colorUR,markerUR,legend,
   'UCT: Rlx',
   log,line,ptLine,aUR,bUR)
# UCT Rlx + Isolation by hand
 if drawUCTIso_byhand_:
  cut_UCT_isoByHand=isoCut+'&&'+extraCut
  h_UCT_isoByHand,max_UCT_isoByHand,vert_UCT_isoByHand,hor_UCT_isoByHand = rate_histo(
   ntuple_UCT_rlx,cut_UCT_isoByHand,binning,L1G_CALIB_FACTOR,
   scale,colorUIbh,markerUIbh,legend,
   'UCT: Rlx + IsoByHand<%0.1f'%(ISOTHRESHOLD),
   log,line,ptLine,aUIbh,bUIbh)
# UCT Isolated
 if drawUCTIso_:
  cut_UCT_iso=extraCut
  h_UCT_iso,max_UCT_iso,vert_UCT_iso,hor_UCT_iso = rate_histo(
   ntuple_UCT_iso,cut_UCT_iso,binning,L1G_CALIB_FACTOR,
   scale,colorUI,markerUI,legend,
   'UCT: Iso < 0.30',
   log,line,ptLine,aUI,bUI)

 frame.SetMaximum(5E5)
 #frame.SetMaximum(5*max(max_UCT_rlx,max_UCT_iso,max_UCT_isoByHand,max_L1_rlx,max_L1_iso))
 frame.SetMinimum(100)
 legend.Draw()
 save=raw_input("Type save to save as "+saveWhere+name+info+'.png (enter to continue)\n')
 if save=="save": canvas.SaveAs(saveWhere+name+info+'.png')
 #canvas.SaveAs(saveWhere+name+info+'.png')
######################################################################
##### RATES ##########################################################
######################################################################

######################################################################
###### DRAW PLOTS ####################################################
######################################################################
##############
# Rate Plots #
##############
if ratePlots == True:
 binRate = [36,0,80]

# binning,
# ntuple_UCT_rlx=None,
# ntuple_UCT_iso=None,
# ntuple_L1_rlx =None,
# ntuple_L1_iso =None,
# filename='',
# setLOG=True,
# isoCut='(2>1)',extraCut='(2>1)',
# drawUCTIso_=False,
# drawUCTRlx_=False,
# drawUCTIso_byhand_=False,
# drawL1Iso_=False,
# drawL1Rlx_=False,
# line=False
# ptLine=20,


 print("about to call MRP")
 make_rate_plot(
 binRate,
 ntuple_UCT_rlx=rate_rlx_UCT_ntuple,
 ntuple_UCT_iso=rate_iso_UCT_ntuple,
 ntuple_L1_rlx =rate_rlx_L1_ntuple,
 ntuple_L1_iso =rate_iso_L1_ntuple,
 filename='',
 setLOG=True,
 isoCut='(( pt[0]>=63 && (jetPt[0]-regionPt[0])/regionPt[0]<100)||(pt[0]<63&&(jetPt[0]-pt[0])/pt[0]<'+str(ISOTHRESHOLD)+'))',
 extraCut='(2>1)',
 drawUCTIso_=drawUCTIso,
 drawUCTRlx_=drawUCTRlx,
 drawUCTIso_byhand_=drawUCTIso_byhand,
 drawL1Iso_=drawL1Iso,
 drawL1Rlx_=drawL1Rlx,
 line=rateLine,
 ptLine=l1ptVal
 )
