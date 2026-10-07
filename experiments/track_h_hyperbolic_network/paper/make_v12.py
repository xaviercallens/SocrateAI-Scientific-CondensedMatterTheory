#!/usr/bin/env python3
"""Generate paper/main_v1_2.tex (version 1.2 DRAFT) from paper/main.tex (version 1.1, the published record)
by explicit replacements, each asserted to match exactly once. main.tex and main.pdf are never touched, so the
v1.1 artefacts (Zenodo 10.5281/zenodo.23002378, the GitHub release attachment) stay reproducible.

Every number in the inserted text comes from a recorded, preregistered result (ledger H0-X-0008 and
H3-X-0001..0007); nothing here is new evidence. Text is built without .format/f-strings (it contains braces).
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
t = (HERE / "main.tex").read_text()


def rep(old, new):
    global t
    assert t.count(old) == 1, (t.count(old), old[:70])
    t = t.replace(old, new)


def para(heading, new=None, append=None):
    """Replace or extend the paragraph that starts with `heading` (paragraphs end at a blank line)."""
    global t
    assert t.count(heading) == 1, (t.count(heading), heading)
    i = t.index(heading)
    j = t.index("\n\n", i)
    t = t[:i] + new + t[j:] if new is not None else t[:j] + append + t[j:]


# ---- title, abstract ------------------------------------------------------------------------------------
rep(r"Preprint, version 1.1 (revised after peer review; version 1.0: doi:10.5281/zenodo.23000391)}",
    r"Preprint, version 1.2 (draft; version 1.1: doi:10.5281/zenodo.23002378, version 1.0: doi:10.5281/zenodo.23000391)}")
rep(r"lattice and as $O(\sqrt N)$ on flat ones.",
    r"lattice and as $O(\sqrt N)$ on flat ones; across five hyperbolic tilings $\log\kappa$ is nearly a function of $d_{\max}$ "
    r"alone (spread at most $0.56$ decades at equal depth), whereas at equal depth flat lattices are at least $1.8$ decades "
    r"worse, because the dependence on depth is concave for hyperbolic tilings and linear for flat ones. The difference is "
    r"not in how fast a single edge's boundary signal decays with depth, which is alike on all lattices, but in the "
    r"collinearity of the signals of equal-depth edges: on flat lattices they collapse onto a low-dimensional subspace "
    r"and the condition number grows by about a decade per unit of depth, on hyperbolic tilings they stay nearly "
    r"independent and it grows by $0.3$--$0.4$.")
rep(r"All data, code and a claim-by-claim",
    r"In simulation, a single-node defect is detected and localised at the $3\times10^{-4}$ precision budget on both "
    r"geometries, but the flat lattice fails at measurement noise $100\times$ below the hyperbolic one at $N\approx316$, and "
    r"component tolerance up to $5\%$ does not degrade localisation. All data, code and a claim-by-claim")

# ---- preregistration paragraph ------------------------------------------------------------------------
rep(r"including refutation criteria and rival functional forms~\cite{TrackHRepo}. Deviations are reported where they occur.",
    r"including refutation criteria and rival functional forms~\cite{TrackHRepo}. Deviations are reported where they occur. "
    r"The additional analyses of this version (preregistrations 5--11) were committed before each run in the same way.")

# ---- erratum of v1.1: TeX swallows the space after the \ARBLARGE control word ("27.1.Over") -------------
rep("\\ARBLARGE\nOver the whole tested range", "\\ARBLARGE{}\nOver the whole tested range")

# ---- mechanism sentence, qualified --------------------------------------------------------------------
rep(r"The mechanism is the scaling of depth with size.",
    r"The first part of the mechanism is the scaling of depth with size.")
rep(r"increases with depth; only on the flat lattice does depth grow as a power of $N$.",
    r"increases with depth; on the flat lattice depth grows as a power of $N$. Section~\ref{sec:tilings} shows that this is "
    r"only half of the explanation: the dependence of $\kappa$ on depth is itself different in the two classes.")

# ---- new subsection: other tilings ------------------------------------------------------------------------
TIL = r"""\subsection{Other tilings: depth is not the whole mechanism}
\label{sec:tilings}
The construction of Section~\ref{sec:cond} extends to any $\{p,q\}$ with $(p-2)(q-2)>4$. We computed $\kappa$ for
$\{7,3\}$, $\{8,3\}$, $\{5,4\}$, $\{6,4\}$ and $\{4,5\}$ up to six tile layers and $N=2888$ (Table~\ref{tab:tilings}), from
the closed-form Gram matrix of Section~\ref{sec:arb} in double precision. Forming $G=J^\top J$ squares the condition number,
so every value carries the bound $\varepsilon_{\mathrm{mach}}\kappa(G)$, at most $4\times10^{-9}$ in $\log_{10}\kappa$
here. Two controls against the direct SVD of version 1.0 pass; the second passed only after the control tolerance was
amended, before any tiling had been computed, to include this floor (preregistration 11, Deviation~1). Every interior
node of every tiling has degree $q$.

