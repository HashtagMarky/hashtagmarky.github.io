---
title: "Car Boot GBA Build"
date: 2025-07-06
project: gba-mod
episode: 1
summary: "I picked up a tired looking GBA for pennies on the pound at a car boot sale and turned it into something I'm genuinely proud of! A bright purple shell, IPS screen, USB-C charging, all in an afternoon."
description: "A full GBA mod built around a car boot sale find — including an IPS screen, purple shell and a USB-C battery pack. All picked up from AliExpress and installed with an iFixit toolkit."
stats:
  Source: Car boot sale
  Shell colour: Purple
  Screen: Drop-In Laminated IPS v5
  Power: USB-C battery pack
  Toolkit: iFixit
  Toal cost: Sub £100
---

## The Find

I've never had much luck at car boot sales when it comes to finding old hardware, which is why I wasn't even specifically looking. I'd gone out on a quiet Sunday morning with my partner, when I spotted a bunch of old game consoles layed out all over a blanket on the floor. It was buried under a tangle of random cables and sat by a SEGA Genesis, but there is was, a Game Boy Advance in fairly rough cosmetic condition. Now this would be my first time getting some original hardware to play GBA games on, other than using the second slot on a Nintendo DS, but I knew just how much working second hands one are currently going for. The person selling it however, either had no idea, or didn't care. It didn't have any batteries for me to test it out on the spot, but for the price it was going for, I was willing to take the risk.

The shell was a bit grubby and had a few scratches, but with a fresh set of batteries, it powered on and played sound. Working internals were all I needed, so started shopping around.

![Car Boot GBA Front](/images/devlog/gba-car-boot-build/car-boot-gba-front.jpg)
![Car Boot GBA Back](/images/devlog/gba-car-boot-build/car-boot-gba-back.jpg)

## The Parts

I watched a lot of reviews, trying to understand what parts are best, whether the premium machined shells were worth it, or whether I could go cheaper. In the end ordered almost everything from AliExpress as a bundle. It included:

- **Purple replacement shell**. I went with a plastic shell over a machined metal one. It came with all screws needed for an installation, which was useful as I would later realise the GBA I got was missing some.
- **IPS screen kit**. The drop-in replacement with a backlit screen, that I made sure had the right ribbon connecter for my GBA.
- **USB-C battery pack**. A rechargeable lithium battery pack that had to be shipped seperately. It slots into the battery tray and comes with a precut USB-C slot that can be used to charge it. I made sure that it allows for a large number of voltages.
- **Replacement buttons and pads**. The only parts I got from Amazon instead of AliExpress. Pearlescent blue and purple buttons that match the shell.

<div style="display: flex; flex-wrap: wrap; gap: 8px; align-items: flex-start;">
<img src="/images/devlog/gba-car-boot-build/ikigai-on-car-boot-gba.jpg" alt="Pokémon Ikigai on the Car Boot GBA Build">
</div>

*[Pokémon Ikigai's Purple Rotom Start Menu](/devlog/rotom-phone-start-menu) on matching hardware.*

The parts from AliExpress took about two and a half weeks to arrive, which gave me plenty of time to watch a few teardown videos to get prepared.

## The Build

I'd been given an iFixit toolkit (feel free to sponsor me) for my birthday that I hadn't even used yet, I knew the GBA uses tri-wing screws on the shell and Phillips heads were needed on the internals, so digging it out felt like a no brainer. As soon as I opened it, I gave the motherboard a bit of a scrub. I used some nail polish remover with high Isopropyl Alcohol content, some cotton buds and some light elbow grease.

<div style="display: flex; flex-wrap: wrap; gap: 8px; align-items: flex-start;">
<img src="/images/devlog/gba-car-boot-build/hearth-on-car-boot-gba.jpg" alt="Pokémon Hearth on the Car Boot GBA Build">
</div>

*[Doodle's Pokémon Hearth](https://www.hackdex.app/hack/pokemon-hearth) on the car boot GBA.*

With the motherboard clean, I moved it over to my new shell, reading to start the fiddly job of installing the IPS screen. The ribbon cable had to be routed carefully but fortunately the kit came with a custom shell that made it truly "drop-in", overall I actually found the process very easy. There are touch pads that can be stuck to the shell that can be used to change screen setting, which I did also try to add to the right places. Once it was in and I powered it on to test it out, working fine, no dead zones so hopefully worth every bit of fiddling. The USB-C battery pack was also straightforward. It slots in where the AA tray lives and came with a custom cover that allows for a cable. It feels odd to have a wire go into the bottom of the GBA, but I'm sure I can live with it. The new buttons and pads went in without any drama, but really gave the kit a nice accent.

## The Result

I am really really pleased with how this turned out. The purple shell is bright, the screen is sharp and the buttons are super clean. The total cost for everything and its shipping, other than the tools that I already had, was around £75, much less than what a refurbished unit in similar condition would run on eBay.

But more to the point: **I cannot wait to play Pokémon on it**.

<div style="display: flex; flex-wrap: wrap; gap: 8px; align-items: flex-start;">
<img src="/images/devlog/gba-car-boot-build/transform-on-car-boot-gba.jpg" alt="Pokémon Transform on the Car Boot GBA Build">
</div>

*[Phantonomy and Zatsu's Pokémon Transform](https://www.hackdex.app/hack/pokemon-transform) on the car boot GBA.*

With development of [Pokémon Ikigai](/ikigai) under way, I cannot wait to test it out so far on actual hardware. And with TARC2 (Team Aqua's ROM-Hacking Competition) well underway, I know I'll have some great entries to play soon.
