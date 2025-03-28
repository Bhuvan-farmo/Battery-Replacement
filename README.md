# Battery Replacement Data Scraper

## Overview
This Python script uses **Selenium** to scrape battery replacement data for each device from the Command Centre web interface. The script:
- Extracts IMEI numbers from the main device table.
- Opens the corresponding device details page.
- Identifies and extracts battery voltage information.
- Saves the collected data into an **Excel file (battery_info.xlsx)**.

## Requirements
### Install Dependencies
Ensure you have the necessary Python libraries installed:
```bash
pip install selenium pandas openpyxl
```

### WebDriver Setup
You need to have **Google Chrome** installed along with the **Chrome WebDriver**. 
- Download the correct version from: [ChromeDriver](https://sites.google.com/chromium.org/driver/)
- Place the driver in a known directory and update your system PATH if necessary.

## How to Run
Run the script using Python:
```bash
python script.py
```
It will navigate through the website, extract data, and attempt to save the results in **battery_info.xlsx**.

## Issues & Debugging
### ✅ Device Links Are Opening Correctly
The script successfully finds the IMEI numbers and navigates to the correct device pages.

### ❌ Battery Column Data Not Being Picked Up
- The script searches for the **"Battery (V)"** column dynamically but might fail if the column header format differs.
- **Troubleshooting:**
  - Check if the table structure has multiple `<th>` headers.
  - Print the detected headers using:
    ```python
    for i, header in enumerate(headers):
        print(f"Column {i}: {header.text}")
    ```
  - Update the script to match the exact column name.

### ❌ Unable to Save Data to Excel
- The script prints the collected battery data but does not create an Excel file.
- **Possible causes:**
  - **pandas or openpyxl not installed** → Run `pip install pandas openpyxl`
  - **No write permission** → Try saving the file in a different directory:
    ```python
    save_path = os.path.join(os.path.expanduser("~"), "Desktop", "battery_info.xlsx")
    ```
  - **Data is empty** → Ensure data is being collected before writing to Excel.

## Next Steps
- Fix column detection logic for "Battery (V)".
- Improve error handling and logging.
- Ensure file is written successfully and verify the saved content.

---
If you encounter additional issues, print debug logs and check the website structure for changes. Happy coding! 🚀

