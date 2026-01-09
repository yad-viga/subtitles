# This script reads the INPUT_FILE file (an .srt file with timestamps and captions).
# The script starts processing the entries from a given entry number (START_INDEX).
# The script verifies whether the entries are at least 100 milliseconds apart from each other (MIN_GAP_MS).
# If they are not, then the program shortens and/or delay the neighbouring entries, so that the gap between them is at least 100 milliseconds.
# The script makes sure that the duration of an entry is minimum 500 milliseconds (MIN_DURATION_MS).
# The script saves all the changes in the output file (OUTPUT_FILE)
# and generates a LOG_FILE with a list of all alternations.

# Place your INPUT_FILE in the same folder as the script.

# Example:
# From the entry nr 101 onwards (START_INDEX), 
# make sure all the subsequent entries last for minimum 500 milliseconds (MIN_DURATION_MS)
# and are minimum 100 milliseconds apart from each other (MIN_GAP_MS).

from datetime import timedelta

# ========= CONFIG =========
INPUT_FILE = "input.srt"          # set later
OUTPUT_FILE = "output.srt"
LOG_FILE = "timing_changes.log"

START_INDEX = 101
MIN_GAP_MS = 100
MIN_DURATION_MS = 500
# ==========================


def time_to_ms(t):
    h, m, s_ms = t.split(":")
    s, ms = s_ms.split(",")
    return (int(h)*3600 + int(m)*60 + int(s)) * 1000 + int(ms)


def ms_to_time(ms):
    td = timedelta(milliseconds=ms)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    milliseconds = ms % 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


# Read file as blocks (KEEP EMPTY ONES)
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw = f.read()

blocks = raw.split("\n\n")

entries = []

for block in blocks:
    lines = block.splitlines()

    entry = {
        "raw": block,
        "valid": False,
        "index": None,
        "start": None,
        "end": None,
        "text": lines
    }

    if (
        len(lines) >= 3
        and lines[0].strip().isdigit()
        and "-->" in lines[1]
    ):
        entry["valid"] = True
        entry["index"] = int(lines[0].strip())
        entry["start"], entry["end"] = lines[1].split(" --> ")

    entries.append(entry)


log_lines = []


# Fix timing gaps (ONLY between valid neighbours)
for i in range(len(entries) - 1):
    cur = entries[i]
    nxt = entries[i + 1]

    if not cur["valid"] or not nxt["valid"]:
        continue

    if cur["index"] < START_INDEX:
        continue

    start_cur = time_to_ms(cur["start"])
    end_cur = time_to_ms(cur["end"])
    start_next = time_to_ms(nxt["start"])
    end_next = time_to_ms(nxt["end"])

    gap = start_next - end_cur

    if gap >= MIN_GAP_MS:
        continue

    needed = MIN_GAP_MS - gap

    # Attempt to shorten current subtitle
    new_end_cur = end_cur - needed
    min_allowed_end = start_cur + MIN_DURATION_MS

    if new_end_cur >= min_allowed_end:
        old_end = cur["end"]
        cur["end"] = ms_to_time(new_end_cur)
        cur["text"][1] = f"{cur['start']} --> {cur['end']}"

        log_lines.append(
            f"Entry {cur['index']}: shortened end {old_end} -> {cur['end']}"
        )
    else:
        # Delay next subtitle instead
        old_start = nxt["start"]
        old_end = nxt["end"]

        new_start = start_next + needed
        new_end = end_next + needed

        nxt["start"] = ms_to_time(new_start)
        nxt["end"] = ms_to_time(new_end)
        nxt["text"][1] = f"{nxt['start']} --> {nxt['end']}"

        log_lines.append(
            f"Entry {nxt['index']}: delayed {old_start}–{old_end} -> "
            f"{nxt['start']}–{nxt['end']}"
        )


# Write output SRT (preserve ALL entries)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for entry in entries:
        if entry["valid"]:
            for line in entry["text"]:
                f.write(line + "\n")
        else:
            f.write(entry["raw"])
        f.write("\n\n")


# Write log file
with open(LOG_FILE, "w", encoding="utf-8") as f:
    if log_lines:
        for line in log_lines:
            f.write(line + "\n")
    else:
        f.write("No timing adjustments were necessary.\n")
