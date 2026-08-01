# PhishGuard
# 🔐 Phishing Website Detection

Hey! 👋

This is one of my machine learning projects. I built it because phishing websites are everywhere, and I wanted to see if a machine could tell the difference between a genuine website and a fake one just by looking at its URL.

The idea is simple:

You paste a website link into the application, click **Predict**, and the model tells you whether the website looks **Legitimate** or **Phishing**.

---

## 🤔 Why did I build this?

Mostly to learn.

I wanted to combine **Machine Learning** with **Flask** and create something that people can actually interact with instead of just training a model in a notebook.

This project also helped me understand how a trained model can be deployed as a web application.

---

## 🛠️ What I used

* Python
* Flask
* Scikit-learn
* SQLAlchemy
* HTML
* CSS
* JavaScript
* Bootstrap
* SQLite


## 📂 Project Structure

```text
phishing-website-detection/
│── app.py
│── model/
│   ├── phishing_model.pkl
│── templates/
│── static/
│── database/
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation

1. Clone the repository

```bash
git clone https://github.com/abhirammmmmm7/phishing-website-detection.git
```

2. Navigate to the project folder

```bash
cd phishing-website-detection
```

3. Create a virtual environment

```bash
python -m venv venv
```

4. Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

5. Install dependencies

```bash
pip install -r requirements.txt
```

6. Run the application

```bash
python app.py
```

---



## ⚙️ How it works

1. Enter a website URL.
2. The application extracts important URL features.
3. A trained Machine Learning model analyzes those features.
4. The result is shown as either:

   * ✅ Legitimate
   * 🚨 Phishing

Pretty straightforward.

---

## 📚 What I learned

This project taught me a lot about:

* Training machine learning models
* Feature extraction
* Flask backend development
* Working with databases
* Deploying ML models
* Connecting frontend and backend

---

## 🚀 What's next?

If I continue working on this project, I'd like to:

* Improve prediction accuracy
* Add real-time URL reputation checks
* Support more phishing indicators
* Deploy it online for public use

---

## 👨‍💻 About me

I'm **Abhiram S**, a Python Full Stack Developer who enjoys building projects that combine web development and machine learning.

If you have any suggestions or feedback, feel free to reach out—or even better, fork the project and make it better!

⭐ Thanks for checking it out!

