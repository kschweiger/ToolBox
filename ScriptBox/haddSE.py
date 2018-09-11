from glob import glob
import sys
import os
import subprocess

#############################################################
############### Configure Logging
import logging
log_format = (
    '[%(asctime)s] %(levelname)-8s %(message)s')
logging.basicConfig(
    format=log_format,
    level=logging.INFO,
)
#############################################################
#############################################################


def runSingleHadd(directory, SEprefix, tmpFile, altOutput, local):
    print altOutput
    if directory.endswith("/"):
        directory = directory[0:-1]
    if altOutput.endswith("/"):
        altOutput = altOutput[0:-1]
    logging.info("Running of single directory %s", directory)
    fileList = os.listdir(directory)
    inputfiles = ""
    for file_ in fileList:
        logging.debug("Found file %s", SEprefix+directory+"/"+file_)
        inputfiles += SEprefix+directory+"/"+file_+" "
    haddCommand = "hadd {0}/tmpout.root {1}".format(tmpFile, inputfiles)
    logging.debug("Command: %s", haddCommand)
    logging.info("hadd to output file %s/tmpout.root", tmpFile)
    process = subprocess.Popen(haddCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error != "":
        print len(error)
        for line in error.split("\n"):
            if line != "":
                logging.error(line)
        logging.info("Exiting......")
        exit()
    else:
        pass
    if not local:
        datasetName = directory.split("/")[-1]
        if altOutput is None:
            logging.info("Transferring tmpout to SE")
            transfercommand = "xrdcp --force {0}/tmpout.root {1}{2}.root".format(tmpFile, SEprefix, directory)
        else:
            logging.info("Transferring tmpout to SE with user set destination")
            transfercommand = "xrdcp --force {0}/tmpout.root {1}{2}/{3}.root".format(tmpFile, SEprefix, altOutput, datasetName)
        logging.debug(transfercommand)
        process = subprocess.Popen(transfercommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        # if error != "":
        #     for line in error.split("\n"):
        #         if line != "":
        #             logging.error(line)
        #     logging.info("Exiting......")
        #     exit()
        logging.info("Transfer complete to %s.root", directory)
        process = subprocess.Popen("rm {0}/tmpout.root".format(tmpFile), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info("Removed tmpfile")
    else:
        logging.info("Local mode! Will rename outputfile")
        datasetName = directory.split("/")[-1]
        renameCommand = "mv {0}/tmpout.root {0}/{1}.root".format(tmpFile, datasetName)
        process = subprocess.Popen(renameCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if error != "":
            for line in error.split("\n"):
                if line != "":
                    logging.error(line)
            logging.info("Exiting......")
            exit()
        logging.info("Renamed to %s.root",datasetName)
            
def runMultHadd(startdirectory, SEprefix, tmpFile, altOutput, local):
    if startdirectory.endswith("/"):
        startdirectory = startdirectory[0:-1]
    dirList = os.listdir(startdirectory)
    for dir_ in dirList:
        runSingleHadd(startdirectory+"/"+dir_, SEprefix, tmpFile, altOutput, local)



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Handling crab jobs')
    parser.add_argument('--type', action="store", required=True, help="Run on single dataset or muliple", choices=["Single","Multi"], type=str)
    parser.add_argument('--dir', action="store", required=True, help="Start directory", type=str)
    parser.add_argument("--prefix", default="root://t3dcachedb.psi.ch/", help="server prefix to add to rootfiles", type=str)
    parser.add_argument("--tmpOut", default="/mnt/t3nfs01/data01/shome/koschwei/scratch", help="Output of the tmp file", type=str)
    parser.add_argument("--logging", default = "INFO", help="Set log level", type=str, choices=["INFO","DEBUG"])
    parser.add_argument("--altOutput", default=None, help="Alternative output for the transfer to the SE")
    parser.add_argument("--noSETransfer", action = "store_true", help="If set, the output will be renamed instead of copied to the SE")
    args = parser.parse_args()
    logging.getLogger().setLevel(args.logging)

    if args.type == "Single":
        runSingleHadd(args.dir, args.prefix, args.tmpOut, args.altOutput, args.noSETransfer)
    else:
        runMultHadd(args.dir, args.prefix, args.tmpOut, args.altOutput, args.noSETransfer)
