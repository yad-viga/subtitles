# subtitles
This repository contains scripts I used to process .srt files.

An SRT file is a plain text subtitle file that contains dialogue and timestamps, used to display captions or subtitles on videos.

When a file with captions is long, it is worth to automate actions.

Examples of such actions can be the following:

*) Make sure the timestamps are minimum 100 milliseconds apart from each other AND the duration of an entry is minimum 500 milliseconds.

*) Move all the entries, starting from a given entry (eg. from entry nr 53), up by 10 positions. Move only the text, not its timing. Keep the timing as it was in the original file.

More details about each script are commented out in respective files.
The filenames are self-describing.
The code from the scripts can be executed in https://colab.research.google.com. It is an environment available for free.
