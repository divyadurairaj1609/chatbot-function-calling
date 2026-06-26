import requests
import xml.etree.ElementTree as ET

def get_latest_news(topic="general"):
    """Get latest news headlines without any API key"""
    try:
        topic_lower = topic.lower()

        # Choose the right RSS feed based on topic
        if any(word in topic_lower for word in ["tech", "ai", "technology", "software", "computer"]):
            # HackerNews for tech news
            url = "https://hnrss.org/frontpage"
            source = "Hacker News"
        elif any(word in topic_lower for word in ["sport", "cricket", "football", "soccer"]):
            url = "http://feeds.bbci.co.uk/sport/rss.xml"
            source = "BBC Sport"
        elif any(word in topic_lower for word in ["business", "economy", "finance", "market"]):
            url = "http://feeds.bbci.co.uk/news/business/rss.xml"
            source = "BBC Business"
        elif any(word in topic_lower for word in ["science", "space", "health"]):
            url = "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml"
            source = "BBC Science"
        else:
            # General world news
            url = "http://feeds.bbci.co.uk/news/world/rss.xml"
            source = "BBC World News"

        response = requests.get(url, timeout=10)
        root = ET.fromstring(response.content)

        # Parse RSS feed
        headlines = []
        for item in root.findall(".//item")[:5]:
            title = item.find("title")
            description = item.find("description")
            pub_date = item.find("pubDate")

            if title is not None:
                headlines.append({
                    "title": title.text,
                    "description": description.text if description is not None else "",
                    "date": pub_date.text if pub_date is not None else ""
                })

        if not headlines:
            return f"No news found for topic '{topic}'"

        result = f"\nLatest News from {source}:\n"
        result += f"Topic: {topic.title()}\n"
        result += "-" * 40 + "\n"

        for i, news in enumerate(headlines, 1):
            result += f"\n{i}. {news['title']}\n"
            if news['description']:
                # Clean description — remove HTML tags
                desc = news['description']
                desc = desc.replace('<p>', '').replace('</p>', '')
                desc = desc.replace('<b>', '').replace('</b>', '')
                if len(desc) > 150:
                    desc = desc[:150] + "..."
                result += f"   {desc}\n"

        return result

    except Exception as e:
        return f"Could not fetch news. Please try again."