# 🏥 Smart Pharma Inventory: AI-Driven Demand Forecasting
**An Integrated AI & Management Engineering Solution for Digital Health Operations**

---

## 🌟 Executive Summary
This project represents a "Masterpiece" integration of **Artificial Intelligence** (Technical depth from Harbin Engineering University) and **Management Engineering** (Strategic optimization from Thammasat University). 

In the healthcare sector, drug stockouts can be life-threatening, while overstocking leads to massive financial waste through expiration. This system leverages **Machine Learning** to predict pharmaceutical demand and applies **Industrial Engineering (IE)** principles to optimize inventory levels.

---

## 🚀 Key Objectives
* **AI Perspective:** Build a high-accuracy Time-Series model to predict daily drug consumption.
* **Management Perspective:** Categorize inventory using **ABC Analysis** to prioritize high-value/high-volume medicines.
* **Digital Health Impact:** Ensure 99% service levels for critical medication while reducing holding costs by ~15-20%.

---

## 📊 Methodology & Workflow

### 1. Multi-Granularity Data Processing
We analyze pharmaceutical sales data across four temporal scales: **Hourly, Daily, Weekly, and Monthly**.
* **Data Cleaning:** Handling time-series continuity, missing values, and outlier detection.
* **Feature Engineering:** Creating temporal features such as `Is_Weekend`, `Seasonality`, and `Holiday_Effect`.

![Correlation Graph](/output.png)

### 2. Strategic Inventory Categorization (ABC Analysis)
Using Management Engineering principles, we classify drugs based on their cumulative sales impact:
* **Class A:** Top 70% of sales volume (Critical focus for AI Prediction).
* **Class B:** Next 20% (Standard monitoring).
* **Class C:** Bottom 10% (Low-frequency items).

![Correlation Graph](/output2.png)

### 3. Predictive Modeling (In Progress)
Currently implementing Time-Series Forecasting models (e.g., **LSTM** or **Prophet**) to provide 7-day look-ahead demand forecasts for Class A medications.

### 4. Full-Stack Integration
Deploying the model via a **Flask Web Application** to provide a real-time dashboard for hospital pharmacists and supply chain managers.

---

## 🛠️ Tech Stack & Tools
| Category | Technology |
| :--- | :--- |
| **Languages** | Python (Data Science), JavaScript (Logic/UI) |
| **AI/ML** | Pandas, Scikit-learn, (TensorFlow/Prophet - Pending) |
| **Backend** | Flask (Python Web Framework) |
| **Management** | ABC Analysis, Safety Stock Optimization |
| **DevOps** | Git/GitHub, VS Code, Docker (Planned) |
| **E-Portfolio** | Documented on Notion & Hosted on GitHub |

---

## 📈 Projected Results
* **Accuracy:** Target >85% Mean Absolute Percentage Error (MAPE) for Top-selling drugs.
* **Efficiency:** Automated re-order point calculations based on AI forecasts.
* **Visibility:** Interactive dashboard for non-technical healthcare stakeholders.

---

## 👩‍💻 About the Author
**Patthamon Charaschimpleekul**
* **Dual Degree Candidate:** - B.Eng. Artificial Intelligence, Harbin Engineering University
  - B.Eng. Management Engineering, Thammasat University
* **Focus:** Digital Health, AI Ethics, and Operational Excellence.

---
# 🏥 Smart Pharma Inventory: AI-Driven Demand Forecasting
**An Integrated AI & Management Engineering Solution for Digital Health Operations**

---

## 🌟 Executive Summary
This project represents a "Masterpiece" integration of **Artificial Intelligence** (Technical depth from Harbin Engineering University) and **Management Engineering** (Strategic optimization from Thammasat University). 

In the healthcare sector, drug stockouts can be life-threatening, while overstocking leads to massive financial waste through expiration. This system leverages **Machine Learning** to predict pharmaceutical demand and applies **Industrial Engineering (IE)** principles to optimize inventory levels.

---

## 🚀 Key Objectives
* **AI Perspective:** Build a high-accuracy Time-Series model to predict daily drug consumption.
* **Management Perspective:** Categorize inventory using **ABC Analysis** to prioritize high-value/high-volume medicines.
* **Digital Health Impact:** Ensure 99% service levels for critical medication while reducing holding costs by ~15-20%.

---

## 📊 Methodology & Workflow

### 1. Multi-Granularity Data Processing
We analyze pharmaceutical sales data across four temporal scales: **Hourly, Daily, Weekly, and Monthly**.
* **Data Cleaning:** Handling time-series continuity, missing values, and outlier detection.
* **Feature Engineering:** Creating temporal features such as `Is_Weekend`, `Seasonality`, and `Holiday_Effect`.

> **[INSERT IMAGE: A screenshot of your 'Drug Sales Correlation Heatmap' or 'Monthly Trends Graph']**

### 2. Strategic Inventory Categorization (ABC Analysis)
Using Management Engineering principles, we classify drugs based on their cumulative sales impact:
* **Class A:** Top 70% of sales volume (Critical focus for AI Prediction).
* **Class B:** Next 20% (Standard monitoring).
* **Class C:** Bottom 10% (Low-frequency items).

> **[INSERT IMAGE: The Bar Chart showing 'Share of Total Sales by Drug Category']**

### 3. Predictive Modeling (In Progress)
Currently implementing Time-Series Forecasting models (e.g., **LSTM** or **Prophet**) to provide 7-day look-ahead demand forecasts for Class A medications.

### 4. Full-Stack Integration
Deploying the model via a **Flask Web Application** to provide a real-time dashboard for hospital pharmacists and supply chain managers.

---

## 🛠️ Tech Stack & Tools
| Category | Technology |
| :--- | :--- |
| **Languages** | Python (Data Science), JavaScript (Logic/UI) |
| **AI/ML** | Pandas, Scikit-learn, (TensorFlow/Prophet - Pending) |
| **Backend** | Flask (Python Web Framework) |
| **Management** | ABC Analysis, Safety Stock Optimization |
| **DevOps** | Git/GitHub, VS Code, Docker (Planned) |
| **E-Portfolio** | Documented on Notion & Hosted on GitHub |

---

## 📈 Projected Results
* **Accuracy:** Target >85% Mean Absolute Percentage Error (MAPE) for Top-selling drugs.
* **Efficiency:** Automated re-order point calculations based on AI forecasts.
* **Visibility:** Interactive dashboard for non-technical healthcare stakeholders.

---

## 👩‍💻 About the Author
**Patthamon Charaschimpleekul**
* **Dual Degree Candidate:** - B.Eng. Artificial Intelligence, Harbin Engineering University
  - B.Eng. Management Engineering, Thammasat University
* **Focus:** Digital Health, AI Ethics, and Operational Excellence.

---