Five preregistered predictions were tested: four held and one was refuted. $\log\kappa$ is concave in the number of
layers for $\{7,3\}$ and $\{8,3\}$, and $\{8,3\}$ is better conditioned than $\{7,3\}$ at equal layer count
($2.31<2.46$, $3.06<3.27$, $3.69<3.89$). The prediction that the local exponent
$\mathrm d\log\kappa/\mathrm d\log N$ between the two largest sizes is at most $1.5$ for $\{8,3\}$ and at most $1.0$ for the
$q=4,5$ tilings was refuted for two of the three: the exponents are $1.10$ ($\{8,3\}$), $0.98$ ($\{6,4\}$), $1.19$ ($\{5,4\}$)
and $1.06$ ($\{4,5\}$). They decrease with size (for $\{5,4\}$: $1.50$, $1.35$, $1.19$) but stay above one in the tested range.

The main result concerns depth. At equal maximal depth $d_{\max}$ the hyperbolic tilings agree to within $0.45$, $0.25$,
$0.56$ and $0.21$ decades at $d_{\max}=1,2,3,5$, although $N$ varies by a factor of about $15$ at fixed depth (at
$d_{\max}=3$, $N$ runs from $112$ to $1710$). Within the hyperbolic class depth is therefore nearly a sufficient statistic
for $\kappa$. Across classes it is not: at $d_{\max}=5$ the square ($5.07$) and triangular ($8.67$) lattices exceed the
hyperbolic maximum ($3.27$) by at least $1.8$ decades (Fig.~\ref{fig:tilings}). The figure shows why. The increment of
$\log_{10}\kappa$ per unit of depth falls from about $0.66$ ($d_{\max}$ from $1$ to $2$, $\{5,4\}$) to $0.57$ ($2\to3$) and, on
$\{7,3\}$, to $0.40$ ($3\to5$) and $0.31$ ($5\to7$), whereas for the flat lattices it is roughly constant, $1.1$--$1.2$ per unit.
The scaling of depth with size, discussed above, is thus true but only half of the explanation; the other half is the
different dependence of $\kappa$ on depth.

\begin{figure}[t]
\centering
\includegraphics[width=0.75\linewidth]{fig_tilings.pdf}
\caption{$\log_{10}\kappa$ against maximal depth $d_{\max}$: five hyperbolic tilings (filled markers) nearly coincide and
are concave in depth; the square and triangular lattices (open markers, double-precision values) are roughly linear and
lie far above at equal depth.}
\label{fig:tilings}
\end{figure}

