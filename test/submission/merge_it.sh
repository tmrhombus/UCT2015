#!/bin/sh
# Merge Efficiency and Rate Files using farmoutAnalysisJobs

version="13july24"

farmoutAnalysisJobs \
   --merge \
   --input-files-per-job=9999 \
   --input-dir=root://cmsxrootd.hep.wisc.edu//store/user/${USER}/${version}-EIC3-EGEfficiency-makeEfficiencyTree_cfg\
   merged_EGefficiency \
   $CMSSW_BASE

farmoutAnalysisJobs \
   --merge \
   --input-files-per-job=9999 \
   --input-dir=root://cmsxrootd.hep.wisc.edu//store/user/${USER}/${version}-TauEfficiency-makeEfficiencyTree_cfg\
   merged_TAUefficiency \
   $CMSSW_BASE

farmoutAnalysisJobs \
   --merge \
   --input-files-per-job=9999 \
   --input-dir=root://cmsxrootd.hep.wisc.edu//store/user/${USER}/${version}-JetEfficiency-makeEfficiencyTree_cfg\
   merged_JETefficiency \
   $CMSSW_BASE

farmoutAnalysisJobs \
   --merge \
   --input-files-per-job=9999 \
   --input-dir=root://cmsxrootd.hep.wisc.edu//store/user/${USER}/${version}-RATE-makeRateTrees_cfg\
   merged_UCTrates \
   $CMSSW_BASE
