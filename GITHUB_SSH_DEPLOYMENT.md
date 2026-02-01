# GitHub SSH Deployment Commands

## Complete Step-by-Step Guide to Deploy with SSH

### Step 1: Check if you have SSH keys

```powershell
# Check for existing SSH keys
ls ~/.ssh
```

If you see `id_rsa` and `id_rsa.pub` (or `id_ed25519` and `id_ed25519.pub`), you already have SSH keys. Skip to Step 3.

### Step 2: Generate SSH Key (if you don't have one)

```powershell
# Generate new SSH key (use your GitHub email)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Press Enter to accept default location
# Enter a passphrase (optional but recommended)
```

For older systems that don't support Ed25519:
```powershell
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

### Step 3: Start SSH Agent and Add Key

```powershell
# Start SSH agent
Start-Service ssh-agent

# Add your SSH key to the agent
ssh-add ~/.ssh/id_ed25519
# OR if you used RSA:
# ssh-add ~/.ssh/id_rsa
```

### Step 4: Copy SSH Public Key

```powershell
# Copy public key to clipboard
Get-Content ~/.ssh/id_ed25519.pub | Set-Clipboard
# OR for RSA:
# Get-Content ~/.ssh/id_rsa.pub | Set-Clipboard

# Alternatively, display it and copy manually
cat ~/.ssh/id_ed25519.pub
```

### Step 5: Add SSH Key to GitHub

1. Go to GitHub: https://github.com/settings/keys
2. Click **"New SSH key"**
3. Title: `My Windows PC` (or any name you prefer)
4. Key type: **Authentication Key**
5. Paste your public key (from clipboard)
6. Click **"Add SSH key"**

### Step 6: Test SSH Connection

```powershell
# Test GitHub SSH connection
ssh -T git@github.com
```

You should see:
```
Hi YOUR_USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
```

### Step 7: Navigate to Project Directory

```powershell
cd c:\Users\aabha\OneDrive\Pictures\forensic-messenger
```

### Step 8: Initialize Git Repository

```powershell
# Initialize git (if not already done)
git init

# Configure git (replace with your details)
git config user.name "Your Name"
git config user.email "your_email@example.com"

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Complete Forensic Cyber Tech Cloud Messenger implementation

- FastAPI backend with REST + WebSocket APIs
- React + TypeScript frontend with cyber-forensic theme
- Multi-database architecture (PostgreSQL, MongoDB, Redis, Elasticsearch)
- JWT authentication with message encryption (AES-256)
- Real-time messaging with WebSocket and Redis pub/sub
- File upload/download with S3-compatible storage
- Full-text search with Elasticsearch
- Bot and webhook support for integrations
- Docker deployment with docker-compose
- Prometheus metrics and monitoring
- Comprehensive documentation and CI/CD pipeline

Features:
✅ Real-time messaging
✅ Workspace multi-tenancy
✅ Message encryption
✅ Rate limiting
✅ RBAC
✅ Audit logging
✅ OAuth2 support"
```

### Step 9: Create GitHub Repository

**Option A: Using GitHub CLI (if installed)**
```powershell
# Install GitHub CLI if not installed
winget install --id GitHub.cli

# Login to GitHub
gh auth login

# Create repository
gh repo create forensic-messenger --public --source=. --remote=origin --push
```

**Option B: Manual (Web Browser)**
1. Go to https://github.com/new
2. Repository name: `forensic-messenger`
3. Description: `Enterprise-grade Slack alternative with real-time messaging, encryption, and multi-tenancy`
4. Choose: **Public** or **Private**
5. **DO NOT** check any boxes (no README, .gitignore, or license)
6. Click **"Create repository"**

### Step 10: Add Remote and Push (if created manually)

```powershell
# Set main branch
git branch -M main

# Add remote with SSH URL (replace YOUR_USERNAME)
git remote add origin git@github.com:YOUR_USERNAME/forensic-messenger.git

# Verify remote
git remote -v

# Push to GitHub
git push -u origin main
```

### Step 11: Verify Upload

```powershell
# Check repository status
git status

# View remote URL
git remote get-url origin
```

Visit your repository: `https://github.com/YOUR_USERNAME/forensic-messenger`

---

## Quick Commands (All-in-One)

If you already have SSH set up and repository created:

```powershell
cd c:\Users\aabha\OneDrive\Pictures\forensic-messenger
git init
git add .
git commit -m "Initial commit: Complete Forensic Cyber Tech Cloud Messenger"
git branch -M main
git remote add origin git@github.com:YOUR_USERNAME/forensic-messenger.git
git push -u origin main
```

---

## Future Updates

After initial push, to update your repository:

```powershell
# Navigate to project
cd c:\Users\aabha\OneDrive\Pictures\forensic-messenger

# Check status
git status

# Add changes
git add .

# Commit with message
git commit -m "feat: your feature description"

# Push to GitHub
git push
```

---

## Troubleshooting

### Permission Denied (publickey)

```powershell
# Ensure SSH agent is running
Start-Service ssh-agent

# Add key again
ssh-add ~/.ssh/id_ed25519

# Test connection
ssh -T git@github.com
```

### Repository Already Exists

```powershell
# Remove existing remote
git remote remove origin

# Add correct remote
git remote add origin git@github.com:YOUR_USERNAME/forensic-messenger.git

# Push
git push -u origin main
```

### Large Files Error

If you get errors about large files:

```powershell
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.zip"
git lfs track "*.mp4"

# Add .gitattributes
git add .gitattributes
git commit -m "chore: configure Git LFS"
git push
```

---

## Repository Settings (After Upload)

### 1. Add Topics
Go to your repository → Click gear icon next to "About" → Add topics:
- `slack-alternative`
- `real-time-messaging`
- `fastapi`
- `react`
- `typescript`
- `websocket`
- `docker`
- `collaboration-platform`
- `enterprise`
- `cyber-security`

### 2. Enable GitHub Actions
- Go to "Actions" tab
- Click "I understand my workflows, go ahead and enable them"

### 3. Add Repository Secrets (for CI/CD)
Settings → Secrets and variables → Actions → New repository secret:
- `SECRET_KEY` = (generate with: `openssl rand -hex 32`)
- `ENCRYPTION_KEY` = (generate with: `openssl rand -hex 32`)

### 4. Enable Discussions (Optional)
Settings → Features → Check "Discussions"

### 5. Set Branch Protection (Recommended)
Settings → Branches → Add rule for `main`:
- ✅ Require pull request reviews before merging
- ✅ Require status checks to pass before merging

---

## Your Repository is Now Live! 🎉

**Repository URL:** `https://github.com/YOUR_USERNAME/forensic-messenger`

**Clone URL (SSH):** `git@github.com:YOUR_USERNAME/forensic-messenger.git`

**Clone URL (HTTPS):** `https://github.com/YOUR_USERNAME/forensic-messenger.git`

Share your project with the world! 🚀
