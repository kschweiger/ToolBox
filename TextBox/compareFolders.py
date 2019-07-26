import glob

def main(folders, width, title):
    files = {}
    fileNames = {}
    folderName = {}
    filePaths = {}
    fileSets = {}
    for folder in folders:
        folderName[folder] = folder.split("/")[-2] if folder.endswith("/") else folder.split("/")[-1]
        files[folder] = glob.glob(folder+"/*.pdf")
        fileNames[folder] = {}
        filePaths[folder] = {}
        for _file in files[folder]:
            fileNames[folder][_file] = _file.split("/")[-1]
            filePaths[folder][_file.split("/")[-1]] = _file
            
        fileSets[folder] = set(filePaths[folder].keys())

    for iFolder, folder in enumerate(folders):
        if iFolder == 0:
            resSet = fileSets[folder]
        else:
            resSet = resSet.intersection(fileSets[folder])

    files2Plot = sorted(list(resSet))

    _title = title
    title = title.replace("_"," ")
    # assert isinstance(files, list)
    # assert isinstance(titles, list)
    # assert len(files) == len(titles)
    # assert len(files) == nColumns

    lines = ""
    
    lines += "\\documentclass[english,9pt]{beamer} \n"
    lines += "\\usetheme{uzhneu-en} \n"
    lines += "\\begin{document} \n"
    lines += "\\title["+title+"]{"+title+"} \n"
    lines += "\\maketitle \n"
    for i,file_ in enumerate(files2Plot):
        lines += "\\begin{frame}{AutoGen Page "+str(i)+"}\label{slide:PDFAutoGenPage"+str(i)+"} \n"
        lines += " \\begin{columns}[c] \n"
        for folder in folders:        
            lines += " \column{"+width+"\\textwidth} \n"
            lines += "  \centering "+folderName[folder].replace("_","-")+" \n"
            lines += "  \\begin{figure} \n"
            lines += "   \includegraphics[width=1\\textwidth]{"+filePaths[folder][file_]+"} \n"
            lines += "  \end{figure} \n"
        lines += " \end{columns} \n"
        lines += "\end{frame} \n"

    lines += "\\end{document} \n"

    with open(_title+".tex", "w") as f:
        f.write(lines)

    print("Compile with: pdflatex "+_title+".tex")
        
if __name__ == "__main__":
    import argparse
    ##############################################################################################################
    ##############################################################################################################
    # Argument parser definitions:
    argumentparser = argparse.ArgumentParser(
        description='Description'
    )
    argumentparser.add_argument(
        "--folders",
        action = "store",
        help = "PDF files for the comparsion. ",
        nargs='+',
        type = str,
    )
    argumentparser.add_argument(
        "--columnWidth",
        action = "store",
        help = "Column width",
        type = str,
        default = "0.5",
    )
    argumentparser.add_argument(
        "--title",
        action = "store",
        help = "Column width",
        type = str,
        required=True
    )
    
    
    args = argumentparser.parse_args()
    main(args.folders, args.columnWidth, args.title)
