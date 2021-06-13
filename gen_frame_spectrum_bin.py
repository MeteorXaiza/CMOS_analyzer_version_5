# coding:utf-8


import argparse

from xaizalibs.standardlib import *
from xaizalibs.nplib import *
from xaizalibs.pltlib import *
from xaizalibs.CMOSanalyzerlib import *


class Manager():
    def __init__(self):
        self.config = Config()
        self.frameSpectrum = FrameSpectrum()
    def main(self):
        self.saveFrameStatsFile()
        self.defineBins()
        self.loadFromFrameFileList()
        self.saveFrameSpectrumBinFile()
        self.saveFrameSpectrumImgFile()
    def saveFrameStatsFile(self):
        if self.config.strOutputFrameStatsFileAbsPath is not None:
            mkdirs(
                genLsStrDirPathAndFileName(
                    self.config.strOutputFrameStatsFileAbsPath)[0],
                message=True)
            self.config.frameStats.saveAsFrameStatsFile(
                self.config.strOutputFrameStatsFileAbsPath, message=True)
    def defineBins(self):
        self.frameSpectrum.defineBins(
            self.config.strBins, self.config.frameStats)
    def loadFromFrameFileList(self):
        for strFrameFileAbsPath in self.config.lsStrFrameFileAbsPath:
            if self.config.eventList is not None:
                frameNum = self.config.eventList.getFrameNum(
                    strFrameFileAbsPath, moveDir=True)
                if frameNum is None:
                    print(
                        'WARINING : event data of ' + strFrameFileAbsPath +
                        ' is not found in the event list')
                    eventData = None
                else:
                    eventData = self.config.eventList.lsEventData[frameNum]
            else:
                eventData = None
            self.frameSpectrum.loadFrameFile(
                    strFrameFileAbsPath,
                    strFilledVal=self.config.strFilledVal,
                    strValidPixelCondition=self.config.strValidPixelCondition,
                    message=True,
                    strInvalidFrameShapeProcessMode=(
                        self.config.strInvalidFrameShapeProcessMode),
                    lsArrReferenceFrame=self.config.lsArrReferenceFrame,
                    tpValidFrameShape=self.config.tpValidFrameShape,
                    eventData=eventData)
            if self.config.limitFrameNum is not None:
                if (
                        self.config.limitFrameNum
                        <= self.frameSpectrum.frameCnt):
                    break
            print('')
    def saveFrameSpectrumBinFile(self):
        dicAppendixHeader = {
            'LABEL' : self.config.strLabel,
            'COLOR' : self.config.strColor,
            'EVLIST' : self.config.strEventListFileAbsPath,
            'VALUE' : self.config.strFilledVal,
            'BINS' : self.config.strBins,
            'VALIDPIX' : self.config.strValidPixelCondition}
        for cnt in range(len(self.config.lsStrReferenceFrameFileAbsPath)):
            dicAppendixHeader['REF' + str(cnt)] = (
                self.config.lsStrReferenceFrameFileAbsPath[cnt])
        if self.config.strInputFrameStatsFileAbsPath is not None:
            dicAppendixHeader['FSTATS'] = (
                self.config.strInputFrameStatsFileAbsPath)
        elif self.config.strOutputFrameStatsFileAbsPath is not None:
            dicAppendixHeader['FSTATS'] = (
                self.config.strOutputFrameStatsFileAbsPath)
        mkdirs(
            genLsStrDirPathAndFileName(
                self.config.strFrameSpectrumBinFileAbsPath)[0],
                message=True)
        self.frameSpectrum.saveAsSpectrumBinFile(
            self.config.strFrameSpectrumBinFileAbsPath, message=True,
            dicAppendixHeader=dicAppendixHeader)
    def saveFrameSpectrumImgFile(self):
        if self.config.strFrameSpectrumImgFileAbsPath is None:
            return None
        setHistFromVal(self.frameSpectrum.arrCnt, self.frameSpectrum.arrBins)
        plt.xlabel(self.config.strXLabel)
        plt.ylabel(self.config.strYLabel)
        plt.yscale(self.config.strYScale)
        mkdirs(
            genLsStrDirPathAndFileName(
                self.config.strFrameSpectrumImgFileAbsPath)[0],
            message=True)
        plt.savefig(self.config.strFrameSpectrumImgFileAbsPath)
        print(
            self.config.strFrameSpectrumImgFileAbsPath + ' has been saved.')


