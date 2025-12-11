# AggieAI

Welcome to AggieAI, your AI assistant for all things Utah State Aggies! This helpful chatbot will provide you with all of the information you need to cheer on your Aggies. AggieAI has access to a comprehensive database containing information about players positions, jersey numbers, how many championships they have won, and even their academic records.

Additionally, AggieAI is well versed on gameday procedures, school traditions, and guidelines and other info on major events in Aggie athletics. You can also request updates on the latest scores and standings, and AggieAI will be happy to help out!

## Starter Examples

Below are examples of how to request the different information that AggieAI has access to. Feel free to copy and paste these prompts into the chatbot to get started!

### Player Database

You can ask AggieAI questions about specific players, such as:

_What position did Bobby Wagner play for the Aggies?_

_What classes did Mason Falslev take at Utah State?_

### Gameday Policies and Traditions

You can ask AggieAI questions about gameday, such as:

_When do fans sing the Scotsman?_

_Can I bring my backpack into Aggie games?_

### Recent Games

AggieAI can fill you in when you miss a game and want to find out what the score was:

_When is the next Utah State men's basketball game?_

_What was the score of the last Utah State football game?_



## Test Cases (for Matt)

#### Test 1

**Question:** What number did Darius Brown wear and how many championships did he win?

**Answer:** He wore number 10 and won 1 championship. This comes from the database.

#### Test 2

**Question:** What classes did Mason Falslev take and what were his grades?

**Answer:** It should tell you that he took math twice and got an F once and an A once, he got a B in physical education, and an F in history. This comes from the database as well (and clearly uses made up data).

#### Test 3

**Question:** When are fans supposed to sing the Scotsman?

**Answer:** This will call the RAG tool. The response will tell you that the song should start 2 beats after "Hail the Utah State Aggies" and that students will mimick milking a cow.

#### Test 4

**Question:** How can I get Big Blue to come to my company party?

**Answer:** This will also call the RAG tool. The response will tell you that you need to fill out the mascot request form at least three weeks before your event and that Big Blue's appearance is subject to availability and travel restrictions.

#### Test 5

**Question:** What bowl game is Utah State playing in this year?

**Answer:** This will call the websearch tool. Utah State is playing in the Famous Idaho Potato bowl against Washington State.
