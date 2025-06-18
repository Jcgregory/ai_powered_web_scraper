# 🕸️ Ethical AI-Powered Web Scraper (with Tor + Content Filtering)

This project is a powerful yet ethical web scraper built in Python that uses Tor for anonymity, content filtering via LLMs (or static logic), and polite crawling practices. It is designed for testing and research purposes.

## ⚙️ Features

- 🌐 **Tor-Enabled Anonymous Crawling**  
  Uses `socks5h://127.0.0.1:9050` to route all traffic through Tor.

- 📜 **robots.txt Override (Test Mode)**  
  Controlled override option to skip robots.txt checks during local testing.

- 🤖 **LLM-Based Relevance Filtering** *(Optional)*  
  Uses [Ollama](https://ollama.com) with a local model (e.g., `mistral`) to determine if a page contains relevant content.

- 🖼️ **Content Extraction**  
  Extracts clean page titles, paragraphs, image metadata, and table data.

- 📚 **Focused Content Scraping**  
  Can be configured to scrape only relevant sections (like Wikipedia/Fandom “Contents”).

- 🔁 **User-Agent Rotation & Polite Delays**  
  Random headers and sleep intervals to reduce detection and stay polite.

---

## 📁 Project Structure
.
├── crawler.py # Main scraper script
├── tor_awake.py # Starts Tor with custom bridges
├── tor_logs.py # For streaming Tor logs
├── test_tor.py # Verifies Tor routing
├── .gitignore
└── README.md


---

## 🛠️ Requirements

- Python 3.8+
- [Tor](https://www.torproject.org/) (configured to run in background or via `tor_awake.py`)
- [Ollama](https://ollama.com) *(optional, for content filtering)*

Install dependencies:
```bash
pip install -r requirements.txt

Ethics & Disclaimer
This tool is intended strictly for educational and ethical testing purposes.
Always respect robots.txt, Terms of Service, and legal policies of the sites you target.
You are responsible for any misuse.

📄 License
Licensed under the MIT License.
