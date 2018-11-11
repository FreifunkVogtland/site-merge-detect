#!/usr/bin/python3
# -*- coding: utf-8; -*-

import json
import os
import os.path
import sys


def load_whitelisted():
    whitelisted_sites = json.load(open('whitelisted_sites.json'))

    if type(whitelisted_sites) is not list:
        raise Exception('whitelisted_sites.json not a simple list')

    for site in whitelisted_sites:
        if type(site) is not str:
            raise Exception('whitelisted_sites entry not a string')

    return whitelisted_sites


def get_nodes(meshviewer):
    nodes = {}

    for node in meshviewer['nodes']:
        node_id = node.get('node_id')
        if node_id is None:
            continue

        domain = node.get('domain')
        if domain is None:
            continue

        nodes[node_id] = domain

    return nodes


def get_nodes_with_invalid_sites(nodes, whitelisted):
    invalid = []

    if not whitelisted:
        return invalid

    for node_id in nodes:
        if nodes[node_id] not in whitelisted:
            invalid.append({
                'node_id': node_id,
                'domain': nodes[node_id],
            })

    return invalid


def print_invalid_site_nodes(invalid_site_nodes):
    print("Nodes with invalid domain found")
    print("===============================\n")

    for node in invalid_site_nodes:
        print(" * {node_id} ({domain})".format(**node))

    print()


def get_intersite_links(nodes, meshviewer):
    intersite = []
    links = set()

    for link in meshviewer['links']:
        source_domain = nodes.get(link['source'])
        if source_domain is None:
            continue

        target_domain = nodes.get(link['target'])
        if target_domain is None:
            continue

        if source_domain == target_domain:
            continue

        if link['source'] < link['target']:
            node_id1 = link['source']
            domain1 = source_domain
            node_id2 = link['target']
            domain2 = target_domain
        else:
            node_id1 = link['target']
            domain1 = target_domain
            node_id2 = link['source']
            domain2 = source_domain

        linkid = (node_id1, link['type'], node_id2)
        if linkid in links:
            continue

        links.add(linkid)

        intersite.append({
            'domain1': domain1,
            'node_id1': node_id1,
            'type': link['type'],
            'node_id2': node_id2,
            'domain2': domain2,
        })

    return intersite


def print_intersite_links(intersite_links):
    print("Links with different domain found")
    print("=================================\n")

    for link in intersite_links:
        fmt = " * {node_id1} ({domain1})"
        fmt += " <--({type})--> "
        fmt += "{node_id2} ({domain2})"
        print(fmt.format(**link))

    print()


def main():
    if len(sys.argv) != 2:
        print("./site-merge-detect.py nodes.json")
        sys.exit(1)

    meshviewer_in = sys.argv[1]

    # load
    meshviewer = json.load(open(meshviewer_in, encoding='utf-8'))
    whitelisted = load_whitelisted()

    # process
    nodes = get_nodes(meshviewer)
    invalid_site_nodes = get_nodes_with_invalid_sites(nodes, whitelisted)
    intersite_links = get_intersite_links(nodes, meshviewer)

    # list errors
    exit_code = 0

    if invalid_site_nodes:
        exit_code = 1
        print_invalid_site_nodes(invalid_site_nodes)

    if intersite_links:
        exit_code = 1
        print_intersite_links(intersite_links)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
