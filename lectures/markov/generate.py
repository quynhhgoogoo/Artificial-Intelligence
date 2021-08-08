import markovify
import sys

# Read text from file
if len(sys.argv) != 2:
    sys.exit("Usage: python generate.py file.txt")
print("Loading data...")

with open(sys.argv[1]) as f:
    text = f.read()

# Train model
text_model = markovify.Text(text)

# Generate sentence
print()
for i in range(5):
    print(text_model.make_sentence())
    print()
