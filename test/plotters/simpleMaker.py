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

def hist2D(treeA,varA,varB,selA,selB,
binA,binB,style='COLZ',xaxis='',yaxis='',title='',calA=1.,calB=1.,logg=None):
 ''' make a 2D histogram '''
 draw_string = "(%s * %0.2f):(%s * %0.2f)" % (varA,calA,varB,calB)
 cut = cutString(selA+selB)
 htemp = TH2D("htemp","htemp",
  binA[0],binA[1],binA[2],
  binB[0],binB[1],binB[2])
 treeA.Draw(draw_string+'>>htemp',cut,style)
 htemp.GetXaxis().SetTitle(xaxis)
 htemp.GetYaxis().SetTitle(yaxis)
 htemp.SetTitle(title)
 print(draw_string)
 print(cut)
 if logg is not None:
  logg.write('Draw String: '+draw_string+'\n')
  logg.write('Cut String:  '+cut+'\n\n')
 return htemp

def cutString(cuts=['cutA','cutB']):
 ''' take an array and turn it into a cut string '''
 string = '(%s' %(cuts.pop())
 while cuts:
  string+=' && %s' %(cuts.pop())
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

def hist2Dfriend(treeA,friendB,varA,varB,selA,selB,
binA,binB,style='COLZ',xaxis='',yaxis='',title='',calA=1.,calB=1.,logg=None):
 ''' make a 2D histogram, trees better be friends (: '''
 frVarB = friendInsert(friendB,varB)
 draw_string = "(%s * %0.2f):(%s * %0.2f)" % (varA,calA,frVarB,calB)
 cutB = friendCut(friendB,selB)
 cut = cutString(selA+cutB)
 htemp = TH2D("htemp","htemp",
  binA[0],binA[1],binA[2],
  binB[0],binB[1],binB[2])
 treeA.Draw(draw_string+'>>htemp',cut,style)
 htemp.GetXaxis().SetTitle(xaxis)
 htemp.GetYaxis().SetTitle(yaxis)
 htemp.SetTitle(title)
 #print(draw_string)
 #print(cut)
 if logg is not None:
  logg.write('Draw String: '+draw_string+'\n')
  logg.write('Cut String:  '+cut+'\n\n')
 return htemp

def friendCut(friend,cuts=['cutA','cutB']):
 ''' takes ['pt>5'] and makes it [friend.pt>5] '''
 cut = []
 while cuts:
  cut.append('%s.%s'%(friend,cuts.pop()))
 #print(cut)
 return cut

def friendInsert(friend='MY',stringIn='string'):
 ''' goes through string and adds <friend.> to each word
     doesn't work if you have consecutive numbers in leafname '''
 stringOut = ''
 for i,c in enumerate(stringIn):
  if i == 0 and stringIn[i].isalpha:
   stringOut+=friend+'.'
  if stringIn[i].isalpha() and not stringIn[i-1].isalnum():
   stringOut+=friend+'.'
  stringOut+=stringIn[i]
 #print stringIn
 #print stringOut
 return stringOut

