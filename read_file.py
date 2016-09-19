
links = ["alpha", "#kappa", "beta", "gamma"]
index = 0
for link in links:
	print("processing %s",  link)
	
	if link.startswith('#'):
		index += 1
		continue;
		
	#process(link)
	processed = True
	if processed :
		links[index] ="## " + links[index]
	
	index += 1

print(links)

	
