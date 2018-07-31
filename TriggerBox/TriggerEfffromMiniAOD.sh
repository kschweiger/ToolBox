#!/bin/bash

source common.sh

cd $GC_SCRATCH

python /mnt/t3nfs01/data01/shome/koschwei/ToolBox/PlotBox/getTriggerEfffromMiniAODBatch.py out $FILE_NAMES
