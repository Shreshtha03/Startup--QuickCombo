# QuickCombo Deployment Guide (TRULY FREE + NO CARD)

Follow these steps for 24/7 hosting with **Zero Credit Card Required**.

## 1. Backend & Database (AlwaysData.com)
AlwaysData is a premium French hosting service that stays live for life on their free tier.
1. Go to [AlwaysData.com](https://www.alwaysdata.com/) and register for a **Free Account** (Hobby plan).
2. **No Credit Card Required.**
3. In the dashboard, go to **Web** -> **Sites** and add a new "Python WSGI" site.
4. Go to **Databases** -> **PostgreSQL** and create a new database.
5. You will get a host (e.g. `postgresql-ayuxhx06.alwaysdata.net`).
6. This will be your `DATABASE_URL`.

## 2. Frontend (Vercel.com)
1. Go to [Vercel.com](https://vercel.com/) and connect your GitHub.
2. Select the `frontend` directory.
3. **No Credit Card Required** for the Hobby plan.
4. Add environment variables:
   - `NEXT_PUBLIC_API_URL`: (Your AlwaysData site URL, e.g. `https://ayuxhx06.alwaysdata.net`)
   - `NEXT_PUBLIC_UPI_ID`: `ayushtomar061004-1@okaxis`
   - `NEXT_PUBLIC_UPI_NAME`: `Ayush Tomar`
5. Deploy!

---

### Why this setup?
- **AlwaysData:** Unlike Koyeb, they don't ask for a card for the free tier. Your server stays live 24/7.
- **Vercel:** Best for your Next.js app, extremely fast and card-free.

I've updated the code (`settings.py`) to work perfectly with this setup. Just push the code and follow these two sites!