class Config():
    def __init__(self):
        self.lsStrFrameFileAbsPath = None
        self.limitFrameNum = None
        self.strEventListFileAbsPath = None
        self.eventList = None
        self.lsStrReferenceFrameFileAbsPath = None
        self.lsArrReferenceFrame = None
        self.strValidPixelCondition = None
        self.strFilledVal= None
        self.strBins = None
        self.strInputFrameStatsFileAbsPath = None
        self.frameStats = None
        self.strLabel = None
        self.strColor = None
        self.HDUIndex = None
        self.tpValidFrameShape = None
        self.strInvalidFrameShapeProcessMode = None
        self.strXLabel = None
        self.strYLabel = None
        self.strFrameSpectrumBinFileAbsPath = None
        self.strFrameSpectrumImgFileAbsPath = None
        self.strOutputFrameStatsFileAbsPath = None
        self.set()
    def genCommandLineArg(self):
        parser = argparse.ArgumentParser(
            description=(
                'generate frame spectrum bin file (fits).'))
        parser.add_argument(
            '-c', '--config_file', help='config file path (init : None)')
        parser.add_argument(
            '-i', '--input_directory', default='./',
            help='input directory path (init : ./)')
        parser.add_argument(
            '-m', '--match_file_name', default='.+\.fits',
            help='file name as regular expression (init : .+\\.fits)')
        parser.add_argument(
            '--frame_list_file',
            help='frame list file (init : None)')
        parser.add_argument(
            '--limit_frame_num',
            help='limit frame number in analysis (init : None)')
        parser.add_argument(
            '--event_list_file', help='event list file path (init : None)')
        parser.add_argument(
            '--valid_pixel', help='valid pixel condition (init : None)')
        parser.add_argument(
            '-fv', '--filled_value', default='raw',
            help='filled value (init : raw)')
        parser.add_argument(
            '-r', '--reference_frame_list_file',
            help='reference frame list file (init : None)')
        parser.add_argument(
            '-b', '--bins', default='np.arange(ceil(min)-1,floor(max)+2)',
            help='spectrum bins (init : np.arange(ceil(min)-1,floor(max)+2))')
        parser.add_argument(
            '-ifs', '--input_frame_stats_file',
            help='input frame stats file (init : None')
        parser.add_argument(
            '-l', '--label',
            help='label of spectrum (init : None)')
        parser.add_argument(
            '-cl', '--color', default='red',
            help='color of spectrum (init : red)')
        parser.add_argument(
            '--HDU_index', default='0',
            help='HDU index containing frame data (init : 0)')
        parser.add_argument(
            '--valid_frame_shape',
            help='valid frame shape (init : None)')
        parser.add_argument(
            '--invalid_frame_shape_process_mode',
            help='invalid frame shape process mode (init : first)')
        parser.add_argument(
            '-xl', '--x_label', default='PH [ch]',
            help='x label of spectrum (init : PH [ch])')
        parser.add_argument(
            '-yl', '--y_label', default='intensity [counts/bin]',
            help='x label of spectrum (init : intensity [counts/bin])')
        parser.add_argument(
            '-ys', '--y_scale', default='log',
            help='y scale of spectrum (init : log)')
        parser.add_argument(
            '-o', '--frame_spectrum_bin_file',
            help='frame spectrum bin file path(output) (init : None)')
        parser.add_argument(
            '-oi', '--frame_spectrum_img_file',
            help='frame spectrum img file path(output) (init : None)')
        parser.add_argument(
            '-ofs', '--output_frame_stats_file',
            help='frame stats file path(output) (init : None)')
        return parser.parse_args()
    def set(self):
        commandLineArg = self.genCommandLineArg()
        if commandLineArg.config_file is not None:
            dicConfigFile = getDicIni(
                getStrAbsPath(commandLineArg.config_file), message=True)
        else:
            dicConfigFile = None
        strInputDirPath = getConfig(
            commandLineArg.input_directory, ['-i','--input_directory'],
            dicConfigFile, 'input', 'directory_path')
        strMatchFileName = getConfig(
            commandLineArg.match_file_name, ['-m', '--match_file_name'],
            dicConfigFile, 'input', 'match_file_name')
        strFrameListFilePath = getConfig(
            commandLineArg.frame_list_file, ['--frame_list_file'],
            dicConfigFile, 'input', 'frame_list_file_path')
        strLimitFrameNum = getConfig(
            commandLineArg.limit_frame_num, ['--limit_frame_num'],
            dicConfigFile, 'input', 'limit_frame_num')
        strEventListFilePath = getConfig(
            commandLineArg.event_list_file, ['--event_list_file'],
            dicConfigFile, 'input', 'event_list_file_path')
        strValidPixelCondition = getConfig(
            commandLineArg.valid_pixel, ['--valid_pixel'], dicConfigFile,
            'input', 'valid_pixel')
        strFilledVal = getConfig(
            commandLineArg.filled_value, ['-fv', '--filled_value'],
            dicConfigFile, 'input', 'filled_value')
        strReferenceFrameListFilePath = getConfig(
            commandLineArg.reference_frame_list_file,
            ['-r', '--reference_frame_list_file'], dicConfigFile, 'input',
            'reference_frame_list_file_path')
        strBins = getConfig(
            commandLineArg.bins,
            ['-b', '--bins'], dicConfigFile, 'input',
            'bins')
        strInputFrameStatsFilePath = getConfig(
            commandLineArg.input_frame_stats_file,
            ['-ifs', '--input_frame_stats_file'], dicConfigFile, 'input',
            'frame_stats_file_path')
        strLabel = getConfig(
            commandLineArg.label, ['-l', '--label'], dicConfigFile,
            'input', 'label')
        strColor = getConfig(
            commandLineArg.color, ['-cl', '--color'], dicConfigFile,
            'input', 'color')
        strHDUIndex = getConfig(
            commandLineArg.HDU_index, ['--HDU_index'], dicConfigFile,
            'input', 'HDU_index')
        strValidFrameShape = getConfig(
            commandLineArg.valid_frame_shape, ['--valid_frame_shape'],
            dicConfigFile, 'input', 'valid_frame_shape')
        strInvalidFrameShapeProcessMode = getConfig(
            commandLineArg.invalid_frame_shape_process_mode,
            ['--invalid_frame_shape_process_mode'], dicConfigFile, 'input',
            'invalid_frame_shape_process_mode')
        strXLabel = getConfig(
            commandLineArg.x_label, ['-xl', '--x_label'], dicConfigFile,
            'input', 'x_label')
        strYLabel = getConfig(
            commandLineArg.y_label, ['-yl', '--y_label'], dicConfigFile,
            'input', 'y_label')
        strYScale = getConfig(
            commandLineArg.y_scale, ['-ys', '--y_scale'], dicConfigFile,
            'input', 'y_scale')
        strOutputFrameStatsFilePath = getConfig(
            commandLineArg.output_frame_stats_file,
            ['-ofs', '--output_frame_stats_file'], dicConfigFile, 'output',
            'frame_stats_file_path')
        strFrameSpectrumBinFilePath = getConfig(
            commandLineArg.frame_spectrum_bin_file,
            ['-o', '--frame_spectrum_bin_file'], dicConfigFile, 'output',
            'frame_spectrum_bin_file_path')
        strFrameSpectrumImgFilePath = getConfig(
            commandLineArg.frame_spectrum_img_file,
            ['-oi', '--frame_spectrum_img_file'], dicConfigFile, 'output',
            'frame_spectrum_img_file_path')
        # self.lsStrFrameFileAbsPath の設定
        if strFrameListFilePath is not None:
            lsStrFrameFilePath = getLsStrTxtLine(
                getStrAbsPath(strFrameListFilePath), message=True)
        else:
            if strInputDirPath[-1] not in ['/', '\\']:
                strInputDirPath += '/'
            lsStrFrameFileName = sorted(
                getLsStrFileName(strInputDirPath, match=strMatchFileName))
            lsStrFrameFilePath = []
            for strFrameFileName in lsStrFrameFileName:
                lsStrFrameFilePath.append(
                    strInputDirPath + strFrameFileName)
        self.lsStrFrameFileAbsPath = []
        for strFrameFilePath in lsStrFrameFilePath:
            self.lsStrFrameFileAbsPath.append(getStrAbsPath(strFrameFilePath))
        # self.limitFrameNum の設定
        if strLimitFrameNum is not None:
            self.limitFrameNum = int(strLimitFrameNum)
        else:
            self.limitFrameNum = None
        # self.strEventListFileAbsPath と self.eventList の設定
        if strEventListFilePath is not None:
            self.strEventListFileAbsPath = getStrAbsPath(strEventListFilePath)
            self.eventList = EventList()
            self.eventList.loadEventListFile(
                self.strEventListFileAbsPath, message=True)
        else:
            self.strEventListFileAbsPath = None
            self.eventList = None
        # self.strValidPixelCondition の設定
        self.strValidPixelCondition = strValidPixelCondition
        # self.strFilledVal の設定
        self.strFilledVal = strFilledVal
        # self.lsStrReferenceFrameFileAbsPath と self.lsArrReferenceFrame の設定
        self.lsStrReferenceFrameFileAbsPath = []
        self.lsArrReferenceFrame = []
        if strReferenceFrameListFilePath is not None:
            lsStrReferenceFrameFilePath = getLsStrTxtLine(
                getStrAbsPath(strReferenceFrameListFilePath), message=True)
            for strReferenceFrameFilePath in lsStrReferenceFrameFilePath:
                strReferenceFrameFileAbsPath = getStrAbsPath(
                    strReferenceFrameFilePath)
                self.lsStrReferenceFrameFileAbsPath.append(
                    strReferenceFrameFileAbsPath)
                self.lsArrReferenceFrame.append(
                    getArrFits(strReferenceFrameFileAbsPath, message=True))
        # self.strBins の設定
        self.strBins = strBins
        # self.strInputFrameStatsFileAbsPath と self.frameStats の設定
        if strInputFrameStatsFilePath is not None:
            self.strInputFrameStatsFileAbsPath = getStrAbsPath(
                strInputFrameStatsFilePath)
            self.frameStats = FrameStats()
            self.frameStats.loadFrameStatsFile(
                getStrAbsPath(strInputFrameStatsFilePath), message=True)
        else:
            self.strInputFrameStatsFileAbsPath = None
            self.frameStats = None
        # self.strLabel の設定
        if strLabel is None:
            self.strLabel = self.strFilledVal
        else:
            self.strLabel = strLabel
        # self.strColor の設定
        self.strColor = strColor
        # self.HDUIndex の設定
        self.HDUIndex = int(strHDUIndex)
        # self.tpValidFrameShape の設定
        if strValidFrameShape is not None:
            tpGroups = re.match('(\d+)x(\d+)', strValidFrameShape).groups()
            self.tpValidFrameShape = (int(tpGroups[0]), int(tpGroups[1]))
        else:
            self.tpValidFrameShape = None
        # self.strInvalidFrameShapeProcessMode の設定
        self.strInvalidFrameShapeProcessMode = strInvalidFrameShapeProcessMode
        self.strXLabel = strXLabel
        self.strYLabel = strYLabel
        self.strYScale = strYScale
        # self.strFrameSpectrumBinFilePath の設定
        self.strFrameSpectrumBinFileAbsPath = self.getStrAbsPath(
            strFrameSpectrumBinFilePath)
        # self.strFrameSpectrumBinFilePath の設定
        self.strFrameSpectrumImgFileAbsPath = self.getStrAbsPath(
            strFrameSpectrumImgFilePath)
        # self.strOutputFrameStatsFilePath の設定
        self.strOutputFrameStatsFileAbsPath = self.getStrAbsPath(
            strOutputFrameStatsFilePath)
        # self.frameStats をコンフィグから設定
        if self.frameStats is None:
            self.frameStats = self.genFrameStats()
    def genFrameStats(self):
        ret = FrameStats()
        for strFrameFileAbsPath in self.lsStrFrameFileAbsPath:
            if self.eventList is not None:
                frameNum = self.eventList.getFrameNum(
                    strFrameFileAbsPath, moveDir=True)
                if frameNum is None:
                    eventData = None
                else:
                    eventData = self.eventList.lsEventData[frameNum]
            else:
                eventData = None
            ret.loadFrameFile(
                strFrameFileAbsPath, strFilledVal=self.strFilledVal,
                strValidPixelCondition=self.strValidPixelCondition,
                message=True, eventData=eventData,
                strInvalidFrameShapeProcessMode=(
                    self.strInvalidFrameShapeProcessMode),
                tpValidFrameShape=self.tpValidFrameShape,
                lsArrReferenceFrame=self.lsArrReferenceFrame)
            if self.limitFrameNum is not None:
                if self.limitFrameNum <= ret.frameCnt:
                    break
        return ret
    def getStrAbsPath(self, strPath):
        if strPath is None:
            return None
        else:
            return getStrAbsPath(strPath)


manager = Manager()
manager.main()
