import re
import json
from collections import defaultdict

class WordPieceTokenizer:
    def __init__(self, vocab_limit=1000):
        self.vocab = []
        self.vocab_limit = vocab_limit
        self.common_words = { 
            "a", "an", "the", "and", "or", "but", "if", "while", "with",
            "in", "on", "at", "to", "of", "for", "by", "as",
            "this", "that", "these", "those",
            "what", "which", "who", "whom", "where", "when",
            "why", "how", "only", "own", "same",
            "so", "than", "too"
        }  # Manually defined stopwords

    def clean_text(self, text):
        text = text.lower().strip()
        text = re.sub(r"\s+", ' ', text)  # Remove extra spaces
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        words = text.split()
        return [word for word in words if word not in self.common_words]  # Remove stopwords

    def calculate_pair_scores(self, split_map, word_count):
        letter_count = defaultdict(int)
        pair_count = defaultdict(int)

        for word, count in word_count.items():
            parts = split_map[word]
            if len(parts) == 1:
                letter_count[parts[0]] += count
                continue

            for j in range(len(parts) - 1):
                pair = (parts[j], parts[j + 1])
                letter_count[parts[j]] += count
                pair_count[pair] += count
            letter_count[parts[-1]] += count

        if not pair_count:
            return {}

        return {
            pair: freq / (letter_count[pair[0]] + letter_count[pair[1]] + 1e-5)
            for pair, freq in pair_count.items()
        }

    def merge_best_pair(self, token_a, token_b, split_map):
        for word in split_map.keys():
            parts = split_map[word]
            if len(parts) <= 1:
                continue
            new_split = []
            index = 0
            while index < len(parts):
                if index < len(parts) - 1 and parts[index] == token_a and parts[index + 1] == token_b:
                    combined = token_a + token_b[2:] if token_b.startswith("##") else token_a + token_b
                    new_split.append(combined)
                    index += 2
                else:
                    new_split.append(parts[index])
                    index += 1
            split_map[word] = new_split
        return split_map

    def build_vocabulary(self, tokenized_corpus):
        word_count = defaultdict(int)
        for token in tokenized_corpus:
            word_count[token] += 1

        split_map = {
            word: [c if i == 0 else f"##{c}" for i, c in enumerate(word)]
            for word in word_count.keys()
        }

        alphabet_set = sorted({char for word in word_count for char in word})
        self.vocab = ["[PAD]", "[UNK]"] + alphabet_set  # Unique tokens were used

        while len(self.vocab) < self.vocab_limit:
            pair_scores = self.calculate_pair_scores(split_map, word_count)
            if not pair_scores:
                break  # No more pairs to merge, but continue the process

            best_pair, _ = max(pair_scores.items(), key=lambda x: x[1])

            split_map = self.merge_best_pair(best_pair[0], best_pair[1], split_map)
            merged_token = (
                best_pair[0] + best_pair[1][2:] if best_pair[1].startswith("##")
                else best_pair[0] + best_pair[1]
            )

            # Add merged tokens and other tokens to the vocab without restrictions
            if merged_token not in self.vocab:
                self.vocab.append(merged_token)

            # Allow the vocabulary to grow beyond frequent subword pairs
            if len(self.vocab) >= self.vocab_limit:
                break

        # Add any leftover single words to the vocabulary
        for word in word_count:
            if word not in self.vocab:
                self.vocab.append(word)
            if len(self.vocab) >= self.vocab_limit:
                break

        print(f"Constructed Vocabulary: {len(self.vocab)}")

    def save_vocabulary(self, path):
        with open(path, "w") as f:
            for token in self.vocab:
                f.write(token + "\n")

    def encode_single_word(self, word):
        token_list = []
        while word:
            index = len(word)
            while index > 0 and word[:index] not in self.vocab:
                index -= 1

            if index == 0:
                # Instead of `[UNK]`, break word into meaningful subwords
                subwords = [word[:i] for i in range(2, len(word) + 1) if word[:i] in self.vocab]
                if subwords:
                    token_list.extend(subwords)
                else:
                    token_list.append("[UNK]")
                break

            token_list.append(word[:index])
            word = word[index:]
            if word:
                word = f"##{word}"
        return token_list

    def tokenize_corpus(self, input_data):
        tokenized_results = []
        for entry in input_data:
            sentence = entry['sentence']
            sentence_id = entry['id']
            words = self.clean_text(sentence)
            tokens = []
            for word in words:
                tokens.extend(self.encode_single_word(word))
            tokenized_results.append({'id': sentence_id, 'tokens': tokens})
        return tokenized_results


if __name__ == "__main__":
    user_input = input("Enter vocabulary size (default is 1000): ").strip()
    vocab_limit = int(user_input) if user_input.isdigit() else 1000  # Default to larger vocab size

    with open("corpus.txt", "r") as corpus_file:
        text_data = corpus_file.read()

    with open("sample_test.json", "r") as sample_file:
        input_sentences = json.load(sample_file)

    tokenizer = WordPieceTokenizer(vocab_limit)
    preprocessed_tokens = tokenizer.clean_text(text_data)
    tokenizer.build_vocabulary(preprocessed_tokens)
    tokenizer.save_vocabulary("vocabulary.txt")
    tokenized_output = tokenizer.tokenize_corpus(input_sentences)

    with open("tokenized_data.json", "w") as output_file:
        json.dump(tokenized_output, output_file, indent=4)
