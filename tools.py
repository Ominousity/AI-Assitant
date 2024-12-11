from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def handle_cookies(driver: webdriver.Chrome):
    try:
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "L2AGLb"))
        )
        cookie_button.click()
    except:
        print("No cookie consent prompt found or handled.")


def get_weather_data(today: bool, days: int, city: str = "Esbjerg") -> list:
    if days > 7:
        return "No more than 7 days of forecast is allowed."

    driver = webdriver.Chrome()

    driver.get(f"https://www.google.com/search?q=weather+{city}")

    handle_cookies(driver)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'UQt4rd'))
    )

    if today and days == 1:
        current_temp = driver.find_element(By.ID, 'wob_tm').text
        current_weather = driver.find_element(By.ID, 'wob_dc').text
        humidity = driver.find_element(By.ID, 'wob_hm').text
        downfall = driver.find_element(By.ID, 'wob_pp').text
        wind = driver.find_element(By.ID, 'wob_ws').text
        

        driver.quit()
        return f"Temperature: {current_temp}, Weather: {current_weather}°, Humidity: {humidity}, Wind: {wind} Downfall: {downfall}"
    else:
        forecast = []
        for i in range(days):
            day_div = driver.find_element(By.CSS_SELECTOR, f'div[data-wob-di="{i+1}"]')
            day_div.click()

            day = driver.find_element(By.CLASS_NAME, 'wob_dts').text.split(" ")[0]
            current_temp = driver.find_element(By.ID, 'wob_tm').text
            current_weather = driver.find_element(By.ID, 'wob_dc').text
            humidity = driver.find_element(By.ID, 'wob_hm').text
            downfall = driver.find_element(By.ID, 'wob_pp').text
            wind = driver.find_element(By.ID, 'wob_ws').text

            forecast.append(f"Day: {day}, Temperature: {current_temp}°, Weather: {current_weather}, Humidity: {humidity}, Wind: {wind} Downfall: {downfall}")
        
        print(forecast)
        return forecast
