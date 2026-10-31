import importlib.util
from pathlib import Path
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('setup', SOURCE / 'scripts/setup.py')
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def run_install(self, **kwargs):
        return setup.install(self.root, SOURCE, revision='test-snapshot', **kwargs)

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}

    def test_empty_repeat_and_exact_skills(self):
        self.run_install()
        before = self.snapshot()
        self.assertEqual(self.run_install(), [])
        self.assertEqual(before, self.snapshot())
        self.assertFalse((self.root / 'docs/learning').exists())
        self.assertEqual((SOURCE / 'templates/ContextAndIntent.md').read_bytes(), (self.root / 'docs/ContextAndIntent.md').read_bytes())
        for name in ('shared-understanding', 'adaptive-teaching'):
            self.assertEqual((SOURCE / 'skills' / name / 'SKILL.md').read_bytes(), (self.root / '.agents/skills' / name / 'SKILL.md').read_bytes())

    def test_existing_rules_and_custom_consensus(self):
        rules = b'# Existing rules\r\nNever deploy without approval.\r\n'
        (self.root / 'AGENTS.md').write_bytes(rules)
        (self.root / 'notes').mkdir()
        (self.root / 'notes/common.md').write_text('Keep my terms', encoding='utf-8')
        self.run_install(consensus='notes/common.md', learning='notes/study')
        self.assertTrue((self.root / 'AGENTS.md').read_bytes().startswith(rules))
        self.assertEqual((self.root / 'notes/common.md').read_text(), 'Keep my terms')
        self.assertFalse((self.root / 'docs/CollaborationConsensus.md').exists())

    def test_conflicting_skill_no_mutation(self):
        p = self.root / '.agents/skills/adaptive-teaching/SKILL.md'
        p.parent.mkdir(parents=True)
        p.write_text('Custom teaching')
        before = self.snapshot()
        with self.assertRaises(ValueError):
            self.run_install()
        self.assertEqual(before, self.snapshot())

    def test_custom_context_no_mutation(self):
        p = self.root / 'docs/ContextAndIntent.md'
        p.parent.mkdir(parents=True)
        p.write_text('Custom context rules', encoding='utf-8')
        before = self.snapshot()
        with self.assertRaises(ValueError):
            self.run_install()
        self.assertEqual(before, self.snapshot())

    def test_escape_and_config_change_rejected(self):
        with self.assertRaises(ValueError):
            self.run_install(consensus='../outside.md')
        self.assertEqual(self.snapshot(), {})
        self.run_install()
        before = self.snapshot()
        with self.assertRaises(ValueError):
            self.run_install(consensus='other.md')
        self.assertEqual(before, self.snapshot())


if __name__ == '__main__':
    unittest.main()
