from typing import Type, Dict, List
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool, tool
import random

# Pre-approved destinations from Lahore
APPROVED_DESTINATIONS = ["Hunza", "Naran", "Skardu", "Murree", "Swat", "Gilgit"]
APPROVED_DESTINATIONS_STR = ", ".join(APPROVED_DESTINATIONS[:-1]) + f", or {APPROVED_DESTINATIONS[-1]}"

# Weather patterns for each destination
WEATHER_PATTERNS: Dict[str, str] = {
    "skardu": "snowy",  # Only Skardu has snow
    "hunza": "sunny",
    "naran": "partly cloudy",
    "murree": "sunny",
    "swat": "partly cloudy",
    "gilgit": "sunny",
}

# Flexible input parser helpers -------------------------------------------------
def _parse_key_value_string(input_text: str) -> Dict[str, str]:
    """Parse flexible inputs like 'Lahore to Murree', 'Lahore, Murree',
    or JSON-like '{"origin":"Lahore","destination":"Murree"}'.
    Returns a dict with possible keys: origin, destination, mode, days, budget, destination.
    """
    input_text = (input_text or "").strip()
    # Try JSON first
    try:
        import json
        data = json.loads(input_text)
        if isinstance(data, dict):
            return {k: str(v) for k, v in data.items()}
    except Exception:
        pass

    # Try patterns
    lower = input_text.lower()
    if " to " in lower:
        parts = [p.strip() for p in input_text.split(" to ")]
        if len(parts) == 2:
            return {"origin": parts[0], "destination": parts[1]}
    if "," in input_text:
        parts = [p.strip() for p in input_text.split(",")]
        if len(parts) >= 2:
            result = {"origin": parts[0], "destination": parts[1]}
            if len(parts) >= 3:
                result["mode"] = parts[2]
            return result
    return {}

# Distance data from Lahore to destinations
DISTANCES: Dict[tuple, int] = {
    ("Lahore", "Hunza"): 650,
    ("Lahore", "Naran"): 400,
    ("Lahore", "Skardu"): 700,
    ("Lahore", "Murree"): 300,
    ("Lahore", "Swat"): 450,
    ("Lahore", "Gilgit"): 600,
}

# Cost per day for each destination
COSTS_PER_DAY: Dict[str, int] = {
    "hunza": 80,
    "naran": 60,
    "skardu": 70,
    "murree": 40,
    "swat": 50,
    "gilgit": 65,
}

def _validate_destination(destination: str) -> str:
    """Validate that destination is in approved list. Returns error message if invalid, empty string if valid."""
    if destination not in APPROVED_DESTINATIONS:
        return f"Error: {destination} is not an approved destination. Use get_approved_destinations to see available options."
    return ""

@tool
def get_user_location(_: str = "") -> str:
    """Get user's current location. Always returns 'Lahore' in this demo. Pass any string as input (ignored)."""
    # print("\n" + "="*50)
    # print("🤔 HUMAN-IN-THE-LOOP: Location Required")
    # print("="*50)
    # user_location = input("What city are you starting your trip from? Enter your location: ").strip()
    # print(f"📍 Got it! Starting from: {user_location}")
    # print("="*50 + "\n")
    return "Lahore"

@tool
def get_approved_destinations() -> str:
    """Get list of pre-approved destinations from Lahore. Only these destinations can be recommended."""
    destinations = ", ".join(APPROVED_DESTINATIONS)
    return f"Approved destinations from Lahore: {destinations}"

@tool
def get_weather(destination: str) -> str:
    """Get weather information for a pre-approved destination. Only works with approved destinations: Hunza, Naran, Skardu, Murree, Swat, or Gilgit."""
    error = _validate_destination(destination)
    if error:
        return error
    
    weather = WEATHER_PATTERNS.get(destination.lower(), "cloudy")
    print(f"🌤️  Weather in {destination}: {weather}")
    # Keep output minimal and exact so the agent can’t reinterpret it
    return f"Weather in {destination}: {weather}"

# Flexible, decorator-based tools (avoid pydantic parsing issues) --------------

@tool
def calculate_distance(input: str) -> str:
    """Calculate distance. Action Input formats accepted:
    - JSON: {"origin":"Lahore", "destination":"Murree"}
    - Text: "Lahore to Murree" or "Lahore, Murree"
    Returns distance in km.
    """
    data = _parse_key_value_string(input)
    origin = data.get("origin")
    destination = data.get("destination")
    if not origin or not destination:
        return "Error: Provide origin and destination. E.g., {\"origin\":\"Lahore\",\"destination\":\"Murree\"}"
    error = _validate_destination(destination)
    if error:
        return error
    distance = DISTANCES.get((origin, destination))
    if distance is None:
        return f"Error: No distance data for {origin} to {destination}"
    print(f"📏 Distance from {origin} to {destination}: {distance} km")
    return f"{distance} km"


