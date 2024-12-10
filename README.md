# Scalping Bot for Index CFDs on IG

This project is a Python-based scalping bot designed to trade index CFDs (e.g., GER30) on the IG trading platform. The bot leverages a moving average crossover strategy, incorporates robust risk management, and features a real-time monitoring dashboard.

## Features
- **Trading Logic**:
  - Scalps index CFDs using short and long moving average crossovers.
  - Supports stop-loss and take-profit for every trade.
- **Risk Management**:
  - Adjustable risk percentage per trade.
  - Daily loss limit to control potential losses.
- **Monitoring Interface**:
  - Real-time dashboard displaying trade history and cumulative P&L.
  - Visualizes P&L over time using charts.
- **Integration with IG**:
  - Uses IG's REST API for trading and WebSocket for real-time price data.

## Prerequisites
- Python 3.8 or higher.
- IG trading account with API access (use the demo environment for testing).
- Required Python libraries (see Installation).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/scalping-bot.git
   cd scalping-bot
  ```
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root with the following:
   ```plaintext
   IG_API_KEY=your_api_key
   IG_USERNAME=your_username
   IG_PASSWORD=your_password
  ```

5. Customize `config.json` to configure trading parameters:
   ```json
   {
       "symbol": "CS.D.DAX.FD.MAR.IP",
       "short_moving_average_period": 5,
       "long_moving_average_period": 20,
       "risk_percentage_per_trade": 1,
       "stop_loss_points": 10,
       "take_profit_points": 20,
       "daily_loss_limit": 5
   }

## Usage
1. **Start the bot**:
   ```bash
   python ig_scalping_bot.py
   ```
2. **Access the dashboard**:
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser to view:
   - Total P&L.
   - Trade history.
   - P&L chart.

3. **Stop the bot**:
   Press `CTRL+C` in the terminal.

## Dashboard Features
- **Real-Time Monitoring**:
  - View active trades and historical performance.
- **Cumulative P&L Chart**:
  - Visualize your performance over time.
- **Trade Details**:
  - View entry/exit prices, timestamps, and P&L for each trade.

## Example Trade Data
| Timestamp           | Symbol       | Action | Entry Price | Exit Price | PnL   |
|---------------------|--------------|--------|-------------|------------|-------|
| 2024-12-09 10:30:00 | GER30        | BUY    | 15600       | 15620      | +20.0 |
| 2024-12-09 10:45:00 | GER30        | SELL   | 15620       | 15600      | -20.0 |

## Customization
- Modify trading logic by editing the `scalping_strategy` function in `ig_scalping_bot.py`.
- Adjust risk parameters in the `config.json` file.
- Customize the Flask dashboard in `templates/dashboard.html`.


## Limitations
- The bot is designed for educational and testing purposes. Use it on a demo account first.
- Requires consistent internet connection for real-time trading and data streaming.
- Scalping strategies can result in frequent small losses or gains; adjust risk parameters accordingly.


## Future Enhancements
- Add support for multiple symbols.
- Integrate advanced technical indicators (e.g., RSI, Bollinger Bands).
- Implement more robust error handling and retries for API requests.

## License
This project is open-source under the MIT License.

## Disclaimer
Trading CFDs involves significant risk and may not be suitable for all investors. The bot is provided as-is, and the developers are not responsible for any financial losses incurred.
```

This is formatted as a complete Markdown file and ready for use. Let me know if you need any further modifications!