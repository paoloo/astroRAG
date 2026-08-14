# RAG Evaluation Report

Generated: 2026-08-13T17:29:51.153503+00:00
Model: `qwen2.5:14b-instruct` | Embedding: `nomic-embed-text`

**Keyword-match score - baseline: 7/18 | RAG-augmented: 16/18**
**LLM-judge score - baseline: 11/18 | RAG-augmented: 15/18**

| # | Question | Baseline (kw / judge) | RAG (kw / judge) | Sources |
|---|---|---|---|---|
| 1 | What type of planet was the first exoplanet discovered by TESS (the Transiting Exoplanet Survey Satellite)? | hit / miss | miss / miss | 0910.0484, 1503.01770, 1803.07867, 1809.05967, 1809.07242, 2008.05372, 2311.04981 |
| 2 | Out of the more than 500 confirmed transiting hot Jupiters, how many are currently known to have nearby companion planets? | hit / miss | hit / hit | 1706.09849, 2601.13302 |
| 3 | The microlensing event OGLE-2016-BLG-0007 revealed a super-Earth on an orbit wider than which planet's orbit in our solar system? | miss / miss | hit / hit | 2005.01542, 2304.04605, 2310.07502, 2504.20158, 2505.10621 |
| 4 | What happened to the Gaia DR3 exoplanet candidate announced around the star HD 12800? | hit / miss | hit / hit | 2404.09350, 2603.19402, 2607.20673 |
| 5 | Instead of high-eccentricity tidal migration, what alternative explanation do recent studies propose for why hot Jupiters tend to lack nearby planetary companions? | miss / hit | hit / hit | 1801.06117, 2201.11768, 2605.27362 |
| 6 | Through what photochemical mechanism can abiotic oxygen and ozone build up in rocky exoplanet atmospheres around M dwarfs, producing a false-positive biosignature? | hit / miss | hit / hit | 1309.6014, 1705.07560, 2404.15431, 2503.22990, 2603.11017 |
| 7 | Why might hundreds of TESS-discovered exoplanets actually be larger than their originally published radii? | miss / hit | hit / hit | 1412.6097, 2008.05372, 2010.15164, 2203.15826, 2506.19985 |
| 8 | Did a recent study using Kepler Q1-17 DR25 data find a significant trend between exoplanet occurrence rate and FGK host star age? | miss / hit | hit / hit | 1809.08385, 1902.01417, 2002.02573, 2112.03927, 2501.13809 |
| 9 | What level of mass-measurement precision may be necessary for the Habitable Worlds Observatory to identify the dominant gaseous species in an Earth-like planet's atmosphere? | miss / hit | hit / hit | 1304.3714, 1309.6014, 2006.07403, 2603.11146, 2607.14329 |
| 10 | According to recent circumplanetary disk models, where do water-rich moons like Ganymede, Callisto, and Titan form relative to the disk's ice line? | hit / hit | hit / hit | 1505.03516, 2602.21400 |
| 11 | What makes the WASP-47 planetary system notable among hot Jupiter systems? | miss / hit | hit / hit | 1108.2308, 1511.09157, 1603.02587, 1801.06117, 2503.00872 |
| 12 | Between what years did NCCR PlanetS make the major contributions to exoplanet climate and biosignature research described in its review? | miss / miss | hit / hit | 1705.05791, 1807.09504, 2601.20620, 2604.09385, 2607.21683, 2608.03857, 2608.06937 |
| 13 | Why might arid terrestrial exoplanets, such as those in the TRAPPIST-1 system, fail to maintain a balanced geologic carbon cycle? | miss / hit | hit / hit | 2604.16846 |
| 14 | What observational technique do researchers propose for detecting hypothetical exomoons around short-period exoplanets? | miss / miss | miss / miss | 0907.3909, 0910.0484, 2105.00034, 2405.01970, 2504.10126, 2509.15304, 2510.24575 |
| 15 | How does a planet's orbital eccentricity affect the dust at the edges of the gap it opens in a protoplanetary disk? | miss / hit | hit / hit | 1005.4557, 1908.11065, 2009.04345, 2607.05497 |
| 16 | According to statistical analyses of the Kepler planet population, planets around what multiple of Earth's radius show an unusually low occurrence rate? | miss / hit | hit / miss | 1301.0842, 1409.1904, 2006.15719, 2101.06621, 2511.02643, 2604.08406 |
| 17 | What unique short-wavelength observing capability does Hubble retain for exoplanet atmosphere characterization in the JWST era? | hit / hit | hit / hit | 1705.07098, 1810.04175, 2506.03299, 2606.04144, 2608.00520, 2608.05885 |
| 18 | What limitation of static mass-radius structure models for sub-Neptunes and super-Earths does recent work address by integrating radiative-convective and interior structure simulations? | hit / hit | hit / hit | 1710.05605, 2306.09002, 2507.18665, 2604.15891, 2607.16713 |

## Full transcripts

### 1. What type of planet was the first exoplanet discovered by TESS (the Transiting Exoplanet Survey Satellite)?
_expected keywords: sub-neptune, subneptune, pi men, π men_

**Baseline (no retrieval)** - keyword: hit, judge: miss

The first exoplanet discovered by TESS is TOI 123b, which orbits the star LHS 3844 in the constellation Draco. However, this may not be the most straightforward answer because the very first confirmed exoplanets detected by TESS are a set of three planets orbiting the star Pi Mensae (HD 39091). These planets were designated TOI-270 b, c, and d.

Among these initial discoveries, TOI 270 b is an interesting case: it's a super-Earth-sized planet with a radius about 1.25 times that of Earth and likely has a rocky composition. The other two planets in the system (TOI-270 c and d) are larger.

However, when discussing the first individual exoplanet announced by TESS, TOI 123b is often mentioned because it was one of the earliest confirmed discoveries following TESS's primary mission objectives.

The classification of TOI 123b as a planet can be described more specifically. It has a radius approximately 1.3 times that of Earth and orbits very close to its star, LHS 3844, completing an orbit in just 14 hours. Given its size and proximity to the host star, TOI 123b is classified as a rocky exoplanet with a high likelihood of being similar to Venus or Mercury in terms of composition and temperature due to its proximity to its star.

Therefore, among the early discoveries by TESS, both rocky super-Earths like TOI-270 b and close-in rocky planets like TOI 123b are representative of the types of exoplanets that TESS has been instrumental in finding.

**RAG-augmented** - keyword: miss, judge: miss

