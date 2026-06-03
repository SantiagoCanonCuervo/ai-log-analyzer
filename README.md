# 🔍 AI Log Analyzer

AI-powered log analysis tool built with Python, Streamlit and Gemini AI for automated troubleshooting and diagnostics.

---

## 🚀 Features

* Analyze multiple `.log` and `.txt` files
* Manual error input support
* AI-powered diagnostics using Gemini
* Detect warnings and critical errors
* Technical troubleshooting analysis
* Suggested solutions for incidents
* Bulk log processing
* Interactive Streamlit interface

---

## 🛠️ Technologies Used

* Python
* Streamlit
* Google Gemini AI
* python-dotenv
* File handling
* Prompt engineering

---

## 📂 Supported Inputs

### Upload log files

* `.log`
* `.txt`

### Manual input

You can also paste:

* errors
* stack traces
* console outputs
* troubleshooting logs

directly into the application.

---

## 📷 Example Use Cases

* Application troubleshooting
* Server diagnostics
* Windows error analysis
* Incident investigation
* Log inspection
* Error detection and reporting

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/SantiagoCanonCuervo/ai-log-analyzer.git
```

Go to project folder:

```bash
cd ai-log-analyzer
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

Run the application:

```bash
streamlit run analizador_logs.py
```

---

## 📋 Requirements

Create a `requirements.txt` file with:

```txt
streamlit
python-dotenv
google-genai
```

---

## 🧠 How It Works

The application:

1. Reads uploaded log files or manual errors
2. Combines all logs into a single analysis context
3. Sends the information to Gemini AI
4. Generates:

   * technical diagnostics
   * error explanations
   * possible causes
   * troubleshooting recommendations

---

## 🔒 Security

Sensitive information such as API keys are protected using `.env` variables and `.gitignore`.

---

## 📌 Future Improvements

* PDF export
* CSV reports
* Severity filters
* Real-time monitoring
* Dashboard analytics
* Docker support
* Local AI model integration

---

▶️ EJECUTE

python -m streamlit run analizador_logs.py

## 👨‍💻 Author

Santiago Cañón Cuervo

Self-taught developer focused on automation, troubleshooting and backend technologies.

GitHub:
github.com/SantiagoCanonCuervo
