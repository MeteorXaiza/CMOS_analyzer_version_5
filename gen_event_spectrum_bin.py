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
        arrSpectrumVal = self.config.eventList.genArrSpectrumVal(
            self.config.strFilledVal, self.config.strBins,
            self.config.strValidEventCondition)
        if self.config.strEventSpectrumBinFileAbsPath is not None:
            dicHeader = {
                'EVLIST' : self.config.strEventListFileAbsPath,
                'VALUE' : self.config.strFilledVal,
                'BINS' : self.config.strBins,
                'LABEL' : self.config.strLabel,
                'COLOR' : self.config.strColor,
                'VALID' : self.config.strValidEventCondition}
            mkdirs(
                genLsStrDirPathAndFileName(
                        self.config.strEventSpectrumBinFileAbsPath
                    )[0], message=True)
            saveAsFits(
                arrSpectrumVal, self.config.strEventSpectrumBinFileAbsPath,
                header=dicHeader, message=True)
        if self.config.strEventSpectrumImgFileAbsPath is not None:
            setHistFromVal(arrSpectrumVal[0,:-1], arrSpectrumVal[1])
            plt.xlabel(self.config.strXLabel)
            plt.ylabel(self.config.strYLabel)
            plt.yscale(self.config.strYScale)
            mkdirs(
                genLsStrDirPathAndFileName(
                        self.config.strEventSpectrumImgFileAbsPath
                    )[0], message=True)
            plt.savefig(self.config.strEventSpectrumImgFileAbsPath)
            print(
                self.config.strEventSpectrumImgFileAbsPath + ' has been saved.')


class Config():
    def __init__(self):
        self.strEventListFileAbsPath = None
        self.eventList = None
        self.strFilledVal = None
        self.strBins = None
        self.strValidEventCondition = None
        self.strLabel = None
        self.strColor = None
        self.strXLabel = None
        self.strYLabel = None
        self.strYScale = None
        self.strEventSpectrumBinFileAbsPath = None
        self.strEventSpectrumImgFileAbsPath = None
        self.set()
    def genCommandLineArg(self):
        parser = argparse.ArgumentParser(
            description=(
                'generate event spectrum bin file (fits).'))
        parser.add_argument(
            '-c', '--config_file', help='config file path (init : None)')
        parser.add_argument(
            '-i', '--event_list_file',
            help='event list file path (init : None)')
        parser.add_argument(
            '-fv', '--filled_value', default='PHasum',
            help='filled value in spectrum (init : PHasum)')
        parser.add_argument(
            '-b', '--bins', default='np.arange(ceil(min)-1,floor(max)+2)',
            help='bins (init : np.arange(ceil(min)-1,floor(max)+2))')
        parser.add_argument(
            '-ve', '--valid_event',
            help='valid event condition (init : None)')
        parser.add_argument(
            '-l', '--label',
            help='label of spectrum (init : None)')
        parser.add_argument(
            '-cl', '--color', default='red',
            help='color of spectrum (init : red)')
        parser.add_argument(
            '-xl', '--x_label', default='PHasum [ch]',
            help='x label of spectrum (init : PHasum [ch])')
        parser.add_argument(
            '-yl', '--y_label', default='intensity [counts/bin]',
            help='x label of spectrum (init : intensity [counts/bin])')
        parser.add_argument(
            '-ys', '--y_scale', default='log',
            help='y scale of spectrum (init : log)')
        parser.add_argument(
            '-o', '--event_spectrum_bin_file',
            help='event spectrum bin file path (init : None)')
        parser.add_argument(
            '-oi', '--event_spectrum_img_file',
            help='event spectrum img file path (init : None)')
        return parser.parse_args()
    def set(self):
        commandLineArg = self.genCommandLineArg()
        if commandLineArg.config_file is not None:
            dicConfigFile = getDicIni(
                getStrAbsPath(commandLineArg.config_file), message=True)
        else:
            dicConfigFile = None
        strEventListFilePath = getConfig(
            commandLineArg.event_list_file, ['-i','--event_list_file'],
            dicConfigFile, 'input', 'event_list_file_path')
        strFilledVal = getConfig(
            commandLineArg.filled_value, ['-fv', '--filled_value'],
            dicConfigFile, 'input', 'filled_value')
        strBins = getConfig(
            commandLineArg.bins, ['-b', '--bins'], dicConfigFile, 'input',
            'bins')
        strValidEventCondition = getConfig(
            commandLineArg.valid_event, ['-ve', '--valid_event'], dicConfigFile,
            'input', 'valid_event')
        strLabel = getConfig(
            commandLineArg.label, ['-l', '--label'], dicConfigFile,
            'input', 'label')
        strColor = getConfig(
            commandLineArg.color, ['-cl', '--color'], dicConfigFile,
            'input', 'color')
        strXLabel = getConfig(
            commandLineArg.x_label, ['-xl', '--x_label'], dicConfigFile,
            'input', 'x_label')
        strYLabel = getConfig(
            commandLineArg.y_label, ['-yl', '--y_label'], dicConfigFile,
            'input', 'y_label')
        strYScale = getConfig(
            commandLineArg.y_scale, ['-ys', '--y_scale'], dicConfigFile,
            'input', 'y_scale')
        strEventSpectrumBinFilePath = getConfig(
            commandLineArg.event_spectrum_bin_file,
            ['-o', '--event_spectrum_bin_file'], dicConfigFile, 'output',
            'event_spectrum_bin_file_path')
        strEventSpectrumImgFilePath = getConfig(
            commandLineArg.event_spectrum_img_file,
            ['-oi', '--event_spectrum_img_file'], dicConfigFile, 'output',
            'event_spectrum_img_file_path')
        # self.strEventListFileAbsPath の設定
        self.strEventListFileAbsPath = getStrAbsPath(strEventListFilePath)
        # self.eventList の設定
        self.eventList = EventList()
        self.eventList.loadEventListFile(
            self.strEventListFileAbsPath, message=True)
        # self.strFilledVal の設定
        self.strFilledVal = strFilledVal
        # self.strBins の設定
        self.strBins = strBins
        # self.strValidEventCondition の設定
        self.strValidEventCondition = strValidEventCondition
        # self.strLabel の設定
        self.strLabel = strLabel
        # self.strColor の設定
        self.strColor = strColor
        # self.strLabel が None ならば再設定
        if strLabel is not None:
            strLabel = strEventListFilePath
            if strFilledVal != 'PHasum':
                strLabel += '(val:' + self.strFilledVal + ')'
            if strValidEventCondition is not None:
                strLabel += '(valid:' + self.strValidEventCondition + ')'
        self.strXLabel = strXLabel
        self.strYLabel = strYLabel
        self.strYScale = strYScale
        # self.strEventSpectrumBinFileAbsPath の設定
        self.strEventSpectrumBinFileAbsPath = self.getStrAbsPath(
            strEventSpectrumBinFilePath)
        # self.strEventSpectrumImgFileAbsPath の設定
        self.strEventSpectrumImgFileAbsPath = self.getStrAbsPath(
            strEventSpectrumImgFilePath)
    def getStrAbsPath(self, strPath):
        if strPath is None:
            return None
        else:
            return getStrAbsPath(strPath)


manager = Manager()
manager.main()
