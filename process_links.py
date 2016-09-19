
def process(url):
	return True

links = ["alpha", "#kappa", "beta", "gamma"]
index = 0

for link in links:
	print("processing %s" % (link))
	
	if link.startswith('#'):
		index += 1
		continue;
		
	if process(link):
		links[index] ="## " + links[index]
	
	index += 1

print(links)	
