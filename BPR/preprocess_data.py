from pathlib import Path
import csv
import os
from collections import defaultdict

root_path = Path("../../OData")
save_path = Path("./Amazon_Digital_Music")
data_path = root_path / "Amazon_Digital_Music/Digital_Music.csv"
os.makedirs(save_path, exist_ok=True)

train_path = save_path / "train.csv"
test_path = save_path / "test.csv"

user2raw = defaultdict(list)

# load all
with data_path.open("r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) < 4:
            continue
        user_raw = row[0]
        item_raw = row[1]
        timestamp = int(float(row[3]))
        user2raw[user_raw].append((item_raw, timestamp))

# filter >= 20
filtered_users = {u: items for u, items in user2raw.items() if len(items) >= 20}
print("Users >=20:", len(filtered_users))

# reindex users + items
new_u_idx = {}
new_i_idx = {}
u_cnt = i_cnt = 0

for u in filtered_users:
    new_u_idx[u] = u_cnt
    u_cnt += 1

# sort & remap
final_interactions = defaultdict(list)

for u_raw, pairs in filtered_users.items():
    u = new_u_idx[u_raw]
    pairs.sort(key=lambda x: x[1])
    for item_raw, ts in pairs:
        if item_raw not in new_i_idx:
            new_i_idx[item_raw] = i_cnt
            i_cnt += 1
        i = new_i_idx[item_raw]
        final_interactions[u].append(i)


print("Total items after filtering:", len(new_i_idx))
print("Max item idx:", max(new_i_idx.values()))

# write train/test
with train_path.open("w") as f_train, test_path.open("w") as f_test:
    for u in sorted(final_interactions):
        items = final_interactions[u]
        train_items = items[:-1]
        test_item = items[-1]
        f_train.write(" ".join([str(u), *map(str, train_items)]) + "\n")
        f_test.write(f"{u} {test_item}\n")