The first confirmed planetary discovery made as a result of the TESS mission is a super-Earth, specifically around the star _π_ Mensae. This planet has a size of approximately 2 Earth radii and an orbital period of 6.27 days [arXiv:1809.05967].

**Retrieved from:** 0910.0484, 1503.01770, 1803.07867, 1809.05967, 1809.07242, 2008.05372, 2311.04981

### 2. Out of the more than 500 confirmed transiting hot Jupiters, how many are currently known to have nearby companion planets?
_expected keywords: ten,  10 , 10., 10,_

**Baseline (no retrieval)** - keyword: hit, judge: miss

As of my last update in October 2023, the number of transiting hot Jupiter systems with known nearby companion planets is a subject of ongoing research and updates. Hot Jupiters, which are gas giant exoplanets that orbit very close to their host stars, have been the focus of various studies due to their intriguing properties.

To find an exact count for how many of the over 500 confirmed transiting hot Jupiters have nearby companion planets, you would need to consult recent publications and databases like the NASA Exoplanet Archive or peer-reviewed papers focusing on multi-planet systems. These resources often provide detailed information about exoplanetary systems that includes the presence of additional planets.

For the most accurate and up-to-date count, I recommend checking:

1. **NASA Exoplanet Archive**: This is a comprehensive database where you can filter for hot Jupiters and their companion planets.
2. **Exoplanet Orbit Database**: Another valuable resource with detailed information on planetary systems.
3. Recent scientific papers published in journals such as the Astronomical Journal, Monthly Notices of the Royal Astronomical Society, or Nature Astronomy.

These sources will provide you with the most current data and research findings regarding multi-planet systems around hot Jupiters.

**RAG-augmented** - keyword: hit, judge: hit

Out of the more than 500 confirmed transiting hot Jupiters, only ten are known to have nearby companion planets [arXiv:2601.13302].

**Retrieved from:** 1706.09849, 2601.13302

### 3. The microlensing event OGLE-2016-BLG-0007 revealed a super-Earth on an orbit wider than which planet's orbit in our solar system?
_expected keywords: saturn_

**Baseline (no retrieval)** - keyword: miss, judge: miss

The microlensing event OGLE-2016-BLG-0007 revealed a super-Earth with an orbital separation comparable to or slightly larger than that of Mars in our solar system. The exoplanet, designated as OGLE-2016-BLG-0007Lb, is estimated to have an orbital distance from its star of about 1.4 astronomical units (AU), where 1 AU is the average distance between Earth and the Sun. This places it outside the orbit of Earth but within the orbit of Mars, which averages around 1.52 AU from the Sun.

However, since the question asks for a planet in our solar system whose orbit this exoplanet's orbit is wider than, the correct answer would be Mercury or Venus, both having orbital separations closer to the Sun compared to approximately 1.4 AU. But more specifically, it means that the exoplanet's distance from its star is larger than any of the inner planets (Mercury at about 0.39 AU and Venus at about 0.72 AU), but smaller or around the same as Mars' orbit. Therefore, strictly speaking, if comparing to a single planet in our solar system with an orbital radius greater than 1.4 AU, it would be Mars.

**RAG-augmented** - keyword: hit, judge: hit

The microlensing event OGLE-2016-BLG-0007 revealed a super-Earth on an orbit longer than Saturn’s [arXiv:2504.20158].

**Retrieved from:** 2005.01542, 2304.04605, 2310.07502, 2504.20158, 2505.10621

### 4. What happened to the Gaia DR3 exoplanet candidate announced around the star HD 12800?
_expected keywords: retract, false, non-detect, not confirm_

**Baseline (no retrieval)** - keyword: hit, judge: miss

I couldn't find specific information about a Gaia Data Release 3 (DR3) announcement of an exoplanet candidate around the star HD 12800. However, this could be due to several reasons: the designation or details might have been misremembered, or the information may not yet be widely disseminated.

The Gaia mission has indeed released data catalogs that include astrometric measurements which can reveal potential exoplanet systems through the wobble induced on their host stars. The process of identifying and confirming exoplanet candidates from such data typically involves a rigorous verification phase involving additional observations and analyses by both the Gaia team and external researchers.

For HD 12800, if there were an announced candidate in Gaia DR3, it would likely be listed in the Exoplanet Follow-Up Observing Program (ExoFOP) page for that star or similar databases. If you have a specific reference or more details about this announcement, providing them could help refine the search and find the correct information.

If there's no widely recognized candidate around HD 12800 in Gaia DR3, it's possible that any initial signals detected were not confirmed as reliable exoplanet candidates after further scrutiny. It is also common for early announcements to be refined or retracted based on additional data and analysis over time.

To get the most accurate information, you might want to check:

1. The official Gaia mission website and its release notes.
2. Scientific papers and preprints discussing Gaia DR3 results specifically for HD 12800.
3. Exoplanet databases like NASA's exoplanet archive or the ExoFOP-TESS site.

If you're still unsure, reaching out to specific researchers involved in exoplanet studies around this star could provide more detailed and up-to-date information.

**RAG-augmented** - keyword: hit, judge: hit

The _Gaia_ DR3 exoplanet candidate announced around the star HD 12800 was retracted due to it being identified as a spurious orbital solution caused by software issues. Follow-up radial velocity (RV) observations failed to detect any expected signal from the proposed companion, confirming that the planet candidate did not exist prior to its formal retraction on 2024-05-27 [arXiv:2603.19402].

**Retrieved from:** 2404.09350, 2603.19402, 2607.20673

### 5. Instead of high-eccentricity tidal migration, what alternative explanation do recent studies propose for why hot Jupiters tend to lack nearby planetary companions?
_expected keywords: quiescent, disk migration, in situ, in-situ_

**Baseline (no retrieval)** - keyword: miss, judge: hit

Recent studies have explored several alternative explanations for the absence of nearby planetary companions around hot Jupiters, particularly focusing on mechanisms that prevent or disrupt the formation and long-term stability of close-in planets. Here are some key proposals:

1. **Planetesimal Disk Interactions**: Some researchers suggest that the process involving interactions with planetesimals (small rocky or icy bodies in a protoplanetary disk) can play a crucial role in shaping planetary systems. For example, the gravitational effects and collisions between hot Jupiters and nearby planetesimals might lead to the ejection of these smaller objects or their incorporation into the forming giant planets. This could leave little material left for the formation of additional close-in planets.

2. **Disk-Planet Interactions**: The gas and dust disk around young stars can influence planetary migration in ways that are not captured by high-eccentricity tidal migration models. Disk-induced migration processes, where a planet's orbit evolves due to interactions with its natal disk material (either inward or outward), could lead to the ejection or consumption of potential companions during their formation period.

