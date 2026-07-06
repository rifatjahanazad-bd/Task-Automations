import os
import time
import traceback
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#time handeling
#screenshot failure
#district output failure


INPUT_FILE = "adr_input.xlsx"
adr_OUTPUT_FILE = "hcp_data_final.xlsx"

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

try:
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)
    print("✅ Connected to Website!")
except Exception as e:
    print(f"❌ Connection Failed: {e}")
    exit()

if not os.path.exists(INPUT_FILE):
    print(f"❌ '{INPUT_FILE}' NOT FOUND!")
    exit()

# Reads file assuming row 1 contains headers
df = pd.read_excel(INPUT_FILE, dtype=str)

# Creating clean status columns for the output file
df["Output"] = ""
os.makedirs('screenshots', exist_ok=True)

print(f"🔍 Total {len(df)} records to process...\n")

for index, row in df.iterrows():
    # Matching exact column names from your configuration
    hcp_id = str(row.iloc[0]).strip()
    postal_code = str(row.iloc[3]).strip()
    street = str(row.iloc[2]).strip()

    
    print(f"🔎 {index+1}. Processing HCP ID: {hcp_id}")

    if hcp_id == "nan" or not hcp_id:
        df.at[index, 'Status'] = 'N/A'
        df.at[index, 'Notes'] = 'Missing HCP ID'
        continue

    # Navigate to dynamic profile page
    base_url = "https://website......./fromHcpID="
    driver.get(f"{base_url}{hcp_id}")
    # time.sleep(2)
    # check for website loaded proerply or not
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "loader"))) 
    
    try:
        # Step 1: Open creation interface
        create_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Create']")))
        create_btn.click()
        time.sleep(2) #test sleeper

        # Step 2: Select Country
        country_menu = wait.until(EC.presence_of_element_located((By.NAME, "Overarching_Country_ISO_Code")))
        Select(country_menu).select_by_value("DE")
        country_menu.click() ##test passed
        time.sleep(1) #test sleeper
        
        # Step 3: Enter Postal Code and click initial magic button
        postal_input = wait.until(EC.presence_of_element_located((By.NAME, "Postal_Code")))
        postal_input.clear()
        postal_input.send_keys(postal_code)
        time.sleep(1)
        
        #Step 4 - Magic Button
        magic_btn_1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//img[@alt='auto fill button']]")))
        magic_btn_1.click()
        time.sleep(2)

        # Verify City and Prefecture were autofilled
            #@@variables
        city_field = wait.until(EC.presence_of_element_located((By.NAME, "City")))
        prefecture_dropdown = wait.until(EC.presence_of_element_located((By.NAME, "Prefecture")))

        city_value = city_field.get_attribute("value").strip()

        selected_option = prefecture_dropdown.find_element(By.CSS_SELECTOR,"option:checked")
        prefecture_text = selected_option.text.strip()
            #@@logical
        if city_value == "" or prefecture_text == "--Select Prefecture--":
            df.at[index, "Output"] = "City/Prefecture"
            print(f"❌ {index+1}. {hcp_id} -> City/Prefecture Not Found")
            continue

        # Step 5: Enter Street line and click second magic icon

        address_input = wait.until(EC.visibility_of_element_located((By.NAME, "Address_Line_1")))
        address_input.click()
        address_input.clear()
        address_input.send_keys(street)

        #Step 6 District Magic Button Click
        district_input = wait.until(EC.presence_of_element_located((By.NAME, "District")))
        district_magic_btn = district_input.find_element(By.XPATH,"./following-sibling::button")
        district_magic_btn.click()
        time.sleep(1.5)
        
        # Evaluation State 2: District failed to autofill
        district_field = wait.until(EC.presence_of_element_located((By.NAME, "District")))
        district_value = district_field.get_attribute("value").strip()

        if district_value == "":
            df.at[index, "Output"] = "District"
            print(f"❌ {index+1}. {hcp_id} -> District Autofill Failed")
            continue

        # Processing After Clicking
        screenshot_filename = f"HCP_{hcp_id}.png"
        driver.save_screenshot(screenshot_filename) #saves an SS to see a visual where it exactly failed
        
        print(f"✅ {index+1}. {hcp_id} -> Autofilled Successfully")
        df.at[index, "Output"] = "Successful"
        
        print("   ⏸️  Pausing 2 sec for inspection...")
        time.sleep(2)
        
    except Exception as e:
        df.at[index, "Output"] = "Error"

        print(f"\n===== ERROR ON RECORD {index+1} =====")
        print(f"HCP ID: {hcp_id}")
        print(f"Type: {type(e).__name__}")
        print(f"Details: {repr(e)}")
        traceback.print_exc()

        continue
# Commit evaluations to the targeted output file
df.to_excel(adr_OUTPUT_FILE, index=False)
print(f"\n🔥 Completed! Results written to '{adr_OUTPUT_FILE}'")
