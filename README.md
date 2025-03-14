# Coupon_distribution
# Round-Robin Coupon Distribution with Admin Panel

## 📌 Project Overview
This project is a **Flask-based web application** that allows users to claim coupons sequentially (round-robin distribution) while providing an **admin panel** for managing coupons and preventing abuse.

## 🚀 Features
### ✅ **User Side (Guest Users)**
- Claim coupons **without logging in**.
- Coupons are **assigned sequentially** without duplication.
- **Abuse Prevention:**
  - **IP Tracking:** Users can only claim one coupon per **24 hours**.
  - **Cookie-Based Tracking:** Prevents multiple claims from the same browser session.
- **User Feedback:** Displays messages if a user is restricted from claiming.

### ✅ **Admin Panel**
- **Secure Login for Admins** (hashed password authentication).
- **Manage Coupons:**
  - View all available & claimed coupons.
  - Add new coupons.
  - Enable/Disable coupons dynamically.
  - View user claim history (IP/session-based tracking).

## 🛠️ Tech Stack
- **Backend:** Flask (Python)
- **Database:** SQLite (can be upgraded to PostgreSQL/MySQL)
- **Frontend:** HTML, CSS, JavaScript (Flask templates)
- **Security:** Flask-Session, IP & Cookie tracking, Password Hashing
- **Deployment:** PythonAnywhere

## ⚙️ Installation & Setup
### **Step 1: Clone the Repository**
```bash
git clone https://github.com/Shreya728/Coupon_distribution.git
cd Coupon_distribution
```

### **Step 2: Create a Virtual Environment & Install Dependencies**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **Step 3: Run the Flask Application Locally**
```bash
python app.py
```
Visit `http://localhost:5000` for the user page.
Visit `http://localhost:5000/admin` for the admin panel.

## 📊 Database Initialization
- **Automatic Database Setup:** When you run `app.py`, the database is initialized automatically.
- **Admin Credentials (Pre-Configured in `app.py`):**
  - **Username:** `Shreya`
  - **Password:** `shreya123` *(hashed in the database for security)*
  - *(Change the password after the first login for security.)*

## 🌍 Deployment on PythonAnywhere
### **Step 1: Upload Project Files**
- Upload the project folder to PythonAnywhere via Git or the Web UI.

### **Step 2: Set Up Virtual Environment**
```bash
cd ~/Coupon_distribution
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **Step 3: Configure the Web App**
1. Go to the **Web** tab on PythonAnywhere.
2. Select **Manual Configuration** and choose **Python 3.9 or later**.
3. Edit the WSGI file (`/var/www/SHREYAPAT728_pythonanywhere_com_wsgi.py`):
```python
import sys
import os

project_home = u'/home/SHREYAPAT728/Coupon_distribution'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import app as application
```
4. Save and reload the web app.

### **Step 4: Access the Live App**
- **User Page:** [`https://SHREYAPAT728.pythonanywhere.com`](https://SHREYAPAT728.pythonanywhere.com)
- **Admin Panel:** [`https://SHREYAPAT728.pythonanywhere.com/admin`](https://SHREYAPAT728.pythonanywhere.com/admin)

## 🔗 Links
- **Live Demo:** [`https://SHREYAPAT728.pythonanywhere.com`](https://SHREYAPAT728.pythonanywhere.com)
- **GitHub Repository:** [`https://github.com/Shreya728/Coupon_distribution`](https://github.com/Shreya728/Coupon_distribution)

## 📄 License
This project is open-source and available under the **MIT License**.

## 👨‍💻 Contributing
Feel free to contribute by forking the repository, making changes, and submitting a pull request.

---

### 🎯 **This project ensures a secure, scalable, and user-friendly coupon distribution system. Enjoy coding! 🚀**
