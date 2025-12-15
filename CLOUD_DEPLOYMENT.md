# ☁️ Cloud Deployment Guide - Production Ready

## 🎉 Your Portfolio is Running Locally in Docker!

**Container Status:** ✅ Running  
**Local URL:** http://localhost:8080  
**Container Name:** rajeev-portfolio  
**Image:** rajeev-portfolio:latest  

---

## 🚀 Part 2: Deploy to Cloud (Production)

Now let's deploy your Dockerized portfolio to the cloud for production use!

---

## Option 1: Deploy to Docker Hub (Recommended First Step)

### Why Docker Hub?
- ✅ **Free** for public repositories
- ✅ **Easy** to share your image
- ✅ **Required** for most cloud deployments
- ✅ **Professional** - shows DevOps skills

### Steps:

#### 1. Create Docker Hub Account
- Go to: https://hub.docker.com/signup
- Create free account
- Verify email

#### 2. Login to Docker Hub
```bash
docker login
# Enter your Docker Hub username and password
```

#### 3. Tag Your Image
```bash
docker tag rajeev-portfolio:latest rajeevkush1/portfolio:latest
```

#### 4. Push to Docker Hub
```bash
docker push rajeevkush1/portfolio:latest
```

#### 5. Your Image is Now Public!
**Anyone can run your portfolio with:**
```bash
docker run -d -p 8080:80 rajeevkush1/portfolio:latest
```

---

## Option 2: Deploy to Google Cloud Run (Easiest Cloud)

### Why Cloud Run?
- ✅ **Serverless** - Auto-scales from 0 to infinity
- ✅ **Pay-per-use** - Free tier: 2 million requests/month
- ✅ **Fast** - Deploys in 2 minutes
- ✅ **HTTPS** - Automatic SSL certificate
- ✅ **Custom Domain** - Free

### Prerequisites:
- Google Cloud account (free $300 credit)
- gcloud CLI installed

### Deploy Commands:

```bash
# 1. Login to Google Cloud
gcloud auth login

# 2. Set project
gcloud config set project YOUR_PROJECT_ID

# 3. Build and deploy (one command!)
gcloud run deploy portfolio \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 80

# Your site will be live at:
# https://portfolio-XXXXX-uc.a.run.app
```

### Cost:
- **Free tier:** 2M requests, 360K GB-seconds/month
- **After free tier:** ~$0.40 per million requests
- **Your portfolio:** Likely FREE forever!

---

## Option 3: Deploy to AWS ECS (Enterprise)

### Why AWS ECS?
- ✅ **Enterprise-grade** - Used by Fortune 500
- ✅ **Scalable** - Handle millions of users
- ✅ **Integrated** - Works with all AWS services
- ✅ **Professional** - Great for resume

### Prerequisites:
- AWS account
- AWS CLI installed
- ECR repository created

### Deploy Steps:

#### 1. Create ECR Repository
```bash
aws ecr create-repository --repository-name portfolio
```

#### 2. Login to ECR
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
```

#### 3. Tag and Push
```bash
docker tag rajeev-portfolio:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/portfolio:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/portfolio:latest
```

#### 4. Create ECS Task Definition
```json
{
  "family": "portfolio",
  "containerDefinitions": [{
    "name": "portfolio",
    "image": "YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/portfolio:latest",
    "portMappings": [{
      "containerPort": 80,
      "protocol": "tcp"
    }],
    "memory": 512,
    "cpu": 256
  }]
}
```

#### 5. Create ECS Service
```bash
aws ecs create-service \
  --cluster default \
  --service-name portfolio \
  --task-definition portfolio \
  --desired-count 1 \
  --launch-type FARGATE
```

### Cost:
- **Fargate:** ~$15-30/month for 24/7 uptime
- **EC2:** ~$5-10/month (requires more setup)

---

## Option 4: Deploy to Azure Container Instances

### Why Azure?
- ✅ **Simple** - Easiest container deployment
- ✅ **Fast** - Deploy in seconds
- ✅ **Cheap** - Pay only when running
- ✅ **Microsoft** - Great for enterprise

### Deploy Commands:

```bash
# 1. Login to Azure
az login

# 2. Create resource group
az group create --name portfolio-rg --location eastus

# 3. Create container
az container create \
  --resource-group portfolio-rg \
  --name rajeev-portfolio \
  --image rajeevkush1/portfolio:latest \
  --dns-name-label rajeev-portfolio \
  --ports 80

# Your site will be live at:
# http://rajeev-portfolio.eastus.azurecontainer.io
```

### Cost:
- **~$0.0000125/second** when running
- **~$30/month** for 24/7 uptime
- **Free tier:** $200 credit for new accounts

---

## Option 5: Deploy to DigitalOcean App Platform

### Why DigitalOcean?
- ✅ **Developer-friendly** - Simple UI
- ✅ **Affordable** - $5/month for basic apps
- ✅ **Fast** - Global CDN included
- ✅ **Auto-deploy** - GitHub integration

### Deploy Steps:

#### 1. Via Web Interface:
1. Go to: https://cloud.digitalocean.com/apps
2. Click "Create App"
3. Connect GitHub repository
4. Select "Dockerfile" as source
5. Click "Deploy"

#### 2. Via CLI:
```bash
# Install doctl
# Then:
doctl apps create --spec .do/app.yaml
```

### Cost:
- **Basic:** $5/month
- **Professional:** $12/month
- **Includes:** SSL, CDN, auto-scaling

---

## Option 6: Deploy to Heroku

### Why Heroku?
- ✅ **Classic** - Been around forever
- ✅ **Simple** - Git push to deploy
- ✅ **Free tier** - Good for testing
- ✅ **Add-ons** - Easy to extend

### Deploy Commands:

```bash
# 1. Login to Heroku
heroku login

