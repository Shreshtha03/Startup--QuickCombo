# 🚀 QuickCombo Deployment Guide (24/7 LIVE + 100% FREE)

Follow these exact steps to host your project for free without any credit card.

---

## Option 1: AlwaysData (Best for Persistence)
This is the only service that stays **Live 24/7** without any "sleep" mode on the free tier.

### Step-by-Step Backend Setup:
1. **Register:** Go to [AlwaysData.com](https://www.alwaysdata.com/) and create a **Free Account**.
2. **Create Database:** 
   - Go to **Databases** -> **PostgreSQL** and create a database.
   - Note your **Host**, **DB Name**, **User**, and **Password**.
3. **Web Site Configuration:**
   - Go to **Web** -> **Sites**.
   - Type: **Python WSGI**.
   - Command: `gunicorn quickcombo.wsgi:application`
   - Static directory: `/staticfiles/`
4. **Environment Variables:** Set these in the AlwaysData dashboard or a `.env` file:
   - `DATABASE_URL`: `postgres://USER:PASS@HOST:5432/DB_NAME`
   - `ALLOWED_HOSTS`: `*.alwaysdata.net`

---

## Option 2: Render + Neon + Cronhack (Modern Alternative)
If you prefer a more modern interface, use this combo. It needs a small "hack" to stay awake.

### 1. Database: [Neon.tech](https://neon.tech/)
*   **Sign up** with GitHub (No Card).
*   Create a project and copy the **Connection String** (PostgreSQL URL).

### 2. Backend: [Render.com](https://render.com/)
*   **Sign up** with GitHub (No Card).
*   Create a **New Web Service** and connect your repo.
*   **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`
*   **Start Command:** `gunicorn quickcombo.wsgi:application`
*   **Environment Variables:**
    *   `DATABASE_URL`: (Your Neon.tech URL)
    *   `SECRET_KEY`: (Any random string)
    *   `ALLOWED_HOSTS`: `*.onrender.com`

### 3. Keep Awake Hack (Crucial!)
Render free tier "sleeps" after 15 mins. To keep it **24/7 Live**:
1. Go to [Cron-job.org](https://cron-job.org/) (Free).
2. Create a "Cronjob" that pings your Render URL (e.g., `https://your-app.onrender.com`) every **10 minutes**.
3. This keeps the server "awake" forever.

---

## 3. Frontend: Vercel.com
Vercel is the best place for your Next.js app.

1. **Import** your GitHub repo to Vercel.
2. **Root Directory:** set to `frontend`.
3. **Environment Variables:**
   - `NEXT_PUBLIC_API_URL`: Your Backend URL (AlwaysData or Render)
   - `NEXT_PUBLIC_UPI_ID`: `ayushtomar061004-1@okaxis`
   - `NEXT_PUBLIC_UPI_NAME`: `Ayush Tomar`
4. **Deploy!**

---

### Comparison:
| Feature | AlwaysData | Render + Neon |
| :--- | :--- | :--- |
| **Persistence** | Always On | Needs Cron-job.org |
| **Credit Card** | No | No |
| **Interface** | Basic | Very Modern |
| **Setup Speed** | Medium | Fast |
