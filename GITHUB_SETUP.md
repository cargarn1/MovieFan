# GitHub Setup Instructions

## Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `MovieFan` (or your preferred name)
3. Description: "Movie Recommendation & Social Platform API with Zapier Integration"
4. Choose **Public** or **Private**
5. **DO NOT** check:
   - ❌ Add a README file
   - ❌ Add .gitignore
   - ❌ Choose a license
6. Click **"Create repository"**

## Step 2: Connect Local Repository to GitHub

After creating the repository, run these commands:

```bash
# Add the remote repository (replace MovieFan with your repo name if different)
git remote add origin https://github.com/cargarn1/MovieFan.git

# Or if you prefer SSH:
# git remote add origin git@github.com:cargarn1/MovieFan.git

# Rename default branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Alternative: One-liner Setup

If you've already created the repo on GitHub:

```bash
git remote add origin https://github.com/cargarn1/MovieFan.git && \
git branch -M main && \
git push -u origin main
```

## Troubleshooting

### If you get authentication errors:
- Use GitHub CLI: `gh auth login`
- Or use SSH keys instead of HTTPS
- Or use a Personal Access Token

### If you need to change the remote URL:
```bash
git remote set-url origin https://github.com/cargarn1/MovieFan.git
```

### To verify remote is set correctly:
```bash
git remote -v
```



