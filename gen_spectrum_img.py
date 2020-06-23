# coding:utf-8


import argparse

from xaizalibs.standardlib import *
from xaizalibs.nplib import *
from xaizalibs.pltlib import *
from xaizalibs.CMOSanalyzerlib import *


class Manager():
    def __init__(self):
        self.config = Config()
    def main(self):
        if self.config.autoColoring:
            lsArrColor = list(
                genArrHueCircle(
                    np.linspace(
                        0, 2*pi,
                        len(self.config.lsStrSpectrumBinFileAbsPath) + 1
                    )
                )[:-1] / 255.)
        for cnt, strSpectrumBinFileAbsPath in enumerate(
                self.config.lsStrSpectrumBinFileAbsPath):
            dicSpectrumVal = getDicFits(strSpectrumBinFileAbsPath, message=True)
            if self.config.autoColoring:
                color = tuple(lsArrColor[cnt])
            else:
                color = dicSpectrumVal['header']['COLOR']
            strLabel = dicSpectrumVal['header']['LABEL']
            arrSpectrumVal = dicSpectrumVal['data']
            setHistFromVal(
                arrSpectrumVal[0,:-1], arrSpectrumVal[1], color=color,
                label=strLabel)
        plt.xlabel(self.config.strXLable)
        plt.ylabel(self.config.strYLabel)
        plt.yscale(self.config.strYScale)
        if len(self.config.lsStrSpectrumBinFileAbsPath) > 1:
            setLegend()
        plt.savefig(self.config.strSpectrumImgFileAbsPath)
        print(self.config.strSpectrumImgFileAbsPath + ' has been saved.')




class Config():
    def __init__(self):
        self.lsStrSpectrumBinFileAbsPath = None
        self.strXLable = None
        self.strYLabel = None
        self.strXScale = None
        self.autoColoring = None
        self.strSpectrumImgFileAbsPath = None
        self.set()
    def genCommandLineArg(self):
        parser = argparse.ArgumentParser(
            description=(
                'generate spectrum image file (fits).'))
        parser.add_argument(
            '-c', '--config_file', help='config file path (init : None)')
        parser.add_argument(
            '-i', '--spectrum_bin_file',
            help='spectrum bin file path (init : None)')
        parser.add_argument(
            '-sl', '--spectrum_bin_list_file',
            help='spectrum bin list file path (init : PHasum)')
        parser.add_argument(
            '-xl', '--x_label', default='PHasum [ch]',
            help='x label (init : PHasum [ch])')
        parser.add_argument(
            '-yl', '--y_label', default='intensity [counts/bin]',
            help='y label (init : intensity [counts/bin])')
        parser.add_argument(
            '-ys', '--y_scale', default='log',
            help='y scale (init : log)')
        parser.add_argument(
            '--auto_coloring', default='True',
            help='auto coloring (init : True)')
        parser.add_argument(
            '-o', '--spectrum_img_file',
            help='event spectrum img file path (init : None)')
        return parser.parse_args()
    def set(self):
        commandLineArg = self.genCommandLineArg()
        if commandLineArg.config_file is not None:
            dicConfigFile = getDicIni(
                getStrAbsPath(commandLineArg.config_file), message=True)
        else:
            dicConfigFile = None
        strSpectrumBinFilePath = getConfig(
            commandLineArg.spectrum_bin_file, ['-i', '--spectrum_bin_file'],
            dicConfigFile, 'input', 'spectrum_bin_file_path')
        strSpectrumBinListFilePath = getConfig(
            commandLineArg.spectrum_bin_list_file,
            ['-sl', '--spectrum_bin_list_file'], dicConfigFile, 'input',
            'spectrum_bin_list_file_path')
        strXLabel = getConfig(
            commandLineArg.x_label, ['-xl', '--x_label'], dicConfigFile,
            'input', 'x_label')
        strYLabel = getConfig(
            commandLineArg.y_label, ['-yl', '--y_label'], dicConfigFile,
            'input', 'y_label')
        strYScale = getConfig(
            commandLineArg.y_scale, ['-ys', '--y_scale'], dicConfigFile,
            'input', 'y_scale')
        strAutoColoring = getConfig(
            commandLineArg.auto_coloring, ['--auto_coloring'], dicConfigFile,
            'input', 'auto_coloring')
        strSpectrumImgFilePath = getConfig(
            commandLineArg.spectrum_img_file, ['-o', '--spectrum_img_file'],
            dicConfigFile, 'output', 'spectrum_img_file_path')
        self.lsStrSpectrumBinFileAbsPath = []
        if strSpectrumBinFilePath is not None:
            self.lsStrSpectrumBinFileAbsPath.append(
                getStrAbsPath(strSpectrumBinFilePath))
        if strSpectrumBinListFilePath is not None:
            lsStrSpectrumBinFilePath = getLsStrTxtLine(
                strSpectrumBinListFilePath, message=True)
            for strSpectrumBinFilePath in lsStrSpectrumBinFilePath:
                self.lsStrSpectrumBinFileAbsPath.append(
                    getStrAbsPath(strSpectrumBinFilePath))
        self.strXLabel = strXLabel
        self.strYLabel = strYLabel
        self.strYScale = strYScale
        if strAutoColoring == 'False':
            self.autoColoring = False
        else:
            self.autoColoring = True
        self.strSpectrumImgFileAbsPath = getStrAbsPath(strSpectrumImgFilePath)


manager = Manager()
manager.main()
