import pytest
from beerest.core.assertions import Assertions

class TestAssertions:
    def test_assert_equal(self):
        Assertions.assertEqual(1, 1)
        with pytest.raises(AssertionError):
            Assertions.assertEqual(1, 2)
            
    def test_assert_true(self):
        Assertions.assertTrue(True)
        with pytest.raises(AssertionError):
            Assertions.assertTrue(False)
            
    def test_assert_false(self):
        Assertions.assertFalse(False)
        with pytest.raises(AssertionError):
            Assertions.assertFalse(True)
            
    def test_assert_not_null(self):
        Assertions.assertNotNull("value")
        with pytest.raises(AssertionError):
            Assertions.assertNotNull(None)
            
    def test_assert_less(self):
        Assertions.assertLess(1, 2)
        with pytest.raises(AssertionError):
            Assertions.assertLess(2, 1)
            
    def test_assert_greater(self):
        Assertions.assertGreater(2, 1)
        with pytest.raises(AssertionError):
            Assertions.assertGreater(1, 2)
            
    def test_assert_in(self):
        Assertions.assertIn(1, [1, 2, 3])
        with pytest.raises(AssertionError):
            Assertions.assertIn(4, [1, 2, 3])