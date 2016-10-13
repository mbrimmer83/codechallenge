# Selenium web scrape application

## Overview
The goal of the project was to scrape some data from a website on individuals on that site and then follow links to there 
personal profile site and scrape more information. That data was then written to a CSV file
<br>
## Technologies and Languages
- Selenium<br>
- Firefox<br>
- Python<br>
<br>
## Logic
My thought process was to give the location of each leader and then get the information for each one. I wanted to be as general
as possible when gettin information after giving the intial location of each leader. I wanted to click each leaders profile link per the
instuctions and pull information from there prifile. 
## Problems and Challenges
1) Intitially Firefox would not run with Selenium and after a little research I fixed the problem by reverting to an older version
of Firefox that Selenium drivers were updated to interact with.<br>
2) I spent a good amount of time verifing that the page was loading. Many of the articles I read told me this was unnecessary with 
newer version of selenium. However, when I would select the leadership tab, the data would sometimes not be there. 
My assumption was that my python was running before javascript had completely updated the DOM since I was navigating after
the page had loaded. This seems to have fixed the problem and my functions run as expected.<br>
3) I initially just built functions to get each piece of data by leader location alone. I only wanted to use one main selector
and then have that code be reran for each leader given only there location. This seemed logical in that each leaders html was 
structured the same with each having there own div. I then refactored into a Leader class in order to reduce the amount of 
duplicated code.<br>
4) I ran into a problem when selenium click the linkedIn link for the first time, I was not logged in to LinkedIn. I would 
then log in and switch the logged_in variable to True so that I would not repeat the process after the initial log in. The 
instuctions said to click the links. Another solution would be to follow each link that I have stored so selenium isnt 
opening new browsers for each link. To test this, a username and password will need to be entered as I do not wish to 
give out my password for linkedin.<br>
