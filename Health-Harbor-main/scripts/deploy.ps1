# Health Harbor - Quick Deploy Script
# ====================================

Write-Host "🚀 Health Harbor Deployment Helper" -ForegroundColor Cyan
Write-Host "====================================`n" -ForegroundColor Cyan

# Check if in correct directory
$currentPath = Get-Location
if (!(Test-Path "vitalplunder")) {
    Write-Host "❌ Error: Please run this script from the Health-Harbor-main folder" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Deploying from: $currentPath`n" -ForegroundColor Green

# Step 1: Check Git
Write-Host "📦 Step 1: Checking Git..." -ForegroundColor Yellow
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git is not installed. Please install Git first." -ForegroundColor Red
    Write-Host "   Download from: https://git-scm.com/download/win" -ForegroundColor Gray
    exit 1
}
Write-Host "✅ Git is installed`n" -ForegroundColor Green

# Step 2: Initialize Git (if needed)
if (!(Test-Path ".git")) {
    Write-Host "📦 Step 2: Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git repository initialized`n" -ForegroundColor Green
} else {
    Write-Host "✅ Git repository already exists`n" -ForegroundColor Green
}

# Step 3: Add files
Write-Host "📦 Step 3: Adding files to Git..." -ForegroundColor Yellow
git add .
Write-Host "✅ Files added`n" -ForegroundColor Green

# Step 4: Commit
Write-Host "📦 Step 4: Committing changes..." -ForegroundColor Yellow
$commitMessage = Read-Host "Enter commit message (or press Enter for default)"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Initial deployment - Health Harbor"
}
git commit -m "$commitMessage"
Write-Host "✅ Changes committed`n" -ForegroundColor Green

# Step 5: GitHub remote
Write-Host "📦 Step 5: Configure GitHub remote..." -ForegroundColor Yellow
$githubUser = Read-Host "Enter your GitHub username"
$repoName = Read-Host "Enter repository name (default: health-harbor)"
if ([string]::IsNullOrWhiteSpace($repoName)) {
    $repoName = "health-harbor"
}

$remoteUrl = "https://github.com/$githubUser/$repoName.git"

# Check if remote already exists
$existingRemote = git remote get-url origin 2>$null
if ($existingRemote) {
    Write-Host "⚠️  Remote 'origin' already exists: $existingRemote" -ForegroundColor Yellow
    $updateRemote = Read-Host "Update to new URL? (y/n)"
    if ($updateRemote -eq 'y') {
        git remote set-url origin $remoteUrl
        Write-Host "✅ Remote updated`n" -ForegroundColor Green
    }
} else {
    git remote add origin $remoteUrl
    Write-Host "✅ Remote added`n" -ForegroundColor Green
}

# Step 6: Push
Write-Host "📦 Step 6: Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "⚠️  Make sure you've created the repository on GitHub first!" -ForegroundColor Yellow
Write-Host "   Create it at: https://github.com/new" -ForegroundColor Gray
$pushNow = Read-Host "Ready to push? (y/n)"
if ($pushNow -eq 'y') {
    git branch -M main
    git push -u origin main
    Write-Host "✅ Pushed to GitHub!`n" -ForegroundColor Green
} else {
    Write-Host "⏭️  Skipping push. You can do it later with: git push -u origin main`n" -ForegroundColor Yellow
}

# Step 7: Next steps
Write-Host "`n🎉 Git setup complete!" -ForegroundColor Green
Write-Host "`n📋 Next Steps:" -ForegroundColor Cyan
Write-Host "=============`n" -ForegroundColor Cyan

Write-Host "1. Backend Deployment (Render):" -ForegroundColor Yellow
Write-Host "   → Go to: https://render.com/" -ForegroundColor Gray
Write-Host "   → Click 'New +' → 'Web Service'" -ForegroundColor Gray
Write-Host "   → Connect your GitHub repo" -ForegroundColor Gray
Write-Host "   → Root directory: vitalplunder/backend" -ForegroundColor Gray
Write-Host "   → Add environment variables from .env file" -ForegroundColor Gray
Write-Host ""

Write-Host "2. Frontend Deployment (Vercel):" -ForegroundColor Yellow
Write-Host "   → Go to: https://vercel.com/" -ForegroundColor Gray
Write-Host "   → Click 'Add New...' → 'Project'" -ForegroundColor Gray
Write-Host "   → Import your GitHub repo" -ForegroundColor Gray
Write-Host "   → Root directory: vitalplunder/frontend" -ForegroundColor Gray
Write-Host "   → Add VITE_API_BASE_URL environment variable" -ForegroundColor Gray
Write-Host ""

Write-Host "3. Read full deployment guide:" -ForegroundColor Yellow
Write-Host "   → DEPLOYMENT.md" -ForegroundColor Gray
Write-Host "   → DEPLOYMENT_CHECKLIST.md" -ForegroundColor Gray
Write-Host ""

Write-Host "✨ Your code is ready for deployment!" -ForegroundColor Green
Write-Host ""
