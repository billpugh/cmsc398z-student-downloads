# CMSC 398Z - Week 12 - Nov 21st, 2025

## Work in class

This week, we are going to continue on the project we did last week, building a new version of the app that uses a REST API + JavaScript frontend. 

Things to do:
* Read ARCHITECTURE-GUIDE-phase2.md in the cmsc398z-sma directory, then
* Open claude in the cmsc398z-sma repository, and tell it to  "Read TODO-phase2.md and guide me through Phase 2"

Several notes:
* When I first did phase2, it made new versions of database.py and models.py that were almost, but not exactly, the same as the versions used in phase 1. So I updated the instructions so suggest that as part of moving to phase 2, it should suggest refactoring those files into a shared version that could be used by both phase 1 and phase 2 (phase 1 and phase 2 were already sharing the same database). This way, we don't have to worry about these files getting out of sync if we were maintaining two different versions.
* I was informed of a nice tool to let you use the campus CAS service when running a web service locally. If your web service is just running as localhost, CAS won't work. However, while on the campus network (may require VPN), the [hostname localhost.dev.umd.edu will resolve to the same ip address as localhost, and will with with UMD CAS](https://umd.service-now.com/kb_view.do?sys_kb_id=d946fabc1b06fd50df8784415b4bcbef&sysparm_class_name=kb_knowledge). 
* We haven't done as many run throughs to fine tune phase 2 and we did for phase 1, and you may fine that claude blows through some important points without taking time to make sure you understand the key concepts. Make sure you look at some of the frontend and backend code and understand some of those concepts. If you need to, ask claude to explain them, or ask it to point you to code to help understand those key concepts.
* One of the goals of phase 2 is getting to a single page application (SPA), where the application rarely needs to reload the entire web page. For example, if you add a new post, it should just refresh the listing of posts to show your post. Claude might not initially do that. Once you get phase 2 initially working, ask Claude if the code is working as a SPA and using refreshes where possible.



## Submitting your work

You need to submit the following:

* Work on implementing the minimum feature set and one additional feature for Phase 2. Submit this ideally by end of class, but no later than Saturday to be considered on-time.
  * At a minimum, this includes ARCHITECTURE.md and phase2/DECISIONS-MADE-phase2.md, which will be completed by Claude as you do your work.
* Update and submit REFLECTIONS.md by noon Tuesday, Nov 25th
  * This doesn't have to be much of an update over what you did last week. It is Thanksgiving week, you don't need to spend more than 5 minutes on it.
  * If you did any additional work after your initial phase 2 submission, you can submit that as well, which at a minimum includes updates files for ARCHITECTURE.md and phase2/DECISIONS-MADE-phase2.md.