\paragraph{Where the difference comes from.} Three further preregistered computations (preregistrations 16, 18 and 19)
locate the difference. Write $d_e=H[a]-H[b]$ for the boundary signature of edge $e=(a,b)$, so that the Jacobian column
of $e$ is the upper triangle of $d_ed_e^\top$, and assign to $e$ the depth $\min(\mathrm{depth}(a),\mathrm{depth}(b))$.
(i) \emph{Amplitude is not the difference.} The mean of $\log_{10}\|d_e\|^2$ per edge depth, relative to depth $0$, falls
by nearly the same amount on every lattice: at depth $3$ it is between $-2.0$ and $-2.4$ decades on the five hyperbolic
tilings and $-2.4$ on both flat lattices, with the same concave profile (exploratory, no prediction). (ii) \emph{Coherence
is.} For the columns of all edges of one depth, let $f_d=\mathrm{PR}_d/n_d$ be the participation ratio of the eigenvalues
of their normalised Gram matrix divided by their number ($1$ for orthogonal columns, $1/n_d$ for collinear ones;
inner products in closed form, $\langle J_e,J_f\rangle=\tfrac12[(d_e\!\cdot\! d_f)^2-\sum_i d_{e,i}^2d_{f,i}^2]$, checked
against the explicit Jacobian to $2\times10^{-15}$). On the largest instance of each hyperbolic tiling $f_d$ stays between
$0.79$ and $0.99$ at every depth; on square $R{=}10$ it falls from $0.71$ at depth $0$ to $0.39$ at depth $3$ and $0.14$ at
depth $7$, on triangular $R{=}6.45$ from $0.52$ to $0.23$ and $0.20$. Deep flat edges share nearly the same boundary
signature. (iii) \emph{This is what sets $\kappa$.} Restricting the Jacobian to the columns of depth $\le d$, the condition
number grows by $0.98$ (square $R{=}10$) and $1.19$ (triangular $R{=}6.45$) decades per unit of depth beyond depth $1$,
against $0.28$ to $0.44$ on the five hyperbolic tilings (Table~\ref{tab:coherence}); the full-depth values reproduce
Table~\ref{tab:tilings} and version 1.0. The deficit is not an artefact of class size: with six randomly chosen columns
per depth class (fifty draws), the flat lattices still fall to $0.35$ and $0.46$ at their deepest class while every
hyperbolic tiling stays at or above $0.85$. The depth-$0\to1$ step is about one decade on every lattice and does not
separate the classes.

Of the eight predictions fixed for (ii) and (iii), four held and four were refuted; all four refutations were
statistical errors on our side, recorded in the repository: three predictions were set on the median $|\cos|$ between
column pairs, which is near zero on every lattice because most pairs are far apart, and one assumed that six random
columns would show a deficit that only the whole class of $76$ columns shows. The result stands on the predictions set
on $f_d$ and on the restricted condition number. A first argument for the collapse (preregistration 20) treats the
boundary signature of a depth-$d$ node on a flat disk as a harmonic-measure bump of width $\approx d$ boundary sites
on a boundary of length $\approx2\pi R$, so that the $\approx2\pi R$ columns of depth $d$ span only $\approx R/d$
directions and $d\,f_d$ should be constant, while on a hyperbolic disk the number of depth-$d$ nodes shrinks as fast as
their bumps widen and $f_d$ stays $O(1)$. On instances the argument had not seen, $d\,f_d$ is constant within a factor
$1.26$ on square $R{=}16$ over $2\le d\le12$ and $1.42$ on triangular $R{=}10.75$, and $f_d\ge0.76$ on $\{7,3\}$
$L{=}5$ and $\{4,5\}$ $L{=}7$ at every depth; but the same argument's prediction of an $R$-independent growth rate of
the restricted condition number was refuted ($1.26$ decades per depth at $R{=}16$ against $0.98$ at $R{=}10$). The
band-counting picture therefore stands and the rate of growth of $\kappa$ on flat disks remains underived.

\begin{figure}[t]
\centering
\includegraphics[width=0.95\linewidth]{fig_coherence_matched.pdf}
\caption{Left: effective dimension fraction of six randomly chosen equal-depth Jacobian columns (median of fifty draws)
against edge depth; hyperbolic tilings (filled markers, solid) stay near $1$, flat lattices (open markers, dashed) fall
with depth. Right: $\log_{10}\kappa$ of the Jacobian restricted to the columns of depth $\le d$.}
\label{fig:coherence}
\end{figure}

