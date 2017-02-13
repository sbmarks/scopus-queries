import requests
import json
import csv

apikey = <INSERT YOUR OWN API KEY HERE>
instid = <INSERT YOUR OWN INSTITUTIONAL ID HERE>


## List of years to fetch
yearList = ["2009", "2010", "2011", "2012", "2013", "2014", "2015"]

## define a function to parse one page of records
def parse_records (recordSet):
    ## print the SCOPUS IDs
    for r in range(len(recordSet['search-results']['entry'])):
        print(str(recordSet['search-results']['entry'][r]['dc:identifier']))
        allResults.append(str(recordSet['search-results']['entry'][r]['dc:identifier']))
    return;

## define a function to do the Scopus record retrieval
def get_scopus_list (ISSN, year):
    print("Get ISSN " + ISSN + " for year " + year)
    searchURL = str("http://api.elsevier.com/content/search/scopus?query=ISSN(" +
                       ISSN +
                       ")+AND+DOCTYPE(ar)+AND+PUBYEAR+IS+" +
                       year +
                       "+AND+AF-ID(" +
                       instid +
                       ")")
    print(searchURL)
    resp = requests.get(searchURL, headers={'Accept':'application/json','X-ELS-APIKey': apikey})
    results = resp.json()
    ## an error will exist if it's an empty set, handle this
    if 'error' in results['search-results']['entry'][0]:
        print("ERROR! " + str(results['search-results']['entry'][0]['error']))
    else:
        ## write the results
        parse_records(results)
        
        #### do this!
        ## test if there is a next, only do the loop if so
        ##### do this!
        
        done = 0
        ## as long as we know we're not done
        while done == 0:
            ## check all [search-result][link] for @ref next which means there's more records
            for s in range(len(results['search-results']['link'])):
                ## if there is a next record
                if 'next' in results['search-results']['link'][s]['@ref']:
                    print("Lots! Link to next is " + str(results['search-results']['link'][s]['@href']))
                    nextURL = str(results['search-results']['link'][s]['@href'])
                    resp = requests.get(nextURL, headers={'Accept':'application/json','X-ELS-APIKey': apikey})
                    results = resp.json()
                    parse_records(results)
                ## if there's not, peace out    
                else:
                    parse_records(results) 
                    ## this will create duplicates but it doesn't matter because we're deduping anyway
                    done = 1
                
    return;




## create list to hold all results
allResults = []

## for each ISSN
for ISSN in ISSNList:   
## for each year 2009-2014
    for year in yearList:
        get_scopus_list(ISSN, year)

## convert to a set to de-duplicate Scopus IDs
allResults = list(set(allResults))
print(allResults)

outputFile = open('scopusids.csv', 'w')
wr = csv.writer(outputFile, quoting=csv.QUOTE_ALL)
wr.writerow(allResults)
outputFile.close()
