# AI Services Hub Dashboard

Dashboard Z0ramp AI

## 🚀 Quick Start

1. **Create environment file (.env):**
   Create a `.env` file in the project root with the API URL:
   ```env
   ASCLOUD_API_URL={url}
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server:**
   ```bash
   uvicorn main:app --reload --port 5000
   ```

4. **Server:**
   ```bash
   Uvicorn running on http://127.0.0.1:5000
   ```

## 🛠️ Technologies

* **Backend:** FastAPI (Python)
* **Frontend:** HTMX + Tailwind CSS + Jinja2 Templates
* **Environment Loading:** Python-Dotenv
