import os
import time
import requests
import pandas as pd
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import matplotlib.pyplot as plt

# Load environment variables
load_dotenv()

# IG API credentials
IG_API_URL = "https://demo-api.ig.com/gateway/deal"
IG_API_KEY = os.getenv("IG_API_KEY")
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")

# Initialize Flask app
app = Flask(__name__)

# Global variables for monitoring
trade_data = pd.DataFrame(columns=["Timestamp", "Symbol", "Action", "Entry Price", "Exit Price", "PnL"])
total_pnl = 0

# Configuration
CONFIG = {
    "symbol": "CS.D.DAX.FD.MAR.IP",  # Example for GER30
    "short_moving_average_period": 5,
    "long_moving_average_period": 20,
    "risk_percentage_per_trade": 1,
    "stop_loss_points": 10,
    "take_profit_points": 20,
    "daily_loss_limit": 5,
    "polling_interval": 10  # In seconds
}

# Authentication
def authenticate():
    headers = {
        "X-IG-API-KEY": IG_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "identifier": IG_USERNAME,
        "password": IG_PASSWORD
    }
    response = requests.post(f"{IG_API_URL}/session", json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["oauthToken"]
    else:
        raise Exception("Authentication failed.")

# Fetch price data
def fetch_price_data(symbol):
    response = requests.get(f"{IG_API_URL}/markets/{symbol}", headers={
        "X-IG-API-KEY": IG_API_KEY
    })
    if response.status_code == 200:
        return response.json()["prices"]
    else:
        raise Exception("Failed to fetch price data.")

# Calculate moving averages
def calculate_moving_averages(prices, short_period, long_period):
    prices["SMA_Short"] = prices["closePrice"].rolling(window=short_period).mean()
    prices["SMA_Long"] = prices["closePrice"].rolling(window=long_period).mean()
    return prices

# Place a trade
def place_trade(symbol, size, direction):
    global trade_data, total_pnl
    entry_price = fetch_price_data(symbol)["closePrice"]
    exit_price = entry_price + CONFIG["take_profit_points"] if direction == "BUY" else entry_price - CONFIG["stop_loss_points"]
    pnl = (exit_price - entry_price) * size if direction == "BUY" else (entry_price - exit_price) * size

    # Update trade data
    trade_data = trade_data.append({
        "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "Symbol": symbol,
        "Action": direction,
        "Entry Price": entry_price,
        "Exit Price": exit_price,
        "PnL": pnl
    }, ignore_index=True)

    total_pnl += pnl
    print(f"Trade placed: {direction} {size} on {symbol}. PnL: {pnl}")

# Scalping logic
def scalping_strategy():
    prices = fetch_price_data(CONFIG["symbol"])
    prices = calculate_moving_averages(prices, CONFIG["short_moving_average_period"], CONFIG["long_moving_average_period"])

    # Check for crossover
    if prices["SMA_Short"].iloc[-1] > prices["SMA_Long"].iloc[-1]:
        place_trade(CONFIG["symbol"], 1, "BUY")
    elif prices["SMA_Short"].iloc[-1] < prices["SMA_Long"].iloc[-1]:
        place_trade(CONFIG["symbol"], 1, "SELL")

# Flask monitoring interface
@app.route("/")
def dashboard():
    return render_template("dashboard.html", total_pnl=total_pnl, trades=trade_data.to_dict(orient="records"))

@app.route("/historical")
def historical():
    return jsonify(trade_data.to_dict(orient="records"))

@app.route("/pnl_chart")
def pnl_chart():
    plt.figure(figsize=(10, 6))
    plt.plot(trade_data["Timestamp"], trade_data["PnL"].cumsum(), marker="o")
    plt.title("Cumulative P&L Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Cumulative P&L")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/pnl_chart.png")
    return jsonify({"status": "Chart updated"})

# Main loop
if __name__ == "__main__":
    auth_token = authenticate()
    print("Bot authenticated and running...")

    # Run the bot in a separate thread
    while True:
        try:
            scalping_strategy()
            time.sleep(CONFIG["polling_interval"])
        except KeyboardInterrupt:
            print("Bot stopped.")
            break

    # Start Flask app
    app.run(debug=True)
