# GitHub Deployment Instructions

Follow these steps to deploy your Forensic Cyber Tech Cloud Messenger to GitHub:

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `forensic-messenger` (or your preferred name)
3. Description: "Enterprise-grade Slack alternative with real-time messaging, encryption, and multi-tenancy"
4. Choose: **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Initialize Git Repository

Open PowerShell/Terminal in your project directory:

```powershell
cd c:\Users\aabha\OneDrive\Pictures\forensic-messenger

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Complete Forensic Cyber Tech Cloud Messenger implementation"
```

## Step 3: Connect to GitHub

Replace `YOUR_USERNAME` with your actual GitHub username:

```powershell
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/forensic-messenger.git

# Verify remote
git remote -v
```

## Step 4: Push to GitHub

```powershell
# Push to main branch
git branch -M main
git push -u origin main
```

## Step 5: Configure Repository Settings

### Enable GitHub Actions

1. Go to your repository on GitHub
2. Click "Actions" tab
3. Enable workflows if prompted
4. The CI/CD pipeline will run automatically on push

### Add Repository Secrets

For CI/CD to work, add these secrets:

1. Go to Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add the following secrets:

```
SECRET_KEY=your-secret-key-for-testing
ENCRYPTION_KEY=your-encryption-key-32-chars
```

### Enable GitHub Pages (Optional)

If you want to host documentation:

1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: main, folder: /docs
4. Save

## Step 6: Add Topics and Description

1. Go to your repository main page
2. Click the gear icon next to "About"
3. Add description: "Enterprise-grade Slack alternative with real-time messaging, encryption, and multi-tenancy"
4. Add topics: `slack-alternative`, `real-time-messaging`, `fastapi`, `react`, `typescript`, `websocket`, `docker`, `collaboration-platform`
5. Save changes

## Step 7: Create Release (Optional)

```powershell
# Create a tag
git tag -a v1.0.0 -m "Release v1.0.0: Initial production-ready release"

# Push tag
git push origin v1.0.0
```

Then on GitHub:
1. Go to Releases
2. Click "Create a new release"
3. Choose tag: v1.0.0
4. Release title: "v1.0.0 - Initial Release"
5. Describe features and changes
6. Click "Publish release"

## Step 8: Update README with Your Repository URL

Update these files with your actual GitHub username:

1. `README.md` - Replace repository URL placeholders
2. `CONTRIBUTING.md` - Replace repository URL placeholders

```powershell
# Quick find and replace (PowerShell)
$files = @("README.md", "CONTRIBUTING.md")
foreach ($file in $files) {
    (Get-Content $file) -replace 'YOUR_USERNAME', 'your-actual-username' | Set-Content $file
}

# Commit the changes
git add README.md CONTRIBUTING.md
git commit -m "docs: update repository URLs"
git push
```

## Step 9: Verify Deployment

Check that everything is working:

- [ ] Repository is visible on GitHub
- [ ] All files are uploaded
- [ ] README displays correctly
- [ ] GitHub Actions workflow runs successfully
- [ ] License is recognized
- [ ] Topics are displayed

## Step 10: Share Your Project

Your repository is now live! Share it:

```
https://github.com/YOUR_USERNAME/forensic-messenger
```

## Continuous Deployment

Every time you push changes:

```powershell
git add .
git commit -m "feat: your feature description"
git push
```

The CI/CD pipeline will automatically:
1. Run backend tests
2. Build frontend
3. Build Docker images
4. Run security scans

## Troubleshooting

### Authentication Issues

If you have authentication problems:

```powershell
# Use GitHub CLI
gh auth login

# Or use Personal Access Token
# Generate at: https://github.com/settings/tokens
# Use token as password when pushing
```

### Large Files

If you have files larger than 100MB:

```powershell
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.mp4"
git lfs track "*.zip"

# Commit .gitattributes
git add .gitattributes
git commit -m "chore: configure Git LFS"
```

## Next Steps

1. **Enable Dependabot**: Settings → Security → Dependabot
2. **Add Branch Protection**: Settings → Branches → Add rule for `main`
3. **Set up Discussions**: Settings → Features → Discussions
4. **Add Wiki**: Document architecture and usage
5. **Create Issues Templates**: .github/ISSUE_TEMPLATE/

---

**Your project is now on GitHub!** 🎉

Repository: `https://github.com/YOUR_USERNAME/forensic-messenger`
