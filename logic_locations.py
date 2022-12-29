from typing import Callable

from connection_data import area_doors_unpackable
from item_data import items_unpackable
from loadout import Loadout
from logicCommon import ammo_req, can_bomb, can_use_pbs, energy_req, \
    hell_run_energy, lava_run, varia_or_hell_run
from logic_area_shortcuts import SandLand, SpacePort, LifeTemple, SkyWorld, FireHive, \
    PirateLab, Verdite, Geothermal, Suzi, DrayLand
from logic_shortcut import LogicShortcut
from logic_shortcut_data import (
    canFly, shootThroughWalls, breakIce, missileDamage, pinkDoor, pinkSwitch,
    missileBarrier, icePod, electricHyper, killRippers, killGreenPirates
)
from trick_data import Tricks

(
    CraterR, SunkenNestL, RuinedConcourseBL, RuinedConcourseTR, CausewayR,
    SporeFieldTR, SporeFieldBR, OceanShoreR, EleToTurbidPassageR, PileAnchorL,
    ExcavationSiteL, WestCorridorR, FoyerR, ConstructionSiteL, AlluringCenoteR,
    FieldAccessL, TransferStationR, CellarR, SubbasementFissureL,
    WestTerminalAccessL, MezzanineConcourseL, VulnarCanyonL, CanyonPassageR,
    ElevatorToCondenserL, LoadingDockSecurityAreaL, ElevatorToWellspringL,
    NorakBrookL, NorakPerimeterTR, NorakPerimeterBL, VulnarDepthsElevatorEL,
    VulnarDepthsElevatorER, HiveBurrowL, SequesteredInfernoL,
    CollapsedPassageR, MagmaPumpL, ReservoirMaintenanceTunnelR, IntakePumpR,
    ThermalReservoir1R, GeneratorAccessTunnelL, ElevatorToMagmaLakeR,
    MagmaPumpAccessR, FieryGalleryL, RagingPitL, HollowChamberR, PlacidPoolR,
    SporousNookL, RockyRidgeTrailL, TramToSuziIslandR
) = area_doors_unpackable

(
    Missile, Super, PowerBomb, Morph, GravityBoots, Speedball, Bombs, HiJump,
    GravitySuit, DarkVisor, Wave, SpeedBooster, Spazer, Varia, Ice, Grapple,
    MetroidSuit, Plasma, Screw, Hypercharge, Charge, Xray, SpaceJump, Energy,
    Refuel, SmallAmmo, LargeAmmo, DamageAmp, ChargeAmp, SpaceJumpBoost,
    spaceDrop
) = items_unpackable

# above this should not include any shortcuts that reference doors
# so they can be used in the area door logic
# below this cannot be used in area door logic, only location logic

topOfSpaceport = LogicShortcut(lambda loadout: (
    ((
        (spaceDrop not in loadout)
    ) or (
        (spaceDrop in loadout) and
        (LoadingDockSecurityAreaL in loadout) and
        (GravityBoots in loadout) and
        (MetroidSuit in loadout) and
        (SpacePort.spaceportTopFromElevator in loadout)
    ))
))
""" above the grapple gate """

sunkenNestToVulnar = LogicShortcut(lambda loadout: (
    (SunkenNestL in loadout) and
    (GravityBoots in loadout) and
    (pinkDoor in loadout) and  # impact crater bottom right
    (missileBarrier in loadout)
))
""" from sunken nest area door to entrance of vulnar caves """

sensorMaintenance = LogicShortcut(lambda loadout: (
    (sunkenNestToVulnar in loadout) and
    (pinkDoor in loadout) and  # into way of the watcher
    ((  # way of the watcher grey door
        (Missile in loadout) and
        (ammo_req(25) in loadout) and
        (Tricks.movement_moderate in loadout)
    ) or (
        (Super in loadout) and
        (ammo_req(45) in loadout)
    ) or (
        (Screw in loadout)
    )) and
    (Morph in loadout) and
    ((Tricks.mockball_hard in loadout) or (Speedball in loadout)) and
    ((Tricks.morph_jump_3_tile in loadout) or (Speedball in loadout) or (
        (can_bomb(4) in loadout) and
        ((Tricks.morph_jump_4_tile in loadout) or (Bombs in loadout))
    ))
))
""" logic is almost the same for the 2 sensor maintenance items """

ruinedConcourseBDoorToEldersBottom = LogicShortcut(lambda loadout: (
    (RuinedConcourseBL in loadout) and
    (GravityBoots in loadout) and
    ((
        (pinkDoor in loadout)  # pink gate switch
    ) or (
        # through cistern
        ((
            (GravitySuit in loadout) and
            (
                (HiJump in loadout) or (canFly in loadout) or (Tricks.gravity_jump in loadout)
            )
        ) or (
            (HiJump in loadout) and
            (Ice in loadout)  # freeze fish
        ) or (
            (Tricks.sbj_underwater_w_hjb in loadout)  # TODO: verify this
        ))
        # TODO: more tricks for coming through cistern without aqua suit?
    ))
))

ruinedConcourseBDoorToEldersTop = LogicShortcut(lambda loadout: (
    (ruinedConcourseBDoorToEldersBottom in loadout) and
    ((
        (missileDamage in loadout)
    ) or (
        ((HiJump in loadout) and (Tricks.wall_jump_delayed in loadout))
        # tight wall jump from lower chozo statue to higher chozo statue))
    ) or (
        (SpaceJump in loadout)
    ) or (
        (GravitySuit in loadout) and (canFly in loadout)
        # bomb jump from in water
    )) and
    (  # exit gate
        (shootThroughWalls in loadout) or
        (can_bomb(1) in loadout) or
        (Tricks.wave_gate_glitch in loadout) or
        (Screw in loadout)
    )
))
""" ruinedConcourseBDoorToEldersBottom + getting to the door at the top of the room """

norakToLifeTemple = LogicShortcut(lambda loadout: (
    (
        (NorakBrookL in loadout) and
        (LifeTemple.brook in loadout)
    ) or (
        (NorakPerimeterBL in loadout) and
        (LifeTemple.perimBL in loadout)
    ) or (
        (NorakPerimeterTR in loadout) and
        (MetroidSuit in loadout) and
        (GravityBoots in loadout)
    )
))
""" from any of the Norak area doors to Life Temple """

railAccess = LogicShortcut(lambda loadout: (
    (GravityBoots in loadout) and
    (
        (WestTerminalAccessL in loadout) or (
            (MezzanineConcourseL in loadout) and
            (SkyWorld.mezzanineShaft in loadout)
        ) or (
            (ElevatorToCondenserL in loadout) and
            (Morph in loadout) and
            (breakIce in loadout) and
            (SkyWorld.condenser in loadout)
        )
    )
))
""" access to the Sky Temple elevators at West Terminal and Transit Concourse """

collapsedHive = LogicShortcut(lambda loadout: (
    (CollapsedPassageR in loadout) and
    (pinkDoor in loadout) and
    (FireHive.courtyardToCollapsed in loadout)
))
""" collapsed passage door to anything beyond fire temple courtyard """

enterSuzi = LogicShortcut(lambda loadout: (
    (TramToSuziIslandR in loadout) and
    (GravityBoots in loadout) and
    (shootThroughWalls in loadout) and
    ((
        (energy_req(350) in loadout) and
        (Tricks.movement_zoast in loadout)
    ) or (
        (energy_req(550) in loadout) and
        (Tricks.movement_moderate in loadout)
    ) or (
        (energy_req(750) in loadout)
    ))
))
""" from suzi area door to inside with energy requirement """

meanderingPassage = LogicShortcut(lambda loadout: (
    ((OceanShoreR in loadout) or (EleToTurbidPassageR in loadout)) and
    (GravityBoots in loadout) and
    (pinkDoor in loadout) and
    ((GravitySuit in loadout) or (
        (HiJump in loadout) and
        # TODO: Do I need super if I come from EleToTurbidPassageR ?
        ((Super in loadout) or (  # don't need these tricks if I can go through sediment floor
            (Tricks.crouch_or_downgrab in loadout) and  # up from murky gallery
            (Tricks.movement_moderate in loadout) and  # left from murky gallery
            (Tricks.uwu_2_tile in loadout)  # up from submarine crevice
        ))
        # hint: snail will help you up meandering passage
    )) and
    ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
))
""" from OceanShoreR or EleToTurbidPassageR to bottom of meandering passage"""

