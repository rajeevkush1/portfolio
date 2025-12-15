# Quick Deployment Guide

## Deploy to GitHub Pages (Recommended)

### Step 1: Create GitHub Repository
```bash
cd "r:\ML PROJECTS\rajeevportfolio"
git init
git add .
git commit -m "Initial commit: ML Portfolio"
```

### Step 2: Push to GitHub
```bash
# Create a new repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### Step 3: Enable GitHub Pages
1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under "Source", select **main** branch
4. Click **Save**
5. Your site will be live at: `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME`

---

## Deploy to Netlify (Easiest)

### Method 1: Drag & Drop
1. Go to [netlify.com](https://www.netlify.com/)
2. Sign up/Login
3. Drag the entire `rajeevportfolio` folder to Netlify
4. Done! Your site is live

### Method 2: GitHub Integration
1. Push your code to GitHub (see above)
2. Go to Netlify → **New site from Git**
3. Connect your GitHub repository
4. Click **Deploy site**
5. Get a custom domain: `yourname.netlify.app`

---

## Deploy to Vercel

1. Go to [vercel.com](https://vercel.com/)
2. Sign up with GitHub
3. Click **New Project**
4. Import your repository
5. Click **Deploy**
6. Your site is live at: `yourproject.vercel.app`

---

## Custom Domain (Optional)

### For GitHub Pages:
1. Buy a domain (Namecheap, GoDaddy, etc.)
2. Add a `CNAME` file with your domain name
3. Configure DNS settings in your domain provider
4. Wait for DNS propagation (24-48 hours)

### For Netlify/Vercel:
1. Go to Domain Settings
2. Add your custom domain
3. Follow the DNS configuration instructions
4. Done!

---

## Before Deploying - Checklist

- [ ] Replace placeholder images with real photos
- [ ] Update all personal information
- [ ] Test all links (GitHub, LinkedIn, Kaggle, Instagram)
- [ ] Check responsiveness on mobile
- [ ] Verify all project links work
- [ ] Update meta tags for SEO
- [ ] Test in different browsers

---

## Need Help?

- GitHub Pages: https://pages.github.com/
- Netlify Docs: https://docs.netlify.com/
- Vercel Docs: https://vercel.com/docs