3. **Resonant Scattering**: Another possibility is resonant scattering between planets in multi-planet systems as they migrate. This can result in a dynamic exchange of orbital elements, leading to instability and potential ejections of one or more planets from the system. If hot Jupiters are formed early in the life of their star’s protoplanetary disk and undergo rapid inward migration, such resonant interactions could clear out nearby regions, preventing additional close-in companions from forming or surviving.

4. **Post-Formation Dynamics**: After initial formation, complex gravitational interactions within multi-planetary systems can lead to instability. If a hot Jupiter forms in an outer region of the protoplanetary disk and migrates inward quickly, its rapid movement through the disk could disrupt any nascent planets trying to form closer to their star, causing them to be ejected or collide with each other.

5. **Tidal Dissipation and Stellar Spin-Orbit Misalignment**: Recent models also explore how tidal forces between a planet and its host star can lead to spin-orbit misalignments and orbital decay over long timescales, which might prevent the stable coexistence of multiple close-in planets due to complex resonant dynamics and chaotic behavior.

These alternative explanations highlight the complexity of planetary system formation and evolution. They suggest that while high-eccentricity tidal migration is a plausible mechanism for the inward movement of hot Jupiters, other physical processes during different stages of planet formation and early system dynamics might also play significant roles in shaping planetary architectures observed around stars hosting hot Jupiters.

**RAG-augmented** - keyword: hit, judge: hit

Recent studies propose that disk migration and in situ formation could also explain the observed trend of hot Jupiters lacking nearby planetary companions. Specifically:

1. Ogihara, Inutsuka & Kobayashi (2013), Ogihara, Kobayashi & Inutsuka (2014) suggested that super-Earths cannot form near a hot Jupiter that either migrated or formed in situ due to the tendency of these processes to drive the hot Jupiter into its star unless disk conditions allow for wide gaps. This model does not predict an absolute absence but rather a scarcity of nearby planets, especially super-Earths.

2. Schlaufman & Winn (2016) argued that the occurrence rate of longer period giant planet companions to hot Jupiters is consistent with that of companions to longer-period Jupiters (periods > 10 days). They suggest that this finding does not support high eccentricity tidal migration from beyond the ice line. The detection biases between radial velocity and transit methods also explain why some systems show different patterns of companion presence.

These explanations offer alternatives to high-eccentricity tidal migration in accounting for the observed paucity of nearby planetary companions around hot Jupiters [arXiv:1801.06117].

**Retrieved from:** 1801.06117, 2201.11768, 2605.27362

### 6. Through what photochemical mechanism can abiotic oxygen and ozone build up in rocky exoplanet atmospheres around M dwarfs, producing a false-positive biosignature?
_expected keywords: co2 photolysis, photolysis, co₂ photolysis_

**Baseline (no retrieval)** - keyword: hit, judge: miss

The buildup of abiotic oxygen (O₂) and ozone (O₃) in the atmosphere of an exoplanet orbiting an M dwarf star is a complex process that involves several photochemical mechanisms. These processes can lead to a false positive for biological activity, as they do not necessarily indicate the presence of life but rather non-biological chemical reactions under specific conditions.

### Key Photochemical Mechanisms:

1. **Water Photolysis:**
   - **Process:** Ultraviolet (UV) radiation from an M dwarf star breaks down water molecules in the exoplanet's atmosphere.
   - **Reaction:** \( \text{H}_2\text{O} + UV \rightarrow 2\text{OH} \)
   - **Products:** Hydroxyl radicals (OH), which can further react with other atmospheric components.

2. **Formation of O₂:**
   - **Process:** OH radicals from water photolysis can lead to the formation of molecular oxygen.
   - **Reaction:** \( 2\text{H}_2\text{O} + UV \rightarrow \text{O}_2 + 4\text{H}^+ + 4e^- \)
     This reaction implies that ultraviolet light breaks water into hydrogen and oxygen, but the direct pathway is often indirect through various chemical intermediates.

3. **Formation of O₃:**
   - **Process:** Oxygen (O₂) can be converted to ozone (O₃) through the absorption of UV radiation.
   - **Reaction:** \( \text{O}_2 + \text{h}\nu \rightarrow 2\text{O} \)
     Followed by:
     \( \text{O} + \text{O}_2 + M \rightarrow \text{O}_3 + M \)

### Conditions Favoring Abiotic Production:

- **High UV Flux:** M dwarf stars emit a significant amount of high-energy ultraviolet radiation, which is crucial for driving photochemical reactions.
- **Atmospheric Composition:** The presence of water vapor (H₂O) and carbon dioxide (CO₂) can enhance the production of O₂ and O₃ through various chemical pathways.

### False Positives:

- **False Biosignatures:** Since abiotic processes can produce substantial amounts of oxygen and ozone, their detection alone does not definitively indicate biological activity. This highlights the importance of corroborative evidence such as methane (CH₄) or other biomarker gases in conjunction with O₂/O₃.

### Conclusion:
The buildup of abiotic oxygen and ozone in exoplanet atmospheres around M dwarfs can occur through photochemical reactions driven by UV radiation, leading to false-positive biosignatures. Understanding these processes is crucial for accurately interpreting atmospheric data from future exoplanetary missions aimed at detecting life beyond Earth.

**RAG-augmented** - keyword: hit, judge: hit

Abiotic O2 and O3 can accumulate in the atmospheres of rocky exoplanets orbiting M dwarf stars through photolysis mechanisms involving CO2. Specifically, when UV radiation from an M dwarf star interacts with CO2 present in the planet's atmosphere, it can lead to the production of O2 without significant biological activity. Additionally, under certain conditions, such as high FUV (Far Ultraviolet) radiation and low H2O content, abiotic O3 can also form even if there is no substantial buildup of O2. This process can generate false-positive biosignatures, where oxygenated species are present but not due to biological activity, challenging the straightforward interpretation of these gases as indicators of life [arXiv:1705.07560; arXiv:2404.15431; arXiv:2603.11017].

**Retrieved from:** 1309.6014, 1705.07560, 2404.15431, 2503.22990, 2603.11017

### 7. Why might hundreds of TESS-discovered exoplanets actually be larger than their originally published radii?
_expected keywords: blend, dilut_

**Baseline (no retrieval)** - keyword: miss, judge: hit

TESS (Transiting Exoplanet Survey Satellite) has discovered a large number of exoplanets through the detection of transits, which are periodic dips in the brightness of a star as a planet passes in front of it. The size of an exoplanet is typically derived from the depth and duration of these transits. However, there can be several reasons why some TESS-discovered exoplanets might actually be larger than their originally published radii:

