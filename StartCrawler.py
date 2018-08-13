from CrawlUtils import *

def basicTest():
    PageSoup = getUrlSoup(PARSE_URL)
    tvShowList = getTvShowList(PageSoup)
    displayDictList(tvShowList)

#Test
basicTest()