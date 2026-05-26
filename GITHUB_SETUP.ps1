# GitHub Setup Script for docx-intelligent-shredder
# This script automates the creation and pushing of the repo to GitHub

param(
    [string]$GithubUsername = "",
    [string]$RepoName = "docx-intelligent-shredder"
)

# Colors for output
$successColor = 'Green'
$errorColor = 'Red'
$infoColor = 'Cyan'

function Write-Info {
    param([string]$Message)
    Write-Host $Message -ForegroundColor $infoColor
}

function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor $successColor
}

function Write-ErrorMsg {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor $errorColor
}

# Step 0: Validate inputs
if (-not $GithubUsername) {
    Write-ErrorMsg "GitHub username is required"
    Write-Host ""
    Write-Host "Usage:"
    Write-Host "  .\GITHUB_SETUP.ps1 -GithubUsername 'your-username'"
    Write-Host ""
    Write-Host "Example:"
    Write-Host "  .\GITHUB_SETUP.ps1 -GithubUsername 'maximecabon'"
    exit 1
}

# Step 1: Check if git is installed
Write-Info "Step 1: Checking if Git is installed..."
try {
    $gitVersion = git --version
    Write-Success "Git found: $gitVersion"
} catch {
    Write-ErrorMsg "Git is not installed. Please install Git from https://git-scm.com"
    exit 1
}

# Step 2: Check if we're in the right directory
Write-Info "Step 2: Verifying directory structure..."
if (-not (Test-Path "README.md")) {
    Write-ErrorMsg "README.md not found. Please run this script from the repo root directory."
    exit 1
}
Write-Success "Directory structure verified"

# Step 3: Initialize git repo locally
Write-Info "Step 3: Initializing local Git repository..."
if (Test-Path ".git") {
    Write-Host "  .git directory already exists. Skipping init."
} else {
    git init
    Write-Success "Local repository initialized"
}

# Step 4: Add all files
Write-Info "Step 4: Adding files to Git..."
git add .
Write-Success "Files staged"

# Step 5: Initial commit
Write-Info "Step 5: Creating initial commit..."
$commitMessage = "Initial commit: docx-intelligent-shredder v1.0.0`n`nSmart Word document preprocessing tool with intelligent chunking, section extraction, and content preparation for AI pipelines."
git commit -m $commitMessage
Write-Success "Initial commit created"

# Step 6: Set branch to main
Write-Info "Step 6: Setting default branch to main..."
git branch -M main
Write-Success "Branch renamed to main"

# Step 7: Add remote
Write-Info "Step 7: Adding GitHub remote..."
$remoteUrl = "https://github.com/$GithubUsername/$RepoName.git"
git remote remove origin 2>$null  # Remove if exists
git remote add origin $remoteUrl
Write-Success "Remote added: $remoteUrl"

# Step 8: Instructions for next steps
Write-Host ""
Write-Host "=" * 70
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "=" * 70
Write-Host ""
Write-Host "1. CREATE the repository on GitHub (if not already done):"
Write-Host "   → Go to https://github.com/new"
Write-Host "   → Repository name: $RepoName"
Write-Host "   → DO NOT initialize with README, .gitignore, or LICENSE"
Write-Host "   → Click 'Create repository'"
Write-Host ""
Write-Host "2. PUSH to GitHub:"
Write-Host "   Run this command:"
Write-Host ""
Write-Host "   git push -u origin main"
Write-Host ""
Write-Host "3. VERIFY on GitHub:"
Write-Host "   → Go to https://github.com/$GithubUsername/$RepoName"
Write-Host "   → You should see all files"
Write-Host ""
Write-Host "=" * 70
Write-Host ""

# Step 9: Ask if user wants to push now
Write-Host "Ready to push? Make sure the repo exists on GitHub first." -ForegroundColor Yellow
Write-Host "Press Enter to push, or Ctrl+C to cancel..."
Read-Host

Write-Info "Step 9: Pushing to GitHub..."
try {
    git push -u origin main
    Write-Success "Successfully pushed to GitHub!"
    Write-Host ""
    Write-Success "Your repo is live at: https://github.com/$GithubUsername/$RepoName"
} catch {
    Write-ErrorMsg "Push failed. Make sure:"
    Write-Host "  - The repository exists on GitHub"
    Write-Host "  - You have GitHub CLI configured or SSH keys set up"
    Write-Host "  - Run: git push -u origin main"
    exit 1
}
