# CMSC 398Z - Week 11 - Nov 14th, 2025

## Work in class

We are going to be working on developing a social media app, with features similar to Twitter,
Instagram, Threads or BlueSky. We are going the same social media application twice - first as a Flask monolithic app, then as a REST API + JavaScript frontend - to understand architectural trade-offs. This week we will be focusing on building the Flask app, next week we will work on the version using a
REST API + JavaScript frontend. 

Initially, you just build this as an app you can run locally, and we will start with the bare minimum 
set of features and then allow you to decide what additional features to add. You will be asked to 
pick at least one of a list of additional features to add. 

If you add user authentication, then you can deploy your app to [PythonAnywhere](https://www.pythonanywhere.com) or another hosting provider that allows you to let others see your app running. 
You can use a free account to do this, and it is totally up to you if you want to do this.

To make possible to use github to deploy your app, we have created a 
seperate repository, which contains just the files needed for this project. You can create your 
own github repository, private if you wish, and set that up as an additional remote for the project
repository and push to there.  The project repository is [https://github.com/billpugh/cmsc398z-sma](https://github.com/billpugh/cmsc398z-sma), and you can clone it using the command below (do this somewhere 
not inside the cmsc398z-student-downloads repository or any other repository).

```bash
git clone https://github.com/billpugh/cmsc398z-sma.git
```

We've done a fair bit of testing and tuning of the project for phase1, but have not done full run throughs of phase2, which we will be doing next week, so expect to get some more updates 
before next week for phase 2. 

Once you have cloned the project directory, you can open it in VS Code, and start with the README.md file. You should also open a terminal and start Claude in the project directory (so it will have access to 
all the project files, not just the ones in the phase1 directory). The README.md file will tell you how to proceed.


## Submitting your work

You can submit your work using java -jar submit.jar in the project folder. That will submit the files below. All of them other than REFLECTIONS.md should be updated automatically by Claude as you work on the project.
  * ARCHITECTURE.md
  * phase1/DECISIONS-MADE-phase1.md
  * REFLECTIONS.md
  * any .py or .html files developed for the project
    * Not strictly needed, but useful in case there are any issues with Claude not automatically updating the files above.

Note: due the to way the submit process works, it might submit additional files in your project directory, but the .submitIgnore file instructs it to ignore most of the other files that would generally be found there. If you submit manually by uploading files, the above files are the ones you need to submit.


The work you need to submit is the following:

* Work on implementing the minimum feature set and one additional feature for Phase 1. Submit this ideally by end of class, but no later than Saturday to be considered on-time.
  * This includes ARCHITECTURE.md and phase1/DECISIONS-MADE-phase1.md, which will be completed by Claude as you do your work.
* By Tuesday, noon Tuesday, Nov 18th, edit REFLECTIONS.md with comments about your work on the project
  * If you did any additional work on implementing features, those should be reflected in updated ARCHITECTURE.md and phase1/DECISIONS-MADE-phase1.md files.








