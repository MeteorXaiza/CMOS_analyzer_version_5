# coding:utf-8


import argparse

from xaizalibs.standardlib import *
from xaizalibs.nplib import *
from xaizalibs.pltlib import *
from xaizalibs.CMOSanalyzerlib import *


class Manager():
    def __init__(self):
        self.config = Config()
        self.backGround = BackGround(tpFrameShape=self.config.tpValidFrameShape)
    def main(self):
        self.loadFromFrameFileList()
        self.saveStatsFrameFile()
        self.saveStatsFile()
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
            self.backGround.loadSignalFrameFile(
                strFrameFileAbsPath, eventData=eventData,
                HDUIndex=self.config.HDUIndex,
                strInvalidFrameShapeProcessMode=(
                    self.config.strInvalidFrameShapeProcessMode),
                maxLeak=None, message=True)
            if self.config.limitFrameNum is not None:
                if (
                        self.config.limitFrameNum
                        <= len(self.backGround.lsStrSignalFrameFilePath)):
                    break
            print('')
    def saveStatsFrameFile(self):
        dicAppendixHeader = {'EVLIST' : self.config.strEventListFileAbsPath}
        if self.config.strMeanBGFrameFileAbsPath is not None:
            mkdirs(
                genLsStrDirPathAndFileName(
                    self.config.strMeanBGFrameFileAbsPath)[0],
                message=True)
            self.backGround.saveMeanSignalFrameFile(
                self.config.strMeanBGFrameFileAbsPath, message=True,
                dicAppendixHeader=dicAppendixHeader)
        if self.config.strStdBGFrameFileAbsPath is not None:
            mkdirs(
                genLsStrDirPathAndFileName(
                    self.config.strStdBGFrameFileAbsPath)[0],
                message=True)
            self.backGround.saveStdSignalFrameFile(
                self.config.strStdBGFrameFileAbsPath, message=True,
                dicAppendixHeader=dicAppendixHeader)
        if self.config.strSkewnessBGFrameFileAbsPath is not None:
            mkdirs(
                genLsStrDirPathAndFileName(
                    self.config.strSkewnessBGFrameFileAbsPath)[0],
                message=True)
            self.backGround.saveSkewnessSignalFrameFile(
                self.config.strSkewnessBGFrameFileAbsPath, message=True,
                dicAppendixHeader=dicAppendixHeader)
        if self.config.strKurtosisBGFrameFileAbsPath is not None:
            mkdirs(
                genLsStrDirPathAndFileName(
                    self.config.strKurtosisBGFrameFileAbsPath)[0],
                message=True)
            self.backGround.saveKurtosisSignalFrameFile(
                self.config.strKurtosisBGFrameFileAbsPath, message=True,
                dicAppendixHeader=dicAppendixHeader)
        if self.config.strMinBGFrameFileAbsPath is not None:
            mkdirs(
                genLsStrDirPathAndFileName(
                    self.config.strMinBGFrameFileAbsPath)[0],
                message=True)
            self.backGround.saveMinSignalFrameFile(
                self.config.strMinBGFrameFileAbsPath, message=True,
                dicAppendixHeader=dicAppendixHeader)
        if self.config.strMaxBGFrameFileAbsPath is not None:
            mkdirs(
                genLsStrDirPathAndFileName(
                    self.config.strMaxBGFrameFileAbsPath)[0],
                message=True)
            self.backGround.saveMaxSignalFrameFile(
                self.config.strMaxBGFrameFileAbsPath, message=True,
                dicAppendixHeader=dicAppendixHeader)
        if self.config.strCntBGFrameFileAbsPath is not None:
            mkdirs(
                genLsStrDirPathAndFileName(
                    self.config.strCntBGFrameFileAbsPath)[0],
                message=True)
            self.backGround.saveCntSignalFrameFile(
                self.config.strCntBGFrameFileAbsPath, message=True,
                dicAppendixHeader=dicAppendixHeader)
    def saveStatsFile(self):
        if self.config.strPHStatsFileAbsPath is None:
            return None
        dicAppendix = {
            'event_list' : self.config.strEventListFileAbsPath,
            'zero_level_frame' : self.config.strZeroLevelFrameFileAbsPath,
            'signal_frame' : self.backGround.lsStrSignalFrameFilePath}
        if self.config.strZeroLevelFrameFileAbsPath is not None:
            dicAppendix['zero_level_frame'] = (
                self.config.strZeroLevelFrameFileAbsPath)
        elif self.config.strMeanBGFrameFileAbsPath is not None:
            dicAppendix['zero_level_frame'] = (
                self.config.strMeanBGFrameFileAbsPath)
        else:
            dicAppendix['zero_level_frame'] = None
        dicPHStats = self.genDicPHStats()
        dicPHStats['config'] = dicAppendix
        mkdirs(
            genLsStrDirPathAndFileName(
                self.config.strPHStatsFileAbsPath)[0],
            message=True)
        saveAsJSON(
            dicPHStats, self.config.strPHStatsFileAbsPath, indent=2,
            message=True)
    def genDicPHStats(self):
        if self.config.strValidPixelCondition is not None:
            arrIsUnmaskedFrame = self.backGround.genArrIsUnmaskedFrame(
                self.config.strValidPixelCondition)
        else:
            arrIsUnmaskedFrame = None
        if self.config.arrZeroLevelFrame is not None:
            return self.backGround.genDicPHStats(
                self.config.arrZeroLevelFrame,
                arrIsUnmaskedFrame=arrIsUnmaskedFrame)
        else:
            return self.backGround.genDicPHStats(
                self.backGround.genArrMeanPowSignalFrame(1),
                arrIsUnmaskedFrame=arrIsUnmaskedFrame)


