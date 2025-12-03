**🎵 Music-Recommendation**

**In-Context Learning (ICL) Music Recommendation using Gemma 3 (4B) with BPR-MF Baseline**

This repository explores how Large Language Models (LLMs)—specifically **Gemma 3 (4B)**—perform music recommendation via **In-Context Learning (ICL)** and **Chain-of-Thought (CoT)** reasoning.
To benchmark LLM performance, we implement a traditional collaborative filtering model using **BPR-MF** and compare it against LLM-based recommendations.

---

## 📁 Repository Structure

```
Music-Recommendation/
│
├── BPR/                      
│   ├── BPR_MF.py                     # BPR-MF model implementation
│   ├── data.py                       # Dataset loader + negative sampling
│   ├── main.py                       # Training & evaluation entry point
│   └── preprocess_data.py            # Data preprocessing for experiments
│
├── Data/
│   └── prompt_ADM.txt                # Input prompt template for LLM-Rec
│
├── LLM4Music/
│   ├── LLM4Rec.py                    # LLM-based recommender pipeline (Zero/Few-shot)
│   │
│   ├── CoT_manual_inspection.md      # Manual inspection of chain-of-thought samples
│   ├── CoT_reasoning_process.txt     # Model reasoning traces
│   ├── CoT_recommendations.txt       # Generated LLM recommendations
│   │
│   ├── Output-NoShot.txt             # Zero-shot recommendation output
│   ├── Output - FewShot.txt          # Few-shot recommendations (set 1)
│   ├── Output - FewShot2.txt         # Few-shot recommendations (set 2)
│   ├── Output - Recommendations - Few Shot.txt   # Formatted few-shot results
│   ├── Output - Recommendations - Zero Shot.txt  # Formatted zero-shot results
│   ├── Output_result.txt             # Final combined results summary
│   │
│   ├── Reasoning - Few Shot.txt      # Few-shot reasoning traces
│   ├── Reasoning- Zero Shot.txt      # Zero-shot reasoning traces
│   │
│   ├── calculate_hitrate.py          # Evaluation: hit-rate & ranking metrics
│   └── process_data.py               # Preprocessing scripts for LLM data
│
├── .gitignore                        # Git ignore file
└── README.md                         # Project introduction & usage
```

---

## 🎯 Project Goal

This project answers:

> **Can an LLM infer user music preferences from a few examples and generate high-quality recommendations, comparable to collaborative filtering?**

We compare:

* **BPR-MF**: Pure collaborative filtering baseline
* **Gemma 3 (4B) ICL**: LLM reasoning over music taste
* **Gemma 3 (4B) CoT**: Adding chain-of-thought explanation + refinement

---

## 🧠 Methods

### **1️⃣ BPR-MF Baseline**

We implement Bayesian Personalized Ranking with Matrix Factorization.

Included:

* Implicit feedback
* Pairwise ranking loss
* Uniform negative sampling
* HR@K and NDCG@K metrics
* Amazon Digital Music preprocessing

Run training:

```bash
cd BPR
python main.py
```

---

### **2️⃣ LLM Recommendation (Gemma 3:4B)**

Gemma is used to perform:

* Zero-shot
* Few-shot ICL
* Multi-shot preference summarization
* Chain-of-Thought reasoning
* Conversational recommendation refinement

All reasoning and generated outputs are saved under:

```
LLM4Music/CoT_reasoning_process.txt
LLM4Music/CoT_recommendations.txt
LLM4Music/Output-*.txt
```

Run the LLM pipeline:

```bash
cd LLM4Music
python LLM4Rec.py 
```

Example prompt (`prompt_ADM.txt`):

```
Below is the user's music history. Infer their taste and recommend 5 new songs.
Explain your reasoning step-by-step.

User History:
...
```

---

## 📊 Evaluation

We evaluate:

### **Quantitative (Baseline Only)**

* HitRate@10

### **Qualitative (LLM)**

* Genre consistency
* Artist similarity
* Mood coherence
* Reasoning correctness
* Multi-turn adaptability

A final comparison table (placeholder):

| Model      | Setting     | HitRate@10  | Notes                    |
| ---------- | ----------- | ----------- | ------------------------ |
| BPR-MF     | CF baseline |   0.0256    | Standard MF + BPR        |
| Gemma 3 4B | Zero-shot   | —           | Uses no examples         |
| Gemma 3 4B | Few-shot    | —           | 1–3 example preferences  |
| Gemma 3 4B | CoT         |   0.0000    | Chain-of-thought enabled |

---

## 🚀 Getting Started

### **Run BPR baseline**

```bash
python BPR/main.py
```

### **Run LLM inference**

```bash
python LLM4Music/LLM4Rec.py
```
