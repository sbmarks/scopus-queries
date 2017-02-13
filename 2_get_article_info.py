import requests
import json
import csv

apikey = <INSERT YOUR OWN API KEY HERE>


## read in the list of Scopus IDs from scopusids.csv
with open('scopusids.csv') as f:
    reader = csv.reader(f)
    rawlist = list(reader)
    scopusIDList = rawlist[0]

##open output file for writing
outputFile = open('articlerecords.csv', 'w')
wr = csv.writer(outputFile, quoting=csv.QUOTE_ALL)


## get scopus records
for scopusID in scopusIDList:
    url = ("http://api.elsevier.com/content/abstract/scopus_id/"
          + scopusID
          + "?view=FULL")
    resp = requests.get(url,
                    headers={'Accept':'application/json',
                             'X-ELS-APIKey': apikey})
    results = json.loads(resp.text)
    ## empty set to collate records with UofT Corresponding Author
    allResults = []
    
    ## check to see if the primary author's address is in Toronto
    try:
        corr_string = str(results['abstracts-retrieval-response']['item']['bibrecord']['head']['correspondence']['affiliation']['organization'])
    except:
        corr_string = "ERROR"
    ## I left this in because I found it useful to see the institutional affiliations scroll by.
	print(corr_string)
	## Use clever string matching to check institutional affiliation
	## You must figure out your own way here
    if "Toronto" in corr_string:
        print("YEP")
        allResults.append(corr_string)
        try:
            allResults.append(str(results['abstracts-retrieval-response']['item']['bibrecord']['head']['correspondence']['person']['ce:indexed-name']))
        except:
            allResults.append("ERROR")
		try:
            allResults.append(str(results['abstracts-retrieval-response']['item']['bibrecord']['head']['correspondence']['ce:e-address']))
        except:
            allResults.append("ERROR")
        try:
            allResults.append(str(results['abstracts-retrieval-response']['coredata']['prism:issn']))
        except:
            allResults.append("ERROR")
        try:
            allResults.append(str(results['abstracts-retrieval-response']['item']['bibrecord']['head']['source']['sourcetitle']))
        except:
            allResults.append("ERROR")
        try:
            allResults.append(str(results['abstracts-retrieval-response']['item']['bibrecord']['head']['source']['publicationdate']['year']))
        except:
            allResults.append("ERROR")
        wr.writerow(allResults)
        
    else:
        print("NOPE")

outputFile.close()
print("OK DONE")