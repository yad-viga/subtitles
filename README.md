# subtitles
This repository contains scripts to process .srt files.

An SRT file is a plain text subtitle file that contains dialogue and timestamps, used to display captions or subtitles on videos.

When a file with captions is long, it is worth to automate actions.

Examples of such actions can be the following:

* **Enforce a minimum time distance between the entries and a minimum entry duration**
  
  Make sure the timestamps are minimum 100 milliseconds apart from each other AND the duration of an entry is minimum 500 milliseconds.

* **Move the entries up**
  
  Move all the entries, starting from a given entry, up by a given nr of positions. 
For example, move all the entries up by 10 positions, starting from the entry nr 53.
Move only the text, not its timestamps. Keep the timing as it was in the original file.
See: [move-entries-up-by-a-given-nr](https://github.com/yad-viga/subtitles/blob/main/move-entries-up-by-a-given-nr)

Find more details about each script in the comments of respective files.
The filenames are self-describing.
The code from the scripts can be executed in https://colab.research.google.com. It is an environment available for free.
