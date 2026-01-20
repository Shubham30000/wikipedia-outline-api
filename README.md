# Wikipedia Outline Extraction API

> Automated data extraction pipeline that scrapes Wikipedia country pages and transforms unstructured HTML into structured Markdown outlines using FastAPI and XPath.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**🌐 Live Demo:** https://wikipedia-outline-api-2.onrender.com

**Try it now:**
- API Docs: https://wikipedia-outline-api-2.onrender.com/docs
- Example: https://wikipedia-outline-api-2.onrender.com/api/outline?country=India
```

---

### **2. Test Your Live API Right Now**

Open these links in your browser:

✅ **Interactive Docs:**
```
https://wikipedia-outline-api-2.onrender.com/docs
```

✅ **Test with India:**
```
https://wikipedia-outline-api-2.onrender.com/api/outline?country=India
```

✅ **Test with Japan:**
```
https://wikipedia-outline-api-2.onrender.com/api/outline?country=Japan
---

## 📊 Problem Statement

Educational platforms and data analysts often need to extract structured information from Wikipedia pages. Manually copying content or writing custom scrapers for each page is time-consuming and doesn't scale.

This project solves that by:
- Automatically fetching Wikipedia pages for any country
- Extracting heading hierarchy (H1-H6) using XPath
- Converting HTML structure into clean Markdown format
- Serving data through a RESTful API with caching

---

## 🔑 Key Skills Demonstrated

| Skill | Implementation |
|-------|----------------|
| **Web Scraping** | `lxml` with XPath queries to extract headings from Wikipedia HTML |
| **Data Transformation** | Converting hierarchical HTML headings into Markdown format |
| **API Development** | FastAPI with query validation, error handling, and CORS |
| **Caching Strategy** | MD5-based file caching to avoid redundant network requests |
| **ETL Pipeline** | Extract (HTTP) → Transform (Parse) → Load (Format) |

---

## 🏗️ How It Works

```
Client Request (?country=India)
         ↓
FastAPI Endpoint Validation
         ↓
Cache Check (MD5 hash of URL)
         ↓
   [Cache Hit] → Return cached HTML
   [Cache Miss] → Fetch from Wikipedia → Save to cache
         ↓
Parse HTML with lxml (XPath: //h1 | //h2 | ... | //h6)
         ↓
Extract headings in document order
         ↓
Format as Markdown (# for H1, ## for H2, etc.)
         ↓
Return Plain Text Response
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/Shubham30000/wikipedia-outline-api.git
cd wikipedia-outline-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn app.main:app --reload
```

**API runs at:** http://localhost:8000

---

## 💻 Usage

### Basic Request
```bash
curl "http://localhost:8000/api/outline?country=India"
```

### Example Response
```markdown
# Wikipedia Outline: India

## Contents

# India

## Etymology

## History

### Ancient India

### Medieval India

### Early modern India

## Geography

### Climate

### Biodiversity

## Government and politics

### Administrative divisions

#### States

#### Union territories
```

### Interactive Documentation
- **Swagger UI:** http://localhost:8000/docs
- **Try it live:** Test different countries directly in the browser

### Python Client
```python
import requests

response = requests.get(
    "http://localhost:8000/api/outline",
    params={"country": "Japan"}
)

print(response.text)
```

---

## 📁 Project Structure

```
wikipedia-outline-api/
├── app/
│   ├── main.py              # FastAPI app with CORS config
│   ├── api/
│   │   └── routes.py        # API endpoints (/api/outline)
│   ├── core/
│   │   ├── config.py        # Settings and environment vars
│   │   └── cache.py         # MD5-based file caching
│   └── services/
│       ├── wikipedia.py     # HTTP fetching and XPath parsing
│       └── outline.py       # Markdown formatting
├── cache/                   # Cached Wikipedia HTML (gitignored)
├── tests/
│   └── test_api.py         # API tests
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔧 Technical Details

### Technologies Used
- **FastAPI** - Web framework (auto-generated OpenAPI docs)
- **httpx** - Async HTTP client for Wikipedia requests
- **BeautifulSoup4** - HTML parsing (reliable cross-platform deployment)
- **python-dotenv** - Environment variable management
- **uvicorn** - ASGI server

### Why BeautifulSoup4 instead of lxml?
While lxml is faster, BeautifulSoup4 was chosen for:
- **Better deployment compatibility** across cloud platforms
- **No compilation required** (pure Python)
- **Easier setup** for development and testing
- **Sufficient performance** for single-request use cases (~100-200ms difference)

### Why These Choices?

| Decision | Reason |
|----------|--------|
| **File caching** | Simple, no database overhead, works offline after first fetch |
| **MD5 hashing** | Unique cache keys for URLs, handles special characters |
| **Plain text response** | Lightweight, easy to parse by downstream tools |

### Caching Implementation
```python
# Generate unique filename
filename = hashlib.md5(url.encode('utf-8')).hexdigest()
cache_path = f"cache/{filename}"

