from gnews import GNews
import json

def scrape_and_save_text(search_query, n):
	google_news = GNews(language='en', country='US', max_results=n)
	news = google_news.get_news(query)
	with open("dump.temp", 'w', encoding='utf-8') as json_file:
		json.dump(news, json_file, ensure_ascii=False, indent=4)