import urllib.request
import copy

class LTInstance(object):

    STATUS_UPDT = 0     # 实例对比状态，需要更新实例信息
    STATUS_SAME = 1     # 实例相同，不需要更新实例信息
    STATUS_JOIN = 2     # 找不到与其对应的实例，将其加入instancePool

    HEADER_WINDOWS_CHROME = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Referer': ''}
    HEADER_ANDROID_CHROME = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.2.1; M040 Build/JOP40D) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36',
        'Referer': ''}
    HEADER_IOS_CHROME = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4',
        'Referer': ''}

    @staticmethod
    def getWebsiteInfo(url, headers=HEADER_WINDOWS_CHROME, requestMode='GET', encoding='utf-8'):
        try:
            req = urllib.request.Request(url, headers=headers, method=requestMode)
        except Exception as err:
            print(err)
            return None
        else:
            try:
                rst = urllib.request.urlopen(req)
            except Exception as err:
                print(err)
                return None
            else:
                return rst.read().decode(encoding)

    @staticmethod
    def getInstanceSet(websiteInfo):
        pass

    @staticmethod
    def compareInstance(ins_1, ins_2):
        # print('开始')
        # for cpnt in ins_1.compareGroup:
        #     print(cpnt)
        cpntNum = 0
        for cpnt in ins_1.compareGroup:
            # print(cpntNum)
            if cpnt != ins_2.compareGroup[cpntNum]:
                return LTInstance.STATUS_UPDT
            cpntNum += 1

        # print('结束')
        return LTInstance.STATUS_SAME

    def __init__(self):
        self.ID = 0               # 实例ID
        self.instanceName = ''    # 实例名
        self.compareGroup = []    # 实例对照组

    def setID(self, ID):
        self.ID = ID

    def setInstanceName(self, instanceName):
        self.instanceName = instanceName

    def setCompareGroup(self, compareGroup):
        self.compareGroup = compareGroup

    def appendCompareGroupCpnt(self, component):
        self.compareGroup.append(copy.deepcopy(component))





if __name__ == '__main__':
    # print(LTInstance.getWebsiteInfo('https://www.baidu.com'))
    a = LTInstance()
    a.setInstanceName('Nick')
    a.setCompareGroup(['123', '456'])
    b = LTInstance()
    b.setInstanceName('Nick')
    b.setCompareGroup(['d123', 'd456'])

    print(LTInstance.compareInstance(a, b))