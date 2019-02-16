import re
import html.parser
from urllib.request import Request, urlopen

try:
	from bs4 import BeautifulSoup
except:
	from BeautifulSoup import BeautifulSoup


# Read problem number
with open('input.txt', 'r') as f:
	problem_number = f.readline().strip()
	
# BOJ problem address
address = 'http://icpc.me/' + problem_number

# Read BOJ problem page
req = Request(address, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

# Instantiate BeautifulSoup
soup = BeautifulSoup(webpage, "html.parser")

# Read sample inputs and outputs
inputs = soup.find_all('pre', id=re.compile('sample-input-\d'))
outputs = soup.find_all('pre', id=re.compile('sample-output-\d'))

inputs = [data.get_text() for data in inputs]
outputs = [data.get_text() for data in outputs]

# Write sample.txt and input.txt
with open('sample.txt', 'w') as sample, open('input.txt', 'w') as input_txt:
	# Write first sample input to input.txt
	input_txt.write(inputs[0])
	
	# Write title
	sample.write("SAMPLE INPUT AND OUTPUTS\n\n" + address + '\n\n')

	# Find longest line length
	M = max(len(line) for datum in inputs+outputs for line in datum.split('\n'))

	# Wrie sample inputs and outputs
	input_pretty = "="*((M-1)//2)
	input_pretty = input_pretty + "<{}>" + input_pretty

	for i in range(len(inputs)):
		sample.write(input_pretty.format(i+1)+'\n'+inputs[i])
		if inputs[-1]!='\n':
			sample.write('\n')
		sample.write("-"*len(input_pretty.format(i+1))+'\n'+outputs[i]+'\n')