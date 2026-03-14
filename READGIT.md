## Git init:
```Bash
 git init
 type nul > .gitignore
```
📁  .gitignore:
```Text
__pycache__/
*.pyc
.env
venv/
.DS_Store
```
```Bash
git add .
git commit -m "Version 0 - Initial FastAPI Docker project"
git status
git log
```