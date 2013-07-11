RCT 2015 Upgrade Emulator
========================

This is a mirror of the UCT package [in CVS](http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/UserCode/dasu/L1Trigger/UCT2015/).

The main documentation can be found on the [twiki.](https://twiki.cern.ch/twiki/bin/view/CMS/UCT2015)

To checkout

```bash
scram pro CMSSW CMSSW_6_0_1_PostLS1v2_patch4
cd CMSSW_6_0_1_PostLS1v2_patch4/src/

cmsenv

mkdir L1Trigger
cd L1Trigger

#set up cvs
#export CVSROOT=:gserver:<user_name>@cmssw.cvs.cern.ch:/local/reps/CMSSW
#kinit <user_name>@CERN.CH; aklog -cell cern.ch

git clone https://github.com/tmrhombus/UCT2015.git
./UCT2015/recipe

cd ../
scramv1 build
```
