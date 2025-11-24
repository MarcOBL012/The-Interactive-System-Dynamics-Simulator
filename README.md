# **SysDyn-Web: The Interactive System Dynamics Simulator**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![Flask](https://img.shields.io/badge/Flask-2.0-green) ![Vensim](https://img.shields.io/badge/Vensim-Model-red) ![MySQL](https://img.shields.io/badge/MySQL-8.0-orange) ![License](https://img.shields.io/badge/License-MIT-lightgrey)

> **Bridge the gap between complex System Dynamics modeling and accessible web analytics.**

**SysDyn-Web** is a robust web application that integrates **Vensim** system dynamics models directly into a Python **Flask** environment. It allows users to simulate, visualize, and analyze complex dynamic systems (like transport logistics) in real-time through a responsive web interface, without needing the Vensim software installed locally.

---

## 🚀 **Key Features**

* **⚡ Real-Time Simulation Engine:** Powered by **PySD**, converting Vensim (`.mdl`) models into executable Python code on the fly.
* **📊 Interactive Visualization:** Dynamic graphs generated with **Matplotlib** and **mpld3**, offering zoom, pan, and toggle capabilities for every variable.
* **🎛️ Sensitivity Analysis:** Users can modify simulation parameters (e.g., *Rates, Initial Values, Time Steps*) via the UI and instantly see the impact on the system.
* **📥 Data Export:** One-click export of complete simulation results to **CSV** for further external analysis.
* **🔐 Secure Access:** Role-based authentication system backed by a **MySQL** database to manage user access.
* **🌐 Global Accessibility:** Integrated **Ngrok** tunneling to instantly share the localhost server publicly.

---

## 🏗️ **Architecture**

The system follows a Model-View-Controller (MVC) architecture ensuring clean code separation and scalability.

1.  **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript.
2.  **Backend:** Python Flask.
3.  **Simulation:** PySD (translates Vensim models to Python).
4.  **Database:** MySQL (User credentials and Model metadata).
5.  **Infrastructure:** Ngrok (Tunneling).

---

## 🛠️ **Tech Stack**

* **Language:** Python 3.x
* **Web Framework:** Flask
* **Database:** MySQL
* **Modeling Engine:** Vensim (`.mdl`), PySD
* **Data Manipulation:** Pandas, Numpy
* **Visualization:** Matplotlib, mpld3
* **Tunneling:** PyNgrok

---

## 💾 **Installation & Setup**

Follow these steps to get the project running on your local machine.

### 1. Clone the repository
```bash
git clone [https://github.com/your-username/sysdyn-web.git](https://github.com/your-username/sysdyn-web.git)
cd sysdyn-web
