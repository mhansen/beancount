#!/usr/bin/env python3
"""
Parse and realize a beancount input file and output a tree of balances.
"""
import argparse
import datetime

from beancount import load
from beancount.core import realization


# FIXME: This will move into beancount.core.realization.

def reorder_accounts_tree(real_accounts):
    """Reorder the children in a way that is sensible for display.
    We want the most active accounts near the top, and the least
    important ones at the bottom."""

    reorder_accounts_node_by_declaration(real_accounts.get_root())


def reorder_accounts_node_by_declaration(real_account):

    children = []
    for child_account in real_account.children:
        fileloc = reorder_accounts_node_by_declaration(child_account)
        children.append( (fileloc, child_account) )

    children.sort()
    real_account.children[:] = [x[1] for x in children]

    print(real_account.fullname)
    for fileloc, child in children:
        print('  {:64}  {}'.format(child.name, fileloc))
    print()

    if real_account.postings:
        fileloc = real_account.postings[0].fileloc
    else:
        fileloc = children[0][0]
    return fileloc



def reorder_accounts_node_by_date(real_account):

    children = []
    for child_account in real_account.children:
        reorder_accounts_node_by_date(child_account)
        children.append( (child_date, child_account) )
    children.sort(reverse=True)

    real_account.children[:] = [x[1] for x in children]

    last_date = children[0][0] if children else datetime.date(1970, 1, 1)

    if real_account.postings:
        last_posting = real_account.postings[-1]
        if hasattr(last_posting, 'date'):
            date = last_posting.date
        else:
            date = last_posting.entry.date

        if date > last_date:
            last_date = date

    return last_date


def main():
    parser = argparse.ArgumentParser(__doc__.strip())
    parser.add_argument('filename', help='Beancount input filename.')
    opts = parser.parse_args()

    entries, errors, options = load(opts.filename, do_print_errors=True)
    real_accounts = realization.realize(entries)
    reorder_accounts_tree(real_accounts)
    realization.dump_tree_balances(real_accounts)


if __name__ == '__main__':
    main()
