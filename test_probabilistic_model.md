Consider the probabilistic model

2
p(μ|σ) =N(μ| 0,σ²) = √(1/(2πσ²)) exp(-μ²/2σ²)

p(x|μ) = N(x|μ,1) = 1/√(2π) ((x-μ)² ²)

and α set of observations D = {x₁,..., xₙ} consisting of N samples xᵢ € R.

(a) Express p(μ| σ) in terms of α = σ ∑ and justify that this parameter can be understood as a

precision.

(b) Find the MLE estimate for p.

(c) Find the MAP estimate for p.
(d) Can we find p(μ| α) for which the two determined estimates coincide?
# O
)

(e) Derive the posterior predictive distribution which is defined as p(μ| D, α).

State the term for p(μ| D, α) and determine its functional form.

Note: We parametrize μ|α with the precision parameter α = 1/σ² instead of the usual variance σ²
because it leads to α nicer solution.



```text
(b) Find the MLE estimate for p.

(c) Find the MAP estimate for p.
(d) Can we find p(μ| α) for which the two determined estimates coincide?
```




```text
(e) Derive the posterior predictive distribution which is defined as p(μ| D, α).

State the term for p(μ| D, α) and determine its functional form.

```




$$p(\mu|\sigma) =N(\mu| 0,\sigma^{2}) = \sqrt{1/(2\pi\sigma^{2}}) exp(-\mu^{2}/2\sigma^{2})$$




$$p(x|\mu) = N(x|\mu,1) = 1/\sqrt{2\pi} ((x - \mu)² ²)$$




$$and \alpha set of observations D = {x₁,..., xₙ} consisting of N samples xᵢ € R.$$




$$(a) Express p(\mu| \sigma) in terms of \alpha = \sigma \sum and justify that this parameter can be understood as a$$



$(d) Can we find p(\mu| \alpha) for which the two determined estimates coincide?$



$$(e) Derive the posterior predictive distribution which is defined as p(\mu| D, \alpha).$$



$State the term for p(\mu| D, \alpha) and determine its functional form.$



$$Note: We parametrize \mu|\alpha with the precision parameter \alpha = 1/\sigma^{2} instead of the usual variance \sigma^{2}$$



$because it leads to \alpha nicer solution.$
