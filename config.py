"""
Configuration file for SOM Monitor
"""
import os
from typing import List

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

INDUSTRY_BRANDS = {
    "telco": [
    "Telekom",          # Deutsche Telekom / Magenta
    "Vodafone",
    "O2",               # Telefónica Germany
    "1&1",
    "Congstar",         # Telekom discount brand
    "Fraenk",           # Telekom digital brand
    "Otelo",            # Vodafone discount brand
    "Freenet Mobile",
    "Aldi Talk",        # O2 network
    "Lidl Connect",     # Vodafone network
    "WinSIM",
    "PremiumSIM"
],
    "ai": ["OpenAI", "Anthropic","Google","Meta","Cohere","Mistral","xAI"]
}

BRANDS_TO_TRACK = INDUSTRY_BRANDS["telco"]

# Models to query
MODELS = {
    "openai": ["gpt-4o", "gpt-4o-mini"]
}

# Query configuration
RUNS_PER_QUERY = 3
TEMPERATURE = 0.7
MAX_TOKENS = 1000
RATE_LIMIT_DELAY = 1  # seconds between requests

# Category settings
ENABLED_CATEGORIES = {
    "general": True,     # Already done, skip it
    "price": True,        # Need to run this
    "network_quality": True,  # Need to run this
    "student": True,  # Skip this
    "business": True,
    "data_heavy": True,
    "prepaid" : True,
    "5g": True,
    "customer_service": True,
    "roaming": True# Skip this
}

#' Query templates by category

# Query templates by category
QUERY_TEMPLATES = {
    "general": [
        "Welcher Mobilfunkanbieter ist am besten in Deutschland?",
        "Welchen Handyvertrag soll ich in Deutschland nehmen?",
        "Was sind die besten Mobilfunkanbieter in Deutschland?",
        "Ich brauche einen neuen Handytarif. Welche Anbieter gibt es?",
        "Which mobile provider should I choose in Germany?",
        "Best mobile network in Germany?",
    ],
    "price": [
        "Welcher ist der günstigste Mobilfunkanbieter in Deutschland?",
        "Wo bekomme ich den billigsten Handytarif?",
        "Ich suche einen günstigen Handyvertrag, welchen Anbieter empfiehlst du?",
        "What's the cheapest mobile plan in Germany?",
        "Günstige Handytarife Deutschland - welcher Anbieter?",
    ],
    "network_quality": [
        "Welcher Anbieter hat das beste Netz in Deutschland?",
        "Wer hat die beste Netzabdeckung in Deutschland?",
        "Which provider has the best network coverage in Germany?",
        "Bestes Mobilfunknetz Deutschland?",
        "Wo ist das 5G-Netz am besten?",
    ],
    "student": [
        "Bester Handytarif für Studenten in Deutschland?",
        "Welcher Mobilfunkanbieter ist gut für Studenten?",
        "Günstiger Handyvertrag für Studenten?",
        "Best mobile plan for students in Germany?",
    ],
    "business": [
        "Welcher Mobilfunkanbieter ist am besten für Geschäftskunden?",
        "Bester Business-Tarif Deutschland?",
        "Mobilfunk für Unternehmen - welcher Anbieter?",
        "Best mobile provider for business in Germany?",
    ],
    "data_heavy": [
        "Welcher Anbieter hat die besten Datentarife?",
        "Ich brauche viel Datenvolumen, welcher Anbieter?",
        "Unlimited data plan Germany - which provider?",
        "Bester Tarif für viel Internet?",
    ],
    "prepaid": [
        "Beste Prepaid-Karte in Deutschland?",
        "Welche Prepaid-Tarife sind empfehlenswert?",
        "Best prepaid SIM card in Germany?",
        "Prepaid ohne Vertrag - welcher Anbieter?",
    ],
    "5g": [
        "Welcher Anbieter hat das beste 5G-Netz?",
        "5G Verfügbarkeit Deutschland - welcher Provider?",
        "Best 5G coverage in Germany?",
        "Wo bekomme ich 5G in Deutschland?",
    ],
    "customer_service": [
        "Welcher Mobilfunkanbieter hat den besten Kundenservice?",
        "Bei welchem Anbieter ist der Support am besten?",
        "Best customer service mobile provider Germany?",
    ],
    "roaming": [
        "Welcher Anbieter hat die besten Roaming-Konditionen?",
        "Günstiges Roaming in Europa - welcher Anbieter?",
        "Best roaming rates Germany?",
    ]
}
# Storage
DATA_DIR = "data"
RESULTS_FILE = "som_results.json"
HISTORY_FILE = "som_history.csv"

