#!/usr/bin/env python
import sys
import os
from pathlib import Path

import argparse
from distutils.util import strtobool

from skillmap.skillmap_parser import SkillMapParser
from skillmap.skillmap_visitor import SkillMapVisitor

import importlib.metadata

package_metadada = importlib.metadata.metadata("skillmap")
# info from pyproject.toml's `version` and `description`
SKILLMAP_VERSION = package_metadada.get("Version")
SKILLMAP_SUMMARY = package_metadada.get("Summary")


def _skillmap_parser():
    parser = argparse.ArgumentParser(prog="skillmap")
    parser.add_argument(
        "descriptor_toml",
        default=False,
        type=str,
        help="The path to a toml file describing the skillmap",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {SKILLMAP_VERSION} [{SKILLMAP_SUMMARY}]",
        help="show version number",
    )

    # parser.add_argument(
    #     "-f",
    #     "--format",
    #     type=str,
    #     default="mermaid",
    #     help="export format, [mermaid] are supported",
    # )
    return parser


def parse_sys_args(sys_args):
    parser = _skillmap_parser()
    args = parser.parse_args(sys_args)
    return vars(args)


def generate(skillmap_file, format = None):
    skillmap_dict = SkillMapParser().parse(skillmap_file)
    skillmap_graph = SkillMapVisitor().visit(skillmap_dict)
    return skillmap_graph


def main():
    args = parse_sys_args(sys.argv[1:])
    skillmap_file = Path(args["descriptor_toml"])
    # format = args["format"]
    skillmap_graph = generate(skillmap_file, format)
    print(skillmap_graph)
