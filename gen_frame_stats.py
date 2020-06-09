# coding:utf-8


import argparse

from xaizalibs.standardlib import *
from xaizalibs.nplib import *
from xaizalibs.pltlib import *
from xaizalibs.CMOSanalyzerlib import *


class Manager():
    def __init__(self):
        self.config = Config()
        self.frameStats = FrameStats()
    def main(self):
        self.loadFromFrameFileList()
        self.saveFrameStatsFile()
    def loadFromFrameFileList(self):
        for strFrameFileAbsPath in self.config.lsStrFrameFileAbsPath:
            if self.config.eventList is not None:
                frameNum = self.config.eventList.getFrameNum(
                    strFrameFileAbsPath, moveDir=True)
                if frameNum is None:
                    eventData = None
                    print(
                        'WARINING : event data of ' + strFrameFileAbsPath +
                        ' is not found in the event list')
                else:
                    eventData = self.config.eventList.lsEventData[frameNum]
            else:
                eventData = None
            self.frameStats.loadFrameFile(
                    strFrameFileAbsPath, strFilledVal=self.config.strFilledVal,
                    strValidPixelCondition=self.config.strValidPixelCondition,
                    message=True, eventData=eventData,
                    strInvalidFrameShapeProcessMode=(
                        self.config.strInvalidFrameShapeProcessMode),
                    tpValidFrameShape=self.config.tpValidFrameShape,
                    lsArrReferenceFrame=self.config.lsArrReferenceFrame)
            if self.config.limitFrameNum is not None:
                if (
                        self.config.limitFrameNum
                        <= self.frameStats.frameCnt):
                    break
            print('')
    def saveFrameStatsFile(self):
        dicAppendix = {
            'event_list' : self.config.strEventListFileAbsPath,
            'reference_framme' : self.config.lsStrReferenceFrameFileAbsPath,
            'valid_pixel' : self.config.strValidPixelCondition,
            'filled_value' : self.config.strFilledVal
        }
        self.frameStats.saveAsFrameStatsFile(
            self.config.strFrameStatsFileAbsPath, message=True,
            dicAppendix=dicAppendix)


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
        self.HDUIndex = None
        self.tpValidFrameShape = None
        self.strInvalidFrameShapeProcessMode = None
        self.strFrameStatsFileAbsPath = None
        self.set()
    def genCommandLineArg(self):
        parser = argparse.ArgumentParser(
            description=(
                'generate frame stats file (fits).'))
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
            '--HDU_index', default='0',
            help='HDU index containing frame data (init : 0)')
        parser.add_argument(
            '--valid_frame_shape',
            help='valid frame shape (init : None)')
        parser.add_argument(
            '--invalid_frame_shape_process_mode',
            help='invalid frame shape process mode (init : first)')
        parser.add_argument(
            '-o', '--frame_stats_file',
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
        strFrameStatsFilePath = getConfig(
            commandLineArg.frame_stats_file, ['-o', '--frame_stats_file'],
            dicConfigFile, 'output', 'frame_stats_file_path')
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
        # self.strFrameStatsFileAbsPath の設定
        self.strFrameStatsFileAbsPath = getStrAbsPath(strFrameStatsFilePath)


manager = Manager()
manager.main()
