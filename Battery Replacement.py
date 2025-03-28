from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os

def scrape_battery_replacement(url):
    driver = webdriver.Chrome()
    data = []  # List to store battery info

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'devices_table')))

        # Find the table and extract all rows
        table = driver.find_element(By.ID, 'devices_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')  # Get all table rows

        imei_urls = []

        for row in rows:
            try:
                first_link = row.find_element(By.TAG_NAME, 'a')  # Get only the first link in the row
                imei_urls.append(first_link.get_attribute('href'))
            except:
                continue  # Skip rows without a link

        for imei_url in imei_urls:
            driver.get(imei_url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))

            # ✅ Find table headers to locate the **correct** column index of "Battery (V)"
            headers = driver.find_elements(By.XPATH, '//table/thead/tr/th')
            battery_col_index = -1

            for index, header in enumerate(headers):
                if "Battery" in header.text:  # Matches "Battery (V)" or similar variations
                    battery_col_index = index
                    print(f"✅ Found 'Battery (V)' column at index: {battery_col_index}")
                    break

            if battery_col_index == -1:
                print(f"⚠️ Battery column not found for {imei_url}")
                driver.back()
                continue

            # ✅ Extract battery info from the correct column
            rows = driver.find_elements(By.XPATH, '//table/tbody/tr')
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, 'td')
                if len(cols) > battery_col_index:
                    battery_info = cols[battery_col_index].text
                    imei_number = imei_url.split('=')[-1]  # Extract IMEI from URL
                    data.append([imei_number, battery_info])
                    print(f"✅ IMEI: {imei_number}, Battery Info: {battery_info}")

            driver.back()

        # ✅ Debug: Check if data is collected before saving
        if not data:
            print("⚠️ No battery data found. Excel file will not be created.")
        else:
            # Define the file path explicitly
            save_path = os.path.abspath("battery_info.xlsx")

            # Convert to DataFrame and save
            df = pd.DataFrame(data, columns=["IMEI", "Battery Info"])
            
            print(f"📂 Attempting to save file at: {save_path}")  # Debug print

            try:
                df.to_excel(save_path, index=False, engine='openpyxl')
                print(f"✅ Excel file saved successfully at: {save_path}")
            except Exception as e:
                print(f"❌ Failed to save Excel file: {e}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

    finally:
        driver.quit()

# Example usage
scrape_battery_replacement('https://command.test.farmo.com.au:44444')
