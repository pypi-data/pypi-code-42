# DO NOT EDIT!
# This file was automatically generated by "generate_id_constants_from_stableid.py"

import enum


class EffectId(enum.Enum):
    NULL = 0
    PSISTORMPERSISTENT = 1
    GUARDIANSHIELDPERSISTENT = 2
    TEMPORALFIELDGROWINGBUBBLECREATEPERSISTENT = 3
    TEMPORALFIELDAFTERBUBBLECREATEPERSISTENT = 4
    THERMALLANCESFORWARD = 5
    SCANNERSWEEP = 6
    NUKEPERSISTENT = 7
    LIBERATORTARGETMORPHDELAYPERSISTENT = 8
    LIBERATORTARGETMORPHPERSISTENT = 9
    BLINDINGCLOUDCP = 10
    RAVAGERCORROSIVEBILECP = 11
    LURKERMP = 12


    def __repr__(self):
        return f"EffectId.{self.name}"


for item in EffectId:
    assert not item.name in globals()
    globals()[item.name] = item
