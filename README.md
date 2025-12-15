# Electricity Market Dispatch Simulation

## Overview
This project simulates the UK pay-as-clear electricity market using the dataset provided by LCCC.
For each hour, the program calculates:

- The clearing electricity price (£/MWh)

- The dispatched generation mix (wind, solar, gas)

- Whether demand is fully met

All outputs are written to results.csv and results.xlsx

## Method Summary
### 1. Wind/Solar
Available output:
```
output = capacity × load_factor

```
Bid price is £0/MWh.
### 2. Gas
Available is equal to capacity.
Bid is based only on gas costs:

$ \text{bid} = \frac{\text{gas\_price} \times 34.121}{100 \times \text{efficiency}} $





### 3. Dispatch Algorithm
    (1) Dispatch wind (bid = 0)

    (2) Dispatch solar (bid = 0)

    (3) Dispatch gas from lowest bid to highest

## How to Run

Install dependencies:
```
pip install pandas openpyxl
```

Run the script:
```
python auction_progress.py
```

Output file:
`results.csv`

## Output Files

The program generates two output files:

- **results.csv**
- **results.xlsx**

Both files contain the following fields:

| Column | Meaning |
|--------|---------|
| hour | Hour index |
| price | Clearing electricity price (£/MWh) |
| demand | Hourly electricity demand (MWh) |
| remaining | Unserved demand (MWh). `0` indicates demand was fully met. |
| wind | Energy dispatched from wind generators |
| solar | Energy dispatched from solar generators |
| gas | Energy dispatched from gas plants |
| served | `True` if demand was fully met (`remaining == 0`) |

Some hours have a positive remaining value because renewable output (wind or solar) was low during those periods, and even the full gas fleet could not fully meet demand.

