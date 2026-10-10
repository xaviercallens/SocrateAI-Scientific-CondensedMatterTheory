# Literature review: topological data analysis for the conditioning thread (GUDHI, vectorisation, learning, persistent Laplacians)

Date: 2026-10-10. Method: two survey passes through alphaXiv and web search with identifier verification, then 24 papers added to the vector store under the pillar `tda`
(one under `inverse`), fetched and identity-checked by title fragment. Tags: **[V]** record or text fetched this session; **[S]** seen in a citing paper or a listing only.
Before this review the vector store returned nothing closer than cosine distance 0.5 for "persistence diagram", "persistence image" or "effective-resistance TDA"; the gap is now filled.

## 1. Tooling (GUDHI, Inria)
- Maria, Boissonnat, Glisse, Yvinec, *The Gudhi Library*, ICMS 2014 (HAL hal-01108461; no arXiv) [V]. The `representations` module (verified against the online manual) has vectorisations (persistence image, landscape, silhouette, Betti curve, entropy, Atol, topological vector), kernels (sliced Wasserstein, persistence Fisher, scale-space, weighted Gaussian) and metrics; TensorFlow layers for Rips, cubical and lower-star persistence and PersLay. No PyTorch layer in GUDHI itself. On this host: GUDHI 3.13, scikit-learn 1.7, PyTorch 2.7, POT 0.9 (no TensorFlow).

## 2. Vectorisations and their stability (what licenses using diagrams as features)
- Adams et al., persistence images, JMLR 2017, arXiv:1507.06217 [V]: 1-Wasserstein stable with constants independent of diagram size; no additive kernel is W_p-stable for p > 1.
- Bubenik, persistence landscapes, JMLR 2015, arXiv:1207.6437 [V]: sup-landscape distance bounded by bottleneck; p-landscape stability only under bounded total persistence.
- Carrière, Cuturi, Oudot, sliced Wasserstein kernel, ICML 2017, arXiv:1706.03358 [V]: stable and discriminative (two-sided bounds against W_1).
- Royer et al., Atol, AISTATS 2021, arXiv:1909.13472 [V]: k-means quantisation of the mean measure, one parameter. Carrière et al., PersLay, AISTATS 2020, arXiv:1904.09378 [V]. Hofer et al. 2017, Kusano et al. 2016, Reininghaus et al. 2015, Le and Yamada 2018, RipsNet 2022 [V].
- Stability of the diagrams themselves: Cohen-Steiner, Edelsbrunner, Harer 2007 (DCG, no arXiv) [V]; Chazal, de Silva, Glisse, Oudot, arXiv:1207.3674 [V]; Chazal, de Silva, Oudot, arXiv:1207.3885 [V], which covers Rips on **dissimilarity spaces**, so it applies to the sine distance between column lines; Skraba and Turner, Wasserstein stability, arXiv:2006.16824 [V], which also warns that the Lipschitz W_p theorem is widely miscited.

## 3. Differentiable persistence
- Carrière et al., *Optimizing persistent homology based functions*, ICML 2021, arXiv:2010.08356 [V]; Leygonie, Oudot, Tillmann, arXiv:1910.00960 [V]; Brüel-Gabrielsson et al., topology layer, AISTATS 2020, arXiv:1905.12200 [V]; Gameiro, Hiraoka, Obayashi, arXiv:1506.03147 [V]. Relevant if a topological loss were ever used to design a network; not used here.

## 4. Persistent Laplacians and spectral TDA (the objection to paper 2, and the answer)
- Mémoli, Wan, Wang, *Persistent Laplacians*, arXiv:2012.02808 [V]: the up-persistent Laplacian is a Schur complement; for graph pairs it is the Kron reduction, which preserves effective resistance; persistent Cheeger inequality; the nullity gives the persistent Betti number and the **non-zero spectrum carries what persistent homology does not**.
- Wang, Nguyen, Wei, *Persistent spectral graph*, arXiv:1912.04135 [V]: same message, motivated by persistent homology being "constrained to purely topological persistence". Wei and Wei, survey, arXiv:2312.07563 [V]. Lim, Hodge Laplacians on graphs, SIAM Review 2020, arXiv:1507.05379 [V].
- Damrich, Berens, Kobak, NeurIPS 2024, arXiv:2311.03087 [V]: replacing Euclidean distance by effective-resistance or diffusion distance before Rips changes what persistence sees.
- **Consequence for this programme.** Papers 2 and 3 found that nearest-neighbour H₀ of the Jacobian column cloud sees depth only as a power law while σ_min falls exponentially, and that the depth-ordered residual carries the rate. A referee will say: persistent homology is the wrong tool for spectral information, by design; the persistent Laplacian of the same filtration would see it. That objection is correct in kind and must be pre-empted by computing the persistent Laplacian's smallest non-zero eigenvalue on the same clouds (added to preregistration 33 as a measured quantity, see below) and by framing the paper-2 result as a negative control, which is how its reading already puts it.

