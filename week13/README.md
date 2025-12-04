# CMSC 398Z - Week 13 - Dec 5th, 2025

## Submitting your work for this project

You just need to submit docs/LEARNINGS-WEEK1.md from the directory where you worked with Claude to the submit server. We are only asking you to submit that one file, not everything in the directory, so you just upload that file to the [submit server](https://submit.cs.umd.edu/fall2025/view/instructor/projectUtilities.jsp?projectPK=119) for project 13.


## Work in class

We are going to have you work on getting quuly running within codespaces, and then understanding portions of the quuly. This is a big project. Most of it is going to involve you trying to understand quuly and doing a code review, but we also want you to see it running so you can experience how it works from the perspective of a TA. The goals of this weeks lesson are described in [GOAL-WEEK1.md](GOAL-WEEK1.md). We are going to continue working on quuly for our final class next week. 

We have a set of very specific learning objectives for this week. You could also use this project as a starting point for learning about other aspects of building a
large web service. You do not need to study these, but you are welcome (and encouraged) to do so if you have free time after completing the learning objectives for the week
 - **Concept A: GraphQL vs REST** - How the API differs from FastAPI
- **Concept B: Go Language** - Reading Go code if you're unfamiliar
- **Concept C: Redis and Real-Time** - Deeper dive into pub/sub
- **Concept D: Docker** - How the containers are configured

Ideally, you will be able to copy a quuly repository on gitlab.cs.umd.edu into a private github repository, and then be able to get quuly running in a Codespaces virtual machine created from that repository. If you don't have a github account, or have significant problems getting this to work, you can still complete the work for the project. If you do have issues with setting up codespaces, you can just get a local copy of the repository and get it running locally. However, this may require installing quite a number of pieces of software on your local machine (we are using codespaces to let you avoid doing this). 

Alternatively, you can also just get a copy of the repository on your local machine and just use Claude to help you understand it, without actually running it. If you don't get it running, you should pair with another student who gets it running just so you can see how it works from the perspective of a TA, and then you can work on trying to understand the code by having Claude help you understand it. 

There are two ways to get your code into a private github repository:

### Direct import into github

I was able to get this working with gitlab.cs.umd.edu, using my umd login name and a gitlab.cs.umd.edu access token. I haven't tried it using ssh authentication for gitlab.cs.umd.edu.

* Go to https://github.com/new/import
  * Provide https://gitlab.cs.umd.edu/cmsc398z-fall25/quuly-codespaces.git as the URL for your source repository
  * provide your gitlab.cs.umd.edu user name and access token
  * Name your repository, something like quuly or quuly-codespaces
  * **mark the repository as private** -- IMPORTANT
  * Hit the "Begin Import" button

### Using a local bridge

#### Step 1
Make a local copy. If you are using https authentication:
```bash
git clone https://gitlab.cs.umd.edu/cmsc398z-fall25/quuly-codespaces.git
cd quuly-codespaces
```

If you are using ssh authentication:
```bash
git clone git@gitlab.cs.umd.edu:cmsc398z-fall25/quuly-codespaces.git
cd quuly-codespaces
```

#### Step 2: Create the Destination Repository

* Go to github.com and create a new repository
* **IMPORTANT: Select Private.** 
* Do not initialize with a README or license.
* Copy the URL of this new empty repository.
* Within the quuly-codespaces project you checked out from gitlab.cs.umd.edu, do:

#### Step 3: Switch remotes and push

```bash
# 1. Rename the original UMD remote to 'upstream' (so you can pull updates later)
git remote rename origin upstream

# 2. Add your new GitHub repo as 'origin'
git remote add origin [YOUR_GITHUB_REPO_URL]

# 3. Push the code to your new private GitHub repo
git push -u origin main
```

### Create codespaces

Now that you have imported a copy of the quuly repository, refresh the page on github.com.

Click the green Code button.

Select the Codespaces tab and click Create codespace on main.

### Open your codespace within VS Code

While you can open your codespace within a browser, the configuration files for quuly need to know the name of the host it is running on so that web links can be directed appropriately. When you run Codespaces within VS Code, it can provide automatic port forwarding so that it can just run as localhost, so you won't need to change anything to the long github.dev URLs that codespace provides.

Your steps:
* Install the [codespaces plugin](https://marketplace.visualstudio.com/items?itemName=GitHub.codespaces) for VS Code
* Type command-shift-P to open the all commands window
* Type codespaces
* Select Codespaces: Connect to Codespace...
* Select your Codespace

### Starting claude in Codespaces

Once you have opened your codespace within VS Code, you should open a terminal window in VS Code and then type `claude`. That will start claude within the codespaces environment, which means it will have direct access to the commands, database and other components of your running application when you get it running.

When you first start claude, it will ask you to authenticate. You will need to do this to get claude access inside of codespaces.

Once claude is running, tell it `walk me through @docs/LESSON_PLAN.md`. An overview of the lesson plan is in [GOAL-WEEK1.md](GOAL-WEEK1.md).





