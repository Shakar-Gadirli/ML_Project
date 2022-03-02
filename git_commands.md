# Git cheatsheet

- Pull all changes from master
  `git checkout master`
  `git pull origin master`
- Create new branch and switch to it
  `git checkout -b <BRANCH_NAME>`
- Change branch's name
  `git branch -m <NEW_NAME>`
- Push changes to branch
  `git add .`
  `git commit -m  "Descriptive message"`
  `git push origin <BRANCH_NAME>`
- Add one file at a time
  `git add <FILENAME>`
- Git folder
  `git add <FOLDER_NAME>/*`
- Delete branch
  `git branch -d <BRANCH_NAME>`
- Reset *uncommited*  changes in a file
  `git reset HEAD <FILENAME>`
- Reset all uncommited changes
  `git reset --hard HEAD`
- Reset to the last commit
  `git reset --hard HEAD^`
- Update the list of branches
  `git remote update origin --prune`
- View the list of branches
  `git branch -a`
- See your configuration (creds and settings)
  `git config -l`

Notes:

- Never work in master branch
- Create new branch for each task
- Give branches meaningful names
- Write short commit messages describing what you have done
- If you want to collaborate with someone in one branch, push your changes, then your friend switches to your branch and runs `git pull origin <BRANCH_NAME>`
- After you are done with your task, push your changes and create merge request in Gitlab
- If you have done different things in one branch, commit them separately
- Don't try to push to master, 