# Check if exists
if os.path.exists(cache_path):
    return read_from_file(cache_path)  # Cache hit
else:
    content = fetch_from_web(url)       # Cache miss
    save_to_file(cache_path, content)
    return content
```

**Benefits:**
- Avoids repeated downloads of same Wikipedia page
- Faster response times (~50-150ms for cached requests)
- Debugging is easier (can inspect cached HTML files)

---

## 📊 Performance Notes

| Metric | Value | Details |
|--------|-------|---------|
| **Response Time (Cached)** | ~50-150ms | Local machine, depends on system |
| **Response Time (Uncached)** | ~2-5s | Depends on Wikipedia response time |
| **Cache Storage** | ~100-500KB per page | Compressed HTML |

*Note: These are observed values during local testing, not production benchmarks.*

---

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

**Test Coverage:** Includes endpoint validation, error handling, and cache logic.

---

## 📖 API Documentation

### Endpoint: `GET /api/outline`

**Description:** Fetch Wikipedia outline for a country

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `country` | string | Yes | Country name (e.g., "India", "United States") |

**Response Format:** `text/plain` (Markdown)

**Status Codes:**
| Code | Meaning |
|------|---------|
| 200 | Success - outline returned |
| 400 | Bad request - empty/invalid country parameter |
| 404 | Wikipedia page not found for this country |
| 503 | Network error while fetching Wikipedia |

**Example:**
```bash
GET /api/outline?country=Vanuatu

# Returns:
# Wikipedia Outline: Vanuatu
# 
# # Vanuatu
# ## Etymology
# ## History
# ### Prehistory
# ...
```

---

## 🧠 What I Learned

Building this project taught me:

1. **XPath is more reliable than CSS selectors** when extracting structured data from HTML
2. **Wikipedia pages vary significantly** across countries - some have deep hierarchies (H1-H6), others are flatter
3. **Caching dramatically improves debugging speed** and prevents getting rate-limited by Wikipedia
4. **FastAPI's automatic query validation** saves a lot of manual error handling code
5. **Extracting headings in document order** (not grouped by level) requires using XPath unions: `//h1 | //h2 | //h3`

---

## 🚀 Deployment

### Option 1: Render (Recommended - Free)

1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: wikipedia-outline-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. Push to GitHub
3. Connect Render to your repo
4. Auto-deploys on every push

### Option 2: Docker

```bash
docker build -t wikipedia-api .
docker run -p 8000:8000 wikipedia-api
```

### Option 3: Local Production

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

## 🔮 Future Enhancements

- [ ] **JSON Output Format** - Add `/api/outline/json` endpoint for structured data
- [ ] **Batch Processing** - Accept multiple countries in one request
- [ ] **Section Filtering** - Extract only specific sections (e.g., "History")
- [ ] **Multi-language Support** - Support non-English Wikipedia editions
- [ ] **Cache TTL** - Auto-refresh cached pages after 7 days
- [ ] **Rate Limiting** - Prevent API abuse with token bucket

---

## ⚖️ Disclaimer

This project is for **educational purposes** and respects Wikipedia's robots.txt policy:
- Uses file caching to minimize load on Wikipedia servers
- Includes proper User-Agent headers
- Does not perform aggressive scraping

For production use, consider using the official [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page).

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Shubham Singh**  
IIT Madras BS in Data Science | Kolkata, India

- 📧 Email: 23f2005282@ds.study.iitm.ac.in
- 💼 LinkedIn: [linkedin.com/in/shubham-singh-50a90a253](https://www.linkedin.com/in/shubham-singh-50a90a253)
- 🐱 GitHub: [github.com/Shubham30000](https://github.com/Shubham30000)

**Open to Data Analyst/Engineering internships starting 2026**

---

## 🙏 Acknowledgments

- **Straive** for the project assignment that inspired this implementation
- **Wikipedia** for providing free, structured knowledge
- **FastAPI community** for excellent documentation

---

## 📞 Questions?

Feel free to:
- Open an issue on GitHub
- Connect with me on LinkedIn
- Email me directly

---

<div align="center">

**⭐ If this project helped you, consider giving it a star! ⭐**

*Built for learning web scraping, ETL pipelines, and API development*

</div>