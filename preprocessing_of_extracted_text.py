import os
import re

input_dir = r"./output_cilanse"
output_dir = r"./cleaned_output_cilanse"
os.makedirs(output_dir, exist_ok=True)

def clean_text(text):
    # Remove non-standard characters except letters, numbers, punctuation
    text = re.sub(r"[^\w\s.,!?;:'\"()\[\]॥।–—\-]", "", text)

    # Normalize multiple newlines and spaces
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    # Fix common OCR artifacts
    text = text.replace(" | ", " I ").replace("|", "I")
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl")  # ligature fixes
    text = text.encode("utf-8", "ignore").decode("utf-8", "ignore")

    return text.strip()

# Process each OCR-extracted file
for file_name in os.listdir(input_dir):
    if file_name.endswith(".txt"):
        file_path = os.path.join(input_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        cleaned_text = clean_text(raw_text)

        # Save cleaned output
        cleaned_path = os.path.join(output_dir, file_name)
        with open(cleaned_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

print(f"✅ Preprocessing complete. Cleaned files saved to: {output_dir}")
