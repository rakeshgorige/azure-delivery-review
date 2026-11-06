import unittest
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from review import CONTROLS, review

class ReviewTests(unittest.TestCase):
    def test_empty_flags_all(self):
        self.assertTrue(all(x['status'] == 'needs review' for x in review({})))

    def test_only_boolean_true_is_declared(self):
        result = review({'terraform_validation': 'true', 'plan_review': True})
        self.assertEqual(result[0]['status'], 'needs review')
        self.assertEqual(result[1]['status'], 'declared')

    def test_requires_object(self):
        with self.assertRaises(ValueError):
            review([])

class CliTests(unittest.TestCase):
    def run_cli(self, contents, *options):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / 'config.json'
            config.write_text(contents, encoding='utf-8')
            return subprocess.run(
                [sys.executable, str(Path(__file__).with_name('review.py')), str(config), *options],
                capture_output=True, text=True, check=False,
            )

    def test_default_text_and_missing_controls_exit_code(self):
        result = self.run_cli('{}')
        self.assertEqual(result.returncode, 1)
        self.assertIn('controls are not independently verified', result.stdout)
        self.assertEqual(result.stdout.count('NEEDS REVIEW'), 6)
        self.assertEqual(result.stderr, '')

    def test_json_report_preserves_boolean_rules_and_disclaimer(self):
        config = {'terraform_validation': 'true', 'plan_review': True}
        result = self.run_cli(json.dumps(config), '--format', 'json')
        self.assertEqual(result.returncode, 1)
        report = json.loads(result.stdout)
        self.assertEqual(report['schema_version'], 1)
        self.assertEqual(report['review_type'], 'declarations_only')
        self.assertIs(report['independently_verified'], False)
        self.assertEqual(report['findings'], review(config))
        self.assertEqual(result.stderr, '')

    def test_all_declared_succeeds(self):
        config = {key: True for key, _ in CONTROLS}
        result = self.run_cli(json.dumps(config), '--format', 'json')
        self.assertEqual(result.returncode, 0)
        self.assertTrue(all(item['status'] == 'declared'
                            for item in json.loads(result.stdout)['findings']))

    def test_invalid_input_has_no_partial_report(self):
        for contents in ('{', '[]'):
            with self.subTest(contents=contents):
                result = self.run_cli(contents, '--format', 'json')
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, '')
                self.assertIn('Error:', result.stderr)

if __name__ == '__main__':
    unittest.main()

