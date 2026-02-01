# Automated GitHub Deployment Script
# For user: 24mcsdf001@student.rru.ac.in

Write-Host "🚀 Forensic Cyber Tech Cloud Messenger - Automated GitHub Deployment" -ForegroundColor Cyan
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host ""

$email = "24mcsdf001@student.rru.ac.in"
$projectPath = "c:\Users\aabha\OneDrive\Pictures\forensic-messenger"

# Navigate to project
Set-Location $projectPath
Write-Host "📁 Working directory: $projectPath" -ForegroundColor Green
Write-Host ""

# Configure Git
Write-Host "⚙️  Configuring Git..." -ForegroundColor Yellow
git config user.email $email
Write-Host "  ✓ Email set to: $email" -ForegroundColor Green

Write-Host ""
Write-Host "📝 Please enter your name (e.g., 'John Doe'):" -ForegroundColor Yellow
$userName = Read-Host
git config user.name $userName
Write-Host "  ✓ Name set to: $userName" -ForegroundColor Green
Write-Host ""

# Initialize Git if needed
if (!(Test-Path ".git")) {
    Write-Host "🔧 Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "  ✓ Git initialized" -ForegroundColor Green
} else {
    Write-Host "  ℹ️  Git already initialized" -ForegroundColor Cyan
}
Write-Host ""

# Update documentation with actual username
Write-Host "📝 Please enter your GitHub username:" -ForegroundColor Yellow
$githubUsername = Read-Host

Write-Host ""
Write-Host "📝 Updating documentation..." -ForegroundColor Yellow
$files = @("README.md", "CONTRIBUTING.md", "GITHUB_DEPLOYMENT.md")
foreach ($file in $files) {
    if (Test-Path $file) {
        (Get-Content $file) -replace 'YOUR_USERNAME', $githubUsername | Set-Content $file
        Write-Host "  ✓ Updated $file" -ForegroundColor Green
    }
}
Write-Host ""

# Add all files
Write-Host "📦 Adding files to Git..." -ForegroundColor Yellow
git add .
Write-Host "  ✓ All files staged" -ForegroundColor Green
Write-Host ""

# Create commit
Write-Host "💾 Creating commit..." -ForegroundColor Yellow
$commitMessage = @"
Initial commit: Complete Forensic Cyber Tech Cloud Messenger

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
✅ OAuth2 support
"@

git commit -m $commitMessage
Write-Host "  ✓ Commit created" -ForegroundColor Green
Write-Host ""

# Set main branch
Write-Host "🌿 Setting main branch..." -ForegroundColor Yellow
git branch -M main
Write-Host "  ✓ Main branch set" -ForegroundColor Green
Write-Host ""

# Check for existing remote
$existingRemote = git remote get-url origin 2>$null
if ($existingRemote) {
    Write-Host "  ⚠️  Remote 'origin' already exists: $existingRemote" -ForegroundColor Yellow
    Write-Host "  Removing old remote..." -ForegroundColor Yellow
    git remote remove origin
}

# Add remote
$repoUrl = "git@github.com:$githubUsername/forensic-messenger.git"
Write-Host "🔗 Adding remote repository..." -ForegroundColor Yellow
git remote add origin $repoUrl
Write-Host "  ✓ Remote added: $repoUrl" -ForegroundColor Green
Write-Host ""

# Display next steps
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host "✅ Git repository is configured and ready!" -ForegroundColor Green
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔑 NEXT STEPS - You need to complete these manually:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1️⃣  CREATE GITHUB REPOSITORY" -ForegroundColor Cyan
Write-Host "   Go to: https://github.com/new" -ForegroundColor White
Write-Host "   Repository name: forensic-messenger" -ForegroundColor White
Write-Host "   Description: Enterprise-grade Slack alternative with real-time messaging" -ForegroundColor White
Write-Host "   Visibility: Public or Private (your choice)" -ForegroundColor White
Write-Host "   ⚠️  DO NOT initialize with README, .gitignore, or license" -ForegroundColor Yellow
Write-Host ""

Write-Host "2️⃣  SET UP SSH KEY (if not already done)" -ForegroundColor Cyan
Write-Host "   Run these commands:" -ForegroundColor White
Write-Host "   ssh-keygen -t ed25519 -C `"$email`"" -ForegroundColor Gray
Write-Host "   Start-Service ssh-agent" -ForegroundColor Gray
Write-Host "   ssh-add ~/.ssh/id_ed25519" -ForegroundColor Gray
Write-Host "   Get-Content ~/.ssh/id_ed25519.pub | Set-Clipboard" -ForegroundColor Gray
Write-Host ""
Write-Host "   Then add the key to GitHub:" -ForegroundColor White
Write-Host "   https://github.com/settings/keys" -ForegroundColor Cyan
Write-Host ""

Write-Host "3️⃣  TEST SSH CONNECTION" -ForegroundColor Cyan
Write-Host "   ssh -T git@github.com" -ForegroundColor Gray
Write-Host ""

Write-Host "4️⃣  PUSH TO GITHUB" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host ""

Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host "📋 Quick Command Summary:" -ForegroundColor Yellow
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "# If you need to set up SSH:" -ForegroundColor White
Write-Host "ssh-keygen -t ed25519 -C `"$email`"" -ForegroundColor Cyan
Write-Host "Start-Service ssh-agent" -ForegroundColor Cyan
Write-Host "ssh-add ~/.ssh/id_ed25519" -ForegroundColor Cyan
Write-Host "Get-Content ~/.ssh/id_ed25519.pub | Set-Clipboard" -ForegroundColor Cyan
Write-Host "# Then add key at: https://github.com/settings/keys" -ForegroundColor Gray
Write-Host ""
Write-Host "# Test SSH:" -ForegroundColor White
Write-Host "ssh -T git@github.com" -ForegroundColor Cyan
Write-Host ""
Write-Host "# Push to GitHub:" -ForegroundColor White
Write-Host "git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host "🎯 Your repository will be live at:" -ForegroundColor Green
Write-Host "https://github.com/$githubUsername/forensic-messenger" -ForegroundColor Cyan
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host ""

# Ask if user wants to push now
Write-Host "Would you like to try pushing to GitHub now? (y/n)" -ForegroundColor Yellow
$response = Read-Host

if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host ""
    Write-Host "🚀 Attempting to push to GitHub..." -ForegroundColor Yellow
    Write-Host ""
    
    try {
        git push -u origin main
        Write-Host ""
        Write-Host "====================================================================" -ForegroundColor Green
        Write-Host "🎉 SUCCESS! Your project is now on GitHub!" -ForegroundColor Green
        Write-Host "====================================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "View your repository at:" -ForegroundColor White
        Write-Host "https://github.com/$githubUsername/forensic-messenger" -ForegroundColor Cyan
        Write-Host ""
    } catch {
        Write-Host ""
        Write-Host "====================================================================" -ForegroundColor Red
        Write-Host "⚠️  Push failed. Please complete the SSH setup first." -ForegroundColor Yellow
        Write-Host "====================================================================" -ForegroundColor Red
        Write-Host ""
        Write-Host "Follow the steps above to:" -ForegroundColor White
        Write-Host "1. Create the repository on GitHub" -ForegroundColor White
        Write-Host "2. Set up SSH key" -ForegroundColor White
        Write-Host "3. Try pushing again with: git push -u origin main" -ForegroundColor Cyan
        Write-Host ""
    }
} else {
    Write-Host ""
    Write-Host "No problem! When you're ready, run:" -ForegroundColor White
    Write-Host "git push -u origin main" -ForegroundColor Cyan
    Write-Host ""
}
