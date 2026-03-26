# QuickCombo Full Deployment Process (End-to-End)

This guide provides the complete, step-by-step process to deploy your QuickCombo project to production for free. We will use **AlwaysData** for the Django Backend, **Neon.tech** for the PostgreSQL Database, and **Vercel** for the Next.js Frontend.

---

## Step 1: Prepare Your Code
1. Ensure all your latest code is saved and pushed to your **GitHub** repository.
2. Make sure you have a `requirements.txt` file in your main backend folder. If missing, generate it by running: `pip freeze > requirements.txt` on your local machine.

---

## Step 2: Set Up the Database (Neon.tech)
1. Go to [Neon.tech](https://neon.tech/) and sign up using your GitHub account.
2. Click **Create Project**, and name the project (e.g., `quickcombo-db`).
3. Select **Postgres** and use the standard options (Free Tier).
4. Go to your **Dashboard**. Under connection details, copy your **Connection String**.
   *(It will look something like this: `postgresql://user:password@endpoint.neon.tech/dbname?sslmode=require`)*
5. **Save this URL somewhere safe**, you will need it for the backend.

---

## Step 3: Deploy Backend (AlwaysData)
*AlwaysData provides reliable, free hosting that runs 24/7.*

1. **Create an Account:**
   - Go to [AlwaysData.com](https://www.alwaysdata.com/) and register for a free account.
2. **Access Web Terminal:**
   - In your AlwaysData dashboard, go to **Remote Access** -> **SSH** (enable it if it's off).
   - Click to open the **Web Terminal**.
3. **Clone Your Code:**
   - Type the following commands in the terminal to download your code:
     ```bash
     cd www/
     git clone <YOUR_GITHUB_REPO_URL> quickcombo_backend
     cd quickcombo_backend
     ```
4. **Create a Virtual Environment & Install Dependencies:**
   - Run these commands one by one:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     pip install gunicorn psycopg2-binary dj-database-url whitenoise
     ```
5. **Add Environment Variables:**
   - In the AlwaysData Dashboard, go to **Environment Variables**.
   - Add the following Keys and Values:
     - `DATABASE_URL`: *(Paste your Neon.tech Connection String here)*
     - `SECRET_KEY`: `any-secure-random-string`
     - `DEBUG`: `False`
     - `ALLOWED_HOSTS`: `<your-alwaysdata-username>.alwaysdata.net`
     - `CORS_ALLOWED_ORIGINS`: `https://your-frontend-domain.vercel.app` *(You can update the actual value in Step 5)*
     - Add any other keys you use (e.g., `BREVO_API_KEY`, `GEOAPIFY_KEY`, `ADMIN_EMAIL`).
6. **Migrate Database & Collect Static Files:**
   - Go back to the Web Terminal (make sure `venv` is active).
   - Run:
     ```bash
     python manage.py migrate
     python manage.py collectstatic --noinput
     ```
7. **Configure the Website on AlwaysData:**
   - In the dashboard, go to **Web** -> **Sites**.
   - Edit the default site (or click **Add a new site**).
   - **Addresses:** `<your-username>.alwaysdata.net`
   - **Type:** **Python WSGI**
   - **Command:** `gunicorn quickcombo.wsgi:application`
   - **Working directory:** `/www/quickcombo_backend/`
   - **Virtualenv directory:** `/www/quickcombo_backend/venv/`
   - Expand the **Static files** section:
     - **URL path:** `/static/`
     - **Directory path:** `/www/quickcombo_backend/staticfiles/`
   - Click **Submit**.

*Your backend is now live! Remember your backend URL (e.g., `https://ayushtomar.alwaysdata.net`).*

---

## Step 4: Deploy Frontend (Vercel)
1. Go to [Vercel.com](https://vercel.com/) and log in with GitHub.
2. Click **Add New** -> **Project**.
3. Find your `QuickCombo` GitHub repository and click **Import**.
4. **Configure the Project:**
   - **Framework Preset:** Next.js
   - **Root Directory:** Click Edit, select your `frontend` folder, and save.
5. **Set Environment Variables:**
   - Under Environment Variables, add:
     - `NEXT_PUBLIC_API_URL`: `<YOUR_ALWAYS_DATA_BACKEND_URL>` *(Make sure there is NO slash at the end, e.g., `https://ayushtomar.alwaysdata.net`)*
     - `NEXT_PUBLIC_UPI_ID`: `ayushtomar061004-1@okaxis`
     - `NEXT_PUBLIC_UPI_NAME`: `Ayush Tomar`
6. Click **Deploy**. Vercel will install your frontend and give you a live URL.

---

## Step 5: Final Connection setup
1. Once Vercel finishes, go to your new Vercel Dashboard and copy your **live frontend URL** (e.g., `https://quickcombo.vercel.app`).
2. **Update Backend CORS Configuration:**
   - Go back to your AlwaysData Dashboard -> **Environment Variables**.
   - Edit `CORS_ALLOWED_ORIGINS` and set it exactly to your Vercel URL (e.g., `https://quickcombo.vercel.app`).
   - Go to **Web** -> **Sites** and restart your site (click the restart icon).

---

🎉 **Congratulations! Your application is successfully deployed and running 24/7!**
