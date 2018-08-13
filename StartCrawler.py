from CrawlUtils import *

PageSoup = getUrlSoup(PARSE_URL)
tvShowList = getTvShowList(PageSoup)
displayDictList(tvShowList)