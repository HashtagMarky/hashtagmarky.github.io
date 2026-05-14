# #M Productions — Brand Identity

**Version 2.0 · May 2026**

-----

## Who is HashtagMarky

|Field      |Value                                                           |
|-----------|----------------------------------------------------------------|
|Handle     |@hashtagmarky (Instagram, TikTok) · @hashtagmrky (Twitter/X)    |
|Brand name |#M Productions                                                  |
|Description|Self-taught Pokémon ROM hacker, book lover, and tech builder    |
|Website    |hashtagmarky.github.io → custom domain (see Domain section)     |
|GitHub     |github.com/HashtagMarky                                         |
|YouTube    |@hashtag-marky                                                  |

### Brand Pillars

Everything Marky makes sits within three content pillars. Each pillar has its own visual accent colour used consistently across the website, devlog entries, and social posts.

|Pillar         |Content                                           |Accent Colour|Hex    |
|---------------|--------------------------------------------------|-------------|-------|
|🎮 ROM Hacking  |Pokémon Ikigai (active), future ROM hack projects |Orange       |#F09040|
|📚 Books        |Sci-fi & fantasy reviews, shelf entries           |Green        |#5CB85C|
|🔧 Tech & Builds|Lego Gameboy (in progress), Homelab (planned)     |Blue         |#5B9BD5|

Colours are defined in `_config.yml` under `colors:` and are applied site-wide through Jekyll-processed CSS. To change a colour, update `_config.yml` only — no CSS editing needed.

### Tone of Voice

- Conversational and honest — not corporate, not trying to be a brand account
- Specific over vague — names routes, book titles, exact problems
- Shows the work, including failures — build logs especially
- Nerd-fluent — comfortable with Pokémon lore, ROM hack terminology, hardware jargon

### Personal Brand vs Studio

HashtagMarky is a **personal brand**, not a studio. @hashtagmarky is the lead identity across all platforms. `#M Productions` works as a site/project label but the handle is the thing people follow and search for.

-----

## Domain & Branding

### The Branding Decision

**Stick with the personal brand. No rebrand needed.**

- **@hashtagmarky** = the person, the social handle, what people search
- **#M Productions** = the site/umbrella label, used in the site title and branding

### Domain Options

|Domain              |Verdict                                                                                                                    |
|--------------------|---------------------------------------------------------------------------------------------------------------------------|
|`hashtagmarky.dev`  |**Best choice.** Matches the handle exactly. `.dev` signals tech/builder. Best SEO alignment with social handle.          |
|`hashtagmarky.com`  |Strong fallback. Most recognisable TLD. Good for broader non-tech audiences.                                               |
|`hashtagmarky.co.uk`|Only if you want to explicitly signal UK base. Limits international discovery slightly.                                    |

### Custom Domain Setup (When Ready)

1. Buy the domain (Namecheap or Porkbun — both ~£10/year)
2. In the registrar, add a `CNAME` record pointing to `hashtagmarky.github.io`
3. In GitHub repo Settings → Pages → Custom domain, enter the domain
4. Enable **Enforce HTTPS** — GitHub provides the SSL certificate free
5. Update all social bio links to the new domain
