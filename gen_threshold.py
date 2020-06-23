# coding:utf-8


import argparse

from scipy.stats import norm
from scipy.stats import t

from xaizalibs.standardlib import *
from xaizalibs.nplib import *
from xaizalibs.pltlib import *
from xaizalibs.CMOSanalyzerlib import *


class Manager():
    def __init__(self):
        self.config = Config()
        self.thresholdManager = ThresholdManager()
        self.dicThreshold = {}
        self.dicHeader = {
            'STD' : self.config.strStdBGFrameFileAbsPath,
            'KURTOSIS' : self.config.strKurtosisBGFrameFileAbsPath}
    def main(self):
        lsStrEvent_thModeColumn = self.config.strEvent_thMode.split('-')
        lsStrSplit_thModeColumn = self.config.strSplit_thMode.split('-')
        if 'frame' in [lsStrEvent_thModeColumn[0], lsStrSplit_thModeColumn[0]]:
            self.thresholdManager.loadPHStatsFile(
                self.config.strPHStatsFileAbsPath, message=True)
        if 'pixel' in [lsStrEvent_thModeColumn[0], lsStrSplit_thModeColumn[0]]:
            self.thresholdManager.loadStdBGFrameFile(
                self.config.strStdBGFrameFileAbsPath, message=True)
            if (
                    (
                        lsStrEvent_thModeColumn[0] == 'pixel'
                        and lsStrEvent_thModeColumn[1] == 't'
                    ) or (
                        lsStrSplit_thModeColumn[0] == 'pixel'
                        and lsStrSplit_thModeColumn[1] == 't')):
                self.thresholdManager.loadKurtosisBGFrameFile(
                    self.config.strKurtosisBGFrameFileAbsPath, message=True)
        self.dicHeader['FTYPE'] = 'event_th'
        self.dicHeader['PROBFUNC'] = lsStrEvent_thModeColumn[1]
        self.dicHeader['PROB'] = lsStrEvent_thModeColumn[2]
        self.setThreshold(
            self.config.strEvent_thMode, 'event_th',
            self.config.strEvent_thFrameFileAbsPath)
        self.dicHeader['FTYPE'] = 'split_th'
        self.dicHeader['PROBFUNC'] = lsStrSplit_thModeColumn[1]
        self.dicHeader['PROB'] = lsStrSplit_thModeColumn[2]
        self.setThreshold(
            self.config.strSplit_thMode, 'split_th',
            self.config.strSplit_thFrameFileAbsPath)
        self.saveThresholdFile()
    def setThreshold(
            self, strThresholdMode, strThresholdKey,
            strThresholdFrameFileAbsPath):
        lsStrThresholdModeColumn = strThresholdMode.split('-')
        if lsStrThresholdModeColumn[0] == 'frame':
            self.dicThreshold[strThresholdKey] = (
                self.thresholdManager.genThreshold(
                    strThresholdMode, tpFrameShape=self.config.tpFrameShape))
        elif lsStrThresholdModeColumn[0] == 'pixel':
            self.dicThreshold[strThresholdKey] = strThresholdFrameFileAbsPath
            mkdirs(
                genLsStrDirPathAndFileName(strThresholdFrameFileAbsPath)[0],
                message=True)
            saveAsFits(
                self.thresholdManager.genThreshold(
                    strThresholdMode,
                    tpFrameShape=self.config.tpFrameShape),
                strThresholdFrameFileAbsPath, message=True,
                header=self.dicHeader)
    def saveThresholdFile(self):
        if self.config.strThresholdFileAbsPath is None:
            return None
        self.dicThreshold['event_th_mode'] = self.config.strEvent_thMode
        self.dicThreshold['split_th_mode'] = self.config.strSplit_thMode
        self.dicThreshold['PH_stats_file'] = (
            self.config.strPHStatsFileAbsPath)
        self.dicThreshold['std_BG_frame_file'] = (
            self.config.strStdBGFrameFileAbsPath)
        self.dicThreshold['kurtosis_BG_frame_file'] = (
            self.config.strKurtosisBGFrameFileAbsPath)
        if self.config.tpFrameShape is not None:
            self.dicThreshold['frame_shape'] = (
                str(self.config.tpFrameShape[0])
                + 'x'
                + str(self.config.tpFrameShape[1]))
        else:
            self.dicThreshold['frame_shape'] = None
        mkdirs(
            genLsStrDirPathAndFileName(self.config.strThresholdFileAbsPath)[0],
            message=True)
        saveAsJSON(
            self.dicThreshold, self.config.strThresholdFileAbsPath,
            message=True, indent=2)


