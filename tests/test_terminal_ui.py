import contextlib
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import terminal_ui as ui


class TerminalTests(unittest.TestCase):
    def test_plain_menu_keeps_default_and_numbers(self):
        output = io.StringIO()
        with patch.object(ui, 'interactive', return_value=False), patch('builtins.input', return_value=''), contextlib.redirect_stdout(output):
            self.assertEqual(ui.choose('Pick', [('1', 'Check'), ('0', 'Exit')], '1', 'Choice: '), '1')
        self.assertIn('1. Check', output.getvalue())

    def test_interactive_selection_preserves_value(self):
        with patch.object(ui, 'interactive', return_value=True), patch('questionary.select') as select:
            select.return_value.unsafe_ask.return_value = '3'
            self.assertEqual(ui.choose('Pick', [('1', 'Check'), ('3', 'Photos')], '1', ''), '3')
        self.assertEqual(select.call_args.kwargs['choices'][1].value, '3')

    def test_cancel_does_not_select_default(self):
        with patch.object(ui, 'interactive', return_value=True), patch('questionary.select') as select:
            select.return_value.unsafe_ask.return_value = None
            with self.assertRaises(KeyboardInterrupt):
                ui.choose('Pick', [('2', 'Rotate')], '2', '')

    def test_destructive_confirmation_defaults_to_no(self):
        with patch.object(ui, 'interactive', return_value=True), patch('questionary.confirm') as confirm:
            confirm.return_value.unsafe_ask.return_value = False
            self.assertEqual(ui.prompt('Replace photos? [y/N]: '), 'n')
        self.assertFalse(confirm.call_args.kwargs['default'])
