#!/usr/bin/env  python

import argparse
import sys
import os
import csv

parser = argparse.ArgumentParser(description='''
Takes one CSV file containing app parameters, and
turns them into YAML for use by Ansible/Jinja2 config generation process.''')

parser.add_argument('-o', nargs='?', type=argparse.FileType('wb', 0),
                    default=sys.stdout, metavar='outFile',
                    help='YAML file to write to')

parser.add_argument('-i', nargs='*', type=argparse.FileType('rb', 0),
                    default=sys.stdin, metavar='inFile',
                    help='CSV file(s) to read from')

parser.add_argument('-debug', action='store_true', help='Enable Debug Mode')

args = parser.parse_args()

debug = args.debug
out_file = args.o

if debug:
    print >> sys.stderr, args

def append_shared_path(shared_path, item_name):
    item_full_name = "/" + shared_path + "/" + item_name
    return item_full_name

out_file.write("---\n\n")

for in_file in args.i:
    list_name = "stdin"
    try:
        list_name = os.path.splitext(os.path.basename(in_file.name))[0]
    except AttributeError as error:
        print >> sys.stderr, "Dictionary will named %s, this mode is flaky." % (list_name)

    list_name = list_name.replace("-", "_")

    if debug:
        print >> sys.stderr, "%s -> %s\n" % (list_name, out_file.name)

    pool_ips = []
    virtual_ips = []
    reader = csv.DictReader(in_file, dialect='excel')
    out_file.write("%s:\n\n" % (list_name))
    try:
        for row in reader:
            row["primary_server"] = append_shared_path(row["shared_path"], row["primary_server"])
            row["secondary_server"] = append_shared_path(row["shared_path"], row["secondary_server"])

            for item, value in row.iteritems():
                out_file.write("%s: \"%s\"" % (item, value))
                out_file.write("\n")

            gslb_pool_name = row["application_name"] + "_Pool"
            out_file.write("gslb_pool: \"%s\"\n" % gslb_pool_name)
            pool_monitors = row["gslb_pool_monitors"].split(",")
            out_file.write("gslb_pool_monitors:\n")
            for monitor in pool_monitors:
                monitor = append_shared_path(row["shared_path"], monitor)
                out_file.write("- name: \"%s\"\n" % monitor) 

    except csv.Error as error:
        sys.exit("outfile %s, infile %s, line %d:, %s" % (out_file, in_file,
                                                 reader.line_num, error))

in_file.close()
out_file.close()