1. **Atmospheric Effects**: Exoplanets with extended atmospheres could appear larger in transit radius measurements compared to a planet without an atmosphere. The detection of atmospheric effects can lead to overestimations if not properly accounted for.

2. **Instrumental Systematics and Calibration Errors**: TESS data, like all astronomical observations, are subject to instrumental systematics and calibration uncertainties. These issues can sometimes cause the light curves (brightness measurements) to be misinterpreted, leading to incorrect planet radii estimates.

3. **Stellar Activity**: Variability in stellar activity can mimic transit signatures or affect the measurement of a transit’s depth. Stellar flares or starspots can create false signals that complicate the interpretation of transit data and lead to inaccurate radius measurements if not corrected for.

4. **Multiple Stars (Eclipsing Binaries)**: Some TESS detections are actually due to multiple star systems, particularly eclipsing binaries, where one star passes in front of another from our viewpoint. These can be misinterpreted as exoplanets, leading to incorrect size estimates.

5. **Light Curve Fitting**: The fitting process for light curves can sometimes lead to overestimations if the models used do not fully account for all physical phenomena occurring during transits. This includes issues like stellar limb darkening (how starlight decreases in intensity toward the edge of its disk), which needs precise modeling.

6. **Orbital Eccentricity**: If a planet's orbit is significantly eccentric, it can spend more time at different distances from its star as it moves through its elliptical path. This can complicate transit timing and shape, leading to incorrect radius estimates if not properly accounted for in the analysis.

7. **Small Sample Size Effects**: The initial sample of TESS discoveries might include a higher proportion of planets where measurement uncertainties are larger due to fewer data points or less optimal observation conditions compared to later samples with better data coverage.

Addressing these issues often requires additional observations and more detailed analyses, such as:
- Using ground-based telescopes to follow up on TESS candidates.
- Applying advanced statistical methods to remove instrumental artifacts from the light curves.
- Modeling stellar activity using long-term monitoring of stars.
- Precise measurements of limb darkening parameters.

These approaches help refine estimates and confirm whether initially detected exoplanets are indeed larger than their original reported sizes.

**RAG-augmented** - keyword: hit, judge: hit

Hundreds of TESS-discovered exoplanets may have larger actual radii compared to their originally published radii due to blending effects caused by the low angular resolution of TESS. This means that light from nearby stars is mixed with the light from the host star of an observed planet, leading to diluted transit signals. As a result, the measured reduction in brightness during transits appears smaller than it actually is because some starlight is coming from sources other than the target star hosting the exoplanet. Consequently, this dilution leads researchers to underestimate the size (radius) of these planets when calculating their sizes based on the observed transit depth [arXiv:2506.19985]. Correcting for these blending effects can increase the reported planet radii by an average factor, as detailed studies indicate corrections ranging from 1.06 to 1.11 for a significant number of TESS-discovered planets with close stellar companions [arXiv:2506.19985].

**Retrieved from:** 1412.6097, 2008.05372, 2010.15164, 2203.15826, 2506.19985

### 8. Did a recent study using Kepler Q1-17 DR25 data find a significant trend between exoplanet occurrence rate and FGK host star age?
_expected keywords: no significant, no trend, not significant_

**Baseline (no retrieval)** - keyword: miss, judge: hit

To my knowledge, the analysis of exoplanets discovered by the Kepler mission continues to provide valuable insights into their formation and evolution. However, as of my last update in October 2023, there has not been a specific recent study highlighted that uses only Kepler Q1-17 DR25 data to find a significant trend between exoplanet occurrence rate and FGK (F-type, G-type, K-type) host star age.

That being said, there have been numerous studies on the relationship between exoplanet occurrence rates and stellar ages using various datasets and time periods. These studies often use different samples of Kepler data to investigate how planet formation and detection might vary with respect to the evolutionary stages of FGK stars.

If you are looking for a specific study that addresses this exact question, I would recommend checking the latest publications in astronomy journals or arXiv preprints, as research in this area is continually evolving. Key papers often analyze large datasets from Kepler over different quarters and data releases to establish trends more robustly.

For precise information, you might want to look into studies specifically mentioning "Kepler Q1-17 DR25" along with keywords like "exoplanet occurrence rate," "stellar age," and "FGK stars." This combination should help narrow down the search for relevant research papers.

**RAG-augmented** - keyword: hit, judge: hit

No, the recent study [arXiv:2501.13809] using Kepler Q1–17 DR25 data did not find a significant trend between exoplanet occurrence rate and FGK host star age. The authors report finding no significant trend between occurrence rate and stellar ages; they observe only a slight, decreasing trend (within 1.5–2.5 _σ_) for low-mass and metal-rich stars, which is inconclusive due to weak trends and small sample sizes.

**Retrieved from:** 1809.08385, 1902.01417, 2002.02573, 2112.03927, 2501.13809

### 9. What level of mass-measurement precision may be necessary for the Habitable Worlds Observatory to identify the dominant gaseous species in an Earth-like planet's atmosphere?
_expected keywords: 10%, ten percent_

**Baseline (no retrieval)** - keyword: miss, judge: hit

To identify and characterize the atmospheric composition of an Earth-like exoplanet, including determining the dominant gaseous species, the Habitable Worlds Observatory (HWO) would require extremely high precision in its mass measurement capabilities. This task involves spectroscopic analysis to detect and quantify the presence of gases like nitrogen, oxygen, carbon dioxide, water vapor, and others that are indicative of a potentially habitable environment.

The necessary level of precision for such measurements can be understood through several key requirements:

1. **Spectral Resolution**: The HWO would need high spectral resolution (e.g., R > 50,000 to R > 100,000) to resolve the fine structure in absorption lines from various atmospheric species.

2. **Signal-to-Noise Ratio (SNR)**: To detect subtle features of specific gases, a very high signal-to-noise ratio is required. This often translates to observing times that are significantly long and multiple observations over different seasons or years to confirm signals.

3. **Atmospheric Signal Strength**: Detecting the atmospheric signature on an Earth-like planet requires measuring reflected starlight (transit method) or thermal emission (direct imaging). For a transiting Earth-sized planet orbiting a Sun-like star at 10 parsecs, achieving SNR > 10 for key gases like oxygen and methane may require observing times of hundreds to thousands of hours.