# ROI Calculation Assumptions (Configurable per client)
ROI_MARKET_DATA = {
    'default': {
        'total_market_size': 10_000_000_000,  # €10B German mobile market
        'your_market_share': 0.15,  # 15% starting assumption
        'avg_customer_value': 300,  # €300 ARPU annually
        'acquisition_cost': 150,  # €150 CAC
        'ai_search_share': 0.35,  # 35% of searches via AI (growing)
        'conversion_rate': 0.15  # 15% of AI searchers convert
    },
    'Vodafone': {
        'total_market_size': 10_000_000_000,
        'your_market_share': 0.22,  # ~22% market share (second largest)
        'avg_customer_value': 320,  # Higher ARPU
        'acquisition_cost': 160,
        'ai_search_share': 0.35,
        'conversion_rate': 0.15
    },
    'Telekom': {
        'total_market_size': 10_000_000_000,
        'your_market_share': 0.36,  # Market leader ~36%
        'avg_customer_value': 350,  # Highest ARPU (premium brand)
        'acquisition_cost': 180,
        'ai_search_share': 0.35,
        'conversion_rate': 0.15
    },
    'O2': {
        'total_market_size': 10_000_000_000,
        'your_market_share': 0.18,  # ~18% market share
        'avg_customer_value': 280,  # Lower ARPU (value brand)
        'acquisition_cost': 140,
        'ai_search_share': 0.35,
        'conversion_rate': 0.15
    },
    '1&1': {
        'total_market_size': 10_000_000_000,
        'your_market_share': 0.08,  # ~8% market share
        'avg_customer_value': 260,
        'acquisition_cost': 130,
        'ai_search_share': 0.35,
        'conversion_rate': 0.15
    }
}

# Campaign budget assumptions by segment
CAMPAIGN_BUDGETS = {
    'Value Seekers': 300_000,  # €300K
    'Quality Demanders': 400_000,  # €400K (premium)
    'Youth Market': 250_000,  # €250K
    'Enterprise Buyers': 500_000,  # €500K (B2B expensive)
    'Tech Pioneers': 350_000,  # €350K
    'Data Power Users': 300_000,  # €300K
    'Flexibility Seekers': 200_000,  # €200K
    'Service Focused': 300_000,  # €300K
    'Global Travelers': 250_000,  # €250K
    'Mainstream Seekers': 400_000,  # €400K (broad)
}

# Visualization
CHART_COLORS = [
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", 
    "#98D8C8", "#F7DC6F", "#BB8FCE"
]


# Query templates by category
QUERY_TEMPLATES = {
    "general": [
        "Welcher Mobilfunkanbieter ist am besten in Deutschland?",
        "Welchen Handyvertrag soll ich in Deutschland nehmen?",
        "Was sind die besten Mobilfunkanbieter in Deutschland?",
        "Ich brauche einen neuen Handytarif. Welche Anbieter gibt es?",
        "Which mobile provider should I choose in Germany?",
        "Best mobile network in Germany?",
    ],
    "price": [
        "Welcher ist der günstigste Mobilfunkanbieter in Deutschland?",
        "Wo bekomme ich den billigsten Handytarif?",
        "Ich suche einen günstigen Handyvertrag, welchen Anbieter empfiehlst du?",
        "What's the cheapest mobile plan in Germany?",
        "Günstige Handytarife Deutschland - welcher Anbieter?",
    ],
    "network_quality": [
        "Welcher Anbieter hat das beste Netz in Deutschland?",
        "Wer hat die beste Netzabdeckung in Deutschland?",
        "Which provider has the best network coverage in Germany?",
        "Bestes Mobilfunknetz Deutschland?",
        "Wo ist das 5G-Netz am besten?",
    ],
    "student": [
        "Bester Handytarif für Studenten in Deutschland?",
        "Welcher Mobilfunkanbieter ist gut für Studenten?",
        "Günstiger Handyvertrag für Studenten?",
        "Best mobile plan for students in Germany?",
    ],
    "business": [
        "Welcher Mobilfunkanbieter ist am besten für Geschäftskunden?",
        "Bester Business-Tarif Deutschland?",
        "Mobilfunk für Unternehmen - welcher Anbieter?",
        "Best mobile provider for business in Germany?",
    ],
    "data_heavy": [
        "Welcher Anbieter hat die besten Datentarife?",
        "Ich brauche viel Datenvolumen, welcher Anbieter?",
        "Unlimited data plan Germany - which provider?",
        "Bester Tarif für viel Internet?",
    ],
    "prepaid": [
        "Beste Prepaid-Karte in Deutschland?",
        "Welche Prepaid-Tarife sind empfehlenswert?",
        "Best prepaid SIM card in Germany?",
        "Prepaid ohne Vertrag - welcher Anbieter?",
    ],
    "5g": [
        "Welcher Anbieter hat das beste 5G-Netz?",
        "5G Verfügbarkeit Deutschland - welcher Provider?",
        "Best 5G coverage in Germany?",
        "Wo bekomme ich 5G in Deutschland?",
    ],
    "customer_service": [
        "Welcher Mobilfunkanbieter hat den besten Kundenservice?",
        "Bei welchem Anbieter ist der Support am besten?",
        "Best customer service mobile provider Germany?",
    ],
    "roaming": [
        "Welcher Anbieter hat die besten Roaming-Konditionen?",
        "Günstiges Roaming in Europa - welcher Anbieter?",
        "Best roaming rates Germany?",
    ]
}
