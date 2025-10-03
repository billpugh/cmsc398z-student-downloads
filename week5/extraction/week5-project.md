# Week 5 project

For our week 5 project, we are going to explore extracting data from 4 different data sources. You can do a deep dive on just one or two of these, or do a exploratory evaluation of 3 or 4 of them. You don't have to pick them in order, pick any subset you want to work on.

* [Unparsable addresses from our week 4 project](#unparsable-addresses)
* [The FEMA emergency declaration document](#fema-emergency-declarations)
* [A recent document describing sanctions of Maryland attorneys](#sanctions-of-maryland-attorneys)
* [A PDF scan of a 1930 census page](#census-data-from-1930) that is notoriously challenging to extract data from
  * Note: this file describes African Americans using terminology commonly used in 1930. If you feel awkward dealing with this file or data, you are free to skip it.

## Json object returned by data extraction

I have generally noted that when you ask for extraction with a multi-schema, the top level json value returned is an object, not an array, the fields of that object may not be consistent. Example requests I've gotten back from the FEMA document include:

```json
{ "type": "array",  "items": [ ... ],  "source": "Table 'Declaration Requests in Process \u2013 12' (page 8 of the briefing)"}
{"type": "array", "items": [ ... ]}
{"declaration_requests": [ ... ]}
{"requests": [ ... ]}
{"declarations": [ ... ]}
```

So first, be aware of this. None of these differences were semantically significant. You might be able to rewrite the system prompt to reduce the variation, or just accommodate it.

## First steps

For each data source you work on, start by

* Come up with a system prompt for extracting the data, if one hasn't been provided.
* Perform the extraction, see if it seems to match the data source. You might see a problem with your prompt, if so see if you can improve it. 
* Perform the extraction 1-2 more times, saving the results to different files. Look at the differences, see if you think it would be helpful to refine the system prompt.
* Write a script that performs the extraction 3-6 times, saving each result to a separate file. It would be good to keep these all organized, perhaps creating a directory for each data source, and numbering the results something like 0.json, 1.json, etc.
  * You could either write one script that takes command line arguments things like the system prompt, the schema and the attachment or fragment to be used, or write a separate script for each document you want to extract data from
  * You find it useful to actually parse the json object returned, augmenting with a property that contains information such as the model used and the tokens consumed, and then write that augmented json out. This will be particularly useful if you want to examine things such as comparing different models.
* Manually examine the outputs again, comparing the results.

## Writing up what you found

In Results.md, write up a short description of what differences you are seeing in the results. For each kind of difference you see:

* Do you think they are semantically equivalent?
* Is this a case taking a majority vote would likely give a consistent answer?
* Are there some redundant data that could be checked for  consistency in order to identify problems?

## Optional: Automate your analysis

Write code that would take the results of several calls to LLMs to extract data and then automatically apply what you found above to produce a consensus result, with low confidence results flagged. Eventually, you might want to develop a pipeline in which your code made several calls to LLMs to extract the data and then produce a consensus result. But for now, you might want to just use the files you already downloaded so as to avoid having to wait for the LLM queries each time you want to try running your code. It might be helpful to also produce summary statistics.

It is likely that whatever you do to automate your analysis will be significantly customized for each datasource.

If you did this for any of your data sources, write it up in Results.md. Give the data source, the files that are your implementation, and a summary or output of your analysis

## Optional: Evaluate model and prompt choices

If you were to actually use this extraction process as part
of a regular pipeline, you'd want to compare different LLM models. Perhaps gpt-5-nano would be sufficient for some tasks, or maybe a more capable model such as gpt-5 gives better results. Perhaps different system prompts would give you more accurate answers, or get the model to provide useful information. Make some requests with different choices, and then evaluate the differences and write up what you see in Results.md. You can use manual or an automatic process to evaluate the differences. 

## Details on data sources

### Unparsable addresses

The file addresses.txt in the week 5 directory is a list of street addresses from week 4 that could not be parsed by `parse_address(address)`. Your goal is to generate either a csv or json with each row/element having 5 items:

* The original street address string (used for matching with original entry)
* Street address, or 0 if not found or parsable
* optional Unit description. May include text (e.g., Apt 6) or be a simple number. Should be blank if not found or not parsed
* Street name
* Street kind (e.g., RD or ST). It doesn't matter what abbreviation is used (e.g., RD, Road or ROAD is fine)

The most important items are the original street address, street name and street kind. Those items should be extracted even of the street address or unit description cannot.

When thinking about incorporating the capability to make calls to LLMs into a tool, you could make a call for each address you need to parse. However, it would be faster and cheaper to batch a call to parse an entire batch of addresses.

### FEMA emergency declarations

This involves parsing the FEMA Daily Operations Briefing, as described [previously](structured-data-extraction.md#something-a-bit-more-impressive). For consistency, you might want to pick a specific date, rather than current one. You could pick a day after a significant disaster, rather than just picking a consistent recent date. For example, the [briefing for 09-28-2024.pdf](https://disastercenter.com/FEMA%20Daily%20Ops%20Briefing%2009-28-2024.pdf) shows some of the disaster declarations after Tropical Cyclone Helene. Note that in URLs passed to llm, spaces will need to be URL-encoded, replacing spaces with %20:

```text
https://disastercenter.com/FEMA%20Daily%20Ops%20Briefing%2009-28-2024.pdf
```

You will almost certainly seem some semantically insignificant variations, but in my own testing I found rare but very significant inconsistencies.

### Sanctions of Maryland attorneys

This example comes from [Derek's llm-playground github repository](https://github.com/dwillis/llm-playground). This is the [sanctions file](https://raw.githubusercontent.com/dwillis/llm-playground/refs/heads/main/sanctionsfy25.txt). Produce a json file with the following properties: name, sanction, date, and description. The date should be in the yyyy-mm-dd format.

### Census data from 1930

This example comes from [Derek's nicar25-pdfs github repository](https://github.com/dwillis/nicar25-pdfs). [NICAR25 is named for the National Institute of Computer Assisted Reporting](https://www.ire.org/training/conferences/nicar-2025/) (although that organization doesn't exist anymore, it's the name of an annual conference for data journalists). The challenge to decipher this pdf is below.

![alt](https://github.com/dwillis/nicar25-pdfs/raw/main/nerdery_challenge.png)

* Note: as mentioned previously this file describes African Americans using terminology commonly used in 1930. If you feel awkward dealing with this file or data, you are free to skip it.

The [PDF file is here](https://raw.githubusercontent.com/dwillis/nicar25-pdfs/refs/heads/main/BlackPop1930.pdf). There are several reasons this is a challenging document to extract data from. You might want to provide a straight forward scheme and instructions and see how that works before trying to fine tune the instructions. The things that look challenging to you might not be challenging to the model.

Your ultimate goal is to generate csv or json file with at least the following entries:

* City and State
* Population in 1930
* Population in 1920
* Population in 1910

However, you may find it useful to extract additional columns from the table to allow you to check for consistency.

Ideally, you would find a way to denote confidence, or lack of it, in each entry.
