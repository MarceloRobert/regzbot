#! /usr/bin/python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0
# Copyright (C) 2021 by Thorsten Leemhuis
__author__ = 'Thorsten Leemhuis <linux@leemhuis.info>'
#
# FIXMELATER:
# * import commits and emails from files
# * maybe: use more of pathlib and less of os and glob (or nothing at all)
# * directly retrieve some mails from lore to see if everything works, once there are some on the list

import glob
import os
import sys
import shutil

import regzbot
import tests.testing_offline
import tests.testing_online
import tests.testing_trackers

SUPPORTED_TESTMODES = {
    'offline': tests.testing_offline,
    'online': tests.testing_online,
    'trackers': tests.testing_trackers,
}

logger = regzbot.logger


def __get_resultfiles(path_testdata, path_tmpdir):
    if not os.path.isdir(path_testdata):
        logger.critical(
            "Directory for expexted results and template %s doesn't exist. Aborting.",
            path_testdata,
        )
        sys.exit(1)

    results_expected = {}
    results_generated = {}
    for mode in SUPPORTED_TESTMODES.keys():
        results_expected[mode] = os.path.join(
            path_testdata, 'expected/results-%s.csv' % mode
        )
        results_generated[mode] = os.path.join(path_tmpdir, 'testresults-%s.csv' % mode)

    return results_expected, results_generated


def check_results(results_expected, results_generated):
    def ask_user(results_expected, results_generated):
        answer = input(
            "Enter 'm' to call meld; enter 'a' or 'y' to accept differences; simply hit enter to move on."
        )
        if answer.lower() == 'm':
            os.system('meld %s %s' % (results_expected, results_generated))
            return False
        if answer.lower() == 'a' or answer.lower() == 'y':
            shutil.copyfile(results_generated, results_expected)
        return True

    with open(results_expected, 'r') as file_expected:
        with open(results_generated, 'r') as file_generated:
            if regzbot.db_diff(
                file_expected,
                file_generated,
                '%s' % results_expected,
                '%s' % results_generated,
            ):
                sys.stdout.write('#######\n')
                while not ask_user(results_expected, results_generated):
                    pass


def init(tmpdir):
    if len(glob.glob(os.path.join(tmpdir, '*'))) > 0:
        logger.critical('aborting, the directory %s is not empty', tmpdir)
        sys.exit(1)


def run(testmodes, testdatapath, tmpdir):
    results_expected, results_generated = __get_resultfiles(testdatapath, tmpdir)

    for mode in SUPPORTED_TESTMODES.keys():
        if testmodes[mode]:
            SUPPORTED_TESTMODES[mode].run(results_generated[mode], tmpdir, testdatapath)

    for mode in SUPPORTED_TESTMODES.keys():
        if testmodes[mode]:
            check_results(results_expected[mode], results_generated[mode])
