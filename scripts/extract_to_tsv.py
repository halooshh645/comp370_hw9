import argparse
import json
import random
import csv


parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output_file", required=True, help="Path to output file")
parser.add_argument("--seed", type=int, help="Value of seed") # command-line args treated as strings by default
parser.add_argument("--exclude", action="append", default=[], help="TSV file containing posts to exclude")
# action = "append" allows us to provide --exclude multiple times => each filename is added to a list
# deafult = [] if no exclusion files are provided, the list is empty
parser.add_argument("json_file")
parser.add_argument("num_posts_to_output", type=int)


args = parser.parse_args()

with open(args.json_file, 'r') as f:
    data = json.load(f) # Reads JSON from a file into a python object

random.seed(args.seed) # if there is seed => python initializes the random generator with that seed BUT  if no seed, python initializes it without a fixed seed

posts = data["data"] 
posts_before_num = len(posts)

# read posts we want to exclude
excluded_names = set()

for filename in args.exclude:
    with open(filename, "r") as f:
        reader = csv.DictReader(f, delimiter='\t')
        
        reader.fieldnames = [name.strip() for name in reader.fieldnames] # removes extra spaces from header

        for row in reader:
            excluded_names.add(row["Name"])

filtered_posts = []

for post in posts:
    if post["name"] not in excluded_names:
        filtered_posts.append(post)


num_excluded = posts_before_num - len(filtered_posts)

print(f"Excluded {num_excluded} posts")


k = min(args.num_posts_to_output, len(filtered_posts))

sampled_posts = random.sample(filtered_posts, k)  # (population, k) => population = list selecting from; k = how many elements you want to select; note: samples without replacement
# sampled_posts is a list of dictionaries because random.sample() returns a list

# writing sampled posts to a TSV file
with open(args.output_file, "w") as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(["Name", "title", "coding"])
    for post in sampled_posts:
        title = post["title"].replace("\t", " ").replace("\n", " ")
        writer.writerow([post["name"], title, ""])
