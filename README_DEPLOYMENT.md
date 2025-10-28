# Deploying Medical Device Litigation Dashboard to Vercel

## Prerequisites
1. Install Vercel CLI: `npm install -g vercel`
2. Create a Vercel account at https://vercel.com
3. Login to Vercel: `vercel login`

## Deployment Steps

### Option 1: Deploy via Vercel CLI (Recommended)

```bash
# 1. Navigate to project directory
cd /Users/praveen/Praveen

# 2. Deploy to Vercel (first time)
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Select your account
# - Link to existing project? No
# - Project name? medical-device-litigation-benchmark (or your choice)
# - Directory containing code? ./ (current directory)
# - Override settings? No

# 3. Deploy to production
vercel --prod
```

### Option 2: Deploy via Vercel Dashboard

1. Go to https://vercel.com/new
2. Import your Git repository (GitHub, GitLab, or Bitbucket)
3. Configure project settings:
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: (leave empty)
   - **Output Directory**: `frontend`
4. Click "Deploy"

### Option 3: Deploy via Git Integration (Best for Continuous Deployment)

```bash
# 1. Initialize git repository (if not already)
git init

# 2. Add remote repository
git remote add origin <your-github-repo-url>

# 3. Commit files
git add .
git commit -m "Initial commit - 48 case litigation dashboard"
git push -u origin main

# 4. Connect to Vercel
# - Go to https://vercel.com/new
# - Import your repository
# - Vercel will auto-deploy on every push
```

## Project Structure for Vercel

```
/Users/praveen/Praveen/
├── frontend/
│   ├── index.html              # Main dashboard
│   ├── data/
│   │   └── benchmark_cases_data_v48.json  # 48 cases (1.06 MB)
│   └── styles.css (if separate)
├── vercel.json                 # Vercel configuration
└── .vercelignore              # Files to exclude from deployment
```

## What Gets Deployed

✅ **Included:**
- `frontend/index.html` - Main dashboard
- `frontend/data/benchmark_cases_data_v48.json` - All 48 cases with 324K+ MDRs
- All static assets (CSS, JS embedded in HTML)

❌ **Excluded:**
- Python scripts
- Raw Excel files (*.xlsx)
- Data processing scripts
- Development files

## Post-Deployment

After deployment, Vercel will provide:
- **Production URL**: `https://medical-device-litigation-benchmark.vercel.app` (or similar)
- **Preview URLs**: For each deployment
- **Analytics**: Traffic and performance metrics

## Environment Variables (if needed)

If you need to add environment variables:
```bash
vercel env add API_KEY
```

Or through Vercel Dashboard:
1. Go to Project Settings
2. Navigate to Environment Variables
3. Add variables

## Custom Domain (Optional)

1. Go to your Vercel project
2. Navigate to Settings → Domains
3. Add your custom domain
4. Follow DNS configuration instructions

## Performance Optimization

The dashboard is optimized for Vercel with:
- Static file serving (no server needed)
- JSON data caching (1 hour)
- CDN distribution worldwide
- Automatic HTTPS
- Gzip compression

## Monitoring

Check your deployment at:
- Dashboard: https://vercel.com/dashboard
- Logs: Project → Deployments → Logs
- Analytics: Project → Analytics

## Troubleshooting

**Issue**: 404 on deployment
- **Fix**: Check `vercel.json` routes configuration

**Issue**: Large file size warning (1.06 MB JSON)
- **Status**: Within Vercel limits (25 MB for hobby plan)
- **Note**: Consider data splitting if you exceed limits

**Issue**: Slow loading
- **Fix**: JSON is cached for 1 hour via headers in `vercel.json`

## Cost

- **Hobby Plan**: FREE (includes 100 GB bandwidth)
- **Pro Plan**: $20/month (if you need more bandwidth)

Your 1.06 MB JSON file should work fine on the free tier.

## Updates

To update the dashboard:
```bash
# Make changes to frontend/index.html or data files
vercel --prod
```

Or if using Git integration:
```bash
git add .
git commit -m "Update dashboard with new data"
git push
# Vercel auto-deploys
```

## Support

- Vercel Docs: https://vercel.com/docs
- Vercel Support: https://vercel.com/support
- Community: https://github.com/vercel/vercel/discussions