class Config():
    def __init__(self):
        self.strEvent_thMode = None
        self.strSplit_thMode = None
        self.strPHStatsFileAbsPath = None
        self.strStdBGFrameFileAbsPath = None
        self.strKurtosisBGFrameFileAbsPath = None
        self.tpFrameShape = None
        self.strThresholdFileAbsPath = None
        self.strEvent_thFrameFileAbsPath = None
        self.strSplit_thFrameFileAbsPath = None
        self.set()
    def genCommandLineArg(self):
        parser = argparse.ArgumentParser(
            description=(
                'generate threshold file (json).'))
        parser.add_argument(
            '-c', '--config_file', help='config file path (init : None)')
        parser.add_argument(
            '-i', '--PH_stats_file',
            help='input PH stats file (init : None)')
        parser.add_argument(
            '--std_BG_frame_file',
            help='std BG frame file (init : None)')
        parser.add_argument(
            '--kurtosis_BG_frame_file',
            help='kurtosis BG frame file (init : None)')
        parser.add_argument(
            '--event_th_mode', default='frame-norm-as10sigma',
            help='event_th mode (init : frame-norm-as10sigma)')
        parser.add_argument(
            '--split_th_mode', default='frame-norm-as3sigma',
            help='split_th mode (init : frame-norm-as3sigma)')
        parser.add_argument(
            '--frame_shape',
            help='frame shape (init : None)')
        parser.add_argument(
            '-o', '--threshold_file',
            help='mean BG file path(output) (init : None)')
        parser.add_argument(
            '--event_th_frame_file',
            help='event_th frame file path(output) (init : None)')
        parser.add_argument(
            '--split_th_frame_file',
            help='split_th frame file path(output) (init : None)')
        return parser.parse_args()
    def set(self):
        commandLineArg = self.genCommandLineArg()
        if commandLineArg.config_file is not None:
            dicConfigFile = getDicIni(
                getStrAbsPath(commandLineArg.config_file), message=True)
        else:
            dicConfigFile = None
        strPHStatsFilePath = getConfig(
            commandLineArg.PH_stats_file, ['-i','--PH_stats_file'],
            dicConfigFile, 'input', 'PH_stats_file_path')
        strStdBGFrameFilePath = getConfig(
            commandLineArg.std_BG_frame_file, ['--std_BG_frame_file'],
            dicConfigFile, 'input', 'std_BG_frame_file_path')
        strKurtosisBGFrameFilePath = getConfig(
            commandLineArg.kurtosis_BG_frame_file, ['--kurtosis_BG_frame_file'],
            dicConfigFile, 'input', 'kurtosis_BG_frame_file_path')
        strEvent_thMode = getConfig(
            commandLineArg.event_th_mode, ['--event_th_mode'],
            dicConfigFile, 'input', 'event_th_mode')
        strSplit_thMode = getConfig(
            commandLineArg.split_th_mode, ['--split_th_mode'],
            dicConfigFile, 'input', 'split_th_mode')
        strFrameShape = getConfig(
            commandLineArg.frame_shape, ['--frame_shape'],
            dicConfigFile, 'input', 'frame_shape')
        strThresholdFilePath = getConfig(
            commandLineArg.threshold_file, ['-o','--threshold_file'],
            dicConfigFile, 'output', 'threshold_file_path')
        strEvent_thFrameFilePath = getConfig(
            commandLineArg.event_th_frame_file, ['--event_th_frame_file'],
            dicConfigFile, 'output', 'event_th_frame_file_path')
        strSplit_thFrameFilePath = getConfig(
            commandLineArg.split_th_frame_file, ['--split_th_frame_file'],
            dicConfigFile, 'output', 'split_th_frame_file_path')
        self.strEvent_thMode = strEvent_thMode
        self.strSplit_thMode = strSplit_thMode
        self.strPHStatsFileAbsPath = self.getStrAbsPath(strPHStatsFilePath)
        self.strStdBGFrameFileAbsPath = self.getStrAbsPath(
            strStdBGFrameFilePath)
        self.strKurtosisBGFrameFileAbsPath = self.getStrAbsPath(
            strKurtosisBGFrameFilePath)
        if strFrameShape is not None:
            tpGroups = re.match('(\d+)x(\d+)', strFrameShape).groups()
            self.tpFrameShape = (int(tpGroups[0]), int(tpGroups[1]))
        else:
            self.tpFrameShape = None
        self.strThresholdFileAbsPath = self.getStrAbsPath(strThresholdFilePath)
        self.strEvent_thFrameFileAbsPath = self.getStrAbsPath(
            strEvent_thFrameFilePath)
        self.strSplit_thFrameFileAbsPath = self.getStrAbsPath(
            strSplit_thFrameFilePath)
    def getStrAbsPath(self, strPath):
        if strPath is None:
            return None
        else:
            return getStrAbsPath(strPath)


