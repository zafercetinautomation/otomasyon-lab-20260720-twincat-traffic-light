"""TwinCAT trafik lambası durum makinesini donanımsız simüle et."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TrafficState(str, Enum):
    """Trafik lambasının sıralı çalışma fazları."""

    VEHICLE_GREEN = "arac_yesil"
    VEHICLE_YELLOW = "arac_sari"
    ALL_RED = "tumu_kirmizi"
    PEDESTRIAN_GREEN = "yaya_yesil"
    PEDESTRIAN_FLASH = "yaya_yanip_sonme"


PHASE_DURATION = {
    TrafficState.VEHICLE_GREEN: 10.0,
    TrafficState.VEHICLE_YELLOW: 3.0,
    TrafficState.ALL_RED: 2.0,
    TrafficState.PEDESTRIAN_GREEN: 7.0,
    TrafficState.PEDESTRIAN_FLASH: 4.0,
}

NEXT_STATE = {
    TrafficState.VEHICLE_GREEN: TrafficState.VEHICLE_YELLOW,
    TrafficState.VEHICLE_YELLOW: TrafficState.ALL_RED,
    TrafficState.ALL_RED: TrafficState.PEDESTRIAN_GREEN,
    TrafficState.PEDESTRIAN_GREEN: TrafficState.PEDESTRIAN_FLASH,
    TrafficState.PEDESTRIAN_FLASH: TrafficState.VEHICLE_GREEN,
}


@dataclass
class TrafficController:
    """Süre tabanlı trafik lambası durum makinesi."""

    state: TrafficState = TrafficState.VEHICLE_GREEN
    elapsed: float = 0.0

    def step(
        self,
        seconds: float,
        *,
        enabled: bool = True,
        emergency_stop: bool = False,
    ) -> dict[str, bool | str]:
        """Zamanı ilerlet ve güncel sembolik çıkışları döndür."""
        if seconds < 0:
            raise ValueError("Süre negatif olamaz.")
        if emergency_stop or not enabled:
            self.state = TrafficState.ALL_RED
            self.elapsed = 0.0
            return self.outputs(safe_stop=True)

        self.elapsed += seconds
        while self.elapsed >= PHASE_DURATION[self.state]:
            self.elapsed -= PHASE_DURATION[self.state]
            self.state = NEXT_STATE[self.state]
        return self.outputs()

    def outputs(self, *, safe_stop: bool = False) -> dict[str, bool | str]:
        """Geçerli durumdan araç ve yaya çıkışlarını üret."""
        if safe_stop:
            return {
                "durum": TrafficState.ALL_RED.value,
                "arac_kirmizi": True,
                "arac_sari": False,
                "arac_yesil": False,
                "yaya_kirmizi": True,
                "yaya_yesil": False,
            }
        return {
            "durum": self.state.value,
            "arac_kirmizi": self.state
            in {
                TrafficState.ALL_RED,
                TrafficState.PEDESTRIAN_GREEN,
                TrafficState.PEDESTRIAN_FLASH,
            },
            "arac_sari": self.state is TrafficState.VEHICLE_YELLOW,
            "arac_yesil": self.state is TrafficState.VEHICLE_GREEN,
            "yaya_kirmizi": self.state
            in {
                TrafficState.VEHICLE_GREEN,
                TrafficState.VEHICLE_YELLOW,
                TrafficState.ALL_RED,
            },
            "yaya_yesil": self.state
            in {
                TrafficState.PEDESTRIAN_GREEN,
                TrafficState.PEDESTRIAN_FLASH,
            },
        }


def color(label: str, red: bool, yellow: bool, green: bool) -> str:
    """Etkin ışığı okunabilir metin olarak döndür."""
    active = "kırmızı" if red else "sarı" if yellow else "yeşil" if green else "kapalı"
    return f"{label}: {active}"


def main() -> None:
    controller = TrafficController()
    for second in range(31):
        output = controller.step(0 if second == 0 else 1)
        vehicle = color(
            "Araç",
            bool(output["arac_kirmizi"]),
            bool(output["arac_sari"]),
            bool(output["arac_yesil"]),
        )
        pedestrian = color(
            "Yaya",
            bool(output["yaya_kirmizi"]),
            False,
            bool(output["yaya_yesil"]),
        )
        print(f"{second:>2} sn | {output['durum']:<18} | {vehicle:<14} | {pedestrian}")


if __name__ == "__main__":
    main()