4. **Mass Measurement Precision**: To distinguish between different atmospheric compositions with high confidence, the mass measurement precision must be very fine. Typically, this means being able to measure planetary masses with a precision of better than a few Earth masses (i.e., ±2-3 M⊕), because slight variations in mass can indicate significant changes in bulk composition and thus atmospheric chemistry.

5. **Atmospheric Mass Determination**: The ability to accurately determine the atmospheric mass or scale height is crucial. This often involves measuring the transit depth with high precision, which also relates to the planet's radius measurement accuracy (±0.1-0.2 R⊕).

Given these factors, achieving a precision in planetary mass measurements of about ±0.5 to ±1 Earth masses would be necessary for confidently identifying the dominant gaseous species and their abundances in an exoplanet’s atmosphere. This level of precision can provide critical information on atmospheric density profiles and bulk composition that can then be correlated with spectroscopic observations.

In summary, while mass measurement is just one part of a multi-faceted approach to characterizing exoplanetary atmospheres, achieving high precision (±0.5-1 M⊕) in planetary masses would support the detailed atmospheric characterization required by the HWO for identifying dominant gaseous species on Earth-like planets.

**RAG-augmented** - keyword: hit, judge: hit

A prior on the planetary mass with a 10% precision is needed to correctly identify the dominant background atmospheric gas and thus properly characterize the habitability of modern-day and Archean Earth-like planets [arXiv:2603.11146].

**Retrieved from:** 1304.3714, 1309.6014, 2006.07403, 2603.11146, 2607.14329

### 10. According to recent circumplanetary disk models, where do water-rich moons like Ganymede, Callisto, and Titan form relative to the disk's ice line?
_expected keywords: ice line, ice-line_

**Baseline (no retrieval)** - keyword: hit, judge: hit

Recent circumplanetary disk models suggest that water-rich moons such as Ganymede, Callisto, and Titan form beyond a critical boundary in their respective planet’s circumplanetary disks known as the "ice line" or "snow line." The ice line is the distance from a central body (in this case, Jupiter for its moons and Saturn for Titan) at which temperatures are low enough for volatile compounds like water to condense into solid ice.

For these moons:

- **Ganymede** and **Callisto**: These moons of Jupiter form beyond the ice line in Jupiter's circumplanetary disk. This region is rich in ices, allowing for the accretion of significant amounts of water and other volatiles that are essential for their growth into large bodies.
  
- **Titan**: Titan, a moon of Saturn, also formed outside its planet’s ice line, where temperatures were low enough to allow the condensation of water and other volatile materials. This location is crucial because it allows for the accretion of substantial amounts of icy material, contributing significantly to the bulk composition and structure of Titan.

The formation beyond the ice line ensures that these moons have a high content of water ice mixed with rock, which explains their large size and the presence of subsurface oceans in some cases. This positioning within the circumplanetary disk is critical for understanding not only their composition but also their geological and atmospheric evolution over time.

**RAG-augmented** - keyword: hit, judge: hit

According to recent circumplanetary disk models, water-rich moons like Ganymede, Callisto, and Titan form just beyond the disk's ice line. This is due to an accumulation of water-ice at this boundary, facilitated by a "cold finger" mechanism where water vapor sublimates from inward-drifting pebbles, diffuses across the ice-line, and recondenses into solid pebbles on the outward side [arXiv:2602.21400].

**Retrieved from:** 1505.03516, 2602.21400

### 11. What makes the WASP-47 planetary system notable among hot Jupiter systems?
_expected keywords: inner and outer, ultra-short-period, ultra short period_

**Baseline (no retrieval)** - keyword: miss, judge: hit

The WASP-47 planetary system is notable for several reasons, especially in the context of hot Jupiters:

1. **Diverse Planet Types**: Unlike most other hot Jupiter systems which typically host only one giant planet, WASP-47 has a diverse collection of planets, including both gas giants and terrestrial-like exoplanets. This makes it unique because many hot Jupiter systems are found to be isolated without additional planetary companions.

2. **Compact Multi-planetary System**: WASP-47 is the first known system that hosts multiple small planets along with a hot Jupiter (WASP-47b) in a compact configuration, resembling systems with super-Earths and mini-Neptunes but also containing a massive gas giant very close to its host star.

3. **Orbital Configuration**: The orbits of the planets around WASP-47 are relatively coplanar, meaning they lie nearly in the same plane, which suggests that these planets likely formed through processes similar to our Solar System's planet formation mechanisms despite their compact and diverse nature.

4. **Host Star Characteristics**: The host star, WASP-47, is a G-type main sequence star (similar to our Sun), but it hosts both gas giants and smaller rocky worlds, which was not expected in such systems due to the high energy environment near the star where these planets orbit very closely.

5. **Discovery of Additional Planets**: The system's discovery expanded beyond just identifying WASP-47b as a hot Jupiter; additional small planets were found during follow-up studies, adding to its significance. For instance, subsequent observations have revealed WASP-47c and d (sub-Neptune-sized exoplanets) along with a terrestrial candidate.

These factors collectively make the WASP-47 system a fascinating case study in planetary science, offering insights into the diversity of planetary architectures that can exist even around stars hosting close-in giant planets.

**RAG-augmented** - keyword: hit, judge: hit

The WASP-47 planetary system is notable among hot Jupiter systems for several reasons:

1. **Unusual Companion Configuration**: Unlike typical hot Jupiter systems, which tend to lack nearby planets (c.f., [arXiv:1801.06117]), WASP-47 hosts both inner and outer low-mass planetary companions alongside its hot Jupiter ([arXiv:2503.00872]; [arXiv:1511.09157]). This makes it unique because the presence of these companions is not common around lonely hot Jupiters.

2. **Ultra-short Period Planet**: The system includes an ultra-short period (USP) planet, WASP-47 e, which orbits extremely close to its star ([arXiv:2503.00872]; [arXiv:1511.09157]). This USP planet is notable for possibly having a rocky composition or a core surrounded by dense volatile materials due to its strong irradiation from the central star.

3. **Planetary Companions in Resonance**: The inner planets of WASP-47 are likely in a coplanar configuration and near mean motion resonances, indicating a relatively quiet dynamical evolution possibly through in-situ formation or smooth orbital migration ([arXiv:2503.00872]; [arXiv:1511.09157]). This contrasts with the typical high-eccentricity migration scenario for hot Jupiters.

4. **Formation Paradigm Insight**: The system's configuration supports a combination of in-situ formation and orbital migration scenarios, challenging the usual lonely hot Jupiter paradigm ([arXiv:2503.00872]; [arXiv:1511.09157]). This insight bridges our understanding between hot Jupiters and warm Jupiters, providing evidence for diverse formation mechanisms.

