"""Analytics command line interface for DeepHyper.

It can be used with:

.. code-block:: console

    $ deephyper-analytics --help

    Command line to analysis the outputs produced by DeepHyper.

    positional arguments:
    {notebook,quickplot,topk}
                            Kind of analytics.
        notebook            Generate a notebook with different types of analysis
        quickplot           Tool to generate a quick 2D plot from file.
        topk                Print the top-k configurations.

    optional arguments:
    -h, --help            show this help message and exit
"""
import argparse
import sys

from deephyper.core.analytics import _topk, _quick_plot



def create_parser():
    """
    :meta private:
    """
    parser = argparse.ArgumentParser(description="Command line to analysis the outputs produced by DeepHyper.")

    subparsers = parser.add_subparsers(help="Kind of analytics.")

    mapping = dict()

    modules = [
        _quick_plot,  # output quick plots
        _topk
    ]

    for module in modules:
        name, func = module.add_subparser(subparsers)
        mapping[name] = func

    return parser, mapping


def main():
    """
    :meta private:
    """
    parser, mapping = create_parser()

    args = parser.parse_args()

    mapping[sys.argv[1]](**vars(args))
