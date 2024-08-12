#!/usr/bin/env python
#
# This file is part of Cynthion.
#
# Copyright (c) 2023 Great Scott Gadgets <info@greatscottgadgets.com>
# SPDX-License-Identifier: BSD-3-Clause

""" Cynthion 'flash' command. """

import logging, platform, sys

from .util import find_cynthion_asset, find_cynthion_bitstream
from .util import flash_bitstream, flash_mcu_firmware, flash_soc_firmware


def cynthion_flash(device, args):
    if args.bitstream is not None:
        flash_bitstream(device, args.bitstream)
    elif args.mcu_firmware is not None:
        flash_mcu_firmware(device, args.mcu_firmware)
    elif args.soc_firmware is not None:
        flash_soc_firmware(device, args.soc_firmware)
    elif args.target == "analyzer":
        flash_bitstream(device, find_cynthion_bitstream(device, "analyzer.bit"))
    elif args.target == "facedancer":
        if platform.system() == "Windows":
            logging.error("\nFacedancer and USBProxy are not currently supported on Windows.")
            logging.error("Attempting to use Facedancer or USBProxy on Windows may cause")
            logging.error("USB analysis to stop working.\n")
            logging.error("For more information please see the tracking issue:\n")
            logging.error("  https://github.com/greatscottgadgets/cynthion/issues/170\n")
            logging.error("Command aborted.")
            sys.exit(1)
        flash_soc_firmware(device, find_cynthion_asset("moondancer.bin"))
        flash_bitstream(device, find_cynthion_bitstream(device, "facedancer.bit"))
    elif args.target == "selftest":
        flash_bitstream(device, find_cynthion_bitstream(device, "selftest.bit"))
    else:
        logging.error(f"unknown target: {args.target}")
        return
