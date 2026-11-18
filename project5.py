import csv
import statistics
import matplotlib.pyplot as plt

# Read states.csv (columns: state, winners, population)
# Each entry: (state, winners, population in millions, winners per million)
data = []
with open("states.csv") as file:
    for row in csv.DictReader(file):
        pop_millions = int(row["population"]) / 1000000
        winners = int(row["winners"])
        data.append((row["state"], winners, pop_millions, winners / pop_millions))

# Mean, median, variance and standard deviation of the probability that a resident of a state is a jackpot winner
probabilities = [d[1] / (d[2] * 1000000) for d in data]
mean = statistics.mean(probabilities)
median = statistics.median(probabilities)
variance = statistics.pvariance(probabilities)
std_dev = statistics.pstdev(probabilities)

print("statistics across ", len(data), "states:")
print("  Mean:     ", mean, "(", round(mean * 1000000, 3), "per million )")
print("  Median:   ", median, "(", round(median * 1000000, 3), "per million )")
print("  Variance: ", variance, "(", round(variance * 1000000 ** 2, 3), "per million^2 )")
print("  Std dev:  ", std_dev, "(", round(std_dev * 1000000, 3), "per million )")

#win rates across all states
by_rate = sorted(data, key=lambda d: d[3])   # lowest first so the best state ends up on top
plt.figure(figsize=(10, 12))
plt.barh([d[0] for d in by_rate], [d[3] for d in by_rate])
plt.axvline(mean * 1000000, color="red", linestyle="--", label="Mean")
plt.axvline(median * 1000000, color="green", linestyle=":", label="Median")
plt.xlabel("Jackpot winners per million residents")
plt.title("Powerball jackpot win rate by state")
plt.legend()
plt.tight_layout()
plt.savefig("win_rates.png")

#states with the most winners per population
top = sorted(data, key=lambda d: d[3], reverse=True)[:10]


plt.figure(figsize=(10, 6))
bars = plt.bar([d[0] for d in top], [d[3] for d in top])
for bar, d in zip(bars, top):
    # label each bar with the raw number of winners
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(d[1]) + " winners",
             ha="center", va="bottom", fontsize=9)
plt.xticks(rotation=45, ha="right")
plt.ylabel("Jackpot winners per million residents")
plt.title("Top 10 states by Powerball jackpot winners per capita")
plt.tight_layout()
plt.savefig("top_states_per_capita.png")

plt.show()