@tool
def get_travel_time(input: str) -> str:
    """Get travel time. Action Input formats accepted:
    - JSON: {"origin":"Lahore", "destination":"Skardu", "mode":"air"}
    - Text: "Lahore, Skardu, air" or "Lahore to Skardu"
    Modes: road (default) or air (only Hunza/Skardu).
    Returns time in hours.
    """
    data = _parse_key_value_string(input)
    origin = data.get("origin")
    destination = data.get("destination")
    mode = (data.get("mode") or "road").lower()
    if not origin or not destination:
        return "Error: Provide origin and destination. E.g., {\"origin\":\"Lahore\",\"destination\":\"Skardu\",\"mode\":\"air\"}"
    error = _validate_destination(destination)
    if error:
        return error
    if mode == "air" and destination.lower() not in ["hunza", "skardu"]:
        return f"Error: Air travel is only available to Hunza and Skardu. {destination} only supports road travel."
    import random as _r
    time_hours = _r.randint(2, 12) if mode == "road" else _r.randint(1, 6)
    print(f"⏱️  Travel time from {origin} to {destination} by {mode}: {time_hours} hours")
    return f"{time_hours} hours"


@tool
def check_budget(input: str) -> str:
    """Check budget affordability. Action Input formats accepted:
    - JSON: {"destination":"Naran","days":3,"budget":400}
    Returns total cost and affordability status.
    """
    data = _parse_key_value_string(input)
    destination = data.get("destination")
    days = data.get("days")
    budget = data.get("budget")
    if not destination or days is None or budget is None:
        return "Error: Provide destination, days, budget. E.g., {\"destination\":\"Naran\",\"days\":3,\"budget\":400}"
    try:
        days_i = int(days)
        budget_f = float(budget)
    except Exception:
        return "Error: days must be int and budget must be number."
    error = _validate_destination(destination)
    if error:
        return error
    cost_per_day = COSTS_PER_DAY.get(destination.lower(), 150)
    total_cost = cost_per_day * days_i
    status = "affordable" if total_cost <= budget_f else "over budget"
    
    return f"Cost: Rs{total_cost} for {days_i} days, {status}"

# ============================================================================
# APPROACH 2: BaseTool Class (Explicit, Type-safe)
# ============================================================================

class CalculateDistanceInput(BaseModel):
    origin: str = Field(description="Starting city name")
    destination: str = Field(description="Destination city name")

class GetTravelTimeInput(BaseModel):
    origin: str = Field(description="Starting city name")
    destination: str = Field(description="Destination city name")
    mode: str = Field(default="road", description="Travel mode: 'road' for driving, 'air' for flying")

class CheckBudgetInput(BaseModel):
    destination: str = Field(description=f"Pre-approved destination: {APPROVED_DESTINATIONS_STR}")
    days: int = Field(description="Number of days for the trip")
    budget: float = Field(description="Available budget in USD")

class CalculateDistanceTool(BaseTool):
    name: str = "calculate_distance"
    description: str = f"Calculate distance between two cities. Use this tool to check if destinations are within your travel range. Only works with: {APPROVED_DESTINATIONS_STR}. Returns distance in km."
    args_schema: Type[BaseModel] = CalculateDistanceInput

    def _run(self, origin: str, destination: str) -> str:
        error = _validate_destination(destination)
        if error:
            return error
        
        distance = DISTANCES.get((origin, destination))
        if not distance:
            return f"Error: No distance data for {origin} to {destination}"
        
        print(f"📏 Distance from {origin} to {destination}: {distance} km")
        return f"{distance} km"


class GetTravelTimeTool(BaseTool):
    name: str = "get_travel_time"
    description: str = f"Get travel time between two cities. Use this tool to check travel duration. Only works with: {APPROVED_DESTINATIONS_STR}. Returns time in hours."
    args_schema: Type[BaseModel] = GetTravelTimeInput

    def _run(self, origin: str, destination: str, mode: str = "road") -> str:
        error = _validate_destination(destination)
        if error:
            return error
        
        # Only Hunza and Skardu allow air travel
        if mode == "air" and destination.lower() not in ["hunza", "skardu"]:
            return f"Error: Air travel is only available to Hunza and Skardu. {destination} only supports road travel."
        
        if mode == "road":
            time_hours = random.randint(2, 12)
        else:  # air (only for Hunza and Skardu)
            time_hours = random.randint(1, 6)
        
        print(f"⏱️  Travel time from {origin} to {destination} by {mode}: {time_hours} hours")
        return f"{time_hours} hours"


class CheckBudgetTool(BaseTool):
    name: str = "check_budget"
    description: str = f"Check budget for pre-approved destinations. Only works with: {APPROVED_DESTINATIONS_STR}. Returns cost and affordability status."
    args_schema: Type[BaseModel] = CheckBudgetInput

    def _run(self, destination: str, days: int, budget: float) -> str:
        error = _validate_destination(destination)
        if error:
            return error
        
        cost_per_day = COSTS_PER_DAY.get(destination.lower(), 150)
        total_cost = cost_per_day * days
        
        affordable = total_cost <= budget
        status = "affordable" if affordable else "over budget"
        
        print(f"💰 Budget check for {destination}: ${total_cost} for {days} days - {status}")
        return f"Cost: ${total_cost} for {days} days, {status}"


def get_travel_tools():
    """Get all travel planning tools - mixing both approaches"""
    return [
        # @tool decorator approach (concise)
        get_user_location,
        get_approved_destinations,
        get_weather,
        # Flexible decorator tools to avoid strict parsing issues
        calculate_distance,
        get_travel_time,
        check_budget,
    ]

