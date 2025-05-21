import asyncio
import csv
from playwright.async_api import async_playwright
from modules.crawler_clean import clean_text
import re


IS_DETAIL_MODE = True  

async def crawl_tweets(search_keyword, limit, output_path, auth_token):
    SEARCH_TAB = "live"
    TWITTER_SEARCH_URL = f"https://x.com/search?q={search_keyword} lang:id&src=typed_query&f={SEARCH_TAB}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await context.add_cookies([{
            "name": "auth_token",
            "value": auth_token,
            "domain": ".x.com",
            "path": "/",
            "secure": True,
            "httpOnly": True,
            "sameSite": "None",
        }])

        await page.goto(TWITTER_SEARCH_URL)
        try:
            await page.wait_for_selector("article", timeout=5000)
        except Exception:
            print("⚠️ Gagal memuat tweet. Mungkin token tidak valid.")
            await browser.close()
            return False

        tweets_data = []
        tweet_ids = set()
        scroll_attempt = 0
        MAX_SCROLL = 100
        
        while len(tweets_data) < MAX_SCROLL and scroll_attempt < 20:
            tweets = await page.query_selector_all("article")
            for tweet in tweets:
                try:

                    link_elem = await tweet.query_selector("a[href*='/status/']")
                    if not link_elem:
                        continue
                    tweet_url = await link_elem.get_attribute("href")
                    tweet_id = tweet_url.split("/")[-1]
                    if tweet_id in tweet_ids:
                        continue
                    tweet_ids.add(tweet_id)

                    time_elem = await tweet.query_selector("time")
                    timestamp = await time_elem.get_attribute("datetime") if time_elem else None

                    user_elem = await tweet.query_selector("div[dir='ltr'] span")
                    username = await user_elem.inner_text() if user_elem else "unknown"

                    content_elem = await tweet.query_selector("div[data-testid='tweetText']")
                    content = await content_elem.inner_text() if content_elem else ""

                    image_elem = await tweet.query_selector("img[src*='twimg']")
                    image_url = await image_elem.get_attribute("src") if image_elem else ""

                    reply_to_username = ""
                    is_reply = False
                    reply_to_element = await tweet.query_selector("a[href*='/status/'][aria-label*='Membalas']")
                    if reply_to_element:
                        is_reply = True
                        reply_text = await reply_to_element.get_attribute("aria-label")
                        
                        if reply_text and "@" in reply_text:
                            reply_to_username = reply_text.split("@")[1]
                            
                            reply_to_username = re.sub(r'[^a-zA-Z0-9_]', '', reply_to_username)

                    cleaned_text = clean_text(content, is_reply, reply_to_username if IS_DETAIL_MODE else None)

                    tweets_data.append({
                        "conversation_id_str": tweet_id,
                        "created_at": timestamp,
                        "favorite_count": 0,
                        "full_text": cleaned_text,
                        "id_str": tweet_id,
                        "image_url": image_url,
                        "in_reply_to_screen_name": reply_to_username,
                        "lang": "und",
                        "location": "",
                        "quote_count": 0,
                        "reply_count": 0,
                        "retweet_count": 0,
                        "tweet_url": "https://x.com" + tweet_url,
                        "user_id_str": "",
                        "username": username
                    })


                    if len(tweets_data) >= limit:
                        break
                except Exception:
                    continue

            await page.mouse.wheel(0, 1500)
            await asyncio.sleep(0.1)
            scroll_attempt += 1

        await browser.close()

        if not tweets_data:
            return False

        with open(output_path, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = list(tweets_data[0].keys())
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(tweets_data)

        return True
