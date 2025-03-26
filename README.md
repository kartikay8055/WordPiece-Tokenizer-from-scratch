# 🚀 WordPiece Tokenizer 

## 📌 Overview
This project implements a **WordPiece Tokenizer from scratch**, allowing users to specify the vocabulary size. 
### 🔥 Key Features:
- Customizable vocabulary size
- Efficient tokenization using subword merging
- Stopword removal and text preprocessing
- Outputs tokenized sentences in JSON format
- Saves vocabulary for reuse

---

## 📖 Task 1: WordPiece Tokenizer Implementation

### 🛠️ 1. Preprocessing
- **Lowercasing** – Ensures uniformity and removes case-sensitive discrepancies.
- **Whitespace Normalization** – Eliminates leading/trailing spaces and replaces multiple spaces with a single space.
- **Special Character Removal** – Removes punctuation and symbols.
- **Stopword Removal** – Filters out common words like *the, and, in, of, for*.

---

### 📜 2. Vocabulary Construction
- **Initialization** – The vocabulary starts with special tokens `[PAD]` and `[UNK]`.
- **Character Breakdown** – Each word is split into individual characters.
- **Subword Identification**:
  - Frequent adjacent character pairs are identified.
  - The most frequent pair is merged into a new subword.
  - This process continues until the vocabulary size is reached.

- **Example Vocabulary Tokens:**
  ```
  [PAD]
  [UNK]
  ##ing
  abou
  ##el
  ##eling
  fe
  feel
  feeling
  ```

- **Final vocabulary is saved in** `vocabulary.txt`.

---

### 🔗 3. Tokenization
- **Token Mapping** – Words are converted into subword representations.
- **Longest-Match-First Principle**:
  - The longest subword match from the vocabulary is selected.
  - When a word is split, all subwords except the first are prefixed with `"##"`.
- **Handling Unknown Words**:
  - If a word is not found in the vocabulary, it is decomposed into known subwords.
  - If no valid subwords exist, it is replaced with `[UNK]`.

- **Example Tokenization Output:**
  ```
  Input: "I am feeling great"
  Tokenized: ['I', 'am', 'feeling', '##ing', 'great']
  ```
- **Tokenized sentences are saved in** `tokenized_data.json`.

---

## ⚙️ How to Use
### 1️⃣ Run the Tokenizer
```sh
python tokenizer.py
```
- You will be prompted to enter a vocabulary size.  
  *(Default is 1000 if no input is given.)*

### 2️⃣ Input Files:
- `corpus.txt` – The raw text corpus used to construct the vocabulary.
- `sample_test.json` – JSON file containing test sentences to tokenize.

### 3️⃣ Output Files:
- `vocabulary.txt` – The generated vocabulary.
- `tokenized_data.json` – Tokenized text results.

---

## 📌 Problem Statement
Implement a WordPiece Tokenizer from scratch, allowing a user-defined vocabulary size. Construct a vocabulary and apply it to text tokenization.

---

## 📎 Example JSON Input/Output
### 🔹 Input (`sample_test.json`):
```json
[
    {"id": 1, "sentence": "I am feeling happy today"},
    {"id": 2, "sentence": "Machine learning is exciting"}
]
```

### 🔹 Output (`tokenized_data.json`):
```json
[
    {"id": 1, "tokens": ["I", "am", "feeling", "##ing", "happy", "today"]},
    {"id": 2, "tokens": ["Machine", "learning", "is", "exciting"]}
]
```

---

## 📌 Requirements
- Python 3.x
- JSON module (built-in)
- Regex module (built-in)

---

## 🏆 Conclusion
This implementation provides a robust **WordPiece Tokenizer** with efficient vocabulary construction, preprocessing, and tokenization. It is designed for **NLP tasks** like embedding models and Neural Language Models.


