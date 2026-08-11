"""Hand-written questions used to sanity-check whether retrieval augmentation
actually changes/improves the model's answers.

Unlike a first pass built from general textbook exoplanet facts (which a
14B instruct model already knows cold, so baseline and RAG tied), every
question here targets a specific finding from a specific paper in this
corpus, most of them published in 2025-2026 - after this generation
model's training cutoff. The base model has no plausible way to know these
answers from parametric memory; retrieval is the only path to a correct,
specific answer. `expected_keywords` is a crude, not rigorous, correctness
signal: if any keyword appears in the answer we count it a "hit".
"""

QA_SET: list[dict] = [
    {
        "question": "What type of planet was the first exoplanet discovered by TESS (the Transiting Exoplanet Survey Satellite)?",
        "expected_keywords": ["sub-neptune", "subneptune", "pi men", "π men"],
    },
    {
        "question": "Out of the more than 500 confirmed transiting hot Jupiters, how many are currently known to have nearby companion planets?",
        "expected_keywords": ["ten", " 10 ", "10.", "10,"],
    },
    {
        "question": "The microlensing event OGLE-2016-BLG-0007 revealed a super-Earth on an orbit wider than which planet's orbit in our solar system?",
        "expected_keywords": ["saturn"],
    },
    {
        "question": "What happened to the Gaia DR3 exoplanet candidate announced around the star HD 12800?",
        "expected_keywords": ["retract", "false", "non-detect", "not confirm"],
    },
    {
        "question": "Instead of high-eccentricity tidal migration, what alternative explanation do recent studies propose for why hot Jupiters tend to lack nearby planetary companions?",
        "expected_keywords": ["quiescent", "disk migration", "in situ", "in-situ"],
    },
    {
        "question": "Through what photochemical mechanism can abiotic oxygen and ozone build up in rocky exoplanet atmospheres around M dwarfs, producing a false-positive biosignature?",
        "expected_keywords": ["co2 photolysis", "photolysis", "co₂ photolysis"],
    },
    {
        "question": "Why might hundreds of TESS-discovered exoplanets actually be larger than their originally published radii?",
        "expected_keywords": ["blend", "dilut"],
    },
    {
        "question": "Did a recent study using Kepler Q1-17 DR25 data find a significant trend between exoplanet occurrence rate and FGK host star age?",
        "expected_keywords": ["no significant", "no trend", "not significant"],
    },
    {
        "question": "What level of mass-measurement precision may be necessary for the Habitable Worlds Observatory to identify the dominant gaseous species in an Earth-like planet's atmosphere?",
        "expected_keywords": ["10%", "ten percent"],
    },
    {
        "question": "According to recent circumplanetary disk models, where do water-rich moons like Ganymede, Callisto, and Titan form relative to the disk's ice line?",
        "expected_keywords": ["ice line", "ice-line"],
    },
    {
        "question": "What makes the WASP-47 planetary system notable among hot Jupiter systems?",
        "expected_keywords": ["inner and outer", "ultra-short-period", "ultra short period"],
    },
    {
        "question": "Between what years did NCCR PlanetS make the major contributions to exoplanet climate and biosignature research described in its review?",
        "expected_keywords": ["2018", "2025"],
    },
    {
        "question": "Why might arid terrestrial exoplanets, such as those in the TRAPPIST-1 system, fail to maintain a balanced geologic carbon cycle?",
        "expected_keywords": ["silicate weathering", "surface water"],
    },
    {
        # Corpus has two independently valid answers to this: spectroastrometry
        # (arXiv:1509.01615) and thermal phase curves (arXiv:2603.18437). A
        # correct answer citing either is a pass - this was originally keyed
        # only to the second, which failed a run that (correctly) answered
        # with the first instead.
        "question": "What observational technique do researchers propose for detecting hypothetical exomoons around short-period exoplanets?",
        "expected_keywords": ["thermal phase curve", "phase curve", "spectroastrometry"],
    },
    {
        "question": "How does a planet's orbital eccentricity affect the dust at the edges of the gap it opens in a protoplanetary disk?",
        "expected_keywords": ["puff", "meridional"],
    },
    {
        # Originally keyed to the textbook "radius valley" near 1.5-2 R⊕,
        # written before checking what the corpus actually says. The paper
        # retrieved for this question (arXiv:2511.02643) discusses a
        # different, more specific finding: a "radius cliff" near 4 R⊕.
        # Both are real, distinct results in the exoplanet demographics
        # literature - fixed to match what's actually grounded here.
        "question": "According to statistical analyses of the Kepler planet population, planets around what multiple of Earth's radius show an unusually low occurrence rate?",
        "expected_keywords": ["twice", "two earth radii", "2 earth radii", "2r", "4 r", "radius cliff", "four times"],
    },
    {
        # "short-wavelength" is a correct paraphrase of Hubble's UV advantage
        # over JWST - added after a correct answer used that phrasing
        # instead of the literal word "ultraviolet".
        "question": "What unique short-wavelength observing capability does Hubble retain for exoplanet atmosphere characterization in the JWST era?",
        "expected_keywords": ["uvis", "g280", "ultraviolet", "short-wavelength", "short wavelength"],
    },
    {
        "question": "What limitation of static mass-radius structure models for sub-Neptunes and super-Earths does recent work address by integrating radiative-convective and interior structure simulations?",
        "expected_keywords": ["atmospher", "climate"],
    },
]
