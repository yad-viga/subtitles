# This script reads the INPUT_FILE file (an .srt file with timestamps and captions).
# The script moves all the entries up by a specified number of positions (SHIFT_UP)
# starting from the entry nr START_ENTRY until the entry nr END_ENTRY.
# The script saves all the changes in the output file (OUTPUT_FILE).
# Place your INPUT_FILE in the same folder as the script.
# Known issue: 
# The first moved entry keeps its original number in the OUTPUT_FILE.
# You need to correct this number manually. All the subsequent numbers
# are aligned with the new flow.

# ========= CONFIG =========
INPUT_FILE = "input.srt"      # change later
OUTPUT_FILE = "output.srt"

START_ENTRY = 208
END_ENTRY = 309
SHIFT_UP = 5
# ==========================


# Read file
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Split into subtitle blocks (keep empty ones)
blocks = content.split("\n\n")

total = len(blocks)

# Make a copy for output
new_blocks = blocks.copy()

# Convert to 0-based indices
start_idx = START_ENTRY - 1
end_idx = min(END_ENTRY - 1, total - 1)

# Move blocks up
for i in range(start_idx, end_idx + 1):
    new_blocks[i - SHIFT_UP] = blocks[i]

# Leave the last shifted positions empty
for i in range(end_idx - SHIFT_UP + 1, end_idx + 1):
    if i < total:
        new_blocks[i] = ""

# Renumber entries (preserve text & timestamps)
output_blocks = []

for i, block in enumerate(new_blocks, start=1):
    lines = block.splitlines()

    if lines and lines[0].strip().isdigit():
        lines[0] = str(i)
        output_blocks.append("\n".join(lines))
    else:
        # Empty or malformed entry stays as-is
        output_blocks.append(block)

# Write output
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n\n".join(output_blocks))
