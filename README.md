# 🚀 Cybersecurity Intrusion Detection with Machine Learning

## 📖 Project Overview
This project focuses on detecting cybersecurity intrusions using **machine learning** techniques.  
The dataset includes various network and authentication-related features, and the goal is to classify whether an **attack is detected** or not.

## 📂 Features Used for Detection
- `session_id`
- `network_packet_size`
- `protocol_type`
- `login_attempts`
- `session_duration`
- `encryption_used`
- `ip_reputation_score`
- `failed_logins`
- `browser_type`
- `unusual_time_access`

## ⚠️ Handling Data Imbalance
Cybersecurity datasets often suffer from **imbalanced class distributions** (i.e., fewer attack cases).  
To address this, we used **SMOTE (Synthetic Minority Over-sampling Technique)** to balance the dataset.

### **🔹 Data Balancing Process**
1. **Before Balancing:** The dataset had an unequal distribution of attack vs. non-attack cases.
2. **Applied SMOTE:** Generated synthetic samples to create a balanced dataset.
3. **After Balancing:** Both classes now have equal representation.

## 📊 Data Preprocessing & Model Training
- **Preprocessing:** Data cleaning, feature selection, and normalization.
- **Modeling:** Applied machine learning models such as Random Forest, SVM, and Neural Networks.
- **Evaluation:** Used accuracy, precision, recall, and F1-score.

📊 **Visualization of Class Distribution (Before & After Balancing)**  
![Class Distribution](path_to_visualization_image.png)  

