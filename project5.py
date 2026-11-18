import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Read states.csv (columns: state, winners, population)
data_directory = Path(__file__).parent
states_data = pd.read_csv(data_directory / "states.csv").values.tolist()

#cols: month, jackpots won, jackpot winners, all winners
month_frame = pd.read_csv(data_directory / "months_pb.csv")
month_frame["all_winners"] = (
    month_frame["all_winners"].str.replace(",", "", regex=False).astype(int)
)
month_data = month_frame.values.tolist()


def state_winners_per_million(state_data):
    return state_data[1] / state_data[2] * 1_000_000


# Mean, median, variance and standard deviation of the probability that a resident of a state is a jackpot winner
probabilities = [d[1] / d[2] for d in states_data]
mean = pd.Series(probabilities).mean()
median = pd.Series(probabilities).median()
variance = pd.Series(probabilities).var()
std_dev = pd.Series(probabilities).std()

print("statistics across ", len(states_data), "states:")
print("  Mean:     ", mean, "(", round(mean * 1000000, 3), "per million )")
print("  Median:   ", median, "(", round(median * 1000000, 3), "per million )")
print("  Variance: ", variance, "(", round(variance * 1000000 ** 2, 3), "per million^2 )")
print("  Std dev:  ", std_dev, "(", round(std_dev * 1000000, 3), "per million )")

#win rates across all states
by_rate = sorted(states_data, key=state_winners_per_million)   # lowest first so the best state ends up on top
plt.figure(figsize=(10, 12))
plt.subplot(1,3,1)
plt.barh([d[0] for d in by_rate], [state_winners_per_million(d) for d in by_rate])
plt.axvline(mean * 1000000, color="red", linestyle="--", label="Mean")
plt.axvline(median * 1000000, color="green", linestyle=":", label="Median")
plt.xlabel("Jackpot winners per million residents")
plt.title("Powerball jackpot win rate by state")
plt.legend()
plt.tight_layout()

#states with the most winners per population
top = sorted(states_data, key=state_winners_per_million, reverse=True)[:10]
plt.subplot(1,3,2)
plt.bar([d[0] for d in top], [state_winners_per_million(d) for d in top])
plt.xlabel("State")
plt.ylabel("Jackpot winners per million residents")
plt.title("Top 10 states by Powerball jackpot winners per capita")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("top_states_per_capita.png")

# Months win rates across all months
months = ["December", "November", "October", "September", "August", "July", "June", "May", "April", "March", "February", "January"]
month_winners = [d[2] for d in month_data]
months_mean = pd.Series(month_winners).mean()
months_median = pd.Series(month_winners).median()

plt.subplot(1,3,3)
# Bar showing each month's share of all jackpot winners
plt.barh(months, month_winners)
plt.axvline(months_mean, color="red", linestyle="--", label="Mean")
plt.axvline(months_median, color="green", linestyle=":", label="Median")
plt.xlabel("Jackpot winners")
plt.title("Powerball jackpot win rate by month")
plt.xticks([0, 5, 10, 15, 20, 25, 30, 35, 40, 45])
plt.legend()
plt.tight_layout()

plt.show()