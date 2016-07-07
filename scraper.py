from bs4 import BeautifulSoup
import urllib
import requests

def get_image_url(keyword):
	common_url = "https://en.wikipedia.org/w/api.php?action=query&titles={}&prop=images&format=json"
	r = requests.get(common_url.format(keyword))
	wiki = r.json()
	images = wiki["query"]["pages"].values()[0]["images"]
	urls = list()
	for image in images:
		title = image["title"]
		wiki_url = "https://commons.wikimedia.org/wiki/{}"
		r = urllib.urlopen(wiki_url.format(title)).read()
		soup = BeautifulSoup(r, "html.parser")
		try:
			full_image_div = soup.find_all("div", class_="fullImageLink")[0]
			url = full_image_div.a["href"]
			if url.split(".")[-1] in ["jpeg", "jpg", "png"]:
				return url
		except IndexError:
			pass
	raise Exception("No image found")

if __name__ == "__main__":
	print get_image_url("Barack Obama")
