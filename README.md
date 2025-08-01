# 🧠 Org-Browser

A custom-built organizational browser designed for companies to securely manage and monitor how employees access the web — whether they're working in-office or remotely. Empower your organization with its own browser solution, connected to a central user and activity management system.

## 🚀 Project Goal

> What if each organization had its own internally managed browser — customized to its needs, workflows, and access policies?
> **RetroGlassBrowser** answers that question by giving companies a lightweight desktop browser built with Python and Qt, featuring:

- 🔐 Central login/signup using Google Sheets
- 🌐 Logged browsing activity to a centralized tracker (with IP, timestamp, visited URL)
- 🗂️ Tabbed browsing for efficiency
- 📁 Bookmark support for quick access to work-related pages
- 🖥 Remotely usable across multiple employee devices
- 🎯 Controlled, private environment — not reliant on consumer-grade browsers

## ✨ Features

### 🔒 User Control  
- 🧑‍💼 Login / Signup system  
- 📄 Credentials saved securely (Google Sheets as a lightweight database)

### 📈 Centralized Activity Logging  
- ⏱ Tracks: IP, Username, Date, Time, Visited URL  
- 📊 Uses Google Sheets for real-time logging  
- 🛡️ View logs centrally from Google Drive

### 🌐 Browsing Essentials  
- ➕ Add / close browser tabs  
- 🔁 Refresh, Go Back/Forward, Home  
- 📋 Copy current URL to clipboard  
- 🌐 Open any page in an external browser  
- 📌 Add bookmarks and open saved favorites

### 💼 Workplace-Ready  
- 🏢 Remote & office workers use the same browser  
- 🎛 Browser policies managed centrally  
- 👨‍💼 Keep teams focused on approved workflows  



## 💾 Installation

### 🐍 Requirements
Install Python dependencies from requirements.txt

🟢 Step-by-Step Google Sheets & Credentials Setup
1️⃣ Create the Necessary Google Sheets
	1.	Go to Google Sheets and log in with your organization’s account.
	2.	Create two spreadsheets:
	•	UsersDB (for user login info)
	•	TrackerDB (for activity logs)
 3.	In each spreadsheet:
	•	Add a worksheet/tab:
	•	In `UsersDB`, name a tab `users`, add header row: `Username, PasswordHash`
	•	In `TrackerDB`, name a tab `tracker`, add header row: `IP, Username, Date, Time, URL`
2️⃣ Create a Google Cloud Project
	1.	Visit the Google Cloud Console.
	2.	Click the project dropdown (top-left) → New Project.
	3.	Give it a name (e.g., `RetroGlassBrowserProject`), and click Create.
3️⃣ Enable Google Sheets & Drive APIs
	1.	Open your project.
	2.	In the left menu, go to APIs & Services > Enable APIs and Services.
	3.	Search for:
	•	Google Sheets API — click it, then click Enable.
	•	Google Drive API — click it, then click Enable.
4️⃣ Create a Service Account and Download Credentials JSON
	1.	In the Cloud Console, go to IAM & Admin > Service Accounts.
	2.	Click Create Service Account:
	•	Fill in a name and description.
	•	Click Create and Continue.
	•	Assign the Editor role when prompted for broad read/write access (for testing/development; restrict as needed for prod).
	•	Click Continue and then Done.
	3.	Find your new Service Account in the list.
	•	Click its name.
	•	Go to the Keys tab.
	•	Click Add Key → Create New Key → select JSON → Create.
	•	A file named `credentials.json` will download to your computer.
	•	Save this in your project folder (never share it publicly!).
5️⃣ Share Your Google Sheets with the Service Account
	1.	Open each Google Spreadsheet you created (`UsersDB` and `TrackerDB`).
	2.	Click Share at top right.
	3.	In the email field, paste your Service Account email (from your `credentials.json` under `client_email`: e.g., `your-service@your-project.iam.gserviceaccount.com`).
	4.	Set permission to Editor.
	5.	Click Send.
6️⃣ Confirm Setup
	•	Your Python code can now use the credentials JSON file to authenticate with the Google Sheets API, and read/write to your shared spreadsheets.
	•	Modifications or reads attempted by the app will succeed ONLY if the correct API permissions and sharing are in place.


