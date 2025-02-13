# 📌 Student Minds - Cloud Placement Management Database

A Python-based placement management system with a GUI interface that stores student placement records securely using **Google Sheets & SQLite**.

---

## 🌟 Project Overview

**Student Minds** is a cloud-based placement management system designed to efficiently store and manage placement records of students. The system integrates **Google Sheets** as a cloud database, providing accessibility while ensuring data security.

### 🎯 Key Features
✅ **GUI Interface:** User-friendly interface for managing placement records.  
✅ **Cloud Integration:** Stores data securely in Google Sheets for easy access.  
✅ **CRUD Operations:** Supports Create, Read, Update, and Delete functionalities.  
✅ **Efficient Data Retrieval**: Fetches and updates student placement details in real time.
✅ **Search & Filter:** Easily find student records using search functionality.  
✅ **Secure Access:** Only privileged individuals (college admins, placement officers) can access records.  

---

## 🛠 Tech Stack Used

🔹 **Python** - Core language for application development  
🔹 **Tkinter** - GUI framework for building the user interface  
🔹 **Google Sheets API** - Cloud storage for placement data  
🔹 **SQLite** - Local database for storing data before syncing  
🔹 **Pandas** - Data processing and manipulation  
🔹 **gspread** - Python library for interacting with Google Sheets  

---

## 🚀 Installation Guide

### 🔹 1. Clone the Repository
```bash
git clone https://github.com/lasya1005/Student-Minds.git
cd Student-Minds
```

### 🔹 2. Install Dependencies
Run the following command to install required Python packages:
```bash
pip install -r requirements.txt
```

### 🔹 3. Setup Google Sheets API
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project and enable the **Google Sheets API** & **Google Drive API**.
3. Generate a **service account key** (JSON file) and rename it as `credentials.json`.
4. Share your Google Sheet with the **service account email**.

### 🔹 4. Run the Application
```bash
python main.py
```

---

## 🖥 How It Works
1️⃣ **User Interface** - The GUI allows users to add, update, delete, and search student placement records.  
2️⃣ **Data Storage** - Data is temporarily stored in **SQLite** and synced to **Google Sheets**.  
3️⃣ **Real-time Updates** - The system fetches and updates records dynamically.  

---

## 📜 Project Structure
```
📂 Student-Minds
│── 📜 main.py           # Main application script
│── 📜 config.json       # Configuration file for API keys and settings
│── 📜 requirements.txt  # Dependencies list
│── 📂 database/         # Local SQLite database (PlacementManagement.db)
│── 📂 assets/           # UI icons and assets (if applicable)
│── 📂 logs/             # Log files for debugging
│── 📂 docs/             # Documentation (if needed)
│── 📜 .gitignore        # Ignored files (including credentials.json)
│── 📜 README.md         # Project documentation (this file)
```

---

## 🎯 Future Enhancements
🔹 Add **data visualization** (placement statistics, company trends)  
🔹 Implement **user authentication** (login system for admin access)  
🔹 Enable **export options** (PDF, Excel reports)  
🔹 Integrate **email notifications** (alerts for placement updates)  

---

## 🤝 Contributing
Feel free to fork the repo, make enhancements, and submit pull requests!  

---

## 📧 Contact
**Lasya G** - Developer & Maintainer  
📍 Hyderabad, Telangana  
📩 [LinkedIn](https://www.linkedin.com/in/lasya-ganji-59b7ba2b5/) | [GitHub](https://github.com/lasya1005)  

---

### ⭐ If you like this project, give it a star! 🌟
