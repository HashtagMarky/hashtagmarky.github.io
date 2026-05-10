---
title: "Upgradable Fishing Rod"
date: 2024-10-24
project: feature-branch
summary: "A single fishing rod key item with a dynamic menu of unlocked techniques, replacing the three-rod system with flag-gated progression and a remembered last-used technique."
description: "A pokeemerald implementation of an upgradable fishing rod — one item with a dynamic technique menu, replacing Old Rod, Good Rod, and Super Rod with gated progression."
stats:
  Last branch update: 24th October 2024
  Files changed: 4
---

## What It Does

![Upgradable Fishing Rod with Old Technique](/images/devlog/upgradable-fishing-rod/old-technique.jpg)
![Upgradable Fishing Rod with Good Technique](/images/devlog/upgradable-fishing-rod/good-technique.jpg)
![Upgradable Fishing Rod with Super Technique](/images/devlog/upgradable-fishing-rod/super-technique.jpg)

Replaces the three-rod system with a single `ITEM_VARIABLE_ROD` key item. When used, it opens a dynamic menu showing whichever "techniques" the player has unlocked; Old, Good, and Super. The latter two are gated by flags:

- `OW_FLAG_VARIABLE_ROD_GOOD_TECHNIQUE`: unlocks Good Fishing Technique
- `OW_FLAG_VARIABLE_ROD_SUPER_TECHNIQUE`: unlocks Super Fishing Technique

The last selected technique is written into `OW_VAR_VARIABLE_ROD_USE_TECHNIQUE`. `ItemUseOnFieldCB_VariableRod()` reads that `VAR` and triggers the old, good or super rod fishing logic accordingly. When the rod is used as a registered item, the same `VAR` applies, so the last used technique is remembered between uses without the player having to reselect it.

## How It's Implemented

Four files were changed, including `include/config/overworld.h` containing three new defines for the `VAR` and two `FLAGS` and `src/item_menu.c` containing the three menu actions and handler functions that each write the chosen technique to the `VAR` before fishing begins.

## How to Use It

By default the item is `ITEM_VARIABLE_ROD`. To attach the behaviour to an existing rod item instead, swap the `itemId` and assign `ItemUseOutOfBattle_VariableRod` as its field use function. Repurposing `FLAG_RECEIVED_OLD_ROD`, `FLAG_RECEIVED_GOOD_ROD`, and `FLAG_RECEIVED_SUPER_ROD` for the technique flags is the straightforward route if those flags aren't needed for anything else.

### Installation

The [diff for this feature](https://github.com/HashtagMarky/pokeemerald/commit/d98aa33b603d26ecf536d75e2d301771198f666c) can be used to add these changes.

## Why It's In Ikigai

Giving the player three separate fishing rod key items feels a bit *odd* to me. With modern generations not even including a fishing rod, having one item that the protagonist can ***learn*** to use in different ways as the story progresses fits [Pokémon Ikigai](/ikigai)'s progression design a lot better.
