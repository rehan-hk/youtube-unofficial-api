from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


class WebDriverManager:
    CHROME_DRIVER_PATH = "chromedriver-win64/chromedriver.exe"
    my_date_format = "%b %d, %Y"

    def __init__(self):
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(service=Service(WebDriverManager.CHROME_DRIVER_PATH), options=chrome_options)

    def get_video_info(self, channel_name, n_videos):
        try:
            url_to_channel = f"https://www.youtube.com/{channel_name}/videos"
            self.driver.get(url_to_channel)

            # Scroll to load videos
            scroll_position = 0
            scroll_increment = 2000
            num_scrolls = (n_videos - 1) // 20 + 1
            for _ in range(num_scrolls):
                scroll_position += scroll_increment
                self.driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "ytd-grid-video-renderer")))

            # Extract video links
            video_links = [a.get_attribute('href') for a in self.driver.find_elements(By.CSS_SELECTOR, "a#video-title")]

            # Scrape video information
            scraped_video_info = []
            for video_url in video_links[:n_videos]:
                self.driver.get(video_url)
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "ytd-video-owner-renderer")))
                uploaded_date_element = self.driver.find_element(By.CSS_SELECTOR, "ytd-video-owner-renderer #date")
                uploaded_date_text = uploaded_date_element.get_attribute("innerText")
                try:
                    parsed_date_stamp = datetime.strptime(uploaded_date_text, WebDriverManager.my_date_format)
                except ValueError:
                    parsed_date_stamp = 'live or not available'
                scraped_video_info.append({
                    "url": video_url,
                    "uploaded_date": parsed_date_stamp.strftime(WebDriverManager.my_date_format)
                })

            return scraped_video_info

        except Exception as e:
            raise e

        finally:
            self.driver.quit()