class Config():
    def __init__(self):
        self.lsStrFrameFileAbsPath = None
        self.limitFrameNum = None
        self.strEventListFileAbsPath = None
        self.eventList = None
        self.strValidPixelCondition = None
        self.strZeroLevelFrameFileAbsPath = None
        self.arrZeroLevelFrame = None
        self.HDUIndex = None
        self.tpValidFrameShape = None
        self.strInvalidFrameShapeProcessMode = None
        self.strMeanBGFrameFileAbsPath = None
        self.strStdBGFrameFileAbsPath = None
        self.strSkewnessBGFrameFileAbsPath = None
        self.strKurtosisBGFrameFileAbsPath = None
        self.strMinBGFrameFileAbsPath = None
        self.strMaxBGFrameFileAbsPath = None
        self.strCntBGFrameFileAbsPath = None
        self.strPHStatsFileAbsPath = None
        self.set()
    def genCommandLineArg(self):
        parser = argparse.ArgumentParser(
            description=(
                'generate BG stats frame file and PH stats file(fits).'))
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
            '--zero_level_frame_file',
            help='zero level frame file path (init : None)')
        parser.add_argument(
            '--HDU_index', default='0',
            help='HDU index containing frame data (init : 0)')
        parser.add_argument(
            '--zero_level_frame_file_HDU_index', default='0',
            help=(
                'zero level frame file HDU index containing frame data (init : '
                + '0)'))
        parser.add_argument(
            '--valid_frame_shape',
            help='valid frame shape (init : None)')
        parser.add_argument(
            '--invalid_frame_shape_process_mode', default='continue',
            help='invalid frame shape process mode (init : continue)')
        parser.add_argument(
            '-o', '--mean_BG_frame_file',
            help='mean BG file path(output) (init : None)')
        parser.add_argument(
            '--std_BG_frame_file',
            help='std BG file path(output) (init : None)')
        parser.add_argument(
            '--skewness_BG_frame_file',
            help='skewness BG file path(output) (init : None)')
        parser.add_argument(
            '--kurtosis_BG_frame_file',
            help='kurtosis BG file path(output) (init : None)')
        parser.add_argument(
            '--min_BG_frame_file',
            help='min BG file path(output) (init : None)')
        parser.add_argument(
            '--max_BG_frame_file',
            help='max BG file path(output) (init : None)')
        parser.add_argument(
            '--cnt_BG_frame_file',
            help='cnt BG file path(output) (init : None)')
        parser.add_argument(
            '--PH_stats_file',
            help='PH stats file path(output) (init : None)')
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
        strZeroLevelFrameFilePath = getConfig(
            commandLineArg.zero_level_frame_file,
            ['--zero_level_frame_file'], dicConfigFile,
            'input', 'zero_level_frame_file_path')
        strHDUIndex = getConfig(
            commandLineArg.HDU_index, ['--HDU_index'], dicConfigFile,
            'input', 'HDU_index')
        strZeroLevelFrameFileHDUIndex = getConfig(
            commandLineArg.zero_level_frame_file_HDU_index,
            ['--zero_level_frame_file_HDU_index'], dicConfigFile,
            'input', 'zero_level_frame_file_HDU_index')
        strValidFrameShape = getConfig(
            commandLineArg.valid_frame_shape, ['--valid_frame_shape'],
            dicConfigFile, 'input', 'valid_frame_shape')
        strInvalidFrameShapeProcessMode = getConfig(
            commandLineArg.invalid_frame_shape_process_mode,
            ['--invalid_frame_shape_process_mode'], dicConfigFile, 'input',
            'invalid_frame_shape_process_mode')
        strMeanBGFrameFilePath = getConfig(
            commandLineArg.mean_BG_frame_file,
            ['-o', '--mean_BG_frame_file'], dicConfigFile, 'output',
            'mean_BG_frame_file_path')
        strStdBGFrameFilePath = getConfig(
            commandLineArg.std_BG_frame_file, ['--std_BG_frame_file'],
            dicConfigFile, 'output', 'std_BG_frame_file_path')
        strSkewnessBGFrameFilePath = getConfig(
            commandLineArg.skewness_BG_frame_file,
            ['--skewness_BG_frame_file'], dicConfigFile, 'output',
            'skewness_BG_frame_file_path')
        strKurtosisBGFrameFilePath = getConfig(
            commandLineArg.kurtosis_BG_frame_file,
            ['--kurtosis_BG_frame_file'], dicConfigFile, 'output',
            'kurtosis_BG_frame_file_path')
        strMinBGFrameFilePath = getConfig(
            commandLineArg.min_BG_frame_file, ['--min_BG_frame_file'],
            dicConfigFile, 'output', 'min_BG_frame_file_path')
        strMaxBGFrameFilePath = getConfig(
            commandLineArg.max_BG_frame_file, ['--max_BG_frame_file'],
            dicConfigFile, 'output', 'max_BG_frame_file_path')
        strCntBGFrameFilePath = getConfig(
            commandLineArg.cnt_BG_frame_file, ['--cnt_BG_frame_file'],
            dicConfigFile, 'output', 'cnt_BG_frame_file_path')
        strPHStatsFilePath = getConfig(
            commandLineArg.PH_stats_file, ['--PH_stats_file'],
            dicConfigFile, 'output', 'PH_stats_file_path')
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
        # self.strEventListFileAbsPath と self.eventListの設定
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
        # self.strMeanBGFrameFileAbsPathの設定
        self.strMeanBGFrameFileAbsPath = self.getStrAbsPath(
            strMeanBGFrameFilePath)
        # self.strStdBGFrameFileAbsPath の設定
        self.strStdBGFrameFileAbsPath = self.getStrAbsPath(
            strStdBGFrameFilePath)
        # self.strSkewnessBGFrameFileAbsPath の設定
        self.strSkewnessBGFrameFileAbsPath = self.getStrAbsPath(
            strSkewnessBGFrameFilePath)
        # self.strKurtosisBGFrameFileAbsPath の設定
        self.strKurtosisBGFrameFileAbsPath = self.getStrAbsPath(
            strKurtosisBGFrameFilePath)
        # self.strMinBGFrameFileAbsPath の設定
        self.strMinBGFrameFileAbsPath = self.getStrAbsPath(
            strMinBGFrameFilePath)
        # self.strMinBGFrameFileAbsPath の設定
        self.strMinBGFrameFileAbsPath = self.getStrAbsPath(
            strMinBGFrameFilePath)
        # self.strMaxBGFrameFileAbsPath の設定
        self.strMaxBGFrameFileAbsPath = self.getStrAbsPath(
            strMaxBGFrameFilePath)
        # self.strCntBGFrameFileAbsPath の設定
        self.strCntBGFrameFileAbsPath = self.getStrAbsPath(
            strCntBGFrameFilePath)
        # self.strPHStatsFileAbsPath の設定
        self.strPHStatsFileAbsPath = self.getStrAbsPath(
            strPHStatsFilePath)
    def getStrAbsPath(self, strPath):
        if strPath is None:
            return None
        else:
            return getStrAbsPath(strPath)


manager = Manager()
manager.main()
