import sys
import getTriggerEfffromMiniAOD

if __name__ == "__main__":
    outfilename = sys.argv[1]
    infiles = sys.argv[2:]

    print outfilename,infiles

    getTriggerEfffromMiniAOD.getHistograms(infiles, outfilename)
