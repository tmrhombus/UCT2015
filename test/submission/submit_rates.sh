#!/bin/bash

# Submit rate ntuple jobs on the ZeroBias3 dataset (2012C)
EXPECTED_ARGS=1
if [ $# -ne $EXPECTED_ARGS ]
then
  echo "Usage: $0 JOB_NAME"
  exit 1
fi

farmoutAnalysisJobs $1-HCAL \
  --infer-cmssw-path \
  --input-file-list=zerobias_14TeV_mc_files.txt \
  --input-files-per-job=5 \
  --job-count=100 \
  ../makeRateTrees_cfg.py  isMC=1 stage1B=1 stage1=0 eicCardHcalOnly=1 \
  'inputFiles=$inputFileNames' 'outputFile=$outputFileName' \
  eicIsolationThreshold=3

farmoutAnalysisJobs $1-Norm \
  --infer-cmssw-path \
  --input-file-list=zerobias_14TeV_mc_files.txt \
  --input-files-per-job=5 \
  --job-count=100 \
  ../makeRateTrees_cfg.py  isMC=1 stage1B=0 stage1=1 eicCardHcalOnly=0 \
  'inputFiles=$inputFileNames' 'outputFile=$outputFileName' \
  eicIsolationThreshold=3
