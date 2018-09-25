from CrawlUtils import *
import math
from multiprocessing import Pool
from multiprocessing import cpu_count

def basicTest():
    PageSoup = getUrlSoup(PARSE_URL)
    tvShowList = getTvShowList(PageSoup)
    thShowList = getShowDescriptiveInfoList(feedTestList())

def feedTestList():
	return [{'name':'Test Name','url': '/wiki/$h*!_My_Dad_Says'},{'name':'Andys Gang','url':"/wiki/Andy%27s_Gang"}]

#Tests
basicTest()
