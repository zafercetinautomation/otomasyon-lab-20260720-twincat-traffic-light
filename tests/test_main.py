"""Trafik lambası durum makinesi testleri."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from main import TrafficController, TrafficState


class TrafficControllerTests(unittest.TestCase):
    def test_vehicle_green_changes_to_yellow_after_ten_seconds(self) -> None:
        controller = TrafficController()
        output = controller.step(10)
        self.assertEqual(output["durum"], TrafficState.VEHICLE_YELLOW.value)
        self.assertTrue(output["arac_sari"])
        self.assertFalse(output["arac_yesil"])

    def test_full_cycle_returns_to_vehicle_green(self) -> None:
        controller = TrafficController()
        output = controller.step(26)
        self.assertEqual(output["durum"], TrafficState.VEHICLE_GREEN.value)

    def test_emergency_stop_turns_off_all_green_outputs(self) -> None:
        controller = TrafficController(state=TrafficState.PEDESTRIAN_GREEN)
        output = controller.step(0, emergency_stop=True)
        self.assertEqual(output["durum"], TrafficState.ALL_RED.value)
        self.assertTrue(output["arac_kirmizi"])
        self.assertTrue(output["yaya_kirmizi"])
        self.assertFalse(output["arac_yesil"])
        self.assertFalse(output["yaya_yesil"])

    def test_disabled_controller_uses_safe_stop_outputs(self) -> None:
        controller = TrafficController()
        output = controller.step(0, enabled=False)
        self.assertEqual(output["durum"], TrafficState.ALL_RED.value)

    def test_negative_time_is_rejected(self) -> None:
        controller = TrafficController()
        with self.assertRaisesRegex(ValueError, "negatif"):
            controller.step(-1)


if __name__ == "__main__":
    unittest.main()
