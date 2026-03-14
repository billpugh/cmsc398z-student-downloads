---
marp: true
paginate: true
---

# A Mini-Course to Get CS Students Up to Speed: Effective use of AI Coding Tools: CMSC 398z

## Bill Pugh, Univ. of Maryland
### In 2012, promoted myself to Emeritus Professor of Computer Science

### Presentation for AICSEPAR 2026
### Course web page: https://www.cs.umd.edu/class/fall2025/cmsc398z
### Git repository: https://github.com/billpugh/cmsc398z-student-downloads

---


# We *need* to be having a much bigger conversation

AI coding tools are going to fundamentally change how software gets developed. 
* Maybe by just *a lot*, maybe by *much more* than that. 

We need to understand where the puck is if we want to have any hope of understanding where it might go

Skills often not covered/required in the CS undergraduate curriculum will be essential for students to get software development internships or jobs.
* Not just "How to use AI tools"
* *See next talk*: [What do professional software developers need to know to succeed](https://dl.acm.org/doi/10.1145/3696630.3727251) ...

I'm looking forward to many conversations on this topic at this workshop, and in follow up conversations.

---


![bg fit](experienceIt.jpg)

---


# I'm not suggesting we can stop teaching coding

I've become pretty good at using AI coding tools
* I no longer type source code, or even review it
* I now work at a higher level of abstraction
  * Claude has typed 30,000 lines of python, 2,500 lines of rust over the past month for me on a side project
* Over 53+ years of coding, I've internalized a lot of concepts about software design, algorithms and software architecture
  
I don't know if coding without AI tools is important to learning those concepts 

---
# Back to our originally scheduled presentation  

CMSC 398z: A 1 credit course for Fall 2025 that I decided to offer in June

Started trying to get up to speed myself starting in May

No committee approval needed. 2 hour lab sessions each Friday, no coding expected outside of class

Course goals: try to help student see what AI coding tools were capable of, and what teaching that to students would be like

By great fortune, Derek Willis, an instructor from the Journalism school, already somewhat proficient in use of AI for data and analytics reporting, contacted me about my course and I talked him into being a co-instructor

  
---

# Materials in my class are already out of date

If I taught the same course again this semester, I would want to significantly revise them due to changes in what AI models can do now

Bigger changes needed will be appropriate by next fall

Happy to provide the materials in my class

The goals of what I did in the class and non-AI topics we covered are still largely appropriate 
* python, json, schemas, noisy data, non-deterministic processing, verifying results
* Getting AI tools to work as tutors rather than answer machines


---
# This is moving so damn fast

* Discussions I had at Google and Microsoft in May 25 were out of date by beginning of semester
  * Even course title was out of date
  * Smart autocomplete no longer interesting/relevant
* September: Claude Sonnet 4.5 was a huge step up in capability
* Late November: Claude Opus 4.5 another huge step up. Some professional software developers starting using it to write 90-99% of their code
* February 26: Claude Opus 4.6 and OpenAI Codex 5.3 were another leap forward
* By next Fall 2026: ???
* By Spring 2030: ?????

---
# Course Goals

* Get students familiar with the kinds of programming tasks AI coding tools excel at
  * No assumption that students knew Python, Databases, json, etc
* Get them access to several different coding models
  * Initially, GitHub for education, free for students
  * Considered several other options for agentic AI tools, settled on Claude
  * Told students they should just plan to spend $20/month for 2 months to get access
    * Students can get free access by attending Claude Builders club meeting on campus

---

# Learning Python and using agents - 3 weeks / 6 hours

* Provided `.github/copilot-instructions.md` intended to stop AI from just giving answers
  * Autocomplete in VSCode+Copilot ignores `copilot-instructions.md`
  * would often complete functions just from function name
  * had to disable autocomplete
* Finding and utilizing libraries is a core talent of AI coding tools
* Playing Wordle
  * extension: Wordle helper
* Markov Text Generation
* Poker hand analysis
  * extension: What are my chances of winning with these hole cards
  
---

# csv, dataFrames, json, pydantic, noisy/bad data

* week 4
* Analyze foreclosure data
* Gave them a large file of foreclosure data
* Data was noisy/bad. 
  * Missing zip codes
  * apartment numbers coded inconsistently
  * Some entries had fields that looked like noise
* Use AI tools to analyze data, suggest ways to manage noise, extract signal
  * e.g., suggest reg-exs to extract data components
  


---

# Making calls to LLMs, weeks 5-6

* Using Simon Willison's llm tool for making calls to LLMs
* Explore one of the following
  * Unparsable addresses from our week 4 project
  * The FEMA emergency declaration document
  * A recent document describing sanctions of Maryland attorneys
  * A PDF scan of a 1930 census page that is notoriously challenging to extract data from
* Students had to deal with non-deterministic results, distinguishing between equivalent answers (e.g., Maryland vs. MD) and incompatible answers 


---

# Databases, vector embeddings, week 7

* Didn't assume any previous exposure to databases or SQL
* Using LLMs to understand database schema, write SQL to extract and present data from database
  * Gave them database of UMD course catalog


---

# Modifying Python Idle editor, week 8

* Project from [Spring 2025 offering of UCSD CSE 190](https://cse190largecodebases.github.io/sp25/)
* Worked on getting students moved to Claude


---

# Working on Congressional Record - weeks 9-10

* work on codebase for extracting data from the Congressional record
* Reviewing various issues filed against it
    * Bugs in handling specific cases
    * Not handling content other than speeches well

---

# Building a social media app with tutoring 

* weeks 11-12
* Build a social media app from scratch (e.g., BlueSky, Instagram)
  * Have objects such as posts, users, one or more of likes, follows, images and more
  * First built as a monolithic Flask app in python with a database backend
  * Then rebuilt with a Javascript front end and REST backend
* Put a lot of work into providing guidance so that Claude would work as a tutor, rather than an answer machine

---
# Course Wrap up, weeks 13-14
* Look at quuly aka officehours.cs.umd.edu
  * a very complicated system some UMD students had built for managing queues for course office hours 
  * Had the idea to turn it into a start-up, that didn't go anywhere
  * Software hadn't been touched in years, no one at UMD felt qualified to update it
  * Written in unfamiliar frameworks: React/Go with GraphQL
  * outdated dependencies, no one to address obvious issues and feature requests
* Parting thoughts

---
# Future Work: coding agents as personal tutors

* Rather than as answer machines
* Did this in first python projects, just telling copilot to not write large sections of code
* Moved up a level with social media app
  * Prepared a script listing learning outcomes, places for engagement, etc
  * Needed a lot of tuning, sort of a game on rails
* Advanced effort, make Claude act as tutor for senior level operating system project
  * Specify key learning objectives, ways to interact and engage with students
  * But no linear script, more of an open world game
  * Adding hooks, introspection, lots of potential for future work
* Would have worked more on it, but I got side tracked into using Claude to update a paper in theoretical computer science I published in 1996: V<sub>7</sub>(16) = 28