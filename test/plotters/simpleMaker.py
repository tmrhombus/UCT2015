'''
Some simple common functions
Authors: T.M.Perry, A.Levine, M.Cepeda, E.Friis UW Madison
'''
import ROOT
from ROOT import TH1D,TH2D

def hist(tree,var,cuts='[(2>1)]',binning=[10,-2,-2],xaxis='',title='',cal=1.,logg=None):
 ''' make a 1D histogram '''
 draw_string = "%s * %0.2f" %(var,cal)
 cut = cutString(cuts)
 htemp = TH1D('htemp','htemp',binning[0],binning[1],binning[2])
 tree.Draw(draw_string+'>>htemp',cut)
 htemp.GetXaxis().SetTitle(xaxis)
 htemp.SetTitle(title)
 print(draw_string)
 print(cut)
 if logg is not None:
  logg.write('Draw String: '+draw_string+'\n')
  logg.write('Cut String:  '+cut+'\n')
  logg.write('Binning:     %s \n\n'%(binning)) 
 return htemp 

def hist2D(tree,varA,varB,selA,selB,
binA,binB,style='COLZ',xaxis='',yaxis='',title='',calA=1.,calB=1.,logg=None):
 ''' make a 2D histogram '''
 draw_string = "(%s * %0.2f):(%s * %0.2f)" % (varA,calA,varB,calB)
 cut = cutString(selA+selB)
 htemp = TH2D("htemp","htemp",
  binA[0],binA[1],binA[2],
  binB[0],binB[1],binB[2])
 tree.Draw(draw_string+'>>htemp',cut,style)
 htemp.GetXaxis().SetTitle(xaxis)
 htemp.GetYaxis().SetTitle(yaxis)
 htemp.SetTitle(title)
 print(draw_string)
 print(cut)
 if logg is not None:
  logg.write('Draw String: '+draw_string+'\n')
  logg.write('Cut String:  '+cut+'\n')
  logg.write('BinA:        %s \n'%(binA)) 
  logg.write('BinB:        %s \n\n'%(binB)) 
 return htemp

def cutString(cuts=['cutA','cutB']):
 ''' take an array and turn it into a cut string '''
 string = '(%s' %(cuts.pop())
 while cuts:
  string+=' && %s' %(cuts.pop())
 string+=')'
 #print(string)
 return string

def efficiency(denom, num,color=ROOT.EColor.kBlue,marker=20):
 ''' make an efficiency graph from num,denom called by efficiency '''
 eff = ROOT.TGraphAsymmErrors(num, denom)
 eff.SetMarkerStyle(marker)
 eff.SetMarkerColor(color)
 eff.SetMarkerSize(1.5)
 eff.SetLineColor(color)
 return eff




def eGraph(ntuple,variable,cut,binning,denom,title,leg,color,marker,logg):
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

