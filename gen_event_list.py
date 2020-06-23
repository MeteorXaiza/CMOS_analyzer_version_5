# coding:utf-8


import argparse

from xaizalibs.standardlib import *
from xaizalibs.nplib import *
from xaizalibs.pltlib import *
from xaizalibs.CMOSanalyzerlib import *


class Manager():
    def __init__(self):
        self.config = Config()
        self.eventList = EventList()
    def main(self):
        self.extractFromFrameFileList()
        self.saveEventListFile()
    def extractFromFrameFileList(self):
        for strFrameFilePath in self.config.lsStrFrameFileAbsPath:
            eventData = EventData()
            eventData.extractFromSignalFrameFile(
                strFrameFilePath, self.config.event_th,
                self.config.split_th,
                arrZeroLevelFrame=self.config.arrZeroLevelFrame,
                HDUIndex=self.config.HDUIndex,
                lsArrAppendixFrame=self.config.lsArrAppendixFrame,
                maxLeak=self.config.maxLeak, message=True)
            self.eventList.appendEventData(eventData)
            if self.config.limitFrameNum is not None:
                if (
                        self.config.limitFrameNum
                        <= len(self.eventList.lsEventData)):
                    break
            print('')
    def saveEventListFile(self):
        dicAppendixHeader = {}
        dicAppendixHeader['ZEROLV'] = self.config.strZeroLevelFrameFileAbsPath
        dicAppendixHeader['EVENT_TH'] = self.config.strEvent_th
        dicAppendixHeader['SPLIT_TH'] = self.config.strSplit_th
        for cnt in range(len(self.config.lsStrAppendixFrameFileAbsPath)):
            dicAppendixHeader['APF'+str(cnt)] = (
                self.config.lsStrAppendixFrameFileAbsPath[cnt])
        mkdirs(
            genLsStrDirPathAndFileName(self.config.strEventListFileAbsPath)[0],
            message=True)
        self.eventList.saveAsEventListFile(
            self.config.strEventListFileAbsPath,
            dicAppendixHeader=dicAppendixHeader, message=True)


