# GitHub Repository Creator & Migration Tool

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Windows](https://img.shields.io/badge/platform-windows-lightgrey.svg)](https://www.microsoft.com/windows)

A robust, user-friendly CLI tool for creating new Git repositories and migrating existing ones to GitHub. Perfect for developers who need to quickly bootstrap new projects or migrate repositories from other platforms (like Hugging Face) to their personal GitHub accounts.

## ✨ Features

- **🖱️ GUI Folder Selection** - Intuitive folder picker with console fallback
- **🔄 Smart Repository Detection** - Automatically detects existing Git repositories
- **🔗 Intelligent Remote Management** - Keep, replace, or add remote repositories
- **🛡️ Security Handling** - Automatic resolution of Git security issues (dubious ownership)
- **⚠️ Advanced Error Recovery** - Comprehensive error handling with user-friendly solutions
- **📦 Complete Change Detection** - Commits all changes, not just README files
- **🚀 Flexible Push Options** - Handles merge conflicts and force push scenarios
- **💻 Cross-Platform Ready** - Windows batch file included for easy execution

## 🎯 Use Cases

- **New Project Setup** - Initialize a new repository and push to GitHub
- **Repository Migration** - Move projects from Hugging Face, GitLab, or other platforms
- **Remote URL Changes** - Update existing repositories with new remote URLs
- **Bulk Repository Management** - Streamline repetitive Git operations

## 📋 Prerequisites

- **Python 3.6+** installed and available on PATH
- **Git** installed and configured
- **GitHub account** with repository access
- **Authentication setup** (SSH keys or Personal Access Token)

## 🚀 Quick Start

### Method 1: Using the Batch File (Recommended for Windows)

```bash
# Clone the repository
git clone https://github.com/thechampusman/create_github_repo.py.git
cd create_github_repo.py

# Run the tool
.\run_create_repo.bat
```

### Method 2: Direct Python Execution

```bash
# Interactive mode
python create_github_repo.py

# Command line mode
python create_github_repo.py "C:\path\to\project" "https://github.com/user/repo.git"
```

## 📖 Usage Guide

### Interactive Mode

1. **Launch the tool** using one of the methods above
2. **Select target folder** via GUI dialog or enter path manually
3. **Choose repository action:**
   - Keep existing remote (if repository exists)
   - Replace with new remote
   - Set up new remote (for new repositories)
4. **Enter GitHub repository URL** when prompted
5. **Follow guided prompts** for any conflicts or issues

### Command Line Mode

```bash
python create_github_repo.py [target_folder] [remote_url]
```

**Parameters:**
- `target_folder` (optional) - Path to the project directory
- `remote_url` (optional) - GitHub repository URL (HTTPS or SSH)

## 🛠️ Advanced Features

### Automatic Error Resolution

The tool automatically handles common Git issues:

- **Dubious Ownership** - Adds directories to Git safe list
- **Missing User Config** - Interactive setup for Git user credentials
- **Push Rejections** - Options to pull/merge or force push
- **Authentication Errors** - Clear guidance for setup

### Smart Repository Detection

- Detects existing Git repositories
- Identifies current remote configurations
- Offers appropriate actions based on repository state
- Preserves existing work and history

### Comprehensive Change Management

- Scans for all modified files
- Commits all changes with appropriate messages
- Handles large files and LFS objects
- Supports custom commit messages

## 📁 Project Structure

```
create_github_repo/
├── create_github_repo.py      # Main Python script
├── run_create_repo.bat        # Windows batch runner
├── README.md                  # This documentation
└── .gitignore                 # Git ignore rules
```

## 🔧 Configuration

### Git Authentication Setup

**For HTTPS URLs:**
```bash
# Set up Personal Access Token
git config --global credential.helper store
```

**For SSH URLs:**
```bash
# Generate SSH key (if not exists)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to SSH agent
ssh-add ~/.ssh/id_ed25519
```

### Global Git Configuration

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 🚨 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "Git not found" | Install Git and add to PATH |
| "Permission denied" | Set up SSH keys or use HTTPS with token |
| "Dubious ownership" | Tool will automatically fix this |
| "Push rejected" | Tool offers pull/merge or force push options |
| "tkinter not found" | Use command line mode or install tkinter |

### Manual Recovery Commands

If the tool encounters issues, these manual commands may help:

```bash
# Check repository status
git status

# View current remotes
git remote -v

# Force push (use with caution)
git push -f origin main

# Pull with unrelated histories
git pull origin main --allow-unrelated-histories
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### Development Setup

```bash
git clone https://github.com/thechampusman/create_github_repo.py.git
cd create_github_repo.py
# Make your changes
python create_github_repo.py  # Test locally
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Usman** - [@thechampusman](https://github.com/thechampusman)

## 🙏 Acknowledgments

- Built for developers who frequently work with multiple Git platforms
- Inspired by the need for seamless repository migration workflows
- Designed with user experience and error recovery in mind

---

⭐ **Star this repository** if you find it useful!

🐛 **Report issues** on the [GitHub Issues](https://github.com/thechampusman/create_github_repo.py/issues) page.

💡 **Suggest features** or improvements via issues or pull requests.
