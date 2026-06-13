# HCP Verification Automator (Omnizia Scraper)

A powerful Python-based web automation tool built using **Selenium** and **Pandas**. This script automates the tedious process of manually searching Healthcare Professional (HCP) IDs on the Omnizia platform, verifying their existence, and extracting their names and cities directly into an Excel sheet.

## 💡 The Backstory & Challenge

During my data entry role at **Omnizia**, verifying thousands of unique HCP IDs manually was incredibly time-consuming and prone to human fatigue. Each ID required copying from Excel, searching in the system, waiting for the table to load, and copying back the doctor's Name and City. 

To boost workflow efficiency, I collaborated with an AI assistant to design this automation script. By using this tool, what used to take hours of manual copy-pasting is now completed flawlessly in minutes.

## ✨ Features

* **Bulk Processing:** Reads hundreds of HCP IDs directly from an input Excel file (`Automate.xlsx`).
* **Live Session Attachment:** Connects to an already open Chrome instance via `debuggerAddress (port 9222)`, bypassing login/re-authentication roadblocks.
* **Smart Exception Handling:** Automatically logs "Not Found" or "Error" for invalid IDs without breaking the entire loop.
* **Data Export:** Generates a structured output Excel file (`All_Doctor.xlsx`) combining original IDs with the extracted names and cities.

## 🚀 Tech Stack

* **Language:** Python
* **Libraries:** Selenium, Pandas, Openpyxl (for Excel handling)
* **Browser Driver:** ChromeDriver
