"""Seed corpus for the AdS/CMT literature review.

Each entry is (arxiv_id, pillar, expected_title_fragment). The fragment is not
decoration: `fetch_papers.py` refuses any record whose real arXiv title does not
contain it, so a mistyped identifier fails loudly instead of quietly ingesting
the wrong paper into the vector store.

Pillars follow the structure of the two review documents:
  holography - AdS/CFT and holographic entanglement
  adscmt     - holographic applications to condensed matter
  topology   - topological insulators/superconductors and their classification
  bridge     - anomaly inflow, entanglement spectra, holographic topological matter
  experiment - tabletop analogue-gravity results cited by the experimental programme
"""

SEED_PAPERS: list[tuple[str, str, str]] = [
    # --- Pillar 1: holographic duality and entanglement -------------------
    ("hep-th/9711200", "holography", "Large N Limit of Superconformal"),
    ("hep-th/9802109", "holography", "Gauge Theory Correlators from Non-Critical String"),
    ("hep-th/9802150", "holography", "Anti De Sitter Space and Holography"),
    ("hep-th/0603001", "holography", "Holographic Derivation of Entanglement Entropy"),
    ("0705.0016", "holography", "Covariant Holographic Entanglement Entropy"),
    ("0905.1317", "holography", "Entanglement Renormalization and Holography"),
    ("1005.3035", "holography", "Building up spacetime with quantum entanglement"),
    ("1304.4926", "holography", "Generalized gravitational entropy"),
    ("1306.0533", "holography", "Cool horizons for entangled black holes"),
    ("1503.06237", "holography", "Holographic quantum error-correcting codes"),
    ("hep-th/0405231", "holography", "Viscosity in Strongly Interacting Quantum Field Theories"),

    # --- Pillar 2: AdS/CMT ------------------------------------------------
    ("0903.3246", "adscmt", "Lectures on holographic methods for condensed matter"),
    ("0909.0518", "adscmt", "Holographic duality with a view toward many-body physics"),
    ("0801.2977", "adscmt", "Breaking an Abelian gauge symmetry near a black hole horizon"),
    ("0803.3295", "adscmt", "Building an AdS/CFT superconductor"),
    ("0810.1563", "adscmt", "Holographic Superconductors"),
    ("0907.2694", "adscmt", "Emergent quantum criticality, Fermi surfaces, and AdS"),
    ("0904.1993", "adscmt", "String Theory, Quantum Phase Transitions and the Emergent Fermi"),
    ("1612.07324", "adscmt", "Holographic quantum matter"),
    ("1110.3814", "adscmt", "Lectures on holographic non-Fermi liquids and quantum phase"),
    ("cond-mat/9212030", "adscmt", "Gapless Spin-Fluid Ground State in a Random"),
    ("1604.07818", "adscmt", "Comments on the Sachdev-Ye-Kitaev model"),
    ("1506.05111", "adscmt", "Bekenstein-Hawking Entropy and Strange Metals"),
    ("1405.3651", "adscmt", "Theory of universal incoherent metallic transport"),

    # --- Pillar 3: topological insulators and superconductors -------------
    ("cond-mat/0506581", "topology", "Quantum Spin Hall Effect"),
    ("cond-mat/0607699", "topology", "Topological Insulators in Three Dimensions"),
    ("cond-mat/0611341", "topology", "Topological Insulators with Inversion Symmetry"),
    ("cond-mat/0611399", "topology", "Quantum Spin Hall Effect and Topological Phase Transition in HgTe"),
    ("cond-mat/0010440", "topology", "Unpaired Majorana fermions in quantum wires"),
    ("1002.3895", "topology", "Topological Insulators"),
    ("1008.2026", "topology", "Topological insulators and superconductors"),
    ("0802.3537", "topology", "Topological field theory of time-reversal invariant insulators"),
    ("0803.2786", "topology", "Classification of topological insulators and superconductors in three"),
    ("0912.2157", "topology", "Topological insulators and superconductors: ten-fold way"),
    ("0901.2686", "topology", "Periodic table for topological insulators and superconductors"),
    ("1505.03535", "topology", "Classification of topological quantum matter with symmetries"),

    # --- Pillar 4: the bridge --------------------------------------------
    ("1010.0936", "bridge", "Electromagnetic and gravitational responses and anomalies"),
    ("hep-th/0510092", "bridge", "Topological entanglement entropy"),
    ("cond-mat/0510613", "bridge", "Detecting Topological Order in a Ground State Wave Function"),
    ("0805.0332", "bridge", "Entanglement Spectrum as a Generalization of Entanglement Entropy"),
    ("1103.5437", "bridge", "General relationship between the entanglement spectrum and the edge"),
    ("1511.05505", "bridge", "Quantum phase transition between a topological and a trivial semimetal"),
    ("1610.04413", "bridge", "Notes on Anomaly Induced Transport"),
    # Ryu & Takayanagi realise the ten-fold way inside string theory: the same
    # two authors as the holographic entanglement entropy formula. These two
    # papers are the literal junction between the review's pillars 1 and 3.
    ("1001.0763", "bridge", "Topological Insulators and Superconductors from D-branes"),
    ("1011.0586", "bridge", "Topological field theory and thermal responses of interacting"),
    ("1510.07698", "bridge", "Three Lectures On Topological Phases Of Matter"),
    ("1911.07978", "bridge", "Holographic Topological Semimetals"),
    # Section 5.4 of the review argues that topological order and holography are
    # both quantum error-correcting codes. The toric code is one half of that
    # claim, so it belongs in the corpus rather than being cited from memory.
    ("quant-ph/9707021", "bridge", "Fault-tolerant quantum computation by anyons"),
    # Altland-Zirnbauer: the ten symmetry classes the periodic table is built on.
    ("cond-mat/9602137", "topology", "Novel Symmetry Classes in Mesoscopic"),

    # --- Pillar 5: experiment ---------------------------------------------
    # The feasibility verdicts in docs/experimental_program.md lean on these
    # tabletop results. They are in the corpus so that those verdicts rest on
    # verified sources, not on memory.
    ("1008.1911", "experiment", "Measurement of stimulated Hawking emission in an analogue system"),
    # arXiv title; the Nature Physics version is "Rotational superradiant
    # scattering in a vortex flow". The gate matches the arXiv record.
    ("1612.06180", "experiment", "Observation of superradiance in a vortex flow"),
    ("1511.08145", "experiment", "Observation of noise correlated by the Hawking effect in a water tank"),

    # --- Pillar 7: entanglement-spectrum <-> bulk-boundary PoC -----------
    # Added to check two premises before coding experiments/poc_entanglement_tda/:
    # (a) free-fermion SSH entanglement spectrum mirrors the physical edge
    #     spectrum (Fidkowski; Pollmann-Turner-Berg-Oshikawa);
    # (b) SYK-type Majorana models have a mod-8 (Fidkowski-Kitaev) symmetry
    #     classification, so SYK is NOT topology-free the way a chaotic model
    #     is assumed to be -- if true, this changes the PoC's SYK role from
    #     "negative control" to "second signal system".
    ("0909.2654", "poc", "Entanglement spectrum of topological insulators and superconductors"),
    ("0910.1811", "poc", "Entanglement spectrum of a topological phase in one dimension"),
    ("0904.2197", "poc", "Effects of interactions on the topological classification of free fermion systems"),
    ("1602.06964", "poc", "Sachdev-Ye-Kitaev Model and Thermalization on the Boundary of Many-Body Localized"),
    ("1611.04650", "poc", "Black Holes and Random Matrices"),

    # --- Pillar 6: Shinsei Ryu -------------------------------------------
    # Selected from his full arXiv record (tools/arxiv_author.py ->
    # docs/assets/ryu_arxiv.json, 202 papers). Papers of his already in the
    # other pillars (hep-th/0603001, 0803.2786, 0912.2157, 1001.0763,
    # 1010.0936, 1505.03535) are not repeated. See docs/ryu_review.md.
    ("cond-mat/0112197", "ryu", "Topological Origin of Zero-Energy Edge States in Particle-Hole Symmetric"),
    ("hep-th/0605073", "ryu", "Aspects of Holographic Entanglement Entropy"),
    ("0905.0932", "ryu", "Holographic Entanglement Entropy: An Overview"),
    ("0708.1639", "ryu", "Many-body generalization of the Z2 topological invariant"),
    ("0810.5394", "ryu", "Disordered Systems and the Replica Method in AdS/CFT"),
    ("0901.0924", "ryu", "Fractional Quantum Hall Effect via Holography"),
    ("1007.4234", "ryu", "Topological Insulators and Superconductors from String Theory"),
    ("1202.5805", "ryu", "Interaction effect on topological classification of superconductors"),
    ("1208.3469", "ryu", "Holographic Geometry of Entanglement Renormalization in Quantum Field"),
    ("1406.0307", "ryu", "CPT theorem and classification of topological insulators"),
    ("1605.00570", "ryu", "Holographic duality between"),
    ("1605.07199", "ryu", "Holographic Entanglement Renormalization of Topological Insulators"),
    ("1607.03896", "ryu", "Many-body topological invariants for fermionic symmetry-protected"),
    ("1705.03892", "ryu", "Anomaly Manifestation of Lieb-Schultz-Mattis Theorem"),
    ("2109.02649", "ryu", "Negativity Spectra in Random Tensor Networks and Holography"),
    ("2112.13489", "ryu", "Lindbladian dynamics of the Sachdev-Ye-Kitaev model"),
    ("2202.02548", "ryu", "Many-body topology of non-Hermitian systems"),
    ("2212.00605", "ryu", "Symmetry of Open Quantum Systems"),
    ("2312.17318", "ryu", "Spectral sum rules reflect topological and quantum-geometric invariants"),
    ("2405.05327", "ryu", "Higher Berry Connection for Matrix Product States"),
    ("2601.00761", "ryu", "Exponentially Accelerated Sampling of Pauli Strings"),
]
