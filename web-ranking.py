# define a procedure get_page
# takes as input the url to a web page
# outputs the contents of that web page
def get_page(url):
    try:
    	import urllib
    	return urllib.urlopen(url).read()
    except:
    	return ""



# define a procedure get_next_target 
# takes as input HTML of a page, and outputs
# the url found, and position of the end quote
def get_next_target(page):
	start_link = page.find('<a href=')
	if start_link == -1:
		return None, 0
	start_quote = page.find('"', start_link)
	end_quote = page.find('"', start_quote + 1)
	url = page[start_quote + 1 : end_quote]
	return url, end_quote


# define a procedure get_all_links 
# takes as input HTML of a page, and outputs
# all links appeared on the page
def get_all_links(page):
	links = []
	while True:
		url, endpos = get_next_target(page)
		if url:
			links.append(url)
			page = page[endpos:]
		else:
			break
	return links

# define a procedure union
# takes as input 2 arrays p, q
# add all elements that are in p
# and not in q to q
def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)


# Modify the crawl_web procedure so that instead of just returning the 
# index, it returns an index and a graph. The graph should be a 
# Dictionary where the key:value entries are:
#  url: [list of pages url links to] 
def crawl_web(seed): # returns index, graph of outlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>:[list of pages it links to]
    index = {} 
    while tocrawl: 
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph


# Define a procedure, add_to_index,
# that takes 3 inputs:
# - an index: [[<keyword>,[<url>,...]],...]
# - a keyword: String
# - a url: String
# If the keyword is already
# in the index, add the url
# to the list of urls associated
# with that keyword.
# If the keyword is not in the index,
# add an entry to the index: [keyword,[url]]
def add_to_index(index, keyword, url):
    if keyword in index:
    	index[keyword].append(url)
   	else:
		index[keyword] = [url] #not found, add a new entry

# define a procedure, lookup,
# takes in an index and a key word
# outputs a list containing
# urls where the word appears
def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    return None

# Define a procedure, add_page_to_index,
# that takes three inputs:
#   - index
#   - url (String)
#   - content (String)
# It should update the index to include
# all of the word occurences found in the
# page content by adding the url to the
# word's associated url list.
def add_page_to_index(index,url,content):
    word_list = content.split()
    for word in word_list:
        add_to_index(index, word, url)


# Define a function, hash_string,
# that takes as inputs a keyword
# (string) and a number of buckets,
# and returns a number representing
# the bucket for that keyword.
# def hash_string(keyword,buckets):
#    sum_ord = 0
#    for char in keyword:
#        sum_ord += ord(char)
#    return sum_ord % buckets

# def make_hashtable(nbuckets):
#	table = []
#	for i in (0, nbuckets):
#		table.append([])
#	return table



# define a procedure, compute_ranks,
# that takes a graph, where links are represented as nodes
# outputs the ranks (represented by numbers) of the links 
# large numbers mean high ranks
def compute_ranks(graph):
    d = 0.8 # damping factor (how likely the user clicks on a link on the page, instead of going to
    		# a totally different page)
    numloops = 10 # number of times of refining page ranks
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrankonepage = (1 - d) / npages
            for node in graph:
            	if page in graph[node]:
            		newrankonepage = newrankonepage + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrankonepage
        ranks = newranks
    return ranks


#Define a procedure, lucky_search, that takes as input an index, a ranks
#dictionary (the result of compute_ranks), and a keyword, and returns the one
#URL most likely to be the best site for that keyword. If the keyword does not
#appear in the index, lucky_search should return None.
def lucky_search(index, ranks, keyword):
	pages = lookup(index, keyword)
	if not pages:
		return None
	else:
		best_page = pages[0]
		for candidate in pages:
			if ranks[candidate] > ranks[best_page]:
				best_page = candidate
		return best_page
