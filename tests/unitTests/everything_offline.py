import tempfile

from regzbot.commandl import get_testresults_datadir
from tests.testing import run

"""
Run with
python -m pytest /tests/unitTests/everything_offline.py
so that it gets the pytest from the venv

Run with coverage:
python -m pytest /tests/unitTests/everything_offline.py --cov=regzbot
"""

test_data_dir = get_testresults_datadir()


class TestEverything:
    def test_everything(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            run(
                testmodes={'offline': True, 'online': False, 'trackers': False},
                testdatapath=test_data_dir,
                tmpdir=tmpdir,
            )


# # Setup before everything
# init(tmpdir, testdatadir)
# resultfile = open(resultfilename, 'a')


# # Setup before each group
# # reset git
# for gittree_testing in gittrees_testing:
#     gittrees_testing[gittree_testing].reset()
# update_gittrees()
# # reset email
# for emaildir in emaildirs:
#     emaildirs[emaildir].reset()
# regzbot.db_rollback()


# # Each test
# # run test
# callfunction = getattr(
#     this, '%s_%s_%s' % (testfuncprefix, outercount, innercount)
# )
# instructions = callfunction('test_%s_%s' % (outercount, innercount))

# # process created testdata
# if instructions:
#     if 'mailchk' in instructions:
#         for repsrc in regzbot.ReportSource.getall():
#             if repsrc.kind != 'lore':
#                 continue
#             repsrc.update()
#     if 'gitchk' in instructions:
#         update_gittrees()

# # write results
# resultfile.write('[%s_%s_%s]\n' % (testfuncprefix, outercount, innercount))
# for data in regzbot.export_csv.dumpall_csv():
#     resultfile.write(data)
# resultfile.write('\n')


# # Cleanup after each group
# emaildirs_clear()


# # Cleanup after everything
# regzbot.db_commit()
# regzbot.db_close()
