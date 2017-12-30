import requests
from bs4 import BeautifulSoup
import csv
from urlparse import urljoin

def main():
	''' begins calling scraper with the given url'''
	url = "http://quotes.toscrape.com"
	nexturl = "http://quotes.toscrape.com"
	flag = True
	while flag:
		response = requests.get(nexturl)
		html = response.text.encode("utf-8").decode("ascii", "ignore") # changing encoding to avoid unicode charachters
		soup = BeautifulSoup(html, "html.parser")
		data, nexturl, flag = process_data(soup) # calling process data function

		with open("quotes.csv", "a") as file: # opening csv file in append mode
			writer = csv.writer(file, quoting=csv.QUOTE_ALL)
			for singlequote in data:
				writer.writerow(singlequote)

		if flag:
			nexturl = urljoin(url, nexturl) # changing nexturl


def process_data(soup):
	'''extracting data from given soup'''
	data = []
	quotes = soup.find_all("div", attrs={"class": "quote"}) # find all quotes
	for quote in quotes:
		quote_data = []
		quote_data.append(quote.find("span", attrs={"class":"text"}).text) # extract quote text
		quote_data.append(quote.find("small", attrs={"class":"author"}).text) # extract author
		tags = quote.find_all("a", attrs={"class": "tag"}) # extract all tags
		print tags
		for tag in tags:
			quote_data.append(tag.text) # store each tag text
		data.append(quote_data)

	nextpage = soup.find("li", attrs={"class":"next"}) # check if next page link exists
	if nextpage: # return values according to nextpage value
		nexturl = nextpage.find("a")["href"]
		return data, nexturl, True
	else:
		return data, None, False
	

if __name__=="__main__":
	main()