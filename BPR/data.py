import numpy as np
import torch
from pathlib import Path

class DataLoader():
    def __init__(self, root_path = "./BPR_MF", dataset = "ml_1M"):
        self.path = Path(root_path) / dataset
        if not self.path.exists():
            raise FileNotFoundError(f"Dataset {dataset} not found: {self.path}")

        self.allPos = []
        self.testPos = []
        self.max_item = 0
        self.cnt = 0

        # ----------import training data ----------
        train_path = self.path /"train.csv"
        with train_path.open(mode="r") as f_train:
            for line in f_train:
                item_list = list(map(int, line.strip().split(' ')))
                self.allPos.append([])
                for item in item_list[1:]:
                    self.max_item = max(self.max_item, item + 1)
                    self.cnt += 1
                    self.allPos[-1].append(item)

        self.n_user = len(self.allPos)

        # ---------- import testing data ----------
        test_path = self.path /"test.csv"
        with test_path.open("r") as f_test:
            for line in f_test:
                target_item = list(map(int, line.strip().split(' ')))
                self.testPos.append(target_item[1])

    def generate_data(self, batch_size):
        users = np.random.randint(0, self.n_user, self.cnt)

        for i in range(0, self.n_user, batch_size):
            pos_items, neg_items = [], []
            for user in users[i: i + batch_size]:
                pos_items.append(np.random.choice(self.allPos[user]))
                t = np.random.randint(self.max_item)
                while t in self.allPos[user]:
                    t = np.random.randint(self.max_item)
                neg_items.append(t)
            yield users[i: i + batch_size],pos_items, neg_items

    def evaluate(self,model, device, Ks=(10,), n_neg = 99):
        #AUC, Hit Rate@K & NDCG@K
        AUC_list = []
        HR_K = {K: [] for K in Ks}
        NDCG_list = {K: [] for K in Ks}

        model.eval()
        with torch.no_grad():
            for user_id in range(self.n_user):
                items = [self.testPos[user_id]]
                for _ in range(n_neg):
                    t = np.random.randint(self.max_item)
                    while t in self.allPos[user_id] or t == items[0]:
                        t = np.random.randint(self.max_item)
                    items.append(t)

                users = torch.tensor([user_id] * (n_neg + 1), dtype = torch.long, device = device)
                items_t = torch.tensor(items, dtype = torch.long, device = device)

                #scores[0] - positive
                scores = model.forward(users, items_t).detach().cpu().numpy()

                #AUC (positive > negative)
                wins = np.sum(scores[0] > scores[1:])
                AUC_list.append(wins / float(n_neg))

                #HR@K & NDCG@K
                order = np.argsort(-scores)
                rank = int(np.where(order==0)[0][0]) + 1

                for K in Ks:
                    hit = 1 if rank <= K else 0
                    HR_K[K].append(hit)
                    NDCG = (1.0 / np.log2(1 + rank)) if hit else 0
                    NDCG_list[K].append(NDCG)

        results = {"AUC": float(np.mean(AUC_list)) if AUC_list else 0.0}
        results.update({f"HR@{K}": float(np.mean(HR_K[K])) for K in Ks})
        results.update({f"NDCG@{K}": float(np.mean(NDCG_list[K])) for K in Ks})

        return results
