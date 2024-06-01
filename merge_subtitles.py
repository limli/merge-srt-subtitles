#!/usr/bin/env python

import srt  # for srt format handling
import glob  # for unix style filename matching
import sys  # input arguments
import getopt  # to raise error in case of incorrect arguments
import argparse

def main(argv):
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='merge subtitles',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-p',
        help='primary language',
        required=True)
    parser.add_argument(
        '-s',
        help='secondary language',
        required=True)
    args = parser.parse_args()
    primary_language = args.p
    secondary_language = args.s

    # Read files and convert to list
    primary_path = primary_language
    secondary_path = secondary_language
    primary_file = open(primary_path, 'r', errors='ignore')
    primary_text = primary_file.read()
    primary_file.close()
    secondary_file = open(secondary_path, 'r', errors='ignore')
    secondary_text = secondary_file.read()
    secondary_file.close()
    subtitle_generator_primary = srt.parse(primary_text)
    subtitles_primary = list(subtitle_generator_primary)
    subtitle_generator_secondary = srt.parse(secondary_text)
    subtitles_secondary = list(subtitle_generator_secondary)

    # Make primary yellow
    for s in subtitles_primary:
        s.content = s.content

    # Place secondary on top
    for s in subtitles_secondary:
        s.content = '{\\an8}' + s.content

    # Merge
    subtitles_merged = subtitles_primary + subtitles_secondary
    subtitles_merged = list(srt.sort_and_reindex(subtitles_merged))

    # Write merged to file
    merged_path = primary_path.replace(primary_language, 'merged')
    merged_text = srt.compose(subtitles_merged)
    merged_file = open(merged_path, 'w')
    merged_file.write(merged_text)
    merged_file.close()


if __name__ == "__main__":
    main(sys.argv[1:])