\subsection{Identifiability is exact; the difference is conditioning}"""
rep(r"\subsection{Identifiability is exact; the difference is conditioning}", TIL)
rep(r"\input{tables}", r"\input{tables}" + "\n" + r"\input{tables_v12}")

# ---- new subsection: defect detection and localisation ----------------------------------------------------
DEF = r"""\subsection{Defect detection and localisation in simulation}
\label{sec:defects}
A board would be used to detect and locate faults, so we tested this in simulation, preregistering each step
(preregistrations 5--10) and keeping refutations. A defect multiplies every edge of one interior node by a factor $f$;
the response saturates (at the deepest node $f=2$ gives $27$--$37\%$ of the $f=100$ signal). The data are
Neumann-to-Dirichlet maps with independent i.i.d.\ Gaussian noise $\varepsilon$, relative to their rms entry; the
precision budget of Section~\ref{sec:disorder} is $\varepsilon=3\times10^{-4}$.

\emph{Detection.} Against a known baseline a deep $\times100$ defect is detected at $\varepsilon=3\times10^{-4}$ on all
four lattices, and up to $\varepsilon=10^{-1}$ on $\{7,3\}$ $L=3$ against $10^{-2}$ on square $R=10$. Compared with the
ideal simulation, in the presence of component tolerance $g_e=1+\tau u_e$, $u_e\sim\mathcal U[-1,1]$, it is detected up
to $\tau=5\%$ on both hyperbolic lattices and up to $1\%$ on square $R=10$; comparing a board with its own earlier
measurement it is detected at every $\tau$ tested. A topological readout is less sensitive than the plain resistance
metric: the persistent homology (Gudhi) of the boundary effective-resistance metric shows no signature of a deep defect
above a disorder null, and its noise tolerance is at least $3.3$ times lower than that of the metric.

\emph{Localisation.} A matched-filter decoder over all interior nodes and a known set of eight contrasts recovers the defect
node with top-1 accuracy $1.00$ in all $60$ preregistered cells at $\varepsilon=3\times10^{-4}$ (contrasts $0.8$ to $100$,
three depths, four lattices), on flat and hyperbolic lattices alike. We had predicted that the flat lattices would fail at
deep nodes and weak contrast; two of three predictions were refuted. A noise sweep (Table~\ref{tab:loc}) locates the failure
boundary: at the deepest node the noise tolerance of the hyperbolic lattice exceeds that of the flat lattice by at
least $100\times$ at $N\approx316$, and at the $3\times10^{-4}$ budget the flat board has only $3$--$10\times$
headroom. Component tolerance up to $5\%$ (a fresh random board per trial, ideal-model decoder, both maps from the same
board) does not degrade localisation: $45$ of $48$ cells are perfect, and the three that are not belong to the
noise-limited cell of square $R=10$ ($0.55$--$0.60$ against $0.50$ on an ideal board). We had predicted otherwise,
carrying over the model-based detection result to a differential measurement.

\emph{What this does not show.} The defects are single nodes; the decoder is an oracle with a known contrast set; the noise
is i.i.d.; the cells use twenty trials and a half-decade noise grid; the deepest class is a single node on the square
lattices; and everything is simulation. The advantage of the hyperbolic lattice is a larger noise margin, not that a flat
board cannot localise a defect at ideal noise. Why the flat lattice fails at noise $100\times$ lower, far more than the
$8$--$10\times$ ratio of the boundary signals, is not explained.

\emph{Minimum contrast and hardware-like noise.} Two later preregistered runs (preregistrations 12 and 17) bound the
requirements of a board. At the $3\times10^{-4}$ budget both $\{7,3\}$ $L{=}3$ and square $R{=}10$ localise a $\pm10\%$
change of one deepest node perfectly (our prediction that the flat lattice would fail was refuted); at ten times that
noise the flat lattice still localises only $\times0.5$ and $\times1.5$ (top-1 accuracy $0.10$ and $0.05$ at $\times0.9$
and $\times1.1$) while the hyperbolic lattice keeps $\times0.9$ and $\times1.1$. At $N\approx112$ and contrast $\times2$, a
common-mode offset of up to $10\%$ of the rms entry, a gain drift of up to $1\%$ between the two maps, and quantisation
to $10$ bits leave localisation intact on both lattices ($49$ of $50$ cells at $1.00$, the lowest $0.95$); our three
predictions of failure were refuted in the safe direction, so this is a floor on the chain's requirements, not a
measurement of where they lie.

