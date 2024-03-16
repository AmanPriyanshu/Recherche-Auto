from gnews import GNews
import requests
from urllib.parse import quote
import json

def scrape_and_save_text(search_query, n):
	print({"query": search_query, "n": n})
	google_news = GNews(language='en', country='US', max_results=n)
	news = google_news.get_news(search_query)
	if news is not None:
		return news
	else:
		return "We'll modify the search query. There were no responses, it may be due to using key phrases like \"latest news\" or \"current news\". Also, the topic might be too specialized, please make it broader."

if __name__ == '__main__':
	scrape_and_save_text("Differential Privacy", 5)