Overall, WASP-47 stands out due to its distinctive companion architecture, including the USP planet, and implications on the broader understanding of planetary system dynamics and formation processes.

**Retrieved from:** 1108.2308, 1511.09157, 1603.02587, 1801.06117, 2503.00872

### 12. Between what years did NCCR PlanetS make the major contributions to exoplanet climate and biosignature research described in its review?
_expected keywords: 2018, 2025_

**Baseline (no retrieval)** - keyword: miss, judge: miss

The National Centre of Competence in Research (NCCR) PlanetS, which is a Swiss research network dedicated to planet formation and habitability, made significant contributions to exoplanet climate and biosignature research during the period from 2010 to 2019. This was the active phase of NCCR PlanetS, during which it brought together researchers from various institutions in Switzerland to advance our understanding of planets both within and beyond our solar system.

For more detailed information on specific contributions made by NCCR PlanetS during this period, you may want to refer to their publications and review articles that summarize their research outcomes.

**RAG-augmented** - keyword: hit, judge: hit

NCCR PlanetS made major contributions to exoplanet climate and biosignature research between 2018 and 2025 [arXiv:2601.20620].

**Retrieved from:** 1705.05791, 1807.09504, 2601.20620, 2604.09385, 2607.21683, 2608.03857, 2608.06937

### 13. Why might arid terrestrial exoplanets, such as those in the TRAPPIST-1 system, fail to maintain a balanced geologic carbon cycle?
_expected keywords: silicate weathering, surface water_

**Baseline (no retrieval)** - keyword: miss, judge: hit

Arid terrestrial exoplanets, like some of those found in the TRAPPIST-1 system, may face challenges in maintaining a balanced geologic carbon cycle due to several key factors:

### 1. Limited Water Availability:
The geologic carbon cycle on Earth involves the dissolution and precipitation of silicate minerals through weathering processes, which are highly dependent on liquid water. Arid conditions would significantly reduce the efficiency of chemical weathering and thus slow down the rate at which CO2 is removed from the atmosphere.

### 2. Reduced Atmospheric Moisture:
The presence of moisture in the atmosphere helps transport heat and nutrients across planetary surfaces, contributing to a dynamic carbon cycle. Without adequate atmospheric moisture, there could be less efficient distribution of these vital elements necessary for sustaining life and geologic activity.

### 3. Lack of Volcanic Emissions:
Volcanoes play a crucial role in recycling carbon through the mantle and crust by emitting CO2 into the atmosphere from magma. However, volcanic activity requires significant water to form magmas that are sufficiently fluid to erupt at surface level. Without sufficient water, such eruptions may be less frequent or intense.

### 4. Reduced Tectonic Activity:
Tectonics, including subduction and mountain-building processes, are also crucial for the carbon cycle because they facilitate the long-term storage of carbon in deep Earth reservoirs (e.g., sedimentary basins). Water plays a critical role in lubricating plate boundaries and facilitating these tectonic movements. An arid environment might lead to less active or less effective tectonics, thereby reducing the efficiency with which CO2 is cycled through geological processes.

### 5. Altered Chemical Weathering Rates:
Even if there is some water available on an arid planet, its distribution would likely be sparse and limited to specific regions rather than being uniformly spread across the surface. This patchy availability could result in localized high-efficiency weathering zones but a general reduction overall, leading to imbalanced carbon fluxes.

### 6. Biological Constraints:
The presence of life on an arid planet could also influence the carbon cycle significantly. On Earth, biological processes such as photosynthesis and respiration are integral components of the carbon cycle. However, extreme water scarcity would limit the proliferation of most forms of terrestrial life that require liquid water to survive.

### Summary:
An arid environment would likely result in a sluggish geologic carbon cycle because critical water-dependent processes necessary for maintaining balance (such as chemical weathering and volcanic activity) are significantly reduced or absent. This could lead to an imbalance where CO2 accumulates more rapidly than it can be sequestered, potentially leading to runaway greenhouse effects or other extreme climate conditions unfavorable for sustaining a stable atmosphere conducive to life.

Understanding these constraints is crucial for assessing the habitability of exoplanets and predicting their potential evolutionary paths under various environmental conditions.

**RAG-augmented** - keyword: hit, judge: hit

Arid terrestrial exoplanets may fail to maintain a balanced geologic carbon cycle because they lack sufficient surface water, which is necessary for effective silicate weathering. Silicate weathering acts as a thermostat by drawing down atmospheric CO2 and regulating the planet's temperature over geological timescales. However, in arid conditions, the precipitation required to drive this process is limited, leading to an imbalance where volcanic outgassing of CO2 cannot be adequately countered through weathering reactions. This results in a buildup of atmospheric CO2, potentially triggering runaway greenhouse warming and loss of habitability [arXiv:2604.16846].

**Retrieved from:** 2604.16846

### 14. What observational technique do researchers propose for detecting hypothetical exomoons around short-period exoplanets?
_expected keywords: thermal phase curve, phase curve, spectroastrometry_

**Baseline (no retrieval)** - keyword: miss, judge: miss

Detecting exomoons around short-period exoplanets is a challenging task due to their proximity to their host stars and the small size of moons compared to planets. However, there are several proposed observational techniques that astronomers might use:

1. **Transit Timing Variations (TTV) and Transit Duration Variations (TDV)**: This method relies on observing how the presence of an exomoon can cause slight variations in the timing and duration of transits as seen from Earth. For short-period planets, these effects could be more subtle due to the small distances involved, but they are still a promising avenue for detection.

2. **Doppler Tomography**: This technique involves analyzing high-precision radial velocity data over time to detect the gravitational influence of an exomoon on its planet and its star. The moon's gravity would cause periodic changes in the star's motion that could be detected with sensitive spectrometers. For short-period planets, this method might require long-term observations to accumulate enough data.

3. **Microlensing**: This technique involves observing gravitational lensing events caused by a massive object passing between Earth and another star. While primarily used for detecting exoplanets around distant stars, microlensing can also provide indirect evidence of moons if the system's configuration is just right and allows for high-resolution observations.

4. **Astrometric Observations**: Precise astrometry involves measuring tiny changes in a star’s position over time to detect the gravitational pull of orbiting planets and potential exomoons. The Gaia spacecraft, among others, provides extremely precise positional data that can be used to search for small perturbations caused by moons.

5. **Pulsar Timing**: For systems involving pulsars (rapidly rotating neutron stars), timing analysis of their highly regular pulse patterns can reveal the gravitational effects of orbiting bodies. This method is more specialized and typically applies to extreme environments not common in short-period exoplanet systems, but it demonstrates a high level of precision that could theoretically be applied under certain conditions.

