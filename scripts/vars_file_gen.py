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
            row["http_profile"] = "/" + row["shared_path"] + "/" + row["http_profile"]
            row["tcp_profile"] = "/" + row["shared_path"] + "/" + row["tcp_profile"]
            row["persist_profile"] = "/" + row["shared_path"] + "/" + row["persist_profile"]
            row["policy_vs"] = "/" + row["shared_path"] + "/" + row["policy_vs"]
            row["cert_chain"] = "/" + row["shared_path"] + "/" + row["cert_chain"]
            row["cert_name"] = "/" + row["shared_path"] + "/" + row["app_cert"] + ".crt"
            row["cert_key"] = "/" + row["shared_path"] + "/" + row["app_cert"] + ".key"
            row["pool_name"] = row["application_name"] + "_Pool" 
            row["client_ssl_pf"] = row["application_name"] + "_CL" 
            row["slow_rptime"] = int(row["slow_rptime"])
        
            for item, value in row.iteritems():
                out_file.write("%s: \"%s\"" % (item, value))
                out_file.write("\n")
            pool_name = row["application_name"] + "_Pool"
            out_file.write("pool_members:\n")
            pool_ips = row["pool_members_ips"].split(",")
            for ip in pool_ips:
                out_file.write("- name: \"%s\"\n" % ip) 
                out_file.write("  port: \"%s\"\n" % row["pool_member_port"]) 
                out_file.write("  ip: \"%s\"\n" % ip) 
                out_file.write("  status: true\n") 

            out_file.write("virtual_servers:\n")
            virtual_ips = row["virtual_servers_ips"].split(",")
            i = 0
            for ip in virtual_ips:
                vname = row["application_name"] + "_vs" + str(i)
                out_file.write("- name: \"%s\"\n" % vname)
                out_file.write("  ip: \"%s\"\n" % ip)
                i = i + 1
 
    except csv.Error as error:
        sys.exit("outfile %s, infile %s, line %d:, %s" % (out_file, in_file,
                                                 reader.line_num, error))

in_file.close()
out_file.close()