## 5. Persistent homology of matrices, correlations and conditioning (the closest prior art)
- Ghafuri and Jassim, *SVD based matrix surgery*, arXiv:2302.11446 [V], unrefereed: Rips persistence of point clouds of whole small matrices, well- versus ill-conditioned, qualitative only. Must be cited; it is the only link between persistence and condition numbers found.
- Giusti, Pastalkova, Curto, Itskov, *Clique topology*, PNAS 2015, arXiv:1502.06172 [V]: Betti curves of the order complex of a correlation matrix, invariant under monotone entrywise transforms, argued complementary to eigenvalue analysis. Methodologically the nearest thing to persistence of a Gram matrix.
- Rieck et al., Neural Persistence, ICLR 2019, arXiv:1812.09764 [V]: H₀ of a weight matrix as a filtered bipartite graph.
- Nothing found for persistence with Vandermonde, Krylov, Gram–Schmidt, sine distance or singular values beyond these.

## 6. TDA in physics, inverse problems and learned conditioning
- Phase transitions: Donato et al., PRE 2016, arXiv:1601.03641 [V]; Olsthoorn, Hellsvik, Balatsky, PRR 2020, arXiv:2009.05141 [V]; Cole, Loges, Shiu, PRB 2021, arXiv:2009.14231 [V] (persistence images plus logistic regression, "persistence critical exponents"); Loftus 2026, arXiv:2603.29072 [V, abstract]: H₀ signal is density-driven, H₁ carries the topology. Caputi et al., arXiv:2406.15505 [V, abstract]: Betti signatures distinguish hyperbolic from flat distance matrices (the only persistence-meets-hyperbolic-geometry item found). No persistent homology of {p,q} tilings found.
- Inverse problems: Karvonen, Lassas, Pankka, arXiv:2606.17632 [V]: persistence diagrams stable under the quasi-isometric Calderón forward map (using Alessandrini's log-stability), so persistent features of noisy EIT data certify features of the object. Closest work to topology-aware EIT. Clough et al. 2020, Hu et al. 2019: topological losses in segmentation [V]. No persistence prior for resistor-network inversion found.
- Learned conditioning: Carson and Chen, *Estimating condition number with graph neural networks*, arXiv:2603.10277 [V] (March 2026): a graph network predicts log₁₀ κ from the matrix graph, claimed first of its kind. Häusner, Öktem, Sjölund, neural incomplete factorisation, TMLR 2024, arXiv:2305.16368 [V]; Yang et al., NeurIPS 2025, arXiv:2510.27517 [V, abstract].
- Learned EIT: Hamilton and Hauptmann, Deep D-bar, IEEE TMI 2018, arXiv:1711.03180 [V]; Cen, Jin, Shin, Zhou, Deep Calderón, JCP 2023, arXiv:2304.09074 [V]; Fan and Ying, JCP 2020, arXiv:1906.03944 [V]; de Hoop, Kovachki, Lassas, Nelsen, neural-operator approximation of the EIT inverse map, arXiv:2511.20361 [V]. Lassas, Salo, Tzou, arXiv:1307.1539 [V]: the discrete Calderón problem on resistor networks has more non-uniqueness than the PDE.

## 7. Prior-art risk, updated
| Claim | Risk | Required framing |
|---|---|---|
| Nearest-neighbour persistence of Jacobian columns sees only a power law while σ_min is exponential (paper 2) | Low risk of anticipation; moderate risk of "wrong tool by design" | Cite Mémoli–Wan–Wang and Wang–Nguyen–Wei; present as a negative control; report the persistent Laplacian on the same clouds (preregistration 33). Cite Ghafuri–Jassim and Giusti et al. |
| Gram–Schmidt residual as certified proxy (paper 3) | No TDA prior art; numerical-linear-algebra prior art (rank-revealing QR, Björck, Higham) not covered by this review | Cite the QR literature in a revision. |
| Hyperbolic versus flat conditioning of the discrete Calderón problem | No prior art found (two surveys) | Cite Borcea et al. for the flat baseline, Lassas–Salo–Tzou for discrete non-uniqueness, Caputi et al. for persistence and hyperbolic metrics. |
| Learned persistence features predicting conditioning (preregistration 33) | Carson–Chen 2026 predicts κ with a graph network from the matrix graph; Cole–Loges–Shiu use persistence images plus regression for order parameters | Position as: persistence features of the column cloud, transfer across geometries, compared with a certified proxy; cite both. |

## 8. Vector store
24 papers added (`corpus/seed_papers.py`, pillar `tda`), fetched with identity checks and ingested with `corpus/ingest_chroma.py --ids`. Retrieval: `mcp_adscmt_rag.py`, tool `adscmt_search`, pillar `tda`.