6. **Simultaneous Multi-wavelength Observations**: Combining data from multiple wavelengths (e.g., optical, infrared, and radio) can provide complementary information that enhances the detection capabilities for small bodies like exomoons around short-period planets.

Each technique has its own strengths and challenges, particularly when applied to short-period systems. The choice of method often depends on the specific characteristics of the system being studied, including the distance from Earth, the mass and size of both the planet and potential moon, and available observational capabilities.

**RAG-augmented** - keyword: miss, judge: miss

Researchers propose using transit timing variations (TTV) and transit duration variations (TDV) to detect hypothetical exomoons around short-period exoplanets [arXiv:0910.0484]. This method involves observing deviations in the transiting planet's timing and transit durations, which can be caused by the gravitational influence of a moon orbiting the planet [arXiv:2504.10126].

**Retrieved from:** 0907.3909, 0910.0484, 2105.00034, 2405.01970, 2504.10126, 2509.15304, 2510.24575

### 15. How does a planet's orbital eccentricity affect the dust at the edges of the gap it opens in a protoplanetary disk?
_expected keywords: puff, meridional_

**Baseline (no retrieval)** - keyword: miss, judge: hit

A planet's orbital eccentricity can significantly influence the structure and dynamics of the dust and gas within its vicinity, particularly at the edges of the gap it carves out in a protoplanetary disk. Here are several ways this occurs:

1. **Gap Structure**: A highly eccentric orbit means that the distance between the planet and the central star varies considerably over time. This variation affects how efficiently the planet clears material from the region around its orbit, leading to a more uneven or asymmetric gap structure compared to a circular orbit.

2. **Dust Dynamics**: Eccentricity can cause periodic changes in the gravitational influence of the planet on nearby dust particles. When the planet is closer to the star (pericenter passage), it has a stronger gravitational pull and can effectively clear material from its vicinity more efficiently than when it is farther away (apocenter). This results in enhanced density waves at pericenter, which can lead to clumping or pile-up of dust particles.

3. **Stability Zones**: The horseshoe orbits and tadpole resonances that form around the planet's orbit are affected by eccentricity. These regions provide temporary stable zones for dust particles where they can accumulate. As a result, eccentric orbits may create more complex patterns in the distribution of dust within these resonant regions.

4. **Scattering Patterns**: Dust particles that interact with an eccentrically orbiting planet will experience varying gravitational forces depending on their position relative to the pericenter and apocenter. This can lead to scattering patterns where dust is pushed into specific areas at different phases of the planet's orbit, leading to non-uniform distributions of dust around the gap edges.

5. **Pressure Effects**: The eccentricity also influences the pressure gradients within the disk. These variations can enhance or diminish drag forces on dust particles depending on their position relative to the planet’s orbit, further complicating the dynamics and distribution of dust at the edges of the gap.

6. **Gap Edges Evolution**: Over time, as a planet orbits with significant eccentricity, it may periodically push material towards the inner and outer edges of its gap, creating wave patterns that can be observable in dust emission or absorption signatures.

7. **Tidal Forces**: The varying distance between the planet and star due to eccentricity causes tidal forces to change, affecting how the disk's material is stretched and compressed at different points along the orbit. This deformation can lead to enhanced trapping of small particles near the gap edges, contributing to the observed structure in protoplanetary disks.

Understanding these effects helps astronomers interpret observations of protoplanetary disks more accurately, particularly when observing dust emission patterns that trace the complex dynamics influenced by eccentric planetary orbits.

**RAG-augmented** - keyword: hit, judge: hit

A planet's orbital eccentricity significantly affects the dust at the edges of the gap it opens in a protoplanetary disk. Specifically, an increase in the planet’s eccentricity amplifies the puff-up effect observed at the gap edges [arXiv:2607.05497]. This enhancement is driven by stronger meridional gas circulation stimulated by eccentric planets, which lifts dust grains to higher elevations within the disk.

Moreover, as the planet's orbital eccentricity grows, it also makes gaps in the dust-to-gas ratio less pronounced and can even cause dust rings at gap edges to become less well-defined or disappear. This occurs because the horseshoe region of an eccentrically orbiting planet broadens radially, promoting active radial transport between the disk and the gap. As a result, the dust distribution around the gap becomes more uniform, diminishing contrasts in surface density [arXiv:2607.05497].

**Retrieved from:** 1005.4557, 1908.11065, 2009.04345, 2607.05497

### 16. According to statistical analyses of the Kepler planet population, planets around what multiple of Earth's radius show an unusually low occurrence rate?
_expected keywords: twice, two earth radii, 2 earth radii, 2r, 4 r, radius cliff, four times_

**Baseline (no retrieval)** - keyword: miss, judge: hit

Based on the statistical analyses of the Kepler planet population, there is a notable dip in the occurrence rate of planets at approximately 2 to 3 times the radius of Earth. This region is often referred to as the "radius valley" or "dip," where fewer planets are detected compared to smaller and larger planets.

This phenomenon has been interpreted by some researchers as potentially being due to different formation pathways for terrestrial (Earth-sized) planets versus mini-Neptunes (planets with hydrogen-helium envelopes). Planets in this size range may have lost their thick gaseous atmospheres early in their history, leading them to be less detectable or they might not form at all in significant numbers.

The exact causes and mechanisms behind the radius valley are still subjects of ongoing research and debate within the astronomical community.

**RAG-augmented** - keyword: hit, judge: miss

The provided excerpts do not specify a particular multiple of Earth's radius that shows an unusually low occurrence rate. However, there is discussion about potential gaps in planetary size distributions referred to as "radius valley" and "radius cliff," but these are not quantified for specific radii multiples of Earth's radius within the given text. Therefore, based on the provided excerpts alone, I cannot specify a particular multiple of Earth's radius with an unusually low occurrence rate beyond noting that such features exist in the analysis of planetary size distributions.

**Retrieved from:** 1301.0842, 1409.1904, 2006.15719, 2101.06621, 2511.02643, 2604.08406

### 17. What unique short-wavelength observing capability does Hubble retain for exoplanet atmosphere characterization in the JWST era?
_expected keywords: uvis, g280, ultraviolet, short-wavelength, short wavelength_

**Baseline (no retrieval)** - keyword: hit, judge: hit

The James Webb Space Telescope (JWST) is a powerful instrument with capabilities that significantly extend our understanding of exoplanets, particularly in the infrared spectrum. However, even as we enter the JWST era, the Hubble Space Telescope (HST) still retains unique observing capabilities that are valuable for exoplanet atmosphere characterization, especially at shorter wavelengths.

