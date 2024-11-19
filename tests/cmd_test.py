import subprocess
import unittest


class CMDTest(unittest.TestCase):

    def test_example_text(self):
        # Example text as --infile
        cp = subprocess.run(
            "python3 -m ciall.cmd --conf=example/example_conf.yaml --infile=example/example_text.tsv",
            shell=True)
        self.assertEqual(cp.returncode, 0)

        # Example text as piped input
        cp = subprocess.run(
            "cat example/example_text.tsv | python3 -m ciall.cmd --conf=example/example_conf.yaml",
            shell=True)
        self.assertEqual(cp.returncode, 0)

    def test_accuracy_test(self):
        # Example accuracy test
        cp = subprocess.run(
            "python3 -m ciall.cmd --conf=example/example_conf.yaml --infile=example/example_accuracy_test.tsv --accuracy",
            shell=True)
        self.assertEqual(cp.returncode, 0)

    def test_user_errors(self):
        # no input file
        cp = subprocess.run(
            "python3 -m ciall.cmd --conf=example/example_conf.yaml",
            shell=True,
            capture_output=True)
        self.assertEqual(cp.returncode, 1)
        self.assertEqual(cp.stdout, b'No input data!\n')

        # Input file doesn't exist
        cp = subprocess.run(
            "python3 -m ciall.cmd --conf=example/example_conf.yaml --infile=i_dont_exist.tsv",
            shell=True,
            capture_output=True)
        self.assertEqual(cp.returncode, 1)
        self.assertEqual(cp.stdout, b'Input file doesn\'t exist: i_dont_exist.tsv\n')