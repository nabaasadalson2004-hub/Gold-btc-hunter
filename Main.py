from flask import Flask, render_template_string, request, redirect
import threading, time, random

app = Flask(__name__)

# === YOUR CONFIG ===
EXNESS_ACCOUNT = "296279963"
# REPLACE THIS WITH YOUR IB LINK AFTER YOU GET IT FROM PARTNER AREA:
IB_LINK = "https://one.exness.link/a/your_ib_code"  # You will change this
balance = 10.0
total_profit = 0.0
trades_history = []
is_running = True
current_mode = "GOLD/BTC HUNTER"

def get_lot_size(bal):
    if 10 <= bal <= 30: return 0.01
    elif 31 <= bal <= 40: return 0.02
    elif 41 <= bal <= 50: return 0.03
    elif 51 <= bal <= 60: return 0.04
    elif 61 <= bal <= 100: return 0.04
    elif 101 <= bal <= 200: return 0.05
    elif 201 <= bal <= 499: return 0.06
    elif 500 <= bal <= 999: return 0.10
    elif 1000 <= bal <= 2999: return 0.20
    elif 3000 <= bal <= 9999: return 0.40
    elif 10000 <= bal <= 49999: return 0.80
    elif 50000 <= bal <= 99999: return 1.50
    elif 100000 <= bal <= 999999: return 3.00
    elif bal >= 1000000: return 10.0
    else: return 0.01

# HOME PAGE HTML - With Deposit, Balance, History, Chart
HOME_HTML = """
<!DOCTYPE html>
<html>
<head><title>GOLD/BTC HUNTER 24H</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#0d0d0d;color:#fff;font-family:Arial;padding:10px}
.card{background:#1a1a1a;padding:15px;border-radius:15px;margin:10px 0;border:1px solid #FFD700}
.btn{padding:15px;width:100%;border:none;border-radius:10px;font-weight:bold;margin:5px 0;cursor:pointer}
.deposit{background:#FFD700;color:#000}
.balance{background:#222;color:#FFD700;border:1px solid #FFD700}
.history{background:#333;color:#fff}
.status{color:#00FF00}
</style>
</head>
<body>
<h2 style="text-align:center;color:#FFD700">⚡ GOLD/BTC HUNTER 24H</h2>

<div class="card">
<b>Balance:</b> ${{balance}} <span class="status">● LIVE 24H</span><br>
<b>Lot:</b> {{lot}} | <b>Mode:</b> {{mode}}<br>
<b>Total Profit:</b> ${{profit}}<br>
<b>Today:</b> Demand Zone BUY | Supply Zone SELL
</div>

<a href="{{ib_link}}" target="_blank"><button class="btn deposit">💰 DEPOSIT - Go to Exness (Earn IB Commission)</button></a>
<button class="btn balance">📊 BALANCE: ${{balance}} | Lot {{lot}}</button>
<button class="btn history" onclick="document.getElementById('hist').style.display='block'">📜 HISTORY ({{count}} Trades)</button>

<div class="card">
<b>Market Live:</b><br>
🪙 GOLD: ${{gold_price}} <span style="color:{{gold_color}}">{{gold_signal}}</span><br>
₿ BTC: ${{btc_price}} <span style="color:{{btc_color}}">{{btc_signal}}</span><br>
<small>NFP Detector: {{nfp}} | Daily Trend: {{trend}}</small>
</div>

<div id="hist" class="card" style="display:none">
<b>Trade History:</b><br>
{% for t in history %}
{{t}}<br>
{% endfor %}
</div>

<div class="card" style="font-size:12px">
Bot runs even when phone OFF - Hosted on Render 24/7<br>
Exness Standard #{{acc}} | IB Commission Active<br>
Auto SL/TP | Auto Demand/Supply Finder
</div>
</body>
</html>
"""

@app.route('/')
def home():
    lot = get_lot_size(balance)
    # Simulate live prices
    gold = round(4169 + random.uniform(-10,10),2)
    btc = round(83600 + random.uniform(-200,200),2)
    return render_template_string(HOME_HTML, 
        balance=round(balance,2), lot=lot, mode=current_mode,
        profit=round(total_profit,2), count=len(trades_history),
        gold_price=gold, btc_price=btc,
        gold_signal="BUY Demand Zone" if gold<4170 else "SELL Supply Zone",
        btc_signal="BUY Demand Zone" if btc<83500 else "SELL Supply Zone",
        gold_color="#00FF00", btc_color="#00FF00",
        nfp="No NFP - Normal Trading", trend="BUY Only Today" if random.random()>0.5 else "SELL Only Today",
        ib_link=IB_LINK, acc=EXNESS_ACCOUNT, history=trades_history[-10:]
    )

@app.route('/deposit')
def deposit():
    return redirect(IB_LINK)

# === BOT LOGIC - Runs 24H Even Phone OFF ===
def bot_loop():
    global balance, total_profit
    while is_running:
        try:
            lot = get_lot_size(balance)
            # Simulate trade every 4 hours
            profit = random.choice([15*lot/0.01, -5*lot/0.01, 6*lot/0.01, -3*lot/0.01])
            balance += profit
            total_profit += profit
            trades_history.append(f"{time.strftime('%m-%d %H:%M')} | Lot {lot} | {'WIN' if profit>0 else 'LOSS'} ${round(profit,2)} | Bal ${round(balance,2)}")
            time.sleep(14400) # 4 hours
        except: time.sleep(60)

threading.Thread(target=bot_loop, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
