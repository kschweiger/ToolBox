#!/bin/bash

pathtoskims=$1

echo "Using skims in folder: $pathtoskims"

for file in $pathtoskims/*.root ; do
    echo "Starting file: $file"
    root -b -q -l "AddLeptonWeights.cc(\"$file\")"
done
