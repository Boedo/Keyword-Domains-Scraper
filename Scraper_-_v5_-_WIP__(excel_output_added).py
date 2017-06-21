from BeautifulSoup import BeautifulSoup
import urllib2
import time
import xlwt

############################
# Creating an output file
############################
my_xls = xlwt.Workbook(encoding='ascii') # Creating a workbook
my_sheet1 = my_xls.add_sheet("Keywords DB") # Adding sheet to store urls per keyword
xls_saved = 'Keywords_to_DB.xls'

####
line_sheet1 = 0
col_sheet1 = 0

############################
# Formatting the query, querying, fetching the results
############################
def query(keyword, results):

    line_sheet1 = 1

    site= "http://www.google.co.uk/search?q=" + keyword + results # creates the search url
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'} # replicates a real User-Agent

    req = urllib2.Request(site, headers=hdr) # performs the search with added User-Agent

    try:
        page = urllib2.urlopen(req).read() # reads html source of the landing page
        soup = BeautifulSoup(page) # passes code source to BeautifulSoup
        target = soup.findAll('cite') # find all element in cite tags [,attrs={'class':'_Rm'}]
        for element in target: # for each value wrapped in cite tags
            # print element.text # print its content
            link = element.text
            my_sheet1.write(line_sheet1, col_sheet1, link)

            line_sheet1 += 1

    except urllib2.HTTPError, e:
        print e.fp.read()

    time.sleep(8) # Pauses after fetching results for the target keyword

#############################
# Defining what to search for
#############################

search = ["google","bing","facebook","elvis"] # List of keywords

numbers_urls = 100 # Number of results looked for
numbers = "&num=%s" % (numbers_urls) # Parameter appended to the query

for index, value in enumerate(search):
    searched = search[index]  # index of keyword searched for
    final_search = searched.replace(" ", "+") # formats keyword for google url

    print ' '
    print ' '
    print '#########################'
    print 'Now fetching the first ' + str(numbers_urls) + ' urls for target keyword: ' + searched
    print 'Keywords left to process: ' + str(len(search) - index)
    print '#########################'
    print ' '
    print ' '

    time.sleep(2.5)
    my_sheet1.write(line_sheet1, col_sheet1, searched)
    query(final_search, numbers) # passes keyword to the function

    col_sheet1 += 1

my_xls.save(xls_saved)
