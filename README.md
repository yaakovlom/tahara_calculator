# tahara_calculator

This calculator is part of a project in the process of developing software for managing and calculating dates of "וסתות" in Jewish halacha, which will be published בעז"ה in the coming months.

## Installation 
Installation requirements: python3.X+.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the "tahara_calculator"

## Usage
Write down all the "ראייה" dates to calculate in a separate text file ([xxx.txt](https://github.com/yaakovlom/tahara_calculator/blob/main/example_dates.txt)).

The dates must appear in the following format:

dd/mm/yyyy o

dd = hebrew date day

mm = hebrew date maonth, When ניסן == 1 and אדר ב' == 13

yyyy = hebrew date year

o = "עונה", when day == 1 and naight == 0.

Each date must appear in a separate line


```bash
python calculator.py example_dates.txt
```

or 

```bash
python calculator.py
```

## support
Feel free to ask, review or comment on my email address:

yaakovlwork@gmail.com

## Authors and acknowledgment
Based on the amazing [pyluach](https://github.com/simlist/pyluach) package that helps process Hebrew dates.

I Thank 'ה for all the graces and good people He has placed in my way.

## licenses
[MIT](https://choosealicense.com/licenses/mit/)
