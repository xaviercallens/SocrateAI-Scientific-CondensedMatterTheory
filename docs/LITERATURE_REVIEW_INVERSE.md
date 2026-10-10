# Literature review: inverse conductance, conditioning of node-set matrices, hyperbolic circuits

Date: 2026-10-08. Method: the project vector store (3420 chunks before, 17 papers added now in the pillars `inverse`,
`conditioning`, `hyperbolic`), reached through the repository's own MCP server, plus three survey passes through alphaXiv
and web search. Tags: **[V]** = the paper's text or abstract was read in this session; **[S]** = existence confirmed only
through a citing paper or a record; **[U]** = not confirmed, do not cite before checking.
Nothing below is a claim about Track H results. It is the prior-art map that the cylinder note must respect.

## 1. What is already known (and must be cited as such)

**Exponential ill-posedness of the inverse conductivity problem.**
- Mandache, Inverse Problems 17 (2001), exponential instability [S].
- Di Cristo, Rondi, *Examples of exponential instability for elliptic inverse problems*, arXiv:math/0303126 [V].
- Alessandrini 1988 (logarithmic stability) and Alessandrini-Vessella 2005 (Lipschitz stability for piecewise constant conductivity) [S].
- Rondi 2006: the Lipschitz constant grows exponentially with the number of regions [S].

**Discrete networks.**
- Curtis-Ingerman-Morrow 1998 and Colin de Verdiere-Gitler-Vertigan 1996: recovery on circular planar networks [S].
- Borcea-Druskin-Guevara Vasquez-Mamonov, arXiv:1107.0343 [V]: in the layered case the Fourier blocks reduce to a Vandermonde-type
  inversion that is exponentially ill-conditioned; cites Gautschi-Inglese. Column sums of the response matrix vanish.
- Borcea-Guevara Vasquez-Mamonov, arXiv:1105.1183 [V]: Fig. 6 shows the condition number growing exponentially with the number of boundary nodes.
- Deng-Jin, arXiv:2509.18203 [V, abstract]: numerical exponential growth of the condition number with slice index on lattices; rigorous analysis stated open.
- Also: arXiv:2312.11721, 1104.4858, 1104.4998, 2501.00345, 1609.03041 [V as records].

**Vandermonde, Hankel and potential-theoretic conditioning.**
- Gautschi 1962 and Gautschi-Inglese 1988: exponential lower bounds for real nodes [S].
- Beckermann, Numer. Math. 85 (2000) 553: sharp-up-to-polynomial exponential rates for real nodes. For a real interval the base equals the exponential of the
  maximum over the unit circle of the Green function (survey's own arithmetic; the paper does not state it in that form) [V, abstract].
- Pan, arXiv:1504.02118 [V]: lower bound through the nodal polynomial on the unit circle, square case.
- Berg-Szwarc, arXiv:0906.4506 [V]: exponential rate for the smallest Hankel eigenvalue with compact support. Widom-Wilf 1966 and Szego 1936 give sharp Hankel rates [S, content unread].
- Beckermann-Townsend arXiv:1609.09494, Aubel-Boelcskei arXiv:1701.02538, Batenkov-Goldman arXiv:2107.09326, Trefethen arXiv:1908.11097,
  Demanet-Townsend arXiv:1605.09601 [V]: neighbouring results (singular-value decay, unit-disk nodes, the analytic-continuation duality with the same Bernstein-Walsh exponent).

**Hyperbolic lattices and circuits.**
- Kollar-Fitzpatrick-Houck (Nature 2019, arXiv:1802.09549), Lenggenhager et al. (Nat. Commun. 2022, arXiv:2109.01148), Chen et al. (arXiv:2205.05106),
  Boettcher et al. (PRA 2020, arXiv:1910.12318) [V]: hyperbolic lattices realised in circuits; only connectivity matters.
- Basteiro et al. arXiv:2205.05081, Dey et al. arXiv:2404.03062, Chen et al. arXiv:2305.04862 [V]: Dirichlet-truncated tilings, resistor networks with boundary sources,
  claims of holographic tests. Context only. These are holography papers; Track H makes no holographic claim.
- Chen et al. 2205.05106: on a finite hyperbolic flake the boundary is an O(1) fraction of the nodes.
- Spectral gap side: Kesten 1959 (non-amenable iff spectral radius below one), Dodziuk 1984, Higuchi-Shirai (Cheeger constant of {p,q}), Woess 2000,
  Lyons-Peres 2016, Benjamini-Schramm 1996 [S].

## 2. Consequences for the Track H claims

| Finding | Prior-art status | Consequence |
|---|---|---|
| Exponential conditioning of the DtN Jacobian on flat lattices | Qualitatively known (above). | Say so. Do not present as new. |
| Hyperbolic versus flat comparison of that conditioning | Not found in the searches done. Absence is not proof. | Keep as the contribution, worded as "not found". |
| Exact rate on solvable strips from the Green function of the node complement | No source states it. Closest: Beckermann 2000 (real nodes), Szego 1936 and Widom-Wilf 1966 (Hankel), Pan Cor. 4.1. | Medium risk. Read Szego 1936 and Widom-Wilf before any novelty claim. |
| Offset invisibility | Elementary consequence of zero row sums of the response matrix. | Not a result. Machine-checked in section 5. |
| Hardware design | Component and measurement practice from the circuit papers. | Used in section 3. |

Caveat from the survey: the Green-function rate needs the number of nodes to grow faster than the degree. For a square system with about d+1 nodes
the exponent is a discrete nodal (Fekete-type) quantity. Our strips have 25 to 193 distinct nodes against depths up to 25 rows, so the continuous
exponent is an asymptotic statement and the note must state this hypothesis.

## 3. Practical guidance for the RC board (from the circuit papers)

- Only connectivity matters: a flat board with long jumpers is a faithful {7,3} network (Kollar; Lenggenhager).
- Component spread dominates: measure every capacitor with an LCR meter, bin or pair them, and simulate with measured values. Parallel parts average spread by about 1/sqrt(n).
- Probe loading: a 1 Mohm scope input against 100 kohm nodes is a 10 % load. Use a 10 Mohm probe or a buffer, the same on both boards.
- Equalise the boundary treatment between the {7,3} and square boards, since the boundary is an O(1) fraction of the nodes.
- Film or C0G capacitors: leakage must be far above 100 kohm at a 0.1 s time constant. Shield against mains pickup. Single-point ground.

## 4. Items to check before citing (open)

Szego 1936 content; Widom-Wilf 1966 content; Beckermann Habilitation 1996; Tyrtyshnikov 1994; Kesten 1959 venue; Higuchi-Shirai venue and formula;
journal references of 2404.03062 and 2305.04862; Ingerman 2000 and Biesel-Ingerman-Morrow-Shore (not read); arXiv:2601.13915 (unread).

## 5. Formal statement (Lean 4, LeanMaster toolchain)

Four lemmas in `lean/dtn_offsets/DtNOffsets.lean`: zero row sums of the Schur-complement DtN matrix, orthogonality of row and column offsets to a zero-sum matrix, and invariance of a two-candidate matched-filter decision under an orthogonal disturbance. Gates G1 to G4 pass, G5 (independent verifier) not run. Details and limits: `lean/dtn_offsets/STATUS.md`.

## 6. Vector store

17 papers added through `corpus/seed_papers.py`, identity-checked by title fragment (`corpus/fetch_papers.py --ids`, `corpus/ingest_chroma.py --ids`).
Retrieval: `mcp_adscmt_rag.py`, tool `adscmt_search`, pillar filter `inverse`, `conditioning` or `hyperbolic`.
