import numpy as np
import pandas as pd


def raffle(csv_file, seed):
    np.random.seed(seed)

    df = pd.read_csv(csv_file)

    total_amount = df["total_amount_usd_transfer"].sum()  # normalize the total amount
    df["probability"] = df["total_amount_usd_transfer"] / total_amount

    winner = np.random.choice(df["address"], p=df["probability"])

    return winner


csv_file = "data.csv"
winner = raffle(csv_file, seed=696969)
print(f"The winner is: {winner}")

# 8rft37QUrRayFTtMkyniDZdeNa6piQJfhRxRZzQfoLRD
# 8rft37QUrRayFTtMkyniDZdeNa6piQJfhRxRZzQfoLRD
# 8rft37QUrRayFTtMkyniDZdeNa6piQJfhRxRZzQfoLRD
