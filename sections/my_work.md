# My Work

<!--
One `##` block per piece of work, whether it was a job or a project.
Write the story as paragraphs under the block. A `###` line is only the
date of that write-up. Another `###` date under the same name is an update
to the same work, not a new project.

A job block must name the employer in the text. The bot places it under
that role in experience.md. Anything else is a project.

## <Name>
- about: one line on what it is
- type: personal | job | academic | research | hackathon | freelance
- team: solo | team of N          optional; your role if it was a team
- link: repo, live demo, or paper URL
- status: active | archived

### <date, if you have one>
Paragraphs. Go as detailed as you can. The bot pulls the resume lines from here.
-->

## Order Pipeline

- about: Nightly order pipelines at Northwind Analytics
- type: job
- team: team of 4
- link:
- status: active

### March 2024
I built nightly order pipelines at Northwind Analytics with Python and Apache Airflow. Each run reads a small config table in PostgreSQL, loads the listed shop files from Amazon S3, and writes cleaned order tables for the morning sales report. Adding a shop is a new row in that table, not a code change.

I rewrote the slowest reconciliation query so the finance export finishes in about 12 minutes instead of about 40. The check still flags any order whose line totals do not match the payment record.

I paired with the sales analyst to name the columns the weekly dashboard needs, and I documented the runbook so the on-call person can rerun one shop without reloading the whole night.

## Shelf Count

- about: Inventory tracker for a campus bookstore
- type: freelance
- team: solo
- link: https://github.com/jordanhale/shelf-count
- status: active

### August 2024
I built Shelf Count, a solo freelance app for a campus bookstore that was counting stock on paper. It uses FastAPI, PostgreSQL, and a small set of HTML pages. Staff record deliveries, shelf counts, and which titles are on order.

I split suppliers, shelves, and purchase orders into separate modules so a new field on a purchase order does not require edits on the shelf screen. Role checks limit who can change a count versus who can only look one up. The same REST endpoints feed the pages and a later handheld client.

## Meal Window

- about: A site that suggests meals from ingredients already at home
- type: personal
- team: solo
- link: https://github.com/jordanhale/meal-window
- status: active

### November 2024
I built Meal Window, a small site that takes a list of ingredients and returns three recipes that use them. The app is Python and SQLite behind a few REST endpoints, and the recipe list is a static file I curated for the demo.

I packaged the app with Docker so a classmate could run it with one command. The image build is cached, so a text change on the recipe page republishes in under a minute on the sample host.

## Rainfall Notes

- about: A class project comparing models on a public weather table
- type: academic
- team: solo
- link:
- status: active

### May 2023
For a class project I compared three models on a public city-weather table: logistic regression, a random forest, and a small neural net in scikit-learn. The inputs were month, average temperature, and rainfall. On the held-out month, the random forest had the highest accuracy, about 81%. I wrote the comparison in Python and plotted precision and recall for each model. The write-up stayed in the course folder and was not published.
