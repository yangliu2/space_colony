# Contested: Minimum Gravity Level for Long-Term Human Health

## The Question

How much artificial gravity is actually required for a human to remain healthy
over years or decades? The field assumes 1g — but that assumption has no
empirical basis for *partial* gravity.

## What We Know: The Zero-g Evidence Base

The International Space Station has produced the most comprehensive long-duration
human spaceflight data. Scott Kelly's one-year mission (2015–2016) and the
associated NASA Twins Study (Garrett-Bakelman et al. 2019) are the primary
reference:

| Physiological system | Effect observed |
|---|---|
| Bone mineral density | ~$1\%$ loss per month, partially reversible on return |
| Muscle mass | Significant atrophy without countermeasures |
| Cardiovascular | Heart became more spherical; cardiac output dropped |
| Vision (SANS) | 6 of 7 long-duration astronauts developed Spaceflight-Associated Neuro-ocular Syndrome — intracranial pressure shifts flattened the eyeball |
| Telomeres | Lengthened in flight, rapidly shortened on return — mechanism unknown |
| Gut microbiome | Measurable composition shift |

SANS is now NASA's most alarming long-term finding. Kelly required corrective
lenses after return. The mechanism — fluid shift toward the head in
microgravity raising intracranial pressure — is well understood; the
long-term consequence is not **(Mader et al. 2011)**.

**Critical caveat:** All of this data is for $g = 0$. No human has spent more
than a few days at any partial gravity level between $0$ and $1g$.

## The Contested Gap: Partial Gravity Is Unknown Territory

The Moon (Apollo missions, 1969–1972) provided the only human partial-gravity
exposure in history — at $g_{\text{Moon}} = 0.165g$. Maximum surface stay:
3 days 2 hours (Apollo 17). No health effects were measurable at that timescale.

Mars, at $g_{\text{Mars}} = 0.379g$, has never been visited by humans.

The field has therefore been forced to extrapolate from two data points:

$$g = 0 \quad \text{(ISS — years of data)} \qquad g = 1 \quad \text{(Earth — centuries of data)}$$

Everything in between is inference.

## Camp 1: Only 1g Is Proven Safe (Conservative / NASA Default)

**Position:** Until evidence shows otherwise, design for $1g$ artificial gravity.
Any rotating habitat must produce the full $9.81\ \text{m/s}^2$ centripetal
acceleration at the rim.

**Key argument:** The ISS evidence shows that every physiological system
degrades in zero-g. There is no identified threshold below which degradation
stops. Without proof that partial gravity is sufficient, conservative design
requires full gravity.

**Implication for habitat design:** Minimum radius at 2 RPM limit is
$r_{\min} = 224\ \text{m}$. This drives the cost of any first habitat.

## Camp 2: Partial Gravity May Be Sufficient (Globus et al.)

**Position:** The 1g assumption is a policy choice, not an empirical finding.
There is evidence that even small amounts of gravity provide significant
biological benefit over zero-g.

**Key data:** Morey-Holton's hindlimb unloading rat studies
**(Morey-Holton and Globus 1998)** applied varying fractions of normal body
weight to rats otherwise in simulated weightlessness. Results showed a
**roughly linear dose-response** — rats at $0.3g$-equivalent loading retained
significantly more bone and muscle than zero-g controls. The relationship did
not appear to have a sharp threshold.

Globus and Hall (2017) argue this implies a minimum tolerable gravity for
humans could be as low as $0.1g$–$0.3g$. At $0.3g$ and 4 RPM, the
minimum viable habitat radius falls to approximately:

$$r_{\min} = \frac{g_{\text{target}}}{\omega^2} = \frac{0.3 \times 9.81}{(4 \times 2\pi/60)^2} \approx 17\ \text{m}$$

compared to $224\ \text{m}$ at $1g$, 2 RPM. The economic implications are
transformational — a factor of $\sim 130\times$ reduction in minimum floor area.

**Key limitation of this argument:** The rat studies are hindlimb unloading
simulations on Earth, not actual reduced gravity. Extrapolation to humans
is uncertain. The dose-response linearity is plausible but unproven for
human bone, cardiovascular, and neuro-ocular systems.

## What Would Resolve It

A rotating section aboard ISS or a dedicated free-flying testbed exposing
human subjects to $0.3g$, $0.5g$, and $0.7g$ for 6-month periods each.
NASA's Centrifuge Accommodations Module (CAM) was designed for exactly this
purpose and manifested for ISS. It was cancelled in 2005 during NASA budget
cuts **(NASA Office of Inspector General 2007)**.

That cancellation is arguably the single most consequential gap in current
space settlement science. A $\sim\$300\ \text{M}$ instrument cancelled over
two decades ago has left the entire field's minimum viable habitat size
estimation — and therefore its economics — on an empirical foundation of zero
human partial-gravity data.

## Implications for This Model

This model conservatively targets $1g$ at the rim with a 2 RPM upper limit,
placing minimum viable radius at approximately $982\ \text{m}$
(cross-coupling limited, not gravity-level limited at this radius). The
gravity-level slider permits exploration down to $0.3g$. The true answer to
how low gravity can go before humans degrade remains, as of 2026, empirically
open.

## References

- Garrett-Bakelman, Francine E., et al. "The NASA Twins Study: A
  multidimensional analysis of a year-long human spaceflight." *Science* 364.6436
  (2019). **(Garrett-Bakelman et al. 2019)**
- Globus, Al, and Theodore Hall. "Space Settlement: An Easier Way."
  *NSS Space Settlement Journal* (2017). **(Globus and Hall 2017)**
- Mader, Thomas H., et al. "Optic Disc Edema, Globe Flattening, Choroidal
  Folds, and Hyperopic Shifts Observed in Astronauts after Long-duration Space
  Flight." *Ophthalmology* 118.10 (2011): 2058–2069. **(Mader et al. 2011)**
- Morey-Holton, Emily R., and Ruth K. Globus. "Hindlimb-unloading rodent
  model: technical aspects." *Journal of Applied Physiology* 92.4 (2002):
  1367–1377. **(Morey-Holton and Globus 1998)**
- NASA Office of Inspector General. *Review of the Cancellation of the
  Centrifuge Accommodations Module.* NASA, 2007.