doorsToWestCorridorTop = LogicShortcut(lambda loadout: (
    # you don't need gravity boots from west corridor door,
    # but you won't be able to go anywhere else without them
    (GravityBoots in loadout) and
    (
        (WestCorridorR in loadout)
    ) or (
        (ExcavationSiteL in loadout) and
        (killGreenPirates in loadout)
    ) or (
        (ConstructionSiteL in loadout) and
        (PirateLab.constructionLToElevator in loadout) and
        (can_use_pbs(1) in loadout) and
        (killGreenPirates in loadout)
    )
))
""" pirate lab area doors to top of west corridor """

doorsToCentralCorridorBottom = LogicShortcut(lambda loadout: (
    # similar to Mid
    # the only difference is where I have to get out of the water
    (GravityBoots in loadout) and
    ((
        (WestCorridorR in loadout) and
        ((
            # through PB tube
            (killGreenPirates in loadout) and
            (can_use_pbs(1) in loadout) and
            (PirateLab.epiphreaticCrag in loadout)
        ) or (
            # through hydrodynamic chamber
            (PirateLab.westCorridorToCentralTop in loadout) and
            (Screw in loadout) and
            (PirateLab.centralCorridorWater in loadout)
        ))
    ) or (
        (ExcavationSiteL in loadout) and
        (can_use_pbs(1) in loadout) and
        (PirateLab.epiphreaticCrag in loadout)
    ) or (
        (ConstructionSiteL in loadout) and
        (PirateLab.constructionLToElevator in loadout) and
        (PirateLab.epiphreaticCrag in loadout)
    ) or (
        (AlluringCenoteR in loadout) and
        (PirateLab.cenote in loadout) and
        ((Screw in loadout) or (MetroidSuit in loadout)) and
        (PirateLab.centralCorridorWater in loadout)
    ) or (
        (FoyerR in loadout) and
        (PirateLab.eastCorridor in loadout) and
        (PirateLab.centralCorridorWater in loadout)
    ))
))
""" pirate lab area doors to bottom of central corridor """

doorsToCentralCorridorMid = LogicShortcut(lambda loadout: (
    # similar to bottom
    # the only difference is where I have to get out of the water
    (GravityBoots in loadout) and
    ((
        (WestCorridorR in loadout) and
        ((
            # through PB tube
            (killGreenPirates in loadout) and
            (can_use_pbs(1) in loadout) and
            (PirateLab.epiphreaticCrag in loadout) and
            (PirateLab.centralCorridorWater in loadout)
        ) or (
            # through hydrodynamic chamber
            (PirateLab.westCorridorToCentralTop in loadout) and
            (Screw in loadout)
        ))
    ) or (
        (ExcavationSiteL in loadout) and
        (can_use_pbs(1) in loadout) and
        (PirateLab.epiphreaticCrag in loadout) and
        (PirateLab.centralCorridorWater in loadout)
    ) or (
        (ConstructionSiteL in loadout) and
        (PirateLab.constructionLToElevator in loadout) and
        (PirateLab.epiphreaticCrag in loadout) and
        (PirateLab.centralCorridorWater in loadout)
    ) or (
        (AlluringCenoteR in loadout) and
        (PirateLab.cenote in loadout) and
        ((Screw in loadout) or (MetroidSuit in loadout))
    ) or (
        (FoyerR in loadout) and
        (PirateLab.eastCorridor in loadout)
    ))
))
""" pirate lab area doors to middle of central corridor """

