import pandas as pd

def load_data(filepath):
    xls = pd.ExcelFile(filepath)
    wind_plants = pd.read_excel(xls, 'windplants')
    wind_loadfactors = pd.read_excel(xls, 'wind_loadfactors')
    solar_plants = pd.read_excel(xls, 'solarplants')
    solar_loadfactors = pd.read_excel(xls, 'solar_loadfactors')
    gas_plants = pd.read_excel(xls, 'gasplants')
    demand = pd.read_excel(xls, 'demand')
    gas_prices = pd.read_excel(xls, 'gas_prices')

    return {
        'wind_plants': wind_plants,
        'wind_loadfactors': wind_loadfactors,
        'solar_plants': solar_plants,
        'solar_loadfactors': solar_loadfactors,
        'gas_plants': gas_plants,
        'demand': demand,
        'gas_prices': gas_prices,
    }

# Wind/Solar Output = capacity * load_factor
# bid price of gas = （price * 34.121)/(gasplant efficiency * 100)

def wind_output(wind_capacity, wind_load_factor):
    w_o = wind_capacity * wind_load_factor
    return w_o

def solar_output(solar_capacity, solar_load_factor):
    s_o = solar_capacity * solar_load_factor
    return s_o

def gas_bid_price(gas_price, efficiency):
    gas_b_p = (gas_price * 34.121)/(efficiency * 100)
    return gas_b_p

def build_generators_for_hour(hour, data):
    generators = []
    # wind data
    wind_loadfactors_df = data["wind_loadfactors"]
    wind_plants_df = data["wind_plants"]
    # solar data
    solar_loadfactors_df = data["solar_loadfactors"]
    solar_plants_df = data["solar_plants"]
    # gas data
    gas_plants_df = data["gas_plants"]
    gas_prices_df = data["gas_prices"]

    # load factors for wind
    lf_row_wind = wind_loadfactors_df[ wind_loadfactors_df["hour"] == hour ].iloc[0]
    # load factors for solar
    lf_row_solar = solar_loadfactors_df[ solar_loadfactors_df["hour"] == hour ].iloc[0]

    # hourly price for gas
    price_row_gas = gas_prices_df[ gas_prices_df["hour"] == hour ].iloc[0]

    # read wind data
    for idx, row in wind_plants_df.iterrows():
        name = row["name"]
        cap = row["capacity"]
        lf = lf_row_wind[name]

        available = wind_output(cap, lf)

        gen_wind = {
            "name": name,
            "type": "wind",
            "available": available,
            "bid": 0.0
        }

        generators.append(gen_wind)
    #read solar data
    for idx, row in solar_plants_df.iterrows():
        name = row["name"]
        cap = row["capacity"]
        lf = lf_row_solar[name]

        available = solar_output(cap, lf)

        gen_solar = {
            "name": name,
            "type": "solar",
            "available": available,
            "bid": 0.0
        }

        generators.append(gen_solar)
    # read gas data
    for idx, row in gas_plants_df.iterrows():
        name = row["name"]
        efficiency = row["efficiency"]
        cap = row["capacity"]
        price = price_row_gas["price"]

        bid = gas_bid_price(price, efficiency)

        gen_gas = {
            "name": name,
            "type": "gas",
            "available": cap,
            "bid": bid,
        }

        generators.append(gen_gas)

    return generators



def dispatch(demand, generators):
    # sort the generators
    sorted_generators = sorted(generators, key=lambda g: g["bid"])

    remaining = demand
    clearing_price = 0.0

    mix = {
        "wind": 0.0,
        "solar": 0.0,
        "gas": 0.0,
    }

    for gen in sorted_generators:
        if remaining <= 0:
            break

        available = gen["available"]
        take = min(available, remaining)

        remaining -= take

        # different types
        generator_type = gen["type"]
        mix[generator_type] += take

        if take > 0:
            clearing_price = gen["bid"]
    # if remaining > 0:
    #     print(f"Warning: demand not fully met, remaining = {remaining}")

    return clearing_price, mix, remaining

def run(data, hour):
    generators = build_generators_for_hour(hour, data)
    demand_df = data["demand"]
    demand_row = demand_df[demand_df["hour"] == hour].iloc[0]
    demand = demand_row["demand"]

    price, mix, remaining = dispatch(demand, generators)

    if remaining > 0:
        print(f"Hour {hour} NOT fully met! Remaining = {remaining}")

    return {
        "hour": hour,
        "price": price,
        "demand": demand,
        "remaining": remaining,
        "wind": mix["wind"],
        "solar": mix["solar"],
        "gas": mix["gas"],
        "served": remaining <= 0
    }
if __name__ == '__main__':
    data = load_data("data.xlsx")
    # print(data.keys())
    # print(data['wind_plants'].head(5))
    # print(data['gas_prices'].head(5))

    # generators = build_generators_for_hour(20, data)
    # for gen in generators:
    #     print(gen)
    demand_df = data["demand"]
    results = []
    for hour in demand_df["hour"]:
        result = run(data, hour)
        results.append(result)
    results_df = pd.DataFrame(results)
    results_df.to_csv("results.csv", index=False)
    results_df.to_excel("results.xlsx", index=False)




