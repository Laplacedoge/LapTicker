import LTInstance as LTI
import pathlib
import hashlib
import pickle
import datetime
import Anime
import time
import copy
import os

DIR_INSTANCE = pathlib.PurePath('./data/instance')
DIR_IMAGE = pathlib.PurePath('./data/image')
DIR_VIDEO = pathlib.PurePath('./data/video')
# DIR_TEST = pathlib.PurePath('./data/45654/4444')

FLG_HAV_INIT_INS = True

class LapTicker(object):
    topInstanceID = 0
    instanceExtensionName = 'pkl'

    @staticmethod
    def makeFileName(component: list, extension: str, separator: str = '-', havTimeStamp: bool = False):
        pass

    @staticmethod
    def makeFileNameUseMD5(component: list, extension: str, havTimeFactor: bool = False,
                           havTimeStamp: bool = False) -> str:
        '''
        使用MD5算法构造文件名
        :param component: list或是tuple，提供用来hash的字符串因子
        :param extension: 生成文件的扩展名
        :param havTimeFactor: 时间因素，为True则表明将当前的时间加入到用来hash的字符串因子中
        :param havTimeStamp: 时间戳，为True则表明将在文件名中加入时间戳
        :return: str
        '''
        nowTime = datetime.datetime.now()
        md5 = hashlib.md5()
        wholeStr = ''
        for singleStr in component:
            wholeStr += singleStr
        if havTimeFactor:
            wholeStr += nowTime.strftime('%Y%m%d%H%M%S')
        md5.update(wholeStr.encode('utf-8'))
        resultStr = md5.hexdigest().upper()
        if havTimeStamp:
            resultStr += nowTime.strftime('_%Y-%m-%d_%H-%M-%S')
        return resultStr + '.{}'.format(extension)

    def __init__(self):
        self.instancePool = []
        self.initStorageDir([DIR_IMAGE, DIR_VIDEO, DIR_INSTANCE], havNotice=True)
        if FLG_HAV_INIT_INS:
            self.initInstancePool(DIR_INSTANCE)

    def initStorageDir(self, dirSet: list, havNotice: bool=False):
        '''
        初始化存储区文件夹
        :param dirSet:
        :param havNotice: 是否提醒，为True则在每次检查文件夹存在与不存在随之创建时输出提醒信息
        :return: None
        '''
        for dir in dirSet:
            if not os.path.exists(dir):
                os.makedirs(dir)
                print('"[已创建 {}"]'.format(dir))
            else:
                print('"[已存在 {}"]'.format(dir))

    def initInstancePool(self, instanceDir):
        '''
        初始化实例池
        :param instanceDir: 实例存储路径
        :return: None
        '''
        for ins in os.listdir(instanceDir):
            if ins.endswith(LapTicker.instanceExtensionName):
                with open(pathlib.PurePath(instanceDir, ins), 'rb+') as file:
                    self.instancePool.append(pickle.load(file))
                LapTicker.topInstanceID += 1
                self.instancePool[-1].setID(LapTicker.topInstanceID)

    def backupInstancePool(self, instanceDir):
        '''
        备份实例池到实例文件夹
        :param instanceDir:
        :return:
        '''
        for ins in self.instancePool:
            with open(pathlib.PurePath(instanceDir, LapTicker.makeFileNameUseMD5([ins.instanceName], LapTicker.instanceExtensionName)), 'wb+') as file:
                pickle.dump(ins, file)

    def backupInstance(self, instanceDir, ins):
        '''
        备份实例池到实例文件夹
        :param instanceDir:
        :param ins:
        :return:
        '''
        with open(pathlib.PurePath(instanceDir, LapTicker.makeFileNameUseMD5([ins.instanceName], LapTicker.instanceExtensionName)), 'wb+') as file:
            pickle.dump(ins, file)

    def findInstance(self, instanceName):
        '''
        在self.instancePool中寻找instanceName并返回其在self.instancePool中的下标，没有找到则返回None
        :param instanceName: 待寻找的实例名
        :return: 下标或者None
        '''
        insNum = 0
        for subIns in self.instancePool:
            if subIns.instanceName == instanceName:
                return insNum
            else:
                insNum += 1
        return None

    def GO(self, sleepTime=30):
        while True:
            # websiteInfo = Anime.Anime.getWebsiteInfo(Anime.CRT_WEBSITE)
            with open(r'C:\Users\Administrator\Desktop\manhuadb_host.html', 'r+', encoding='utf-8') as file:
                websiteInfo = file.read()
            instanceSet = Anime.Anime.getInstanceSet(websiteInfo)

            updateInsSet = []

            for subIns in instanceSet:
                num = self.findInstance(subIns.instanceName)
                if num == None:
                    self.instancePool.append(copy.deepcopy(subIns))         # 新实例做深拷贝加入self.instancePool实例池
                    LapTicker.topInstanceID += 1                            # LapTicker的实例计数器+1
                    self.instancePool[-1].setID(LapTicker.topInstanceID)    # 给新实例设置新的ID
                    self.backupInstance(DIR_INSTANCE, self.instancePool[-1])# 备份新实例

                    updateInsSet.append(self.instancePool[-1])
                    # print('[有追加]')
                    # 没找到的情况
                else:
                    if LTI.LTInstance.compareInstance(subIns, self.instancePool[num]) == LTI.LTInstance.STATUS_UPDT:
                        self.instancePool[num] = copy.deepcopy(subIns)
                        self.instancePool[num].setID(num + 1)
                        self.backupInstance(DIR_INSTANCE, self.instancePool[num])

                        updateInsSet.append(self.instancePool[num])
                        # print('[有更新]')
                        # 有待更新的情况
                    else:
                        # print('[无更新]')
                        pass    # 完全一样的情况
            if len(updateInsSet) == 0:
                print('[无更新]')
            else:
                for subIns in updateInsSet:
                    print(subIns)
            time.sleep(sleepTime)



if __name__ == '__main__':
    lt = LapTicker()
    lt.GO()