location_logic: dict[str, Callable[[Loadout], bool]] = {
    "Impact Crater: AccelCharge": lambda loadout: (
        (SunkenNestL in loadout) and
        (GravityBoots in loadout) and
        (Morph in loadout) and
        (Spazer in loadout) and
        ((HiJump in loadout) or (SpeedBooster in loadout) or (canFly in loadout))
    ),
    "Subterranean Burrow": lambda loadout: (
        (SunkenNestL in loadout) and
        ((Morph in loadout) or (GravityBoots in loadout))
    ),
    "Sandy Cache": lambda loadout: (
        (OceanShoreR in loadout) and
        (SandLand.shaftToGreenMoon in loadout)
    ),
    "Submarine Nest": lambda loadout: (
        (OceanShoreR in loadout) and
        (GravityBoots in loadout) and
        (pinkDoor in loadout) and  # 2 pink doors if I don't have (morph and (hjb or aqua))
        (
            (GravitySuit in loadout) or
            (
                (HiJump in loadout) and
                (
                    (Ice in loadout) or
                    (Tricks.crouch_precise in loadout)
                )
            ) or
            (Tricks.sbj_underwater_no_hjb in loadout)
        )
    ),
    "Shrine Of The Penumbra": lambda loadout: (
        (OceanShoreR in loadout) and
        (GravityBoots in loadout) and
        (missileDamage in loadout) and  # eye door
        (pinkDoor in loadout) and  # 2 pink doors if I don't have (morph and (hjb or aqua))
        ((GravitySuit in loadout) or (Tricks.sbj_underwater_w_hjb in loadout)) and
        ((
            (can_bomb(1) in loadout) and
            (DarkVisor in loadout)
        ) or (
            (can_use_pbs(2) in loadout)
        ))
    ),
    "Benthic Cache Access": lambda loadout: (
        ((OceanShoreR in loadout) or (EleToTurbidPassageR in loadout)) and
        (GravityBoots in loadout) and
        # if you don't have bombs, you'll need 3 pbs
        (can_bomb(3) in loadout) and
        # and even if you do have bombs, you'll need 1 pb
        (can_use_pbs(1) in loadout) and
        (Super in loadout) and  # submarine crevice bottom left - and some pink doors
        ((GravitySuit in loadout) or (
            (Tricks.sbj_underwater_w_hjb in loadout) and
            # out of benthic shaft without aqua before the balls block you in
            (Tricks.movement_moderate in loadout)
        )) and
        ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
    ),
    "Benthic Cache": lambda loadout: (
        ((OceanShoreR in loadout) or (EleToTurbidPassageR in loadout)) and
        (GravityBoots in loadout) and
        (can_bomb(2) in loadout) and  # submarine crevice, in and out with nowhere to farm between
        (Super in loadout) and  # submarine crevice bottom left - and some pink doors
        ((GravitySuit in loadout) or (
            (HiJump in loadout) and
            # out of benthic shaft without aqua before the balls block you in
            (Tricks.movement_moderate in loadout) and
            # submarine crevice
            (loadout.has_any(Tricks.crouch_precise, Tricks.sbj_underwater_w_hjb, Tricks.uwu_2_tile))
        )) and
        ((DarkVisor in loadout) or (Tricks.dark_medium in loadout))
    ),
    "Ocean Vent Supply Depot": lambda loadout: (
        (meanderingPassage in loadout) and
        (Morph in loadout) and  # inside the room with the item
        (
            ((Super in loadout) and (Tricks.morph_jump_3_tile_water in loadout)) or
            ((GravitySuit in loadout) and (Screw in loadout))
        )  # TODO: or PBs and a lava dive
    ),
    "Sediment Flow": lambda loadout: (
        loadout.has_all(OceanShoreR, GravityBoots, GravitySuit, Super)
    ),
    "Harmonic Growth Enhancer": lambda loadout: (
        ((
            (FieldAccessL in loadout) and
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout))
        ) or (
            (TransferStationR in loadout) and
            (DarkVisor in loadout) and
            (pinkDoor in loadout)  # between east spore field and ESF access
        )) and
        ((DarkVisor in loadout) or (Tricks.dark_easy in loadout)) and
        (can_bomb(1) in loadout) and
        (Morph in loadout) and
        (GravityBoots in loadout) and
        # 5-tile morph jump
        (pinkDoor in loadout)  # between spore collection and spore generator access
    ),
    "Upper Vulnar Power Node": lambda loadout: (
        (sunkenNestToVulnar in loadout) and
        # if you don't have (grapple or can fly), you can get up on the right wall with screw
        (Screw in loadout) and
        (can_use_pbs(2) in loadout) and  # if 20 ammo, you'll need to get drops from red balls
        (MetroidSuit in loadout)
    ),
    "Grand Vault": lambda loadout: (
        (sunkenNestToVulnar in loadout) and
        (Grapple in loadout)
    ),
    "Cistern": lambda loadout: (
        (RuinedConcourseBL in loadout) and (GravityBoots in loadout) and (can_bomb(1) in loadout)
    ),
    "Warrior Shrine: ETank": lambda loadout: (
        (ruinedConcourseBDoorToEldersTop in loadout) and
        (pinkDoor in loadout) and  # to warrior shrine access
        (can_use_pbs(1) in loadout) and  # PB placement is important if you only have 10 ammo
        ((Speedball in loadout) or (Tricks.mockball_hard in loadout))
    ),
    "Vulnar Caves Entrance": lambda loadout: (
        (sunkenNestToVulnar in loadout)
    ),
    "Crypt": lambda loadout: (
        (ruinedConcourseBDoorToEldersTop in loadout) and
        (can_bomb(3) in loadout) and
        (
            (shootThroughWalls in loadout) or
            (Bombs in loadout) or
            (
                (Speedball in loadout) and  # follow your bullet with speedball to hit the switch
                (Tricks.movement_moderate in loadout)
            )
        )
    ),
    "Archives: SpringBall": lambda loadout: (
        (sunkenNestToVulnar in loadout) and
        (pinkDoor in loadout) and  # into way of the watcher
        (Morph in loadout) and
        (Speedball in loadout)
    ),
    "Archives: SJBoost": lambda loadout: (
        (sunkenNestToVulnar in loadout) and
        (pinkDoor in loadout) and  # into way of the watcher
        (Morph in loadout) and
        (Speedball in loadout) and
        (SpeedBooster in loadout)
    ),
    "Sensor Maintenance: ETank": lambda loadout: (  # front
        (sensorMaintenance in loadout)
    ),
    "Eribium Apparatus Room": lambda loadout: (
        (GravityBoots in loadout) and
        (can_bomb(1) in loadout) and
        ((
            (FieldAccessL in loadout) and
            ((DarkVisor in loadout) or (Tricks.dark_easy in loadout)) and
            ((shootThroughWalls in loadout) or (Tricks.wave_gate_glitch in loadout)) and
            (pinkDoor in loadout)  # between east spore field and ESF access
        ) or (
            (TransferStationR in loadout) and
            (DarkVisor in loadout)
        ))
    ),
    "Hot Spring": lambda loadout: (
        (SporousNookL in loadout) and
        (GravityBoots in loadout) and
        (can_bomb(2) in loadout) and
        (Verdite.hotSpring in loadout) and
        ((GravitySuit in loadout) or (Speedball in loadout))  # 2-tile morph jump
    ),
    "Epiphreatic Crag": lambda loadout: (
        (GravityBoots in loadout) and
        ((
            (ConstructionSiteL in loadout) and
            (PirateLab.constructionLToElevator in loadout)
        ) or (
            (ExcavationSiteL in loadout) and
            (can_use_pbs(1) in loadout)
        )) and
        (Morph in loadout) and
        ((GravitySuit in loadout) or (
            (HiJump in loadout) and  # crouch down grab into first small platform
            (Speedball in loadout) and  # ball jump up from there
            (Tricks.crouch_or_downgrab in loadout)
        ) or (
            # go up on the right side, then left above the water
            (PirateLab.epiphreaticCrag_left in loadout) and
            ((can_use_pbs(1) in loadout) or (
                (Screw in loadout) and (Bombs in loadout)
            ))
        ))
    ),
    "Mezzanine Concourse": lambda loadout: (
        (MezzanineConcourseL in loadout) and
        (GravityBoots in loadout) and
        (Morph in loadout) and
        (SkyWorld.mezzanineShaft in loadout) and
        ((Tricks.morph_jump_4_tile in loadout) or (Bombs in loadout) or (Speedball in loadout))
    ),
    "Greater Inferno": lambda loadout: (
        (MagmaPumpAccessR in loadout) and
        (GravityBoots in loadout) and
        (can_use_pbs(1) in loadout) and  # door
        (Super in loadout) and
        # getting through the heat
        (lava_run(850, 1850) in loadout) and
        # hell run without aqua will require crystal flash
        (MetroidSuit in loadout) and
        # open gate
        ((  # with switch
            (
                (GravitySuit in loadout) and
                (can_bomb(2) in loadout)
            ) or (
                # no aqua
                (Speedball in loadout) and
                (can_bomb(2) in loadout)  # for getting stuck in crumbles
            )
        ) or (  # shoot through gate
            (Tricks.wave_gate_glitch in loadout) and
            # This is not the normal usage of this trick, but I don't want to make a trick just for this.
            (shootThroughWalls in loadout)
        )) and
        ((GravitySuit in loadout) or (Speedball in loadout) or (Tricks.morph_jump_3_tile_water in loadout))  # exit
    ),
    "Burning Depths Cache": lambda loadout: (
        (MagmaPumpAccessR in loadout) and
        (GravityBoots in loadout) and
        (can_use_pbs(1) in loadout) and
        (lava_run(550, 1250) in loadout) and
        (MetroidSuit in loadout) and
        (Morph in loadout) and
        ((Spazer in loadout) or (
            (Tricks.searing_gate_tricks in loadout) and
            ((Wave in loadout) or ((Charge in loadout) and (Bombs in loadout)))
        ))
    ),
    "Mining Cache": lambda loadout: (
        (GravityBoots in loadout) and
        (Super in loadout) and
        ((can_bomb(2) in loadout) or loadout.has_all(can_bomb(1), Speedball)) and
        (
            (FieryGalleryL in loadout) and
            (Verdite.fieryTrail in loadout)
        ) or (
            (SporousNookL in loadout) and
            (Verdite.hotSpring in loadout)
        )
    ),
    "Infested Passage": lambda loadout: (
        # copy and paste hive main passage
        (GravityBoots in loadout) and
        ((
            (VulnarDepthsElevatorEL in loadout) and
            (FireHive.hiveEntrance in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (FireHive.crossways in loadout) and
            (FireHive.infernalSequestration in loadout) and
            (icePod in loadout)
        ))
    ),
    "Fire's Boon Shrine": lambda loadout: (
        ((shootThroughWalls in loadout) or (
            (Tricks.ggg in loadout) and
            (Varia in loadout) and  # hell run ggg over spikes not in logic
            (missileDamage in loadout)
            # TODO: another trick because this is harder than others? because of spikes
        )) and
        ((
            (VulnarDepthsElevatorEL in loadout) and
            (FireHive.hiveEntrance in loadout) and
            (icePod in loadout) and
            (FireHive.crossways in loadout) and
            (pinkDoor in loadout) and
            # TODO: something that can kill red pirates, in case door color changes
            # crossways to item and back to crossways
            (varia_or_hell_run(850, heat_and_metroid_suit_not_required=True) in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (FireHive.infernalSequestration in loadout) and
            (pinkDoor in loadout) and
            # TODO: something that can kill red pirates, in case door color changes
            # crossways to item and back to crossways
            (varia_or_hell_run(850, heat_and_metroid_suit_not_required=True) in loadout)
        ) or (
            (collapsedHive in loadout)
        )) and
        (GravityBoots in loadout)
        # TODO: from west: or hell run to fire temple courtyard and patience for slow refill
    ),
    "Fire's Bane Shrine": lambda loadout: (
        (icePod in loadout) and
        (GravityBoots in loadout) and
        (Morph in loadout) and
        ((can_bomb(1) in loadout) or (Speedball in loadout)) and
        # hell run from farm in outer chamber to item and back to farm
        (varia_or_hell_run(650, heat_and_metroid_suit_not_required=True) in loadout) and
        ((
            (VulnarDepthsElevatorEL in loadout) and
            (FireHive.hiveEntrance in loadout) and
            (icePod in loadout) and
            (FireHive.crossways in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (FireHive.infernalSequestration in loadout)
        ) or (
            (collapsedHive in loadout)
        ))
    ),
    "Ancient Shaft": lambda loadout: (
        ((
            (MetroidSuit in loadout) and
            (varia_or_hell_run(450) in loadout)
        ) or (
            # no metroid suit
            ((
                (Varia in loadout) and
                (GravitySuit in loadout) and
                (energy_req(hell_run_energy(450, loadout)) in loadout)
            ) or (
                (Varia in loadout) and
                # no aqua
                (energy_req(hell_run_energy(1250, loadout)) in loadout)
            ) or (
                (GravitySuit in loadout) and
                # no varia
                (energy_req(hell_run_energy(850, loadout)) in loadout)
            ))  # no suits not possible
        )) and
        (GravityBoots in loadout) and
        (
            (GravitySuit in loadout) or (Speedball in loadout) or (Tricks.morph_jump_3_tile_water in loadout)
        ) and
        (can_bomb(4) in loadout) and
        ((
            (VulnarDepthsElevatorEL in loadout) and
            (FireHive.hiveEntrance in loadout) and
            (icePod in loadout) and
            (FireHive.crossways in loadout) and
            (FireHive.crosswaysToCourtyard in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (FireHive.infernalSequestration in loadout) and
            (Morph in loadout) and
            (FireHive.crosswaysToCourtyard in loadout)
        ) or (
            (collapsedHive in loadout)
        ))
    ),
    "Gymnasium": lambda loadout: (  # similar to ancient basin
        (Grapple in loadout) and
        (GravityBoots in loadout) and
        ((  # from west
            ((
                (VulnarDepthsElevatorEL in loadout) and
                (FireHive.hiveEntrance in loadout) and
                (icePod in loadout) and
                (FireHive.crossways in loadout) and
                (FireHive.crosswaysToCourtyard in loadout)
            ) or (
                (SequesteredInfernoL in loadout) and
                (FireHive.infernalSequestration in loadout) and
                (FireHive.crosswaysToCourtyard in loadout)
            ) or (
                (collapsedHive in loadout)  # using fire temple courtyard as a pit stop
            )) and
            # from fire temple courtyard to gymnasium
            (loadout.has_any(killRippers, Varia, Tricks.movement_zoast)) and  # just outside courtyard
            ((  # through power bomb blocks
                (can_use_pbs(3) in loadout) and
                (varia_or_hell_run(507, heat_and_metroid_suit_not_required=True) in loadout)
            ) or (  # through ancient basin
                (can_bomb(3) in loadout) and
                (varia_or_hell_run(869, heat_and_metroid_suit_not_required=True) in loadout)
            ))
        ) or (  # from east, no fire temple courtyard
            (collapsedHive in loadout) and
            (varia_or_hell_run(1450, heat_and_metroid_suit_not_required=True) in loadout)
        ))
    ),
    "Electromechanical Engine": lambda loadout: (
        (Grapple in loadout) and
        (Morph in loadout) and
        (GravityBoots in loadout) and
        # this isn't the same as a morph_jump_3_tile, but I don't know if it's worth making another trick
        ((Tricks.morph_jump_3_tile in loadout) or (Speedball in loadout) or (can_bomb(1) in loadout)) and
        # which area door to come from
        ((
            (ReservoirMaintenanceTunnelR in loadout) and
            (Screw in loadout) and
            (can_bomb(1) in loadout) and
            ((GravitySuit in loadout) or (
                (Tricks.freeze_hard in loadout) and
                (Ice in loadout) and
                ((Tricks.movement_zoast in loadout) or (HiJump in loadout))
            )) and
            (varia_or_hell_run(80) in loadout) and  # cold room
            # not requiring metroid suit
            ((  # security matrix
                loadout.has_all(MetroidSuit, DarkVisor, shootThroughWalls, varia_or_hell_run(311))
            ) or (  # main boiler
                (
                    # not fall in lava (or have metroid suit)
                    (loadout.has_any(MetroidSuit, SpaceJump, Grapple, Tricks.wall_jump_delayed)) and
                    # difficult wall jumps to not fall in lava
                    (varia_or_hell_run(849, heat_and_metroid_suit_not_required=True) in loadout)
                    # TODO: patience and refill in room with red pirates (low drop rate)
                ) or (
                    # fall in lava
                    (loadout.has_any(HiJump, canFly, Grapple, Ice)) and  # left side of main boiler
                    (varia_or_hell_run(1250, heat_and_metroid_suit_not_required=True) in loadout)
                    # TODO: patience and refill in room with red pirates (low drop rate)
                )
            ))
        ) or (
            # The ways that come in the top of central corridor require metroid suit
            (MetroidSuit in loadout) and
            ((  # security matrix
                loadout.has_all(DarkVisor, shootThroughWalls, varia_or_hell_run(311))
            ) or (  # main boiler
                (loadout.has_any(HiJump, canFly, Grapple, Ice)) and  # left side of main boiler
                (varia_or_hell_run(871) in loadout)
                # TODO: patience and refill in room with red pirates (low drop rate)
            )) and
            (
                (ThermalReservoir1R in loadout) and
                (MetroidSuit in loadout) and
                (Geothermal.thermalResAlpha in loadout)
            ) or (
                (GeneratorAccessTunnelL in loadout) and
                (MetroidSuit in loadout) and  # top laser puzzles are 1 way w/o metroid suit
                (can_use_pbs(3) in loadout)
            )
        ))
    ),
    "Depressurization Valve": lambda loadout: (
        (GravityBoots in loadout) and
        # which area door to come from
        ((
            (ReservoirMaintenanceTunnelR in loadout) and
            (Screw in loadout) and
            (can_bomb(1) in loadout) and
            (Geothermal.thermalResBeta in loadout) and
            ((True))  # or (Grapple in loadout) or (MetroidSuit in loadout))
            # This `True` represents the ability to turn the power off and back on again (requiring Screw)
            # It's here in case we disable turning off the power.
        ) or (
            (ThermalReservoir1R in loadout) and
            (MetroidSuit in loadout) and
            (Geothermal.thermalResAlpha in loadout)
        ) or (
            (GeneratorAccessTunnelL in loadout) and
            (MetroidSuit in loadout) and  # top laser puzzles are 1 way w/o metroid suit
            (can_use_pbs(3) in loadout)
        ))
        # TODO: add MagmaPumpL access
        # (because it can be done with neither metroid suit nor bombs)
    ),
    "Loading Dock Storage Area": lambda loadout: (
        (LoadingDockSecurityAreaL in loadout)  # no gravity boots needed
    ),
    "Containment Area": lambda loadout: (
        (GravityBoots in loadout) and
        ((
            (FoyerR in loadout) and
            (PirateLab.eastCorridor in loadout) and
            ((MetroidSuit in loadout) or (Screw in loadout))
        ) or (
            (AlluringCenoteR in loadout) and
            (PirateLab.cenote in loadout)
        ))
    ),
    "Briar: SJBoost": lambda loadout: (  # top  PB tube
        (NorakPerimeterBL in loadout) and
        (GravityBoots in loadout) and
        (can_use_pbs(1) in loadout)
    ),
    "Shrine Of Fervor": lambda loadout: (
        (GravityBoots in loadout) and
        (norakToLifeTemple in loadout) and
        (LifeTemple.veranda in loadout)
    ),
    "Chamber Of Wind": lambda loadout: (
        (GravityBoots in loadout) and
        (norakToLifeTemple in loadout) and
        (LifeTemple.veranda in loadout) and
        (pinkDoor in loadout) and
        ((can_bomb(2) in loadout) or (Screw in loadout)) and  # wall outside the door
        # Chamber of Wind Access both ways
        (SpeedBooster in loadout) and
        ((can_bomb(2) in loadout) or (
            (Speedball in loadout) and
            (Morph in loadout)
        )) and
        # get out of chamber of wind
        ((Tricks.short_charge_2 in loadout) or (canFly in loadout))
    ),
    "Water Garden": lambda loadout: (
        (GravityBoots in loadout) and
        (norakToLifeTemple in loadout) and
        (LifeTemple.veranda in loadout) and
        (SpeedBooster in loadout) and
        (energy_req(163) in loadout)
        # TODO: chamber of stone logic
        # TODO: Might there be a reason to add logic from ElevatorToWellspringL ?
    ),
    "Crocomire's Energy Station": lambda loadout: (
        # similar to crocomire lair, except need to go through bomb blocks on left
        (GravityBoots in loadout) and
        (norakToLifeTemple in loadout) and
        (LifeTemple.veranda in loadout) and
        (SpeedBooster in loadout) and
        (Super in loadout) and  # door to elevator to jungle's heart
        ((  # to get past the bomb blocks in the left side of Croc's room (can't use shinespark for exit)
            (Morph in loadout) and
            (Speedball in loadout)
        ) or (can_bomb(2) in loadout) or (Screw in loadout) or (Tricks.morph_jump_3_tile in loadout))
    ),  # TODO: Might there be a reason to add logic from ElevatorToWellspringL ?
    "Wellspring Cache": lambda loadout: (
        (ElevatorToWellspringL in loadout) and
        (GravityBoots in loadout) and
        (Super in loadout) and
        (Morph in loadout) and
        ((
            (GravitySuit in loadout)
        ) or (
            (HiJump in loadout) and
            (Tricks.crouch_or_downgrab in loadout)
        ) or (
            (Speedball in loadout) and
            (Tricks.sbj_underwater_no_hjb in loadout)
        ) or (
            (Ice in loadout) and
            (ammo_req(20) in loadout) and  # a few supers to knock worm off the wall
            (Tricks.freeze_hard in loadout)
        ))
    ),
    "Frozen Lake Wall: DamageAmp": lambda loadout: (
        (ElevatorToCondenserL in loadout) and
        (GravityBoots in loadout) and
        (can_use_pbs(1) in loadout)
    ),
    "Grand Promenade": lambda loadout: (
        (railAccess in loadout) and (GravityBoots in loadout)
    ),
    "Summit Landing": lambda loadout: (
        (GravityBoots in loadout) and
        (can_bomb(1) in loadout) and
        (railAccess in loadout) and
        (varia_or_hell_run(69) in loadout) and
        (loadout.has_any(Speedball, Tricks.movement_moderate))  # jump through respawning crumble block
    ),
    "Snow Cache": lambda loadout: (
        (railAccess in loadout) and
        (GravityBoots in loadout) and
        (can_bomb(4) in loadout) and
        (varia_or_hell_run(151) in loadout)
    ),
    "Reliquary Access": lambda loadout: (
        # get to the item
        (Super in loadout) and
        (railAccess in loadout) and
        (GravityBoots in loadout) and
        ((SkyWorld.killRidley in loadout) or (
            (can_bomb(1) in loadout) and
            (loadout.has_any(Bombs, Speedball, Tricks.morph_jump_3_tile, Tricks.morph_jump_4_tile))
        )) and
        # get out
        ((
            (SkyWorld.killRidley in loadout) and
            (Morph in loadout) and
            (pinkDoor in loadout)  # stair of Dawn
        ) or (
            (SkyWorld.killPhantoon in loadout) and
            (can_bomb(3) in loadout) and
            (SkyWorld.meetingHall in loadout)
        ))
    ),
    "Syzygy Observatorium": lambda loadout: (
        (railAccess in loadout) and
        (GravityBoots in loadout) and
        ((
            (Screw in loadout) and
            (Morph in loadout) and
            (varia_or_hell_run(90) in loadout)
        ) or (
            (Super in loadout) and
            (SkyWorld.killRidley in loadout)
        ))
    ),
    "Armory Cache 2": lambda loadout: (
        # copy and paste armory cache 3
        (railAccess in loadout) and
        (GravityBoots in loadout) and
        (SkyWorld.meetingHall in loadout) and  # exit or both
        ((
            (Screw in loadout)
        ) or (
            (Super in loadout) and
            (can_bomb(2) in loadout) and
            (SkyWorld.killPhantoon in loadout) and
            loadout.has_any(Bombs, Speedball, Tricks.morph_jump_3_tile, Tricks.morph_jump_4_tile, SkyWorld.killRidley)
        ))
    ),
    "Armory Cache 3": lambda loadout: (
        # copy and paste armory cache 2
        (railAccess in loadout) and
        (GravityBoots in loadout) and
        (SkyWorld.meetingHall in loadout) and  # exit or both
        ((
            (Screw in loadout)
        ) or (
            (Super in loadout) and
            (can_bomb(2) in loadout) and
            (SkyWorld.killPhantoon in loadout) and
            loadout.has_any(Bombs, Speedball, Tricks.morph_jump_3_tile, Tricks.morph_jump_4_tile, SkyWorld.killRidley)
        ))
    ),
    "Drawing Room": lambda loadout: (
        (Super in loadout) and
        (GravityBoots in loadout) and
        (railAccess in loadout) and
        (Morph in loadout) and  # exit
        (pinkDoor in loadout) and  # bottom of stair of dawn
        (varia_or_hell_run(90) in loadout)  # This might require getting i-frames from enemies to avoid spike damage
    ),
    "Impact Crater Overlook": lambda loadout: (
        (SunkenNestL in loadout) and
        (GravityBoots in loadout) and
        (can_bomb(2) in loadout) and
        ((can_use_pbs(1) in loadout) or (Super in loadout)) and
        ((canFly in loadout) or (
            (SpeedBooster in loadout) and (Tricks.movement_zoast in loadout)
            # shinespark to just the right place, and respin, wall jump
        ))
    ),
    "Magma Lake Cache": lambda loadout: (
        (ElevatorToMagmaLakeR in loadout) and (GravityBoots in loadout) and (icePod in loadout) and (Morph in loadout)
    ),
    "Shrine Of The Animate Spark": lambda loadout: (
        (enterSuzi in loadout) and
        (Suzi.cyphers in loadout) and
        ((
            (Hypercharge in loadout) and
            (Charge in loadout)
        ) or (
            (Charge in loadout) and
            (energy_req(
                750
                if (Tricks.movement_zoast in loadout)
                else (
                    1050
                    if (Tricks.movement_moderate in loadout)
                    else 1350
                )
            ) in loadout)
        ))
    ),
    "Docking Port 4": lambda loadout: (  # (4 = letter Omega)
        # copy and paste docking port 3
        (
            (spaceDrop not in loadout) and
            (Grapple in loadout)
        ) or (
            (spaceDrop in loadout) and
            (LoadingDockSecurityAreaL in loadout) and
            (GravityBoots in loadout) and
            (MetroidSuit in loadout)
        )
    ),
    "Ready Room": lambda loadout: (
        (Super in loadout) and
        (topOfSpaceport in loadout)
    ),
    "Torpedo Bay": lambda loadout: (
        (topOfSpaceport in loadout)
    ),
    "Extract Storage": lambda loadout: (
        (can_use_pbs(1) in loadout) and
        (
            (electricHyper in loadout) or
            (
                ((energy_req(250) in loadout) or (Tricks.movement_zoast in loadout)) and
                (can_use_pbs(3) in loadout)
            )
        ) and
        (topOfSpaceport in loadout)
    ),
    "Impact Crater Alcove": lambda loadout: (
        (SunkenNestL in loadout) and
        (GravityBoots in loadout) and
        (can_bomb(2) in loadout) and
        ((canFly in loadout) or (
            (SpeedBooster in loadout) and (Tricks.movement_zoast in loadout)
            # shinespark to just the right place, and respin, wall jump
        ))
    ),
    "Ocean Shore: bottom": lambda loadout: (
        (OceanShoreR in loadout)
    ),
    "Ocean Shore: top": lambda loadout: (
        (OceanShoreR in loadout) and
        (GravityBoots in loadout) and
        (
            loadout.has_all(Tricks.movement_moderate, Tricks.wall_jump_delayed) or
            (canFly in loadout) or
            (HiJump in loadout) or
            ((SpeedBooster in loadout) and (GravitySuit in loadout))
        )
    ),
    "Sandy Burrow: ETank": lambda loadout: (  # top
        (OceanShoreR in loadout) and
        (Morph in loadout) and
        (GravityBoots in loadout) and
        ((GravitySuit in loadout) or (
            loadout.has_all(HiJump, Tricks.movement_zoast)
        ) or (
            (Tricks.sbj_underwater_w_hjb in loadout)
        )) and
        ((
            (GravitySuit in loadout) and
            ((Screw in loadout) or (can_bomb(2) in loadout))
        ) or (
            ((Tricks.sbj_underwater_no_hjb in loadout) or (HiJump in loadout)) and
            (can_bomb(2) in loadout)
        ))
        # can_bomb(2) because the blocks respawn pretty fast
    ),
    "Submarine Alcove": lambda loadout: (
        (meanderingPassage in loadout) and
        (Morph in loadout) and
        (
            (GravitySuit in loadout) or
            (Tricks.sbj_underwater_w_hjb in loadout) or
            loadout.has_all(Tricks.sbj_underwater_no_hjb, Tricks.freeze_hard)
        )
    ),
    "Sediment Floor": lambda loadout: (
        (OceanShoreR in loadout) and
        (GravityBoots in loadout) and
        (Super in loadout) and
        (
            (
                (GravitySuit in loadout)
            ) or (
                (HiJump in loadout) and
                (
                    ((Tricks.uwu_2_tile in loadout) and (Tricks.crouch_precise in loadout)) or
                    (Tricks.freeze_hard in loadout)
                )
            ) or (
                (Tricks.sbj_underwater_no_hjb in loadout) and
                (Tricks.freeze_hard in loadout)
            )
        )
        # TODO: logic from turbid passage (because no super needed)?
    ),
    "Sandy Gully": lambda loadout: (
        (OceanShoreR in loadout) and
        (Super in loadout) and
        (GravityBoots in loadout) and
        (GravitySuit in loadout) and
        ((HiJump in loadout) or (
            (SpaceJump in loadout) and
            (SpaceJumpBoost in loadout)
            # TODO: sjb in logical fill and maybe a logic shortcut for how many
        ) or (
            (Tricks.movement_zoast in loadout)
        ))
        # TODO: rusty said an expert can do this with just gravity boots and hi jump boots
        # I don't see how.
    ),
    "Hall Of The Elders": lambda loadout: (
        (ruinedConcourseBDoorToEldersBottom in loadout) and
        (
            (missileDamage in loadout) or
            (GravitySuit in loadout) or
            (HiJump in loadout) or
            (
                (Ice in loadout) and
                (Tricks.freeze_hard in loadout)
            ) or
            (SpaceJump in loadout) or  # no SJ boost needed
            (Tricks.sbj_underwater_no_hjb in loadout)
        )
    ),
    "Warrior Shrine: AmmoTank bottom": lambda loadout: (
        (ruinedConcourseBDoorToEldersTop in loadout) and
        (Morph in loadout) and
        (pinkDoor in loadout)
    ),
    "Warrior Shrine: AmmoTank top": lambda loadout: (
        (ruinedConcourseBDoorToEldersTop in loadout) and
        (pinkDoor in loadout) and  # to warrior shrine access
        (can_bomb(1) in loadout) and  # PB placement is important if you only have 10 ammo
        ((Speedball in loadout) or (Tricks.mockball_hard in loadout))
    ),
    "Path Of Swords": lambda loadout: (
        (sunkenNestToVulnar in loadout) and
        ((can_bomb(1) in loadout) or (
            (Morph in loadout) and (Screw in loadout)
        ))
    ),
    "Auxiliary Pump Room": lambda loadout: (
        (sunkenNestToVulnar in loadout) and (can_bomb(1) in loadout)
    ),
    "Monitoring Station": lambda loadout: (
        (sunkenNestToVulnar in loadout) and
        (Morph in loadout) and
        ((Speedball in loadout) or (can_bomb(1) in loadout) or (Tricks.movement_zoast in loadout))
    ),
    "Sensor Maintenance: AmmoTank": lambda loadout: (  # back
        (sensorMaintenance in loadout) and
        (can_bomb(2) in loadout)  # TODO: confirm this is the only difference from the other sensor maintenance item
    ),
    "Causeway Overlook": lambda loadout: (
        (CausewayR in loadout) and (GravityBoots in loadout) and (can_bomb(1) in loadout)
    ),
    "Placid Pool": lambda loadout: (
        (PlacidPoolR in loadout) and
        (GravityBoots in loadout) and
        (can_use_pbs(1) in loadout) and
        (icePod in loadout) and
        ((GravitySuit in loadout) or (
            (HiJump in loadout) and (Tricks.crouch_or_downgrab in loadout)
        ) or (
            (Tricks.sbj_underwater_no_hjb in loadout)
        ))
    ),
    "Blazing Chasm": lambda loadout: (
        (ElevatorToMagmaLakeR in loadout) and
        (GravityBoots in loadout) and
        (can_use_pbs(1) in loadout) and
        # no aqua will require crystal flash
        (lava_run(850, 1650) in loadout) and
        (MetroidSuit in loadout) and
        # something to do damage here
        (loadout.has_any(Screw, Plasma, Spazer, shootThroughWalls, Super, Tricks.movement_zoast)) and
        # a non-simple jump to get up blazing chasm
        ((
            (GravitySuit in loadout) and
            ((canFly in loadout) or (Tricks.gravity_jump in loadout))
        ) or (
            (HiJump in loadout)
        ))
    ),
    "Generator Manifold": lambda loadout: (
        (Super in loadout) and
        (GravityBoots in loadout) and
        (can_bomb(4) in loadout) and
        ((
            (ReservoirMaintenanceTunnelR in loadout) and
            (can_bomb(1) in loadout) and
            (Geothermal.thermalResBeta in loadout)
        ) or (
            (GeneratorAccessTunnelL in loadout) and
            (MetroidSuit in loadout) and  # top laser puzzles are 1 way w/o metroid suit
            (Screw in loadout) and
            (can_use_pbs(3) in loadout)
        ) or (
            (ThermalReservoir1R in loadout) and
            (MetroidSuit in loadout) and
            (Screw in loadout) and
            (Geothermal.thermalResAlpha in loadout)
        ))
    ),
    "Fiery Crossing Cache": lambda loadout: (
        (RagingPitL in loadout) and
        (GravityBoots in loadout) and
        (varia_or_hell_run(420) in loadout) and
        (can_use_pbs(1) in loadout)
    ),
    "Dark Crevice Cache": lambda loadout: (
        (ElevatorToMagmaLakeR in loadout) and
        (GravityBoots in loadout) and
        (can_bomb(1) in loadout) and
        (
            (canFly in loadout) or
            (SpeedBooster in loadout) or
            ((HiJump in loadout) and (Tricks.wall_jump_precise in loadout) and (DarkVisor in loadout))
        ) and
        # or wall_jump_insane (same as worst room with no hjb) - and doing it in the dark would be stupid
        ((DarkVisor in loadout) or (Tricks.dark_hard in loadout))
        # TODO: should wall jump in the dark be different from canFly or speedbooster in the dark?
    ),
    "Ancient Basin": lambda loadout: (  # similar to gymnasium
        (GravityBoots in loadout) and
        ((  # from west
            ((
                (VulnarDepthsElevatorEL in loadout) and
                (FireHive.hiveEntrance in loadout) and
                (icePod in loadout) and
                (FireHive.crossways in loadout) and
                (FireHive.crosswaysToCourtyard in loadout)
            ) or (
                (SequesteredInfernoL in loadout) and
                (FireHive.infernalSequestration in loadout) and
                (FireHive.crosswaysToCourtyard in loadout)
            ) or (
                (collapsedHive in loadout)  # using fire temple courtyard as a pit stop
            )) and
            # from fire temple courtyard to item in ancient basin
            (loadout.has_any(killRippers, Varia, Tricks.movement_zoast)) and  # just outside courtyard
            ((  # through power bomb blocks
                (can_use_pbs(3) in loadout) and
                (varia_or_hell_run(444, heat_and_metroid_suit_not_required=True) in loadout)
            ) or (  # through ancient basin
                (can_bomb(3) in loadout) and
                (loadout.has_any(Tricks.crumble_jump, SpaceJump, Speedball, Grapple)) and
                (varia_or_hell_run(661, heat_and_metroid_suit_not_required=True) in loadout)
            ))
        ) or (  # from east, no fire temple courtyard
            (collapsedHive in loadout) and
            (loadout.has_any(Tricks.crumble_jump, SpaceJump, Speedball, Grapple)) and
            (varia_or_hell_run(1216, heat_and_metroid_suit_not_required=True) in loadout)
        ))
    ),
    "Central Corridor: right": lambda loadout: (
        (GravityBoots in loadout) and
        (can_bomb(1) in loadout) and
        (doorsToCentralCorridorBottom in loadout)
    ),
    "Briar: AmmoTank": lambda loadout: (  # bottom
        (norakToLifeTemple in loadout) and
        (Morph in loadout) and
        (GravityBoots in loadout)
    ),
    "Icy Flow": lambda loadout: (
        (railAccess in loadout) and (GravityBoots in loadout) and (SpeedBooster in loadout) and (breakIce in loadout)
    ),
    "Ice Cave": lambda loadout: (
        (railAccess in loadout) and (GravityBoots in loadout) and (breakIce in loadout)
    ),
    "Antechamber": lambda loadout: (
        (railAccess in loadout) and (GravityBoots in loadout) and (can_use_pbs(1) in loadout)
    ),
    "Eddy Channels": lambda loadout: (
        (EleToTurbidPassageR in loadout) and
        (
            (GravitySuit in loadout) or
            (HiJump in loadout) or
            ((Ice in loadout) and (Tricks.freeze_hard in loadout))
        ) and
        (Morph in loadout) and
        (Speedball in loadout) and
        (Super in loadout) and
        (GravityBoots in loadout) and
        (loadout.has_any(DarkVisor, Tricks.dark_medium))
    ),
    "Tram To Suzi Island": lambda loadout: (
        (TramToSuziIslandR in loadout) and (GravityBoots in loadout) and (Spazer in loadout) and (Morph in loadout)
    ),
    "Portico": lambda loadout: (
        (enterSuzi in loadout) and
        (Super in loadout)
    ),
    "Tower Rock Lookout": lambda loadout: (
        (enterSuzi in loadout) and
        (pinkDoor in loadout) and
        (GravitySuit in loadout) and
        ((
            (SpaceJump in loadout) and
            (HiJump in loadout) and
            (SpaceJumpBoost in loadout)
            # TODO: how many sjb required?
        ) or (
            (Bombs in loadout) and
            (Morph in loadout) and
            (Tricks.movement_moderate in loadout)
        ) or (
            (SpeedBooster in loadout) and
            (Tricks.movement_moderate in loadout)
        ))
    ),
    "Reef Nook": lambda loadout: (
        (enterSuzi in loadout) and
        (pinkDoor in loadout) and
        (GravitySuit in loadout) and
        (Morph in loadout) and
        (Suzi.crossOceans in loadout)
    ),
    "Saline Cache": lambda loadout: (
        (enterSuzi in loadout) and
        (Super in loadout) and
        (
            ((GravitySuit in loadout) and (canFly in loadout)) or
            (Tricks.gravity_jump in loadout) or
            (Tricks.sbj_underwater_w_hjb in loadout)
        )
    ),
    "Enervation Chamber": lambda loadout: (
        (enterSuzi in loadout) and
        (Suzi.cyphers in loadout) and
        (Hypercharge in loadout) and
        (Charge in loadout)
    ),
    "Weapon Locker": lambda loadout: (
        (Missile in loadout) and
        (topOfSpaceport in loadout)
    ),
    "Aft Battery": lambda loadout: (
        (Morph in loadout) and
        (topOfSpaceport in loadout)
    ),
    "Forward Battery": lambda loadout: (
        loadout.has_all(Morph, Missile, topOfSpaceport)
    ),
    "Gantry": lambda loadout: (
        (Missile in loadout) and
        (topOfSpaceport in loadout)
    ),
    "Garden Canal": lambda loadout: (
        (NorakPerimeterBL in loadout) and
        (GravityBoots in loadout) and
        (can_use_pbs(1) in loadout) and
        (Spazer in loadout) and
        (LifeTemple.veranda in loadout)
        # TODO: Might there be a reason to add logic from ElevatorToWellspringL ?
    ),
    "Sandy Burrow: AmmoTank": lambda loadout: (  # bottom
        (OceanShoreR in loadout) and
        (Morph in loadout) and
        (GravityBoots in loadout) and
        # up to entrance
        ((GravitySuit in loadout) or (
            loadout.has_all(HiJump, Tricks.movement_zoast)
        ) or (
            (Tricks.sbj_underwater_w_hjb in loadout)
        )) and
        # out
        (  # to get back in hole after getting this item
            (Speedball in loadout) or
            loadout.has_all(GravitySuit, Bombs) or
            loadout.has_all(GravitySuit, PowerBomb) or
            (Tricks.morph_jump_3_tile_water in loadout)
        ) and
        (
            (GravitySuit in loadout) or (
                (Tricks.sbj_underwater_w_hjb in loadout)
            ) or (
                ((HiJump in loadout) and (Ice in loadout) and (Tricks.freeze_hard in loadout))
            )
        )
    ),
    "Trophobiotic Chamber": lambda loadout: (
        (sunkenNestToVulnar in loadout) and (Morph in loadout) and (Speedball in loadout)  # or Tricks.bob
    ),
    "Waste Processing": lambda loadout: (
        (SpeedBooster in loadout) and
        (GravityBoots in loadout) and
        (Morph in loadout) and
        ((can_bomb(1) in loadout) or (Screw in loadout)) and
        ((
            (SubbasementFissureL in loadout) and
            (can_use_pbs(1) in loadout)  # door into waste processing
            # If I didn't have speedbooster, then I would want either 2 pbs
            # or something else to kill green pirates with, because it would
            # be difficult to get up exhaust vent without killing them.
        ) or (
            (CellarR in loadout) and
            (pinkDoor in loadout) and  # door from cellar access to crumbling basement
            (can_bomb(1) in loadout) and
            ((DarkVisor in loadout) or (Tricks.dark_easy in loadout))
        ) or (
            (FieldAccessL in loadout) and
            ((DarkVisor in loadout) or (Tricks.dark_easy in loadout)) and
            (pinkDoor in loadout) and  # field access to east spore field
            (shootThroughWalls in loadout) and
            (can_bomb(1) in loadout)
        ) or (
            (TransferStationR in loadout) and
            (DarkVisor in loadout) and
            (shootThroughWalls in loadout) and
            (can_bomb(1) in loadout)
        ))
    ),
    "Grand Chasm": lambda loadout: (
        (railAccess in loadout) and (GravityBoots in loadout) and (Screw in loadout) and
        (
            # from left
            (can_bomb(6) in loadout) or
            ((can_bomb(4) in loadout) and (Speedball in loadout)) or
            # from right
            (
                (can_bomb(2) in loadout) and
                ((
                    (SpaceJump in loadout)
                ) or (
                    # without space jump you have to run a bit on spikes
                    (energy_req(121) in loadout)
                ))
            )
        )
    ),
    "Mining Site 1": lambda loadout: (  # (1 = letter Alpha)
        (GravityBoots in loadout) and
        (can_bomb(1) in loadout) and
        ((Speedball in loadout) or (Bombs in loadout) or (Tricks.morph_jump_4_tile in loadout)) and
        (pinkDoor in loadout) and
        (loadout.has_any(Ice, killRippers, Tricks.movement_moderate)) and
        ((
            (FieryGalleryL in loadout) and
            (Verdite.fieryTrail in loadout)
        ) or (
            (SporousNookL in loadout) and
            (Verdite.hotSpring in loadout)
        ))
    ),
    "Colosseum": lambda loadout: (  # GT
        (ElevatorToMagmaLakeR in loadout) and (GravityBoots in loadout) and (DrayLand.killGT in loadout)
    ),
    "Lava Pool": lambda loadout: (
        loadout.has_all(GravityBoots, lava_run(664, 1258), MetroidSuit, can_bomb(1)) and
        ((
            (FieryGalleryL in loadout) and
            (Verdite.fieryTrail in loadout)
        ) or (
            (SporousNookL in loadout) and
            (Verdite.hotSpring in loadout)
        ))
        # TODO: logic from Hollow Chamber and Placid Pool (don't have to go through mining site beta)
    ),
    "Hive Main Chamber": lambda loadout: (
        # copy and paste infested passage
        (GravityBoots in loadout) and
        ((
            (VulnarDepthsElevatorEL in loadout) and
            (FireHive.hiveEntrance in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (FireHive.infernalSequestration in loadout) and
            (FireHive.crossways in loadout) and
            (icePod in loadout)
        ))
    ),
    "Crossway Cache": lambda loadout: (
        ((
            (VulnarDepthsElevatorEL in loadout) and
            (FireHive.hiveEntrance in loadout) and
            (icePod in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (FireHive.infernalSequestration in loadout) and
            (FireHive.crossways in loadout)
        ) or (
            (collapsedHive in loadout) and
            (FireHive.crossways in loadout)
        ))
    ),
    "Slag Heap": lambda loadout: (
        # TODO: unit test for the requirements from different area doors
        ((
            (VulnarDepthsElevatorEL in loadout) and
            (FireHive.hiveEntrance in loadout) and
            (icePod in loadout) and
            (FireHive.crossways in loadout)
        ) or (
            (SequesteredInfernoL in loadout) and
            (FireHive.infernalSequestration in loadout)
        ) or (
            (collapsedHive in loadout)
        )) and
        (icePod in loadout) and
        (MetroidSuit in loadout) and
        (can_bomb(3) in loadout) and
        (lava_run(450, 950) in loadout)
    ),
    "Hydrodynamic Chamber": lambda loadout: (
        (GravityBoots in loadout) and
        (Spazer in loadout) and
        (Morph in loadout) and
        ((
            (doorsToWestCorridorTop in loadout) and
            (PirateLab.westCorridorToCentralTop in loadout)
        ) or (
            (doorsToCentralCorridorMid in loadout) and
            (Screw in loadout)
        ))
    ),
    "Central Corridor: left": lambda loadout: (
        # don't need other area doors if everything here will get through east corridor
        (GravitySuit in loadout) and
        (Speedball in loadout) and
        (SpeedBooster in loadout) and
        (GravityBoots in loadout) and
        (Morph in loadout) and
        (can_bomb(1) in loadout) and
        (doorsToCentralCorridorBottom in loadout)
    ),
    "Restricted Area": lambda loadout: (
        (MetroidSuit in loadout) and
        (doorsToCentralCorridorMid in loadout)
        # note: if you accidentally shoot the laser switch, you'll make it so you need shootThroughWalls,
        # so don't do that if you can't shoot through walls
    ),
    "Foundry": lambda loadout: (
        (GravityBoots in loadout) and
        (FoyerR in loadout) and
        (
            (energy_req(129) in loadout) or
            ((MetroidSuit in loadout) and (Speedball in loadout)) or
            (Tricks.movement_zoast in loadout)
        ) and
        (PirateLab.eastCorridor in loadout)
    ),
    "Norak Escarpment": lambda loadout: (
        (NorakBrookL in loadout) and (GravityBoots in loadout) and (canFly in loadout)
    ),
    "Glacier's Reach": lambda loadout: (
        (railAccess in loadout) and
        (GravityBoots in loadout) and
        ((can_bomb(1) in loadout) or (breakIce in loadout)) and
        (varia_or_hell_run(252) in loadout)
    ),
    "Sitting Room": lambda loadout: (
        (can_use_pbs(1) in loadout) and  # might have to farm after opening door
        (GravityBoots in loadout) and
        (railAccess in loadout) and
        (Morph in loadout) and  # exit
        (pinkDoor in loadout) and  # bottom of stair of dawn  # TODO: or get out by killing Phantoon
        (varia_or_hell_run(98) in loadout) and
        ((Speedball in loadout) or (Bombs in loadout) or (
            loadout.has_all(Tricks.morph_jump_3_tile, Tricks.morph_jump_4_tile)
        ) or (
            loadout.has_all(Tricks.morph_jump_4_tile, can_bomb(6))
        ))
    ),
    "Suzi Ruins Map Station Access": lambda loadout: (
        (enterSuzi in loadout) and
        (can_use_pbs(1) in loadout) and
        (Super in loadout)
    ),
    "Obscured Vestibule": lambda loadout: (
        (enterSuzi in loadout) and
        (can_bomb(1) in loadout)
    ),
    "Docking Port 3": lambda loadout: (  # (3 = letter Gamma)
        # copy and paste docking port 4
        (
            (spaceDrop not in loadout) and
            (Grapple in loadout)
        ) or (
            (spaceDrop in loadout) and
            (LoadingDockSecurityAreaL in loadout) and
            (GravityBoots in loadout) and
            (MetroidSuit in loadout)
        )
    ),
    "Arena": lambda loadout: (
        (ruinedConcourseBDoorToEldersTop in loadout)
    ),
    "West Spore Field": lambda loadout: (
        (sunkenNestToVulnar in loadout) and
        (pinkDoor in loadout) and  # into spore field
        (Super in loadout) and  # door into great spore hall
        ((shootThroughWalls in loadout) or (Tricks.ggg in loadout) or (Tricks.wave_gate_glitch in loadout)) and
        ((can_bomb(1) in loadout) or ((Morph in loadout) and (Screw in loadout))) and  # great spore hall
        (pinkSwitch in loadout) and  # return through great spore hall
        # get in to item
        (
            (Speedball in loadout) or
            loadout.has_all(GravitySuit, SpaceJump, SpaceJumpBoost, Tricks.movement_moderate)
        ) and
        # get out (of water)
        ((GravitySuit in loadout) or (HiJump in loadout) or (Tricks.sbj_underwater_no_hjb in loadout))
    ),
    "Magma Chamber": lambda loadout: (
        (ElevatorToMagmaLakeR in loadout) and
        (GravityBoots in loadout) and
        (can_use_pbs(1) in loadout) and  # (return logic)
        ((
            # lower lava
            (DrayLand.killGT in loadout) and
            (DrayLand.lakeMonitoringStation in loadout) and
            (varia_or_hell_run(652, heat_and_metroid_suit_not_required=True) in loadout)
        ) or (
            # lava dive
            (MetroidSuit in loadout) and
            (lava_run(349, 750) in loadout)
            # TODO: measure number with aqua (and lava not lowered) - 750 is a guess
        ))
        # TODO: moonfall? lava dive without metroid suit?
    ),
    "Equipment Locker": lambda loadout: (
        (doorsToWestCorridorTop in loadout) and
        (GravityBoots in loadout) and
        (pinkDoor in loadout) and
        (
            (GravitySuit in loadout) or
            (HiJump in loadout) or
            (can_bomb(1) in loadout) or
            (Tricks.sbj_underwater_no_hjb in loadout)
        ) and
        ((Morph in loadout) or (MetroidSuit in loadout))
    ),
    "Antelier": lambda loadout: (  # spelled "Antilier" in subversion 1.1
        (GravityBoots in loadout) and
        ((
            (doorsToWestCorridorTop in loadout) and
            (PirateLab.westCorridorToCentralTop in loadout) and
            ((PirateLab.waterGauntlet_oneWay in loadout) or (
                # backdoor main hydrology research
                loadout.has_any(GravitySuit, HiJump, Tricks.sbj_underwater_no_hjb)
            ))
        ) or (
            (doorsToCentralCorridorMid in loadout) and
            (Screw in loadout) and
            # backdoor main hydrology research
            loadout.has_any(GravitySuit, HiJump, Tricks.sbj_underwater_no_hjb) and
            (PirateLab.exitMainHydrologyResearch in loadout)
        ))
        # can gravity jump (no gravity suit)
        # through hydrodynamic chamber door into main hydrology research from central corridor
    ),
    "Weapon Research": lambda loadout: (
        (GravityBoots in loadout) and
        ((shootThroughWalls in loadout) or (MetroidSuit in loadout)) and
        ((can_bomb(5) in loadout) or ((Spazer in loadout) and (Morph in loadout))) and
        (doorsToCentralCorridorMid in loadout)
        # TODO: energy or movement or something to kill red pirates?
    ),
    "Crocomire's Lair": lambda loadout: (
        # similar to crocomire energy station, except don't need to go through bomb blocks on left
        (GravityBoots in loadout) and
        (norakToLifeTemple in loadout) and
        (LifeTemple.veranda in loadout) and
        (SpeedBooster in loadout) and
        (Super in loadout)  # door to elevator to jungle's heart
    ),
}