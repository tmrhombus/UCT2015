'''
Some simple common functions
Authors: T.M.Perry, A.Levine, M.Cepeda, E.Friis UW Madison
'''
import ROOT
from ROOT import TH2D

def histogram(tree, var, sel, binning, xaxis='', title='',cal=1.):
 ''' plot a variable using draw and return the histogram '''
 draw_string = "%s * %0.2f>>htemp(%s)" % (var,cal, ", ".join(str(x) for x in binning))
 #print draw_string
 tree.Draw(draw_string, sel, "goff")
 output_histo = ROOT.gDirectory.Get("htemp").Clone()
 output_histo.GetXaxis().SetTitle(xaxis)
 output_histo.SetTitle(title)
 return output_histo

def hist2Dfriend(treeA,friendB,varA,varB,selA,selB,
binA,binB,style='COLZ',xaxis='',yaxis='',title='',calA=1.,calB=1.):
 ''' make a 2D histogram, trees better be friends (: '''
 draw_string = "(%s * %0.2f):(%s.%s * %0.2f)" % (varA,calA,friendB,varB,calB)
 cutB = friendCut(friendB,selB)
 cut = cutString(selA+cutB)
 #print(draw_string)
 #print(cut)
 htemp = TH2D("htemp","htemp",
  binA[0],binA[1],binA[2],
  binB[0],binB[1],binB[2])
 treeA.Draw(draw_string+'>>htemp',cut,style)
 htemp.GetXaxis().SetTitle(xaxis)
 htemp.GetYaxis().SetTitle(yaxis)
 htemp.SetTitle(title)
 return htemp

def friendCut(friend,cuts=['2>1','2>1']):
 cut = []
 while cuts:
  cut.append(friend+'.'+cuts.pop())
 return cut

def cutString(cuts=['(2>1)','(2>1)']):
 ''' take an array (OF STRINGS) and turn it into a cut string'''
 string = '('+cuts.pop()
 while cuts:
  string+=' && '+cuts.pop()
 string+=')'
 #print(string)
 return string

def eGraph(denom, num,color=ROOT.EColor.kBlue,marker=20):
 ''' make an efficiency graph from num,denom called by efficiency '''
 eff = ROOT.TGraphAsymmErrors(num, denom)
 eff.SetMarkerStyle(marker)
 eff.SetMarkerColor(color)
 eff.SetMarkerSize(1.5)
 eff.SetLineColor(color)
 return eff

def efficiency(ntuple,variable,cut,binning,denom,title,leg,color,marker,logg):
 ''' called by script, define parameters for efficiency plot '''
 num = hisogram(ntuple,variable,cut,binning)
 efi = eGraph(denom,num,color,marker)
 leg.AddEntry(efi,title)
 efi.Draw('p')
 logg.write(title+'\n')
 logg.write(ntuple.GetDirectory().GetName()+'\n')
 logg.write('Cut: '+cut+'\n\n')
 return efi

