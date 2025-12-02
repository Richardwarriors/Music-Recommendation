import json

def load_recommendations(filepath):
    """
    Loads recommendations from a file.
    The file is expected to contain blocks of JSON arrays, separated by blank lines.
    """
    with open(filepath, 'r') as f:
        content = f.read().strip()
    
    json_strings = content.split('\n\n\n')
    
    recommendations = []
    for s in json_strings:
        if s:
            try:
                recommendations.append(json.loads(s))
            except json.JSONDecodeError as e:
                print(f"Warning: Could not parse JSON block. Error: {e}")
                print(f"Block content: {s}")
    return recommendations

def load_ground_truth(filepath):
    """
    Loads ground truth from a file.
    Each line corresponds to a user, with items separated by '|'.
    """
    ground_truth = []
    with open(filepath, 'r') as f:
        for line in f:
            items = [item.strip() for item in line.strip().split('|')]
            ground_truth.append(items)
    return ground_truth

def calculate_hitrate(recommendations, ground_truth):
    """
    Calculates hitrate@10.
    A hit is counted if at least one recommended item is in the ground truth list for a user.
    """
    num_users_gt = len(ground_truth)
    num_users_rec = len(recommendations)

    if num_users_rec != num_users_gt:
        print(f"Warning: Number of users in recommendations ({num_users_rec}) does not match ground truth ({num_users_gt}).")
        # Use the smaller number of users for calculation to avoid errors
        num_users = min(num_users_rec, num_users_gt)
        recommendations = recommendations[:num_users]
        ground_truth = ground_truth[:num_users]
    else:
        num_users = num_users_gt

    if num_users == 0:
        return 0.0, 0, 0

    hits = 0
    for i in range(num_users):
        # Handle cases where recommendation list might be shorter than 10
        rec_set = set(recommendations[i])
        gt_set = set(ground_truth[i])
        
        if not rec_set.isdisjoint(gt_set):
            hits += 1
            
    hitrate = hits / num_users if num_users > 0 else 0.0
    return hitrate, hits, num_users

def main():
    # Hardcoded file paths relative to the script's location
    recommendations_file = "Output-NoShot.txt"
    ground_truth_file = "../Data/recommendations.txt"

    recommendations = load_recommendations(recommendations_file)
    ground_truth = load_ground_truth(ground_truth_file)

    hitrate, hits, total_users = calculate_hitrate(recommendations, ground_truth)

    print(f"Total users: {total_users}")
    print(f"Hits: {hits}")
    print(f"Hitrate@10: {hitrate:.4f}")

if __name__ == "__main__":
    main()
