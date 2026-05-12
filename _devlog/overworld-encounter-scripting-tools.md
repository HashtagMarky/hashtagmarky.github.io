---
title: "Overworld Encounter Scripting Tools"
date: 2024-10-04
project: feature-branch
summary: "Three scripting tools for triggering and spawning overworld wild Pokémon encounters in pokeemerald."
description: "pokeemerald scripting tools for overworld wild encounters — built for Pokémon Ikigai."
stats:
  Status: "Superseded by Expansion #8434"
  Last branch update: 15th June 2025
---

## What It Does

![Ikigai Overworld Encounter Scripting Tools in Action](/images/devlog/overworld-encounters/ikiagi_ow_encounters_tools.gif)
![Overworld Wander in Grass Movement](/images/devlog/overworld-encounters/wander_in_grass_movement.gif)

Three tools that make overworld wild Pokémon encounters usable in scripts and cutscenes, not just as ambient spawns. The tools were built in two commits, then improved by [LordRainDance](https://github.com/lordraindance2).

## How It's Implemented

**`GetOverworldMonSpecies`** reads the `graphicsId` of the last selected object event and returns a species ID. It covers every Pokémon object event in vanilla Emerald, and handles the expansion's `OBJ_EVENT_GFX_SPECIES()` macro automatically as well. Shininess is also checked. The species and shiny status are written into `VAR_0x8004` and `VAR_0x8005` respectively.

**`startoverworldencounter`** is a macro that chains this function and others to start a battle. It calls `GetOverworldMonSpecies`, plays the returned species cry, creates the enemy party and triggers the wild battle. Originally the macro required a `level` argument, meaning every encounter in script needed its own level written in manually.

**`setobjectaswildencounter`** calls the script command `ScrCmd_SetObjectAsWildEncounter` that reads a `localId` and `encounterType`. This object must be a variable object event. It calculates whether the Pokémon should spawn, using the equation `SPAWN_ODDS/65536`, and either hides the object via flag or pulls from the map's actual wild encounter table to pick a species. The encounter types that can be used are `ENCOUNTER_FIXED`, `ENCOUNTER_LAND`, `ENCOUNTER_SURF`, `ENCOUNTER_ROCK_SMASH`, `ENCOUNTER_OLD_ROD`, `ENCOUNTER_GOOD_ROD`, and `ENCOUNTER_SUPER_ROD`, pulling from the the relevant encounter tables. There is also a fallback table, in case the encounter header could not be used or if `ENCOUNTER_FIXED` is chosen. The species is packed into the object's graphics ID variable, is how the it is later used again.

### A Contributor Improvement

Later on, I received a PR from `lordraindance2`, which was genuinely amazing. It felt great to know that someone cared enough about my code to submit a very welcome inprovement. It refactored `startoverworldencounter` so levels are drawn automatically from the route's encounter table data rather than requiring a manual argument. The getter functions (`GetLocalLandMon`, `GetLocalWaterMon`, `GetLocalRockSmashMon`, `GetLocalFishingMon`) were changed from returning just a species ID to returning a full `WildPokemon` struct with level included. A new `GenerateOverworldWildMon()` function was added to get encounter data by graphics ID.

### Wander Movement Types

Two additional movement types restrict where object events can wander, making them behave more naturally as overworld wild Pokémon. `MOVEMENT_TYPE_WANDER_IN_GRASS` prevents an object from stepping onto any non-grass metatile, and `MOVEMENT_TYPE_WANDER_IN_WATER` does the same, but for surfable water. Both of these use the existing wander step functions in `MovementType_WanderAround`, with `Step4` adjusted to check metatile behaviour.

*`MovementType_Wander_Step3` was [consolidated in pokeemerald-expansion v1.9.2](https://github.com/rh-hideout/pokeemerald-expansion/pull/5359), so projects on earlier versions should use `MovementType_WanderAround_Step3` instead.*

### Installation

This feature can be pulled by commits. The [`README.md`](https://github.com/HashtagMarky/pokeemerald/blob/ikigai/ow-encounters/README.md) of this branch can be used to add these changes. A full tutorial for the new movement types can be found on the [Team Aqua's Asset Repo wiki](https://github.com/TeamAquasHideout/Team-Aquas-Asset-Repo/wiki/Create-Wander-in-Grass-and-Surfable-Water-Movement-Types).

## Why It's In Ikigai

[Pokémon Ikigai](/productions/ikigai) has scripted moments built around specific wild Pokémon, and these may contain encounters that can be shown better than just having the player step into grass. These tools make that possible without hardcoding species into battle setup scripts or writing specific workarounds for every encounter.