\subsection{RC dynamics and the Dirichlet spectral gap}"""
rep(r"\subsection{RC dynamics and the Dirichlet spectral gap}", DEF)

# ---- integrator controls on other tilings, exact rank on other tilings -----------------------------------------
para(r"\subsection{Integrator controls}",
     append=r" The same two controls were later run (preregistration 15) on $\{8,3\}$ $L{=}2$, $\{5,4\}$ $L{=}3$, "
            r"$\{6,4\}$ $L{=}2$ and $\{4,5\}$ $L{=}4$ ($N=120$ to $200$) with both integrators: every K1 error is below "
            r"$3\times10^{-8}$ and every K2 error below $1.1\times10^{-11}$. The relaxation times are $2.618$ ($\{8,3\}$), "
            r"$0.912$ ($\{5,4\}$), $0.500$ ($\{6,4\}$) and $0.712$ ($\{4,5\}$) in units of $RC$, against $2.750$ for "
            r"$\{7,3\}$ $L{=}2$, and the largest stiffness is $14.9$; the five preregistered predictions held.")
para(r"\subsection{Exact rank certificates}",
     append=r" For the other tilings (preregistration 14) the Jacobian is never formed: $k=E+20$ random linear combinations "
            r"of its rows are built directly from the boundary signatures mod $p$, and rank $E$ of that matrix certifies "
            r"full column rank. Eleven instances of $\{7,3\}$, $\{8,3\}$, $\{5,4\}$, $\{6,4\}$ and $\{4,5\}$ up to "
            r"$N=1160$ and $E=1604$ are certified full rank for both primes (ledger H0-B-0003). A random \emph{subset} "
            r"of rows does not work (a resistor between two boundary nodes affects one row) and was rejected before the "
            r"preregistration was committed.")

# ---- discussion, limitations, research directions --------------------------------------------------------
rep(r"for the RC model a uniformly bounded relaxation time.",
    r"for the RC model a uniformly bounded relaxation time. Depth is the controlling variable within the hyperbolic class; "
    r"across geometries the dependence of $\kappa$ on depth differs (concave versus linear), so depth scaling explains the gap "
    r"only together with that difference, which in turn is the collinearity of the boundary signatures of equal-depth "
    r"edges, not their amplitude (Section~\ref{sec:tilings}).")
rep(r"(v) Only $\{7,3\}$ is studied among hyperbolic tilings.",
    r"(v) Conditioning is computed for five hyperbolic tilings up to six layers and $N=2888$, with unit conductances and full "
    r"boundary; disorder and probe subsampling are studied only on $\{7,3\}$ and the flat lattices; exact rank "
    r"certificates cover the five tilings up to $E=1604$ and the flat lattices up to $N=475$. The coherence mechanism is "
    r"measured, not derived, and the effective-dimension statistic was compared across depth classes of different sizes "
    r"except in the matched-size control.")
rep(r"(vii) The novelty search was targeted, not systematic.",
    r"(vii) The novelty search was targeted, not systematic.\newline "
    r"(viii) Detection and localisation are simulations of single-node defects with an oracle decoder, i.i.d.\ noise, "
    r"tolerance up to $5\%$ and at most twenty trials per cell; multi-node defects and unknown contrasts are untested, and the "
    r"hardware-noise models (offset, gain drift, quantisation) were tested on one grid that never reached failure.")
para(r"\paragraph{Difference imaging.}",
     new=r"\paragraph{Difference imaging.} Single-node localisation from the difference of two boundary maps is now tested in "
         r"simulation (Section~\ref{sec:defects}). Open are multi-node and extended defects, unknown contrasts, tolerance above "
         r"$5\%$, hardware noise, and an explanation of why the flat lattice fails at noise $100\times$ below the hyperbolic one.")
para(r"\paragraph{Other tilings and a scaling law.}",
     new=r"\paragraph{Other tilings and a scaling law.} Section~\ref{sec:tilings} covers five tilings and locates the "
         r"concave-versus-linear difference in the coherence of equal-depth boundary signatures. Open are a derivation of "
         r"that coherence (a plausible route: on a flat disk the harmonic measure seen from depth $d$ is smoothed over a "
         r"boundary arc of length $\sim d$, so the signatures of the $\sim R$ edges at depth $d$ span $\sim R/d$ directions, "
         r"whereas on a hyperbolic disk the boundary grows with the bulk and no such collapse occurs; this is a conjecture, "
         r"not a result), disorder and probe subsampling on the other tilings, tilings with $q\ge6$, and a test of whether "
         r"the exponents of the $q=4,5$ tilings keep falling at larger $N$.")
para(r"\paragraph{Tabletop measurement.}",
     append=r" In simulation (Section~\ref{sec:defects}), a single-node fault is localised at this budget on either geometry, "
            r"and component tolerance up to $5\%$ does not matter for a same-board differential measurement; the benefit of "
            r"the hyperbolic layout is noise robustness, and the board's role is to test that mechanism and the relaxation time.")

# ---- change log, verification table ---------------------------------------------------------------------------
rep(r"\section*{Verification status}",
    r"""\section*{Changes from version 1.1}
