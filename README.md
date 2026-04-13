# AoE-Simulator

An Age of Empires simulation and analysis project suite.

## Overview
AoE-Simulator is a multi-faceted project suite designed to simulate, analyze, and optimize Age of Empires gameplay mechanics. It is broken down into the following core components:

* **Eco Simulator (`eco_sim/`)**: Simulates the economy of the game. It models resources, gathering, unit spawning, and building construction to evaluate different economic decisions.
* **Battle Simulator (`battle_sim/`)**: Simulates unit combat and pathing. It allows you to run deterministic battles between different unit compositions (e.g., Clubman vs Axeman) and evaluate the outcomes.
* **Build Order Optimizer (`optimizer/`)**: Uses genetic algorithms (genomes, fitness functions) to discover optimal build orders for specific goals based on the economy simulator base.
* **Wiki Scraper (`scraper/`)**: Extracts up-to-date unit data and statistics directly from the Age of Empires wiki, storing them in local JSON data structures (`data/units.json`) for use by the simulators.
* **Timeline Stats Analyzer (`stats_analyzer.py`)**: A tool using the Gemini 2.0 Flash API to visually analyze Age of Empires post-game timeline screenshots. It extracts player names, civilizations, and age transition times, converting them into structured JSON or text data.

## Features & Usage

### 1. Stats Analyzer
Uses the Gemini API to extract player data and age transition times from post-game screenshots (looks in `C:\Users\david\Pictures\Screenshots` by default).
Requires `GEMINI_API_KEY` in your `.env` file.
```bash
python stats_analyzer.py
```

### 2. Simulators
You can run verification scripts to see how the simulators behave with the current JSON unit data:

**Battle Simulator Verification:**
```bash
python verify_battle.py
```
**Economy Simulator Verification:**
```bash
python verify_sim.py
```

### 3. Data Scraper
Scrape the latest unit statistics to update the initial JSON data:
```bash
python scraper/main.py
```

## Setup & Installation
1. Ensure Python 3.8+ is installed.
2. Set up a virtual environment (there is an existing `.venv` folder).
   ```bash
   # Windows
   .venv\Scripts\activate
   ```
3. Create a `.env` file in the root directory and add your API keys:
   ```env
   GEMINI_API_KEY="your_genai_api_key_here"
   ```
4. Run the components of your choice!
