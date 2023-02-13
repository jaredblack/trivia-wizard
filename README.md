# Trivia Wizard
## Project description

This is intended to be a helper app for the bar trivia style I do at the trivia nights I host. The basic idea is as follows:
- One person logs in as the host and creates a game session
- A representative from each team joins the game session. For each question, they can submit an answer.
- The host receives these answers in real time and sees them ordered according to when they were sent in.
- The host can quickly select whether to score the answer or not based on its correctness. The game will be able to automatically apply scoring bonuses for teams who submitted the quickest.

## Technology notes
- WebSockets seem like a good fit for this project to broadcast messages between the teams and the host.
- The server and frontend frameworks I pick probably won't matter very much. A Python server that uses the Python websockets module could be good since I am very familiar with Python.

## Basic UI notes
- Team view - a simple page that simply displays a team's name, their current score, and a text box for them to submit the answer to the current question
- Host view - a page that contains all the host controls. From here the host can see answers as they come in, score them as needed, and reset inputs for the next question. They can also modify game settings like point totals.
- Score view - a simple page that just shows all of the teams and their associated scores, ranked in order of who's winning
- Login view - a page that allows you to select to:
    - Host a game: create a new join ID, take you to host view.
    - Join a game: enter a join ID and team name, take you to team view. If you enter the same team name as one that has already joined, you reconnect as that team.
    - Watch game score: enter a join ID, take you to score view

## To-do
- Create *basic* prototype with simplified versions of the team view and host view and run that locally.

## Resources
- [WebSockets tutorial](https://websockets.readthedocs.io/en/stable/intro/tutorial3.html)