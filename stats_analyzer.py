import os
import glob
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Error: GEMINI_API_KEY not found in .env file.")
    exit(1)

# Configuration
SCREENSHOTS_DIR = r"C:\Users\david\Pictures\Screenshots"
OUTPUT_FORMAT = "{player}, {civ}, {date}, {tool_age}, {bronze_age}, {iron_age}"

def get_file_date(filepath):
    try:
        timestamp = os.path.getmtime(filepath)
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except Exception:
        return "Unknown"

def analyze_image_with_gemini(filepath):
    client = genai.Client(api_key=API_KEY)
    
    image = Image.open(filepath)
    
    prompt = """
    Analyze this Age of Empires game timeline image. 
    The x-axis at the bottom represents Time.
    Identify the 5 players in the legend (usually bottom-left or bottom-right). 
    For each player, extract:
    1. Name
    2. Civilization
    3. The times of their Age Transitions (vertical lines on their graph row). 
       - The transitions are for Tool Age (II), Bronze Age (III), and Iron Age (IV).
       - Look for vertical lines labeled with Roman Numerals II, III, IV.
       - Estimate the time for each transition in TOTAL MINUTES (e.g. 15.5 for 15m 30s).
       - If a transition is missing, set it to "defeated".
       - If the time axis seems to be in Hours:Minutes (e.g. 1:00), convert to minutes (60.0).
    
    Return ONLY a valid JSON object with this structure:
    {
        "players": [
            {
                "name": "Player Name",
                "civilization": "Civ Name",
                "tool_age_minutes": float or "defeated",
                "bronze_age_minutes": float or "defeated",
                "iron_age_minutes": float or "defeated"
            }
        ]
    }
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt, image],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        return json.loads(response.text)
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None

def format_time(val):
    if val == "defeated":
        return "defeated"
    try:
        # Round to 1 decimal place
        return f"{float(val):.1f}"
    except:
        return str(val)

def process_image(filepath):
    print(f"Processing: {os.path.basename(filepath)}")
    
    start_time = time.time()
    result = analyze_image_with_gemini(filepath)
    
    if not result or "players" not in result:
        print("Failed to extract data.")
        return

    date_str = get_file_date(filepath)
    print(f"Analysis successful ({time.time() - start_time:.2f}s)")
    # Debug raw JSON
    # print(json.dumps(result, indent=2)) 
    
    for p in result["players"]:
        tool = format_time(p.get("tool_age_minutes", "defeated"))
        bronze = format_time(p.get("bronze_age_minutes", "defeated"))
        iron = format_time(p.get("iron_age_minutes", "defeated"))
        
        print(OUTPUT_FORMAT.format(
            player=p.get("name", "Unknown"),
            civ=p.get("civilization", "Unknown"),
            date=date_str,
            tool_age=tool,
            bronze_age=bronze,
            iron_age=iron
        ))
    
    print("-" * 30)

if __name__ == "__main__":
    files = glob.glob(os.path.join(SCREENSHOTS_DIR, '*.png'))
    if not files:
        print(f"No PNG files found in {SCREENSHOTS_DIR}")
    
    for f in files:
        process_image(f)
        # Sleep to avoid hitting rate limits if processing many
        time.sleep(2)
