import unittest
from src.xiwen.utils.terminal_display import (
    get_TerminalDisplay_instance,
    TerminalDisplay,
)


class TestTerminalDisplay(unittest.TestCase):
    def test_references_to_TerminalDisplay(self):
        """Test separate references are equal"""
        A = TerminalDisplay()
        B = TerminalDisplay()
        self.assertEqual(A, B)

    def test_one_TerminalDisplay_exists(self):
        """Test just one instance exists despite multiple calls"""
        A = TerminalDisplay()
        B = TerminalDisplay()
        self.assertIs(A, B._instance)

    def test_TerminalDisplay_attributes_exist(self):
        """Test TerminalDisplay has expected attributes"""
        A = TerminalDisplay()
        self.assertTrue(hasattr(A, "WELCOME_MESSAGE"))
        self.assertTrue(hasattr(A, "MAIN_MENU_OPTIONS"))
        self.assertTrue(hasattr(A, "DEMO_MESSAGE"))
        self.assertTrue(hasattr(A, "EXPORT_OPTIONS"))
        self.assertTrue(hasattr(A, "EXPORT_OPTIONS_FOR_CUSTOM_GRADES"))
        self.assertTrue(hasattr(A, "UNKNOWN_CHARACTER_VARIANT"))


class TestGetTerminalDisplayInstance(unittest.TestCase):
    def test_instance_returned(self):
        """Test function returns an TerminalDisplay instance"""
        A = get_TerminalDisplay_instance()
        self.assertTrue(isinstance(A, TerminalDisplay))

    def test_returns_same_instance(self):
        """Test multiple calls return same TerminalDisplay instance"""
        A = get_TerminalDisplay_instance()
        B = get_TerminalDisplay_instance()
        self.assertIs(A, B._instance)


if __name__ == "__main__":
    unittest.main()
