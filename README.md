# Trivia Wizard
## Project description

This is intended to be a helper app for the bar trivia style I do at the trivia nights I host. The basic idea is as follows:
- One person logs in as the host and creates a game session
- A representative from each team joins the game session. For each question, they can submit an answer.
- The host receives these answers in real time and sees them ordered according to when they were sent in.
- The host can quickly select whether to score the answer or not based on its correctness. The game will be able to automatically apply scoring bonuses for teams who submitted the quickest.

## Basic UI notes
- Team view - a simple page that simply displays a team's name, their current score, and a text box for them to submit the answer to the current question
- Host view - a page that contains all the host controls. From here the host can see answers as they come in, score them as needed, and reset inputs for the next question. They can also modify game settings like point totals.
    - Host view can also control whether or not score view shows the answers other teams put.
- Score view - a simple page that just shows all of the teams and their associated scores, ranked in order of who's winning
- Login view - a page that allows you to select to:
    - Host a game: create a new join ID, take you to host view.
    - Join a game: enter a join ID and team name, take you to team view. If you enter the same team name as one that has already joined, you reconnect as that team.
    - Watch game score: enter a join ID, take you to score view

## To-do
- Create *basic* prototype with simplified versions of the team view and host view and run that locally.

## Backend features
### Host
- Create game code
- Send score update (propogates to the score view)
- Start timer countdown. This also doubles as enabling question submission (request specifies the length of time. Relayed to the score view and maybe the player view)
- Stop timer countdown. Also disables question submission (Relayed to score and player view)
- Move forward a question (Returns back empty question data if new question, or the already-submitted question data)
- Move backward a question (Returns back the question data from that previous question)
### Player
- Join game (return how many doubles the team gets)
- Submit answer
- Double (return how many remaining doubles). Only successful if timer has not been started for the current question

### Reconnection
- Need to allow for a quick and easy way to reconnect if the socket connection is lost
- Only allow for one host at a time - if there's an open host socket then we should not allow another host to join
- TO FACILITATE THIS: listen for close on every client, and then just reconnect when that happens!
- Also allow a team to reconnect if a team name that's already in is entered (but maybe kick out the other socket)

### Things to explore
- Svelte has some movement/transition things that could help make look things nice. Particularly, transitions when we reorder the score list could be cool.

### To-do before the demo on Monday
- Scoring enhancements
    - Automatically grant bonuses to 1st, 2nd teams to submit

### Future to-do
- Implement the doubling ability from the last trivia night
- Parse score inputs helpfully like adding 100 points if I type +100

### Things to ensure in testing
- Ensure no way for a team to submit multiple answers for a question

## Resources
- [WebSockets tutorial](https://websockets.readthedocs.io/en/stable/intro/tutorial3.html)