One of the key strengths of Hubble is its ability to observe at ultraviolet and visible wavelengths, which complement JWST's infrared capabilities. Here are some specific areas where Hubble remains uniquely capable:

1. **UV Spectroscopy**: 
   - Hubble's Cosmic Origins Spectrograph (COS) and Space Telescope Imaging Spectrograph (STIS) provide high-resolution UV spectroscopy, which is essential for studying the composition of exoplanet atmospheres in ways that are not possible with JWST.
   - The UV spectrum can probe molecules like ozone (O₃), atomic oxygen (O I), and other important species that are key indicators of photochemical processes and atmospheric dynamics.

2. **Atmospheric Escape**:
   - Hubble's ultraviolet observations are critical for studying the upper atmospheres of exoplanets, including phenomena such as hydrogen escape, which is a signature of atmospheric erosion.
   - These measurements help constrain models of stellar irradiation effects on planetary atmospheres and can provide insights into the long-term evolution of exoplanet environments.

3. **Cloud Structure and Composition**:
   - Observations in visible wavelengths with Hubble allow for detailed studies of cloud structures and compositions, which are crucial for understanding atmospheric dynamics and climate.
   - High-resolution imaging from HST can reveal features like clouds and hazes that provide clues about the underlying chemistry and physical processes in exoplanet atmospheres.

4. **Transit Spectroscopy**:
   - While both JWST and Hubble perform transit spectroscopy, Hubble's capabilities at shorter wavelengths (UV/visible) allow for complementary studies of atmospheric composition and structure.
   - This is particularly important for studying smaller, cooler planets where the UV spectrum can provide additional constraints on atmospheric models.

5. **Temporal Variability**:
   - The ability to observe in multiple wavelength bands over time allows Hubble to study how exoplanet atmospheres change with varying stellar activity or planetary orbit phases.
   - This temporal variability is critical for understanding dynamic processes and long-term trends that can be missed by single-epoch observations.

In summary, while JWST offers groundbreaking capabilities in the infrared spectrum, Hubble's unique short-wavelength observing capacity (UV and visible) remains crucial for a comprehensive characterization of exoplanet atmospheres. The combined use of both telescopes provides a more complete picture of these distant worlds, enhancing our understanding of planetary systems beyond our Solar System.

**RAG-augmented** - keyword: hit, judge: hit

In the JWST era, the Hubble Space Telescope (HST) retains its unique capability of observing at short wavelengths that are inaccessible to JWST. Specifically, HST can observe effectively down to the UV regime, while JWST only reaches as blue as 0.5 μm via the NIRSpec/PRISM mode [arXiv:2606.04144]. This short-wavelength capability of HST is crucial for characterizing exoplanet atmospheres in several ways:

- **Aerosol and haze characterization:** Short wavelengths are most effective for detecting scattering caused by aerosols and photochemically generated hazes [arXiv:2606.04144].
  
- **Heavy metal species absorption:** HST is better suited to observe the strong spectral features of heavy metal species that absorb strongly at short wavelengths, which would otherwise be missed with JWST's shorter wavelength limit.

- **Disentangling stellar contamination signals:** Short-wavelength observations are vital for identifying and separating the effects of stellar activity (like starspots and faculae) from planetary atmospheric signatures [arXiv:2606.04144].

These capabilities underscore HST’s continued importance in conjunction with JWST, especially for resolving detailed atmospheric properties that require short-wavelength coverage.

**Retrieved from:** 1705.07098, 1810.04175, 2506.03299, 2606.04144, 2608.00520, 2608.05885

### 18. What limitation of static mass-radius structure models for sub-Neptunes and super-Earths does recent work address by integrating radiative-convective and interior structure simulations?
_expected keywords: atmospher, climate_

**Baseline (no retrieval)** - keyword: hit, judge: hit

Recent advancements in the study of exoplanets, particularly sub-Neptunes (planets with a radius between Earth's and Neptune's) and super-Earths (planets larger than Earth but smaller than Uranus or Neptune), have highlighted limitations in static mass-radius structure models. These traditional models often assume equilibrium states without considering dynamic processes such as the transport of heat through radiative-convective mechanisms, which can significantly affect a planet's internal structure over time.

The main limitation addressed by integrating radiative-convective and interior structure simulations is the oversimplification of heat distribution within these planets. Static models typically fail to account for:

1. **Heat Transport**: The dynamic process of heat transport through convection and radiation, which redistributes thermal energy from the planet's interior to its surface over geological timescales.

2. **Atmospheric Effects on Interior Structure**: The influence of an atmosphere on the internal structure and composition of a planet, including how atmospheric pressure affects the depth at which various materials transition state (e.g., water, ice).

3. **Thermal History**: The evolution of planetary interiors through their thermal history, which can affect their current observable properties like radius and mass.

By integrating radiative-convective simulations with interior structure models, researchers can:

- Better predict how heat is transported within the planet's interior and atmosphere.
- Account for changes in density profiles due to different atmospheric pressures at various depths.
- Model the thermal evolution of planets over time, allowing for a more accurate understanding of their current state.

This approach provides a more comprehensive framework that considers dynamic processes, leading to improved predictions about planetary composition, structure, and habitability. It also enhances our ability to interpret observations from exoplanet surveys like those conducted by missions such as TESS (Transiting Exoplanet Survey Satellite) and Kepler, which provide mass and radius measurements for many sub-Neptunes and super-Earths.

Overall, these integrated models offer a more nuanced understanding of how various physical processes interplay to shape the observable properties of exoplanets.

**RAG-augmented** - keyword: hit, judge: hit

Recent work addresses the limitations of static mass-radius structure models for sub-Neptunes and super-Earths by integrating radiative-convective processes along with detailed interior structure simulations. Specifically, it highlights that existing planetary static-structure models either neglect atmospheric contributions or oversimplify atmospheric temperature structures [arXiv:2604.15891]. The new approach incorporates the influence of local irradiation environments on atmospheric temperature and convective regimes, demonstrating significant impacts on photospheric radii compared to purely adiabatic or isothermal scenarios. This means that sub-Neptunes and super-Earths cannot be categorized by a single family of mass-radius isolines based solely on specific atmosphere compositions or structures; instead, each planet's radius is a function of its unique stellar context and composition [arXiv:2604.15891].

**Retrieved from:** 1710.05605, 2306.09002, 2507.18665, 2604.15891, 2607.16713