class ThresholdManager():
    def __init__(self):
        self.strPHStatsFilePath = None
        self.dicPHStats = None
        self.strStdBGFrameFilePath = None
        self.arrStdBGFrame = None
        self.strKurtosisBGFrameFilePath = None
        self.arrKurtosisBGFrame = None
    def loadPHStatsFile(self, strFilePath, message=False):
        self.strPHStatsFilePath = strFilePath
        self.dicPHStats = getDicJSON(self.strPHStatsFilePath, message=message)
    def loadStdBGFrameFile(self, strFilePath, message=False):
        self.strStdBGFrameFilePath = strFilePath
        self.arrStdBGFrame = getArrFits(
            self.strStdBGFrameFilePath, message=message)
    def loadKurtosisBGFrameFile(self, strFilePath, message=False):
        self.strKurtosisBGFrameFilePath = strFilePath
        self.arrKurtosisBGFrame = getArrFits(
            self.strKurtosisBGFrameFilePath, message=message)
    def genThreshold(self, strThresholdMode, tpFrameShape=None):
        lsStrThresholdModeColumn = strThresholdMode.split('-')
        sigmaMatch = re.match('as(\d*\.?\d*)sigma', lsStrThresholdModeColumn[2])
        fpeMatch = re.match('(\d*\.?\d*)fpe', lsStrThresholdModeColumn[2])
        if tpFrameShape is None:
            if self.arrStdBGFrame is not None:
                tpFrameShape = self.arrStdBGFrame.shape
            elif self.arrKurtosisBGFrame is not None:
                tpFrameShape = self.arrKurtosisBGFrame.shape
        if sigmaMatch is not None:
            prob = norm.sf(float(sigmaMatch.group(1)))
        elif fpeMatch is not None:
            prob = 1 / (np.prod(tpFrameShape) * float(fpeMatch.group(1)))
        if lsStrThresholdModeColumn[0] == 'frame':
            if lsStrThresholdModeColumn[1] == 'norm':
                return norm.isf(prob) * self.dicPHStats['std']
            elif lsStrThresholdModeColumn[1] == 't':
                validKurtosis = max(dicPHStats['kurtosis'], 0)
                if validKurtosis == 0:
                    return norm.isf(prob) * self.dicPHStats['std']
                else:
                    nu = 6 / validKurtosis + 4
                    scale = dicPHStats['std'] * sqrt((nu - 2) / nu)
                    return t.isf(prob, df=nu, scale=scale)
        if lsStrThresholdModeColumn[0] == 'pixel':
            if lsStrThresholdModeColumn[1] == 'norm':
                return norm.isf(prob) * self.arrStdBGFrame
            elif lsStrThresholdModeColumn[1] == 't':
                arrIsTargetKurtosisFrame = ~np.isnan(self.arrKurtosisBGFrame)
                arrIsTargetKurtosisFrame[arrIsTargetKurtosisFrame] *= (
                    self.arrKurtosisBGFrame[arrIsTargetKurtosisFrame] <= 0)
                arrRet = np.ones(tpFrameShape) * np.nan
                arrRet[arrIsTargetKurtosisFrame] = (
                    norm.isf(prob)
                    * self.arrStdBGFrame[arrIsTargetKurtosisFrame])
                arrIsTargetKurtosisFrame = ~np.isnan(self.arrKurtosisBGFrame)
                arrIsTargetKurtosisFrame[arrIsTargetKurtosisFrame] *= (
                    self.arrKurtosisBGFrame[arrIsTargetKurtosisFrame] > 0)
                arrValidNu = (
                    6 / self.arrKurtosisBGFrame[arrIsTargetKurtosisFrame] + 4)
                arrRet[arrIsTargetKurtosisFrame] = (
                    t.isf(prob, df=arrValidNu)
                    * self.arrStdBGFrame[arrIsTargetKurtosisFrame]
                    * np.sqrt((arrValidNu - 2) / arrValidNu))
                return arrRet


manager = Manager()
manager.main()
