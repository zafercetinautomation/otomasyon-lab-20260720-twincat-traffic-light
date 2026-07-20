TYPE E_TrafficState :
(
    VehicleGreen,
    VehicleYellow,
    AllRed,
    PedestrianGreen,
    PedestrianFlash
);
END_TYPE

PROGRAM MAIN
VAR
    (* Sembolik girişler: gerçek I/O adresleri projede ayrıca eşlenmelidir. *)
    bEnable             : BOOL := TRUE;
    bEmergencyStop      : BOOL;

    (* Sembolik çıkışlar *)
    bVehicleRed         : BOOL;
    bVehicleYellow      : BOOL;
    bVehicleGreen       : BOOL;
    bPedestrianRed      : BOOL;
    bPedestrianGreen    : BOOL;

    eState              : E_TrafficState := VehicleGreen;
    fbPhaseTimer        : TON;
    bTimerEnable        : BOOL := TRUE;
    tPhaseDuration      : TIME;
END_VAR

(* Her çevrimde güvenli varsayılan: yeşiller kapalı, kırmızılar açık. *)
bVehicleRed := TRUE;
bVehicleYellow := FALSE;
bVehicleGreen := FALSE;
bPedestrianRed := TRUE;
bPedestrianGreen := FALSE;

(* Bu giriş yalnızca eğitim simülasyonudur; sertifikalı emniyet işlevi değildir. *)
IF bEmergencyStop OR NOT bEnable THEN
    eState := AllRed;
    bTimerEnable := FALSE;
    fbPhaseTimer(IN := FALSE);
    RETURN;
END_IF

(* Duruma göre faz süresini belirle. *)
CASE eState OF
    VehicleGreen:
        tPhaseDuration := T#10S;
    VehicleYellow:
        tPhaseDuration := T#3S;
    AllRed:
        tPhaseDuration := T#2S;
    PedestrianGreen:
        tPhaseDuration := T#7S;
    PedestrianFlash:
        tPhaseDuration := T#4S;
END_CASE

IF NOT bTimerEnable THEN
    bTimerEnable := TRUE;
END_IF
fbPhaseTimer(IN := bTimerEnable, PT := tPhaseDuration);

CASE eState OF
    VehicleGreen:
        bVehicleRed := FALSE;
        bVehicleGreen := TRUE;
        IF fbPhaseTimer.Q THEN
            eState := VehicleYellow;
            bTimerEnable := FALSE;
        END_IF

    VehicleYellow:
        bVehicleRed := FALSE;
        bVehicleYellow := TRUE;
        IF fbPhaseTimer.Q THEN
            eState := AllRed;
            bTimerEnable := FALSE;
        END_IF

    AllRed:
        IF fbPhaseTimer.Q THEN
            eState := PedestrianGreen;
            bTimerEnable := FALSE;
        END_IF

    PedestrianGreen:
        bPedestrianRed := FALSE;
        bPedestrianGreen := TRUE;
        IF fbPhaseTimer.Q THEN
            eState := PedestrianFlash;
            bTimerEnable := FALSE;
        END_IF

    PedestrianFlash:
        bPedestrianRed := FALSE;
        (* Yaklaşık 500 ms yanıp sönme: kalan zamanın saniye bitine göre örnek. *)
        bPedestrianGreen := (TIME_TO_DINT(fbPhaseTimer.ET) / 500) MOD 2 = 0;
        IF fbPhaseTimer.Q THEN
            eState := VehicleGreen;
            bTimerEnable := FALSE;
        END_IF
END_CASE

END_PROGRAM
