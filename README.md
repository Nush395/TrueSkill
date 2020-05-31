# TrueSkill
This library is an implementation of the algorithm described in [the original paper by the team at Microsoft Research](https://www.microsoft.com/en-us/research/wp-content/uploads/2007/01/NIPS2006_0688.pdf). It differs from the complete implementation in that it does not yet model/allow the option for draws to happen in games and doesn't support partial play.

Note: TrueSkill is a patented algorithm by Microsoft Research and is not suitable for commercial use.
## Motivation
I created this library as a fun way of being able to understand the TrueSkill algorithm as part of my journey on all things Bayesian and Machine Learning and also as a way for me to be able to rank games in table football/tennis amongst my mates.
## Requirements
* Python 3.6+
* Scipy 1.1.0
* Numpy 1.18.0
## Usage
### Direct usage
To get started straight away and run the algorithm checkout the code and run using 
```
python trueskill/main.py -h
```
#### Using results of factor graph directly or building your own factor graph.
See the README [here](https://github.com/Nush395/TrueSkill/blob/master/trueskill/trueskill/README.md) if you want to build your own
factor graph using the components or use the TrueSkill environment directly.

#### Saving data
Currently skills are stored in a CSV file as this was a lightweight way that suited my purposes. If you would like to change the way data is stored then inherit from the abstract base class DataSource in trueskill/player_ratings and implement the required methods.

## Tests
This library has tests written using the Python unittest library under the tests package in the code. To run the tests navigate to the project and use:
```
python -m unittest discover
```

## Further explanation
I am currently writing a post detailing my journey to understanding the algorithm which I hope will aid others' understanding, watch this space!

## Credits
As listed above the [original paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2007/01/NIPS2006_0688.pdf) where the details of the TrueSkill algorithm were laid out. 
I used the following blog/article to help with my understanding and it was very useful.
* https://www.moserware.com/assets/computing-your-skill/The%20Math%20Behind%20TrueSkill.pdf

I also took design inspiration for this library from the accompanying code repo for the above article.
* https://github.com/moserware/Skills (C#)
### Other implementations:
Below are listed some other implementations I found that implement the general TrueSkill algorithm very nicely.
* https://github.com/sublee/trueskill (Python)
