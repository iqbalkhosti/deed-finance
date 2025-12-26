# Deed Finance - Subscription Points Planner

A web application that helps Canadians maximize their credit card rewards to cover subscription costs like Netflix, Spotify, ChatGPT, and more.

## 🎯 Features

- **Credit Card Management** - Add cards from RBC, BMO, TD, CIBC, and Scotiabank with accurate bonus category rates
- **Subscription Tracking** - Track 19+ popular subscriptions including streaming, social media, productivity tools, and AI platforms
- **Smart Spending Advisor** - Get personalized recommendations on which card to use for each spending category
- **Points Calculator** - Calculate how much you need to spend to cover your subscriptions with points
- **Email Verification** - Secure account creation with 6-digit verification codes

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLAlchemy with SQLite
- **Frontend:** Bootstrap 5, Jinja2 Templates
- **Authentication:** Flask-Login, Flask-Bcrypt
- **Deployment:** Vercel (Serverless Python)

## 🚀 Live Demo

[View Live Demo](https://your-vercel-url.vercel.app) <!-- Update with your actual URL -->

## 📸 Screenshots

<!-- Add screenshots here -->

## 🏃 Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/iqbalkhosti/deed-finance.git
   cd deed-finance
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Seed the database**
   ```bash
   python seed_data.py
   ```

5. **Run the application**
   ```bash
   flask run
   ```

6. **Open in browser**
   ```
   http://localhost:5000
   ```

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for sessions | Dev key (change in production) |
| `DEV_MODE` | Email mode (true=console, false=SMTP) | `true` |

## 📊 Supported Credit Cards

- **RBC:** Avion Visa Infinite, Cash Back, ION Visa, ION+ Visa
- **BMO:** CashBack World Elite, Rewards, eclipse Visa Infinite
- **TD:** Cash Back Visa Infinite, Aeroplan, First Class Travel
- **CIBC:** Aeroplan, Dividend, Costco Mastercard
- **Scotiabank:** Gold Amex, Momentum, Scene+ Visa

## 📝 Note

This is a portfolio project and demo application. The SQLite database is ephemeral on Vercel (resets on redeploy). For production use, consider migrating to PostgreSQL.

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

Built with ❤️ by [Iqbal Javed](https://github.com/iqbalkhosti)
