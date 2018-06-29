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

        site_code = node.get('site_code')
        if site_code is None:
            continue

        nodes[node_id] = site_code

    return nodes


def get_nodes_with_invalid_sites(nodes, whitelisted):
    invalid = []

    if not whitelisted:
        return invalid

    for node_id in nodes:
        if nodes[node_id] not in whitelisted:
            invalid.append({
                'node_id': node_id,
                'site_code': nodes[node_id],
            })

    return invalid


def print_invalid_site_nodes(invalid_site_nodes):
    print("Nodes with invalid site_code found")
    print("==================================\n")

    for node in invalid_site_nodes:
        print(" * {node_id} ({site_code})".format(**node))

    print()


def get_intersite_links(nodes, meshviewer):
    intersite = []
    links = set()

    for link in meshviewer['links']:
        source_site_code = nodes.get(link['source'])
        if source_site_code is None:
            continue

        target_site_code = nodes.get(link['target'])
        if target_site_code is None:
            continue

        if source_site_code == target_site_code:
            continue

        if link['source'] < link['target']:
            node_id1 = link['source']
            site_code1 = source_site_code
            node_id2 = link['target']
            site_code2 = target_site_code
        else:
            node_id1 = link['target']
            site_code1 = target_site_code
            node_id2 = link['source']
            site_code2 = source_site_code

        linkid = (node_id1, link['type'], node_id2)
        if linkid in links:
            continue

        links.add(linkid)

        intersite.append({
            'site_code1': site_code1,
            'node_id1': node_id1,
            'type': link['type'],
            'node_id2': node_id2,
            'site_code2': site_code2,
        })

    return intersite


def print_intersite_links(intersite_links):
    print("Links with different site_code found")
    print("====================================\n")

    for link in intersite_links:
        fmt = " * {node_id1} ({site_code1})"
        fmt += " <--({type})--> "
        fmt += "{node_id2} ({site_code2})"
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
