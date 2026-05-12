---
title: "Generic Pokémon Cries"
date: 2024-11-12
project: feature-branch
summary: "Five fallback Pokémon cries, chosen by base stat total, for pokeemerald-expansion projects that disable individual species cries to save ROM space."
description: "A pokeemerald-expansion generic cry system with five fallback cries assigned by base stat total, to save ROM instead of disabling individual species cries."
stats:
  Last branch update: 12th November 2024
  Fallback cries: 5
  Files changed: 10
---

## What It Does

For pokeemerald-expansion projects that disable Pokémon cries to save ROM space, by using `P_CRIES_ENABLED` this allows any species to use one of five shared fallback cries based on their base stat total:

| BST | Cry |
|---|---|
| Under 300 | Caterpie |
| 300–399 | Machop |
| 400–499 | Machoke |
| 500–599 | Machamp |
| 600 and above | Tyranitar |

I wanted to take from Generation 1 as the cries are some of the most basic due to the hardware at the time. Machops line seems like a very happy medium, and I hope using Caterpie and Tyranitar cries also gave the extremes a bit more variety.

*Porygon is handled separately. Its cry is hardcoded to play during the pokeemerald-expansion intro sequence by using the `CRY_MODE_RHH_INTRO` constant.*

## How It's Implemented

Two config values in `include/config/pokemon.h` are required to enable this. The pre-existing `P_CRIES_ENABLED` must be set to `FALSE` to disable individual species cries, and the new `P_CRIES_GENERIC` set to `TRUE` enables the generic cry system. A new `GetBaseStatTotal()` function sums all six base stats for a given species. `GetCryIdBySpecies()` is modified to check whether generic cries are active and return the appropriate generic cry instead of the species cry.

The five generic cries are also added in `sound/cry_tables.inc` and `sound/direct_sound_data.inc`, referenced as `Cry_Generic_Small` through `Cry_Generic_Largest`. Swapping any of them out can be done by replacing the cry file in `direct_sound_data.inc`.

## Future Implementation

In the future, I'd love to adjust these cries dynamically within the code based on other species factors. Their type, weight and height, potentially even on a per stat basis. But unfortunately, I'm not currently well enough versed in sound editting to be able to do this.

### Installation

The [diff for this feature](https://github.com/HashtagMarky/pokeemerald/commit/9707bda305f978e59da58aef9e8f9aa14c619696) can be used to add these changes.

## Why It's In Ikigai

ROM space on GBA is always constrained, and individual Pokémon cries are one of the larger consumers. By [Pokémon Ikigai](/productions/ikigai)'s nature, it's impossible to remove any given species, so generic cries by base stat total starts to solve that. A Starly and Giratina will both sound different from each other, even if neither sounds exactly right, but it's better than silence or a single cry for everything.
