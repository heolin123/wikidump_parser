#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse
import re

def normalize(input_text):
    text = input_text.decode('utf-8')
    text = re.sub("&lt;", "<", text)
    text = re.sub("&gt;", ">", text)
    text = re.sub("&quot;", "\"", text)
    text = re.sub("&amp;", "&", text)
    text = re.sub("&nbsp;", " ", text)
    text = re.sub("{{[^}]*}}", "", text)
    text = re.sub("{ [^}]*}", "", text)
    text = re.sub("=[=]* [^=]*=[=]*", "" , text)
    text = re.sub("<[^>]*>([^<]*)</[^>]*>", r"\1", text)
    text = re.sub("\[\[[^\|]*\|([^\]]*)\]\]", r"\1", text)
    text = re.sub("\[\[([^\|]*)\]\]", r"\1", text)
    text = re.sub("\[[^\]]*\]", "", text)
    text = re.sub("<[^>]*>", "", text)
    text = re.sub("['„„”„”]+", "\"", text)
    text = re.sub("(^|\n)[ \*\[\]:;|=!a-z#].*\n", "", text)
    text = re.sub("(^|\n)[^ ]*:[^ ]*\n", "", text)
    text = re.sub("[\[\]]+", "", text)
    text = re.sub("[\n]*\n", "\n", text)
    text = re.sub("[.]*.\n", ".\n", text)
    splited = text.split('\n')
    splited = filter(lambda x: len(x) > 30, splited)
    return "\n".join(splited)


def normalize_file_name(file_name):
    return re.sub("[^a-z]*", "", file_name.lower())


def parse_wiki(input_path, output_file_path, one_file):
    with open(input_path, "r") as ins:
        current_title = ""
        current_text = ""
        read_text = False
        for line in ins:
            if "<title>" in line:
                current_title = re.findall("<title>([^<]*)</title>", line)[0]
            if "</page>" in line:
                normalized_text = normalize(current_text).encode('utf-8')
                if len(normalized_text) > 10:
                    if one_file:
                        output_file = open("{0}/{1}.txt".format(output_file_path, normalize_file_name(current_title)), "w")
                    else:
                        output_file = open(output_file_path, "a")

                    output_file.write(normalized_text)
                    output_file.close()
                current_text = ""
            if "</text>" in line:
                read_text = False
            if read_text:
                current_text += line + "\n"
            if "<text " in line:
                read_text = True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_path', required=True, help="Path to input wiki file")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output_dir', help="Path to output directory where output files will be stored")
    group.add_argument('--output_file', help="Path to one output file, where data will be stored")
    args = parser.parse_args()

    output_one_file = False
    if args.output_dir:
        output_path = args.output_dir
        output_one_file = True
    elif args.output_file:
        output_path = args.output_file

    parse_wiki(args.input_path, output_path, output_one_file)

