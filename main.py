import os
import html
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from schemas import ChatbotQuery, PollingLocator

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = "You are a strictly non-partisan election educator. Provide neutral, factual, and unbiased information about the election process. Do not express political opinions, endorse candidates, or provide biased analysis."

# Cache the GenerativeModel instance
model = None
if GEMINI_API_KEY:
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)

@app.get("/")
async def root():
    return FileResponse("index.html")

@app.get("/api/config")
async def config():
    return {"maps_api_key": os.environ.get("GOOGLE_MAPS_API_KEY", "")}

@app.post("/api/educate")
async def educate(query: ChatbotQuery):
    sanitized_query = query.query.strip()
    # Robust input sanitization as per Security Protocol
    sanitized_query = html.escape(sanitized_query)

    if not GEMINI_API_KEY:
        # Fallback for testing without key
        return {
            "message": f"AI Simulation: To answer '{sanitized_query}', I would explain the process impartially. (Configure GEMINI_API_KEY for real responses)",
            "sanitized_query": sanitized_query
        }

    try:
        response = await model.generate_content_async(sanitized_query)
        return {"message": response.text, "sanitized_query": sanitized_query}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/locate")
async def locate(locator: PollingLocator):
    # Mocked, sanitized JSON response with coordinates
    return {
        "polling_place": f"Mocked Polling Place for ZIP {locator.zip_code}",
        "zip_code": locator.zip_code,
        "lat": 38.8977,
        "lng": -77.0365
    }