# 2. Create app
heroku create rajeev-portfolio

# 3. Set stack to container
heroku stack:set container

# 4. Deploy
git push heroku main

# Your site will be live at:
# https://rajeev-portfolio.herokuapp.com
```

### Cost:
- **Free tier:** 550-1000 dyno hours/month
- **Hobby:** $7/month
- **Note:** Free tier sleeps after 30 min inactivity

---

## 🎯 Recommended Deployment Strategy

### For Your Portfolio:

**Phase 1: Free Hosting (Start Here)**
1. ✅ **GitHub Pages** - Free, easy, perfect for portfolios
   - URL: `https://rajeevkush1.github.io/portfolio/`
   - Cost: $0
   - Setup time: 5 minutes

**Phase 2: Docker Hub (Show DevOps Skills)**
2. ✅ **Push to Docker Hub** - Shows you know containers
   - URL: `hub.docker.com/r/rajeevkush1/portfolio`
   - Cost: $0
   - Setup time: 10 minutes

**Phase 3: Cloud Deployment (Optional)**
3. ⚡ **Google Cloud Run** - If you want custom domain
   - URL: `https://portfolio.rajeevkushwaha.com`
   - Cost: $0 (free tier)
   - Setup time: 15 minutes

---

## 💰 Cost Comparison

| Platform | Free Tier | Monthly Cost | Best For |
|----------|-----------|--------------|----------|
| **GitHub Pages** | ✅ Unlimited | $0 | Portfolios |
| **Docker Hub** | ✅ 1 private repo | $0 | Sharing images |
| **Google Cloud Run** | ✅ 2M requests | $0-5 | Serverless apps |
| **AWS ECS** | ❌ No | $15-30 | Enterprise |
| **Azure ACI** | ✅ $200 credit | $30 | Microsoft stack |
| **DigitalOcean** | ❌ No | $5-12 | Simple apps |
| **Heroku** | ✅ Limited | $0-7 | Quick prototypes |

---

## 🎯 My Recommendation for You

### Best Setup:
1. **GitHub Pages** - For your live portfolio (FREE)
2. **Docker Hub** - To show container skills (FREE)
3. **Local Docker** - For testing changes (FREE)

### Why This Combo?
- ✅ **$0 total cost**
- ✅ **Professional** - Shows multiple skills
- ✅ **Reliable** - GitHub Pages is very stable
- ✅ **Fast** - CDN included
- ✅ **Resume-worthy** - Docker + GitHub + DevOps

---

## 📋 Quick Deploy Checklist

### Docker Hub Deployment:
```bash
# 1. Login
docker login

# 2. Tag
docker tag rajeev-portfolio:latest rajeevkush1/portfolio:latest

# 3. Push
docker push rajeevkush1/portfolio:latest

# 4. Done! Share this:
# docker run -d -p 8080:80 rajeevkush1/portfolio:latest
```

### GitHub Pages (Already Done):
- ✅ Code pushed to GitHub
- ⏳ Enable Pages in settings
- ✅ Live at: `rajeevkush1.github.io/portfolio`

---

## 🚀 Next Steps

**Right Now:**
1. ✅ Portfolio running locally in Docker
2. ⏳ Push Docker image to Docker Hub
3. ⏳ Enable GitHub Pages for free hosting

**Later (Optional):**
- Deploy to Google Cloud Run for custom domain
- Add CI/CD pipeline
- Set up monitoring

---

## 💡 Pro Tips

### 1. Auto-Deploy with GitHub Actions
Create `.github/workflows/docker.yml`:
```yaml
name: Docker Build and Push

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and push
        run: |
          docker build -t rajeevkush1/portfolio:latest .
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u rajeevkush1 --password-stdin
          docker push rajeevkush1/portfolio:latest
```

### 2. Add Health Monitoring
Use UptimeRobot (free) to monitor your site:
- https://uptimerobot.com
- Get alerts if site goes down
- Free for 50 monitors

### 3. Custom Domain
Buy domain ($10/year) and point to:
- GitHub Pages: CNAME record
- Cloud Run: Custom domain mapping
- CloudFlare: Free CDN + SSL

---

## 🎉 Summary

**Your Portfolio Status:**
- ✅ **Local Docker:** Running at http://localhost:8080
- ✅ **GitHub:** Code pushed
- ✅ **Production Ready:** Can deploy anywhere
- ✅ **Professional:** Shows DevOps skills

**Deployment Options:**
- **Free:** GitHub Pages + Docker Hub
- **Cheap:** Google Cloud Run ($0-5/month)
- **Enterprise:** AWS ECS ($15-30/month)

**Recommended:**
1. Enable GitHub Pages (free hosting)
2. Push to Docker Hub (show skills)
3. Keep local Docker for testing

---

**Created:** December 16, 2025, 3:45 AM IST  
**Status:** ✅ Docker Running Locally!  
**Next:** Deploy to Cloud! ☁️
