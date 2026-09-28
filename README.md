<table border="0" style="border: none; border-collapse: collapse;">
  <tr style="border: none;">
    <td width="30%" align="center" valign="middle" style="border: none;">
      <img src="logo.png" alt="Aqar Hunter Logo" width="100%"/>
    </td>
    <td width="70%" valign="top" style="border: none;">
      <h1>🏠 Aqar Hunter Bot</h1>
      <p>
        <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python"/>
        <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-150458" alt="Pandas"/>
        <img src="https://img.shields.io/badge/Google%20Gemini-LLM%20Integration-8E75B2" alt="Google Gemini"/>
        <img src="https://img.shields.io/badge/Telegram-Bot%20API-26A5E4" alt="Telegram Bot API"/>
      </p>
      <p>An end-to-end Data + AI application built with Python. It converts structured real estate transaction data into natural-language market summaries delivered through a Telegram bot interface.</p>
    </td>
  </tr>
</table>

---

## 🎯 Problem & Approach

Analyzing real estate transaction records often requires sifting through large CSV files to identify district-level pricing patterns and activity. 

Aqar Hunter bridges the gap between raw data and user decision-making by allowing users to request a district analysis via Telegram. Instead of relying on an LLM to estimate values, the application performs exact deterministic data processing first, using the LLM solely to format verified figures into clear market insights.

---

## ⚙️ How It Works

```text
User
  ↓
Telegram Bot
  ↓
District Query
  ↓
Transaction Data (CSV)
  ↓
Pandas Data Processing
  ├── Average Price / m²
  ├── Transaction Volume
  └── Historical Price Patterns
  ↓
Google Gemini API
  ↓
Market Insight
```

### Workflow

1. **User Request:** The user inputs a district name into the Telegram bot.
2. **Data Retrieval:** The application queries local transaction CSV records for matching entries.
3. **Data Processing:** Pandas computes exact key metrics (average price/m², transaction counts, and historical patterns).
4. **Context Construction:** The aggregated metrics are injected into a controlled prompt payload.
5. **LLM Generation:** Google Gemini receives the structured context and formats it into a human-readable summary.
6. **Delivery:** The formatted insight is sent back to the user on Telegram.

---

## 📊 Data & Methodology

* **Dataset Scope:** Historical Saudi real estate transaction records ending in **March 2026**.
* **Data Boundary:** The bot explicitly informs users that data is historical and capped at March 2026, preventing misleading real-time assumptions.
* **Grounded LLM Logic:** To avoid LLM numerical hallucinations, all quantitative indicators are calculated programmatically in Pandas prior to API invocation. The Gemini API serves strictly as a natural-language translation layer.

---

## 📁 Project Structure

```text
.
├── data/                # Local transaction datasets (git-ignored)
├── .env                 # API keys & configuration (git-ignored)
├── .gitignore           # Version control exclusion rules
├── analyzer.py          # Data aggregation & statistical logic
├── aqar_api.py          # Gemini API integration & prompt context logic
├── bot.py               # Telegram bot handlers & entry point
├── data_handler.py      # Dataset loading & preprocessing functions
└── README.md            # Project documentation
```

---

## 🛠️ Tech Stack

| Technology | Role |
| :--- | :--- |
| **Python** | Core application language |
| **Pandas** | Data processing, filtering, and metric calculation |
| **Google Gemini API** | Grounded natural-language text generation |
| **pyTelegramBotAPI** | User interface and message handling |
| **python-dotenv** | Secure environment variable loading |

---

## 🔒 Security & Data Privacy

* **Repository Exclusion:** Raw CSV datasets, `.env` files, and private access keys are strictly excluded via `.gitignore`.
* **Access Control:** Includes a basic passkey verification mechanism within the bot to restrict unauthorized usage and protect API quotas.

---

## 📌 Future Improvements

* Integration with live or frequently updated transaction data sources
* Graphical trend charts and visual reports
* Automated ETL data pipelines for dataset ingestion
* Enhanced authentication layer
* Cloud deployment (Docker / Serverless)

---

## 👨‍💻 Author

**Hamoud Alaibani**  
*Data Analysis & Artificial Intelligence (DAAI)*