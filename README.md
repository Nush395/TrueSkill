# TrueSkill
This library is an implementation of the algorithm described in [the original paper by the team at Microsoft Research](https://www.microsoft.com/en-us/research/wp-content/uploads/2007/01/NIPS2006_0688.pdf). It differs from the complete implementation in that it does not yet model/allow the option for draws to happen in games and doesn't support partial play.
## Motivation
I created this library as a fun way of being able to understand the TrueSkill algorithm as part of my journey on all things Bayesian and Machine Learning and also as a way for me to be able to rank games in table football/tennis amongst my mates.
## Requirements
* Python 3.6+
* Scipy 1.1.0
* Numpy 1.18.0
## Usage
### Direct usage
#### Using results of factor graph directly.
In order to 
#### Building your own factor graph
If you would like to directly make use of the components of the factor graph yourself they can be found in [here](src/trueskill/factor_graph.py)

## Credits
As listed above the [original paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2007/01/NIPS2006_0688.pdf) where the details of the TrueSkill algorithm were laid out. 
I used the following blog/article to help with my understanding and it was very useful.
* https://www.moserware.com/assets/computing-your-skill/The%20Math%20Behind%20TrueSkill.pdf

I also took design inspiration for this library from the accompanying code repo for the above article.
* https://github.com/moserware/Skills (C#)

## Further explanation
Please see my blog post here (TBD) for more details on the implementation

## Tests
This library has tests written using the Python unittest library. To run the tests use:
```
python -m unittest discover
```

### Other implementations:
Below are listed some other implementations I found that implement the general TrueSkill algorithm very nicely.
* https://github.com/sublee/trueskill (Python)
