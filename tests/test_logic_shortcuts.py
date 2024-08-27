import pytest

from subversion_rando.area_rando_types import DoorPairs
from subversion_rando.game import Game, GameOptions
from subversion_rando.trick import Trick
from subversion_rando.item_data import Items
from subversion_rando.loadout import Loadout
from subversion_rando.logicCommon import ammo_in_loadout, ammo_req, \
    energy_from_tanks, crystal_flash, energy_req, take_damage, varia_or_hell_run
from subversion_rando.logic_presets import casual, expert
from subversion_rando.logic_shortcut import LogicShortcut


def test_energy_from_tanks() -> None:
    assert energy_from_tanks(0) == 99
    assert energy_from_tanks(1) == 199
    assert energy_from_tanks(2) == 299
    assert energy_from_tanks(3) == 399
    assert energy_from_tanks(4) == 499
    assert energy_from_tanks(7) == 799
    assert energy_from_tanks(10) == 1099
    assert energy_from_tanks(11) == 1199
    assert energy_from_tanks(12) == 1299
    assert energy_from_tanks(13) == 1349
    assert energy_from_tanks(14) == 1399
    assert energy_from_tanks(15) == 1449
    assert energy_from_tanks(16) == 1499


def make_game(logic: frozenset[Trick]) -> Game:
    options = GameOptions(logic, False, "D", True)
    return Game(options, {}, DoorPairs([]), 0)


def test_energy_req() -> None:
    game = make_game(casual)
    loadout = Loadout(game, (Items.Energy for _ in range(10)))

    assert energy_req(900) in loadout
    assert energy_req(1100) not in loadout

    loadout.append(Items.Energy)
    loadout.append(Items.Energy)

    assert energy_req(1100) in loadout

    loadout = Loadout(game)  # empty

    assert energy_req(900) not in loadout

    game = make_game(expert)
    loadout = Loadout(game)  # empty

    assert energy_req(700) not in loadout

    loadout.append(Items.Energy)

    assert energy_req(700) not in loadout

    for _ in range(7):
        loadout.append(Items.Energy)

    assert energy_req(700) in loadout
    assert energy_req(500) in loadout
    assert energy_req(900) not in loadout


def test_take_damage_casual_avoidable() -> None:
    game = make_game(casual)
    loadout = Loadout(game, (Items.Energy for _ in range(7)))

    assert take_damage(798) in loadout
    assert take_damage(799) not in loadout

    loadout.append(Items.MetroidSuit)

    assert take_damage(1050) in loadout
    assert take_damage(1100) not in loadout

    loadout.contents[Items.MetroidSuit] = 0
    loadout.append(Items.Varia)

    assert take_damage(1050) in loadout
    assert take_damage(1100) not in loadout

    loadout.append(Items.Aqua)

    assert take_damage(1500) in loadout
    assert take_damage(1650) not in loadout

    loadout = Loadout(game)

    assert take_damage(80) in loadout
    assert take_damage(125) not in loadout

    loadout.append(Items.Aqua)
    loadout.append(Items.MetroidSuit)
    loadout.append(Items.Varia)

    assert take_damage(350) in loadout
    assert take_damage(450) not in loadout


def test_take_damage_expert_avoidable() -> None:
    game = make_game(expert)
    loadout = Loadout(game, (Items.Energy for _ in range(2)))

    assert take_damage(798) in loadout
    assert take_damage(799) in loadout
    assert take_damage(7000000) in loadout

    loadout.append(Items.Varia)

    assert take_damage(1) in loadout
    assert take_damage(11000) in loadout


def test_take_damage_expert_unavoidable() -> None:
    game = make_game(expert)
    loadout = Loadout(game, (Items.Energy for _ in range(2)))

    assert take_damage(500, 298) in loadout
    assert take_damage(50, 299) not in loadout
    assert take_damage(7000000, 250) in loadout

    loadout.append(Items.Aqua)

    assert take_damage(1, 299) in loadout
    assert take_damage(11000, 380) in loadout
    assert take_damage(240, 420) not in loadout


