from CrawlUtils import *
import math
from multiprocessing import Pool
from multiprocessing import cpu_count

def basicTest():
    PageSoup = getUrlSoup(PARSE_URL)
    tvShowList = getTvShowList(PageSoup)
    thShowdescList = getShowDescriptiveInfoList(tvShowList)

def feedTestList():
	return [{'name':'Test Name','url': '/wiki/$h*!_My_Dad_Says'},{'name':'Andys Gang','url':"/wiki/Andy%27s_Gang"}]

def feed_exception_list():
    return [{'name':'Test name','url':'/wiki/Heckle_and_Jeckle'},{'name':'Test name','url':'/wiki/The_Hudson_Brothers#Television_and_movies'},{'name':'Test name','url':'/wiki/Imogene_Coca'},{'name':'Test name','url':'/wiki/Jack_LaLanne#Books,_television_and_other_media'}]
#Tests
basicTest()
