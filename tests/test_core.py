import unittest

import core


class TestCore(unittest.TestCase):
    def test_01_no_duplicate_connect(self):
        state = core.new_game()
        self.assertTrue(core.connect(state, "T1"))
        self.assertFalse(core.connect(state, "T1"))

    def test_02_no_generate_over_wind(self):
        state = core.new_game()
        state["wind"] = 30
        result = core.generate(state, 10)
        self.assertFalse(result)

    def test_03_storage_by_capacity(self):
        state = core.new_game()
        state["storage"] = 40
        self.assertEqual(core.storage_by_count(state), 40)

    def test_04_cancel_connect_refunds(self):
        state = core.new_game()
        core.connect(state, "T1")
        core.cancel_connect(state, "T1")
        self.assertEqual(state["storage"], 0)

    def test_05_no_generate_on_fault(self):
        state = core.new_game()
        state["converter_fault"] = True
        result = core.generate(state, 10)
        self.assertFalse(result)

    def test_06_gust_once(self):
        state = core.new_game()
        core.gust(state)
        self.assertEqual(state["lifespan"], 95)

    def test_07_no_generate_in_calm(self):
        state = core.new_game()
        state["calm"] = True
        result = core.generate(state, 10)
        self.assertFalse(result)

    def test_08_load_preserves_meter(self):
        state = core.new_game()
        state["meter_id"] = 7
        loaded = core.load_state(core.save_state(state))
        self.assertEqual(loaded["meter_id"], 7)


if __name__ == "__main__":
    unittest.main()