def test_varia_or_hell_run() -> None:
    game = make_game(expert)
    loadout = Loadout(game)

    assert varia_or_hell_run(400) not in loadout
    assert varia_or_hell_run(800) not in loadout
    assert varia_or_hell_run(1200) not in loadout

    for _ in range(10):
        loadout.append(Items.Energy)

    assert varia_or_hell_run(400) in loadout
    assert varia_or_hell_run(800) in loadout
    assert varia_or_hell_run(1200) not in loadout

    loadout.append(Items.Energy)
    loadout.append(Items.Energy)
    loadout.append(Items.Energy)

    assert varia_or_hell_run(1200) in loadout

    loadout.append(Items.Varia)  # varia and energy

    assert varia_or_hell_run(400) in loadout
    assert varia_or_hell_run(800) in loadout
    assert varia_or_hell_run(1200) in loadout
    assert varia_or_hell_run(1400) in loadout

    loadout = Loadout(game)
    loadout.append(Items.Varia)  # only varia, no energy

    assert varia_or_hell_run(400) in loadout
    assert varia_or_hell_run(800) in loadout
    assert varia_or_hell_run(1200) in loadout
    assert varia_or_hell_run(1400) in loadout


def test_other_suit_hell_runs() -> None:
    game = make_game(expert)
    loadout = Loadout(game)
    loadout.append(Items.MetroidSuit)
    loadout.append(Items.Aqua)
    for _ in range(6):
        loadout.append(Items.Energy)

    assert varia_or_hell_run(1450, heat_and_metroid_suit_not_required=True) not in loadout

    loadout.append(Items.Energy)

    assert varia_or_hell_run(1450, heat_and_metroid_suit_not_required=True) in loadout


def test_use_as_bool() -> None:
    """
    `LogicShortcut` must have a connection to a `Loadout`,
    so it must be used with `in loadout`

    It will be easy to forget the `in loadout`,
    so this test is to make sure it raises an exception if it's used without it.
    """
    can_bomb_jump = LogicShortcut(lambda loadout: (
        (Items.GravityBoots in loadout) and
        (Items.Bombs in loadout) and
        (Items.Morph in loadout)
    ))
    game = make_game(casual)
    loadout = Loadout(game)

    with pytest.raises(TypeError):
        _ = (
            can_bomb_jump and (Items.Charge in loadout)  # type: ignore
        )

    with pytest.raises(TypeError):
        _ = (
            can_bomb_jump or (Items.Screw in loadout)  # type: ignore
        )


def test_ammo_in_loadout() -> None:
    game = make_game(casual)
    loadout = Loadout(game)

    assert ammo_in_loadout(loadout) == 0, f"empty loadout has {ammo_in_loadout(loadout)}"

    loadout.append(Items.SmallAmmo)

    assert ammo_in_loadout(loadout) == 5

    loadout.append(Items.LargeAmmo)
    loadout.append(Items.LargeAmmo)
    loadout.append(Items.LargeAmmo)

    assert ammo_in_loadout(loadout) == 35

    loadout.append(Items.PowerBomb)

    assert ammo_in_loadout(loadout) == 45

    loadout.append(Items.Missile)
    loadout.append(Items.Super)

    assert ammo_in_loadout(loadout) == 65

    # TODO: test in game (and then add tests here)
    # If there are 2 power bombs in pool, will the 2nd pick up give 10 ammo? or 0?


def test_ammo_req() -> None:
    game = make_game(casual)
    loadout = Loadout(game)

    assert ammo_req(5) not in loadout

    loadout.append(Items.PowerBomb)
    loadout.append(Items.LargeAmmo)
    loadout.append(Items.LargeAmmo)

    assert ammo_req(20) in loadout
    assert ammo_req(30) in loadout
    assert ammo_req(40) not in loadout

    loadout.append(Items.Missile)
    loadout.append(Items.Super)

    assert ammo_req(40) in loadout
    assert ammo_req(50) in loadout
    assert ammo_req(60) not in loadout

    loadout.append(Items.Morph)

    assert crystal_flash not in loadout

    for _ in range(12):
        loadout.append(Items.SmallAmmo)

    assert crystal_flash in loadout

    loadout.append(Items.SmallAmmo)

    assert crystal_flash in loadout

    loadout.contents[Items.Morph] -= 1

    assert crystal_flash not in loadout


if __name__ == "__main__":
    test_use_as_bool()
