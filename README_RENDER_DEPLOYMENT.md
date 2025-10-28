# Deploying Medical Device Litigation Dashboard to Render

## Quick Start (Dashboard Method - Easiest)

### Step 1: Create Render Account
1. Go to: https://render.com/
2. Sign up with GitHub, GitLab, or Google
3. Confirm your email

### Step 2: Deploy via Render Dashboard

#### Option A: Deploy from Git Repository (Recommended)

1. **Push your code to GitHub:**
   ```bash
   cd /Users/praveen/Praveen
   
   # Initialize git if not already done
   git init
   
   # Add files
   git add frontend/ render.yaml .renderignore README_RENDER_DEPLOYMENT.md
   
   # Commit
   git commit -m "Deploy medical device litigation dashboard"
   
   # Create GitHub repo and push
   git remote add origin https://github.com/YOUR_USERNAME/medical-device-litigation-benchmark.git
   git push -u origin main
   ```

2. **Connect to Render:**
   - Go to https://dashboard.render.com/
   - Click "New +" → "Static Site"
   - Connect your GitHub repository
   - Select "medical-device-litigation-benchmark"
   - Render will auto-detect the `render.yaml` configuration
   - Click "Create Static Site"

#### Option B: Deploy via Blueprint (Using render.yaml)

1. Go to: https://dashboard.render.com/
2. Click "New +" → "Blueprint"
3. Connect your repository
4. Render will read `render.yaml` automatically
5. Click "Apply" to deploy

#### Option C: Manual Setup (No Git Required)

1. Go to: https://dashboard.render.com/
2. Click "New +" → "Static Site"
3. Choose "Public Git repository" or connect Git
4. Configure:
   - **Name**: medical-device-litigation-benchmark
   - **Root Directory**: ./
   - **Build Command**: (leave empty)
   - **Publish Directory**: frontend
5. Click "Create Static Site"

### Step 3: Upload Files (If Not Using Git)

If you chose Manual Setup without Git:
1. Render doesn't support direct file uploads
2. You MUST use Git (GitHub, GitLab, or Bitbucket)
3. Follow Option A above to push to GitHub first

## Alternative: Deploy via Render CLI

### Install Render CLI
```bash
# Install via npm
npm install -g @render/cli

# Or via curl
curl https://render.com/install.sh | bash
```

### Login and Deploy
```bash
# Login to Render
render login

# Deploy (will use render.yaml)
render deploy
```

## What Gets Deployed

✅ **Included:**
- `frontend/index.html` - Main dashboard
- `frontend/data/benchmark_cases_data_v48.json` - All 48 cases (1.06 MB)
- All static assets

❌ **Excluded:**
- Python scripts
- Excel files
- Data processing files
- Development files

## Configuration Explained

The `render.yaml` file tells Render:
- **Type**: Static site (no server needed)
- **Publish Path**: `./frontend` (serve from frontend directory)
- **Routes**: SPA routing (all paths go to index.html)
- **Headers**: Cache control for optimal performance

## After Deployment

Render will provide:
- **Public URL**: `https://medical-device-litigation-benchmark.onrender.com`
- **Custom Domain**: Add your own domain (optional)
- **Automatic Deploys**: On every Git push (if using Git)
- **SSL Certificate**: Automatic HTTPS

## Free Tier Limits

✅ **Render Free Tier Includes:**
- 100GB bandwidth/month
- Always-on (no sleeping!)
- Custom domains
- Automatic SSL
- Unlimited sites

⚠️ **Note**: Free tier for static sites has NO sleeping issues (unlike free web services)

## Updating the Dashboard

### If Using Git:
```bash
# Make changes to frontend files
git add .
git commit -m "Update dashboard"
git push

# Render auto-deploys!
```

### Manual Update:
- Push changes to your Git repository
- Render will automatically redeploy

## Custom Domain

1. Go to your site's settings in Render
2. Click "Custom Domain"
3. Add your domain (e.g., mdl-litigation.com)
4. Update your DNS records as instructed
5. Render handles SSL automatically

## Troubleshooting

### Issue: Files not loading
**Fix**: Check `render.yaml` staticPublishPath is correct

### Issue: 404 errors
**Fix**: Ensure routes are configured for SPA (already done in render.yaml)

### Issue: Large file warning
**Status**: 1.06 MB JSON is fine (limit is 100MB per file)

### Issue: Slow initial load
**Fix**: Static sites on Render don't sleep (unlike web services)

## Monitoring

- Dashboard: https://dashboard.render.com/
- Logs: Site → Events tab
- Analytics: Site → Metrics tab
- Builds: Site → Builds tab

## Cost

- **Free Tier**: Perfect for your dashboard
- **Paid Plans**: Start at $7/month (if you need more)

## Support

- Render Docs: https://render.com/docs
- Community: https://community.render.com/
- Support: https://render.com/support

## Comparison: Render vs Vercel

| Feature | Render | Vercel |
|---------|--------|--------|
| **Free Tier** | 100GB bandwidth | 100GB bandwidth |
| **Sleeping** | No sleeping for static sites | Never sleeps |
| **Setup** | Need Git repo | Can deploy directly |
| **Speed** | Fast | Faster (global CDN) |
| **Complexity** | Simple | Very simple |

Both are excellent choices! Render is slightly more traditional, Vercel is optimized for frontend.

## Quick Commands Reference

```bash
# Push to GitHub
git add .
git commit -m "Update dashboard"
git push

# Deploy via Render CLI
render login
render deploy

# Check status
render status
```

## Next Steps

1. Choose deployment method (Git recommended)
2. Push code to GitHub
3. Connect to Render dashboard
4. Deploy automatically via render.yaml
5. Get your public URL
6. Share with colleagues!

Your dashboard will be live at:
`https://medical-device-litigation-benchmark.onrender.com`
