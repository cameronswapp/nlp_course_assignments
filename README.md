# Course Assignments for Intro to NLP
Assignments associated with DSAI 5810/6810 Fall 2025 Intro to NLP.

## Setup Instructions


1. First fork this repo ("Create New Fork"). 

<img src="images/Screenshot%202025-08-22%20at%208.40.27%E2%80%AFPM.png" alt="drawing" width="200"/>

Forking this main repo will create your own copy of the repo, under your username. Any work you do should go to this new copy
and NOT the original main repo I have created (or else you'll be pushing your assignment work for all to see.)

2. Make sure your forked repo is private. 

I believe this is the default.

3. Add me (Matt) as a contributor. Username is `goodwin-matt`. Send me the repo link as well to make sure I can view it.

That way I can view your assignments and comment as needed.

4. git clone the repo

Run on command line (terminal in mac, powershell in windows) `git clone [URL of the your personal repo copy (click the "Code" dropdown and copy the https address)]`
This will now take your forked repo and pull it down on to your machine.

You now have on your computer what you need to get started.


## Syncing with the original repo
Occasionally, throughout the semester I'll push up new assignments to the original nlp_courese_assignments repo. 
This will require you to then pull those changes to your forked repo. To get those updates:

Add upstream original repo. Only need to do this once. URL should be the HTTPS URL of the original repo.
```commandline
git remote add upstream [URL_of_original_repo (see the Code dropdown again, and select the https address)]
```

Fetch latest updates
```commandline
git fetch upstream
```

Finally, make sure to be on your main branch (git checkout main) and merge in the latest from the original repo.
```commandline
git checkout main
git merge upstream/main
```

## Submitting an Assignment
When submitting an assignment, make a PR and add me as a reviewer.

To do this for each assignment:
- Create a new branch. Do your assignment on this branch.
- While on the new branch, once you add or edit a file and you feel good about the changes, run `git add [file_name]`
- Then run `git commit -m "write a commit message here"`
- Then run `git push` to push your local changes to the remote repo (Github). These changes will be on the branch you created.

Then when you've submitted all of your changes, go to the branch on Github and create a Pull Request and add me as a reviewer.
I'll review your PR and then you can merge your PR into main.

Some other helpful git commands:
- `git status`: see the current status from gits perspective
- `git diff [file_name]`: see what changes you will be adding and committing.