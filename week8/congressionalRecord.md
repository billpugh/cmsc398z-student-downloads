# The Congressional Record project

This tool converts HTML files containing the text of the Congressional Record into structured text data. It is particularly useful for identifying speeches by members of Congress.

* Software hasn't seen updates since 2019, has some problems, include dependencies on deprecated APIs
* Documentation is pretty sparse and poor
* But still serves a useful purpose
* Plan is for our class to reboot it, make it work well. 

If you have time this week, you can download it, try running it, start trying to understand it

## getting started

* Clone the github repository [https://github.com/unitedstates/congressional-record](https://github.com/unitedstates/congressional-record)
* You can ignore the instructions about using pip to install dependencies
* Instead,  use 'uv add certifi' to add missing dependencies
* Use 'uv run python -m congressionalrecord.cli' to run it
  * It will tell you what arguments are needed
  * For example, try 'uv run python -m congressionalrecord.cli 2005-01-01 2005-01-05 json'
* View the [issues on github](https://github.com/unitedstates/congressional-record/issues)
  * In particular, [issue 55](https://github.com/unitedstates/congressional-record/issues/55)
