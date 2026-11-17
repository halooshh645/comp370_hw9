import csv
import matplotlib.pyplot as plt # allows us to create graphs

CATEGORIES = ["AAC", "APP", "CFS", "HT", "CESB", "PSI", "SWB", "SLA"]
def count_categories(filename):
    """
    Takes a filename and counts how many posts belong to each category
    """
    counts = {} # keys = categories; values = number of posts assigned to each category

    with open(filename, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            category = row["Coding"].strip()
            counts[category] = counts.get(category, 0) + 1 # counts.get(category, 0) means if category already exists, retreive its value (current count), otherwise, return 0

    return counts

mcgill = count_categories("../data/final_labeled_dataset_mcgill.tsv")
concordia = count_categories("../data/final_labeled_dataset_concordia.tsv")

# Calculating total number of posts in each:
mcgill_total = sum(mcgill.values())
concordia_total = sum(concordia.values())

# Percentage of category

def calculate_percent(dictionary, total):
        
        percent =  []

        for category in CATEGORIES:
            percent.append(dictionary.get(category, 0)/ total * 100)

        return percent


mcgill_percent = calculate_percent(mcgill, mcgill_total)
concordia_percent = calculate_percent(concordia, concordia_total)

# Plotting the results
x = range(len(CATEGORIES))
width = 0.35

plt.bar([i - width/2 for i in x], mcgill_percent, width, label="McGill")
plt.bar([i + width/2 for i in x], concordia_percent, width, label="Concordia")

plt.xticks(list(x), CATEGORIES)
plt.xlabel("Topic")
plt.ylabel("Relative Abundance (%)")
plt.title("Relative Abundance of Reddit Post Topics")
plt.legend()
plt.tight_layout()
plt.savefig("../results.png")