class Config():
    def __init__(self):
        self.lsStrFrameFileAbsPath = None
        self.limitFrameNum = None
        self.strZeroLevelFrameFileAbsPath = None
        self.arrZeroLevelFrame = None
        self.strEvent_th = None
        self.event_th = None
        self.strSplit_th = None
        self.split_th = None
        self.maxLeak = None
        self.lsStrAppendixFrameFileAbsPath = None
        self.lsArrAppendixFrame = None
        self.HDUIndex = None
        self.tpValidFrameShape = None
        self.strInvalidFrameShapeProcessMode = None
        self.strEventListFileAbsPath = None
        self.set()
    def genCommandLineArg(self):
        parser = argparse.ArgumentParser(
            description=(
                'generate event list file (fits).'))
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
            '-z', '--zero_level_frame_file',
            help='zero level frame file (init : None)')
        parser.add_argument(
            '-th', '--threshold_file', help='threshold file path (init : None)')
        parser.add_argument(
            '-eth', '--event_th', help='event_th (init : None)')
        parser.add_argument(
            '-sth', '--split_th', help='split_th (init : None)')
        parser.add_argument(
            '-ml', '--max_leak', help='max_leak (init : None)')
        parser.add_argument(
            '-a', '--appendix_frame_list_file',
            help='appendix frame list file (init : None)')
        parser.add_argument(
            '--HDU_index', default='0',
            help='HDU index containing frame data (init : 0)')
        parser.add_argument(
            '--zero_level_frame_file_HDU_index', default='0',
            help=(
                'zero level frame file HDU index containing frame data (init : '
                + '0)'))
        parser.add_argument(
            '--invalid_frame_shape_process_mode', default='continue',
            help='invalid frame shape process mode (init : continue)')
        parser.add_argument(
            '-o', '--event_list_file',
            help='event list file path(output) (init : None)')
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
        strZeroLevelFrameFilePath = getConfig(
            commandLineArg.zero_level_frame_file,
            ['-z', '--zero_level_frame_file'], dicConfigFile, 'input',
            'zero_level_frame_file_path')
        strThresholdFilePath = getConfig(
            commandLineArg.threshold_file,
            ['-th', '--threshold_file'], dicConfigFile, 'input',
            'threshold_file_path')
        strEvent_th = getConfig(
            commandLineArg.event_th, ['-eth', '--event_th'], dicConfigFile,
            'input', 'event_th')
        strSplit_th = getConfig(
            commandLineArg.split_th, ['-sth', '--split_th'], dicConfigFile,
            'input', 'split_th')
        strMaxLeak = getConfig(
            commandLineArg.max_leak, ['-ml', '--max_leak'], dicConfigFile,
            'input', 'max_leak')
        strAppendixFrameListFilePath = getConfig(
            commandLineArg.appendix_frame_list_file,
            ['-a', '--appendix_frame_list_file'], dicConfigFile, 'input',
            'appendix_frame_list_file_path')
        strHDUIndex = getConfig(
            commandLineArg.HDU_index, ['--HDU_index'], dicConfigFile,
            'input', 'HDU_index')
        strZeroLevelFrameFileHDUIndex = getConfig(
            commandLineArg.zero_level_frame_file_HDU_index,
            ['--zero_level_frame_file_HDU_index'], dicConfigFile,
            'input', 'zero_level_frame_file_HDU_index')
        strInvalidFrameShapeProcessMode = getConfig(
            commandLineArg.invalid_frame_shape_process_mode,
            ['--invalid_frame_shape_process_mode'], dicConfigFile, 'input',
            'invalid_frame_shape_process_mode')
        strEventListFilePath = getConfig(
            commandLineArg.event_list_file,
            ['--event_list_file', '-o'], dicConfigFile, 'output',
            'event_list_file_path')
        # self.lsStrFrameFileAbsPath の設定
        if strFrameListFilePath is not None:
            lsStrFrameFilePath = getLsStrTxtLine(
                getStrAbsPath(strFrameListFilePath), message=True)
        else:
            if strInputDirPath[-1] not in ['/', '']:
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
        # self.strZeroLevelFrameFileAbsPath と self.arrZeroLevelFrame の設定
        if strZeroLevelFrameFilePath is not None:
            self.strZeroLevelFrameFileAbsPath = getStrAbsPath(
                strZeroLevelFrameFilePath)
            self.arrZeroLevelFrame = getArrFits(
                self.strZeroLevelFrameFileAbsPath, message=True,
                index=int(strZeroLevelFrameFileHDUIndex))
        else:
            self.strZeroLevelFrameFileAbsPath = None
            self.arrZeroLevelFrame = None
        # self.event_th と self.strEvent_th と self.split_th と self.strSplit_th
        # の設定
        if strEvent_th is not None:
            self.event_th = self.genThreshold(strEvent_th)
            self.strEvent_th = strEvent_th
        if strSplit_th is not None:
            self.split_th = self.genThreshold(strSplit_th)
            self.strSplit_th = strSplit_th
        if self.event_th is None or self.split_th is None:
            dicThreshold = getDicJSON(
                getStrAbsPath(strThresholdFilePath), message=True)
            if self.event_th is None:
                self.strEvent_th = str(dicThreshold['event_th'])
                self.event_th = self.genThreshold(self.strEvent_th)
            if self.split_th is None:
                self.strSplit_th = str(dicThreshold['split_th'])
                self.split_th = self.genThreshold(self.strSplit_th)
        # self.maxLeakの設定
        self.maxLeak = int(strMaxLeak)
        # self.lsStrAppendixFrameFileAbsPath と self.lsArrAppendixFrame の設定
        self.lsArrAppendixFrame = []
        self.lsStrAppendixFrameFileAbsPath = []
        if strAppendixFrameListFilePath is not None:
            lsStrAppendixFrameFilePath = getLsStrTxtLine(
                getStrAbsPath(strAppendixFrameListFilePath), message=True)
            for cnt, strAppendixFrameFilePath in enumerate(
                    lsStrAppendixFrameFilePath):
                strAppendixFrameFileAbsPath = getStrAbsPath(
                    strAppendixFrameFilePath)
                self.lsArrAppendixFrame.append(
                    getArrFits(strAppendixFrameFileAbsPath, message=True))
                self.lsStrAppendixFrameFileAbsPath.append(
                    strAppendixFrameFileAbsPath)
        # self.HDUIndex の設定
        self.HDUIndex = int(strHDUIndex)
        # self.strInvalidFrameShapeProcessMode の設定
        self.strInvalidFrameShapeProcessMode = strInvalidFrameShapeProcessMode
        # self.strEventListFileAbsPath の設定
        self.strEventListFileAbsPath = getStrAbsPath(strEventListFilePath)
    def genThreshold(self, strThreshold):
        if re.match('\d+\.?\d*', strThreshold) is not None:
            return float(strThreshold)
        else:
            return getArrFits(getStrAbsPath(strThreshold), message=True)


manager = Manager()
manager.main()