Version 1.2 (draft) adds the following, all preregistered before it was run; nothing in versions 1.0 or 1.1 is altered.
(a) Conditioning across five hyperbolic tilings and a \emph{qualification} of the mechanism statement of version 1.1:
depth scaling is only half of the explanation (Section~\ref{sec:tilings}). One prediction of that analysis was refuted, and
a control tolerance was amended before any result was seen. (b) Defect detection and localisation in simulation, against
measurement noise and component tolerance (Section~\ref{sec:defects}); two localisation predictions and one tolerance
prediction were refuted. (c) The verification table below now also lists the claims of version 1.1 that it omitted.
(d) Erratum: in version 1.1, Section~\ref{sec:cond}, a space is missing after ``27.1'' (a typesetting slip; no
content is affected). (e) The mechanism behind the concave-versus-linear dependence: per-edge amplitude is alike on all
lattices, the coherence of equal-depth boundary signatures differs, and the depth-restricted condition number follows it
(Section~\ref{sec:tilings}); four of eight predictions were refuted, all through statistic choices recorded as lessons,
and a band-counting argument for the collapse was tested on unseen instances (three of four predictions held).
(f) Exact full-rank certificates and integrator controls on the other tilings; minimum detectable contrast and
hardware-like noise in the localisation simulations. Of these later runs, a small model recorded the claims and a larger
one audited them against the data, following a written runbook in the repository.

\section*{Verification status}""")
rep(r"Integrator controls K1/K2, SciPy and rusty-SUNDIALS CVODE & X & H2-X-0004 \\ \bottomrule",
    r"""Integrator controls K1/K2, SciPy and rusty-SUNDIALS CVODE & X & H2-X-0004 \\
Dimension-matched probe control (corrects version 1.0) & X & H0-X-0005 \\
Conditioning under disorder and defects & X & H0-X-0006 \\
Flat growth law beyond double precision (ball arithmetic) & X & H0-X-0007 \\
Conditioning across five tilings (depth nearly universal within the class) & X & H0-X-0008 \\
No persistent-homology signature of a deep defect & X & H3-X-0001 \\
Defect detection against measurement noise & X & H3-X-0002 \\
Defect detection against component tolerance & X & H3-X-0003 \\
Defect response saturates in the contrast & X & H3-X-0004 \\
Localisation at the $3\times10^{-4}$ budget & X & H3-X-0005 \\
Localisation noise margin & X & H3-X-0006 \\
Localisation under component tolerance & X & H3-X-0007 \\
Full rank certified on five tilings, eleven instances & B & H0-B-0003 \\
Integrator controls on four more tilings & X & H2-X-0005 \\
Minimum detectable contrast & X & H3-X-0008 \\
Localisation under offset, drift and quantisation & X & H3-X-0009 \\
Per-edge sensitivity versus depth (exploratory) & X & H0-X-0009 \\
Coherence of equal-depth columns differs between classes & X & H0-X-0010 \\
Depth-restricted $\kappa$ and matched-size coherence & X & H0-X-0011 \\
Band-counting argument on unseen instances (form held, rate refuted) & X & H0-X-0012 \\ \bottomrule""")

(HERE / "main_v1_2.tex").write_text("% GENERATED by paper/make_v12.py from paper/main.tex (version 1.1) -- do not edit\n" + t)
print("wrote main_v1_2.tex")
