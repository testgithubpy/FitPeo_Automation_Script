from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set the path to the chromedriver executable
service = Service('c:/chromedriver/chromedriver.exe')

# Initialize the Chrome driver
driver = webdriver.Chrome(service=service)

# Maximize the browser window
driver.maximize_window()

wait = WebDriverWait(driver, 20)
actions = ActionChains(driver)

# Step 1: Navigate to the FitPeo Homepage
driver.get("https://www.fitpeo.com")
print("Navigated to FitPeo Homepage")

# Step 2: Navigate to the Revenue Calculator Page
revenue_calculator_link = wait.until(
    EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Revenue Calculator')]")))
print("Revenue Calculator link found")
driver.execute_script("arguments[0].click();", revenue_calculator_link)
print("Clicked Revenue Calculator link")

# Step 3: Adjust the Slider to 830
time.sleep(2)  # Wait for the page to load fully
try:
    slider_thumb = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "MuiSlider-thumb")))
    slider_input = driver.find_element(By.XPATH, "//span[@data-index='0']/input[@type='range']")

    # Move the slider thumb by an offset to reach 830
    actions.click_and_hold(slider_thumb).move_by_offset(100, 0).release().perform()  # Adjust offset as needed
    time.sleep(2)  # Wait for the slider to adjust

    # Capture the slider value
    slider_value = int(slider_input.get_dom_attribute("value"))
    print(f"Slider value captured: {slider_value}")

    # Step 4: Now scroll down to CPT Codes section
    driver.execute_script("window.scrollBy(0, 1000);")  # Scroll value slightly adjusted
    time.sleep(2)  # Additional wait for scrolling to complete
    print("Scrolled to CPT Codes section using JavaScript")

    # Step 5: Scroll up and then click CPT-99091, CPT-99453, CPT-99454, and CPT-99474
    cpt_codes = [
        "//input[@class='PrivateSwitchBase-input css-1m9pwf3'][@type='checkbox'][@data-indeterminate='false']",
        "(//input[@class='PrivateSwitchBase-input css-1m9pwf3'][@type='checkbox'][@data-indeterminate='false'])[2]",
        "(//input[@class='PrivateSwitchBase-input css-1m9pwf3'][@type='checkbox'][@data-indeterminate='false'])[3]",
        "//p[contains(text(),'CPT-99474')]/following-sibling::label/span/input[@class='PrivateSwitchBase-input css-1m9pwf3'][@type='checkbox'][@data-indeterminate='false']"
    ]

    clicked_values = [99091, 99453, 99454, 99474]  # These should be the actual values of clicked checkboxes

    for code_xpath in cpt_codes:
        element = wait.until(EC.presence_of_element_located((By.XPATH, code_xpath)))
        driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", element)
        time.sleep(2)  # Allow a moment for scrolling
        driver.execute_script("arguments[0].click();", element)
        print(f"{code_xpath} clicked")
        driver.execute_script("window.scrollBy(0, -20);")  # Slightly move up to keep element in view
        time.sleep(2)  # Wait for observation

    # Step 6: New calculation using captured slider value
    total_reimbursement = sum(value * slider_value for value in clicked_values)
    print(f"Calculated Total Recurring Reimbursement: {total_reimbursement}")

except Exception as e:
    print(f"An error occurred: {e}")

# Close the browser after ensuring the clicks are performed
time.sleep(2)  # Allow some time to observe the change
driver.quit()
print("Browser closed")
