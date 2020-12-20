[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/DataForScience/Causality/master)

# Causality

How do causes lead to effects? Can you associate the cause leading to the observed effect? Big Data opens the doors for us to be able to answer questions such as this, but before we are able to do so, we must dive into the field of Causal Inference, a field championed by Judea Pearl.
In this series of blog posts we will learn about the main ideas of Causality by working our way through “Causal Inference In Statistics” a nice Primer co-authored by Pearl himself.

<p align="center">
<a href='https://amzn.to/3gsFlkO' alt='Judea Pearl — Causal Inference in Statistics: A Primer'><img src='data/causality.jpeg'></a>
 <br/>
  Amazon Affiliate Link: https://amzn.to/3gsFlkO
</p>


The book is divided into Four chapters. The first chapter covers background material in probability and statistics. The other three chapters are (roughly) organized to match the “Three steps” in the ladder of causality as defined by Pearl:

1. — Association
2. — Intervention
3. — Counterfactuals

In this series of blog posts we will cover most of the content of the book, with a special emphasis on the parts that I believe are more interesting or relevant to practical applications. In addition to summarizing and explaining the content, we will also explore some of the ideas using simple (or as simple as possible) Python code you can run on Binder: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/DataForScience/Causality/master)



## Chapter 1
1.2 - [Simpson's Paradox](https://medium.com/data-for-science/causal-inference-part-i-415538211aa1) -- [1.2 - Simpson's Paradox.ipynb](https://github.com/DataForScience/Causality/blob/master/1.2%20-%20Simpsons%20Paradox.ipynb)

1.3 - [Probability Theory](https://medium.com/data-for-science/causal-inference-part-ii-probability-theory-8fc804fa8240) -- [1.3 - Probability and Statistics.ipynb](https://github.com/DataForScience/Causality/blob/master/1.3%20-%20Probability%20and%20Statistics.ipynb)

1.4 - [Graphs](https://medium.com/data-for-science/causal-inference-part-iii-graphs-df043300add1) -- [1.4 - Graphs.ipynb](https://github.com/DataForScience/Causality/blob/master/1.4%20-%20Graphs.ipynb)

1.5 - [Structural Causal Models](https://medium.com/data-for-science/causal-inference-part-iv-structural-causal-models-df10a83be580) -- [1.5 - Structural Causal Models.ipynb](https://github.com/DataForScience/Causality/blob/master/1.5%20-%20Structural%20Causal%20Models.ipynb)

## Chapter 2
2.2 - [Chains and Forks](https://medium.com/data-for-science/causal-inference-part-v-chains-and-forks-7b0b088c346e) -- [2.2 - Chains and Forks.ipynb](https://github.com/DataForScience/Causality/blob/master/2.2%20-%20Chains%20and%20Forks.ipynb)

2.3 - [Colliders](https://medium.com/data-for-science/causal-inference-part-vi-colliders-af07301c9a15) -- [2.3 - Colliders.ipynb](https://github.com/DataForScience/Causality/blob/master/2.3%20-%20Colliders.ipynb)

2.4 - [d-separation](https://medium.com/data-for-science/causal-inference-part-vii-d-separation-aa74e361d34e) -- [2.4 - d-separation.ipynb](https://github.com/DataForScience/Causality/blob/master/2.4%20-%20d-separation.ipynb)

2.5 - [Model Testing and Causal Search](https://medium.com/data-for-science/causal-inference-part-vii-model-testing-and-causal-search-536b796f0384) -- [2.5 - Model Testing and Causal Search.ipynb](https://github.com/DataForScience/Causality/blob/master/2.5%20-%20Model%20Testing%20and%20Causal%20Search.ipynb)

## Chapter 3

3.1 - [Interventions](https://medium.com/data-for-science/causal-inference-part-ix-interventions-c3f94190191d) -- [3.1 - Interventions.ipynb](https://github.com/DataForScience/Causality/blob/master/3.1%20-%20Interventions.ipynb)

3.2 - [Adjustment Formula](https://medium.com/data-for-science/causal-inference-part-x-the-adjustment-formula-f9668469d76) -- [3.2 - The Adjustment Formula.ipynb](https://github.com/DataForScience/Causality/blob/master/3.2%20-%20The%20Adjustment%20Formula.ipynb)

3.3 - [Backdoor Criterion](https://medium.com/data-for-science/causal-inference-part-xi-backdoor-criterion-e29627a1da0e) -- [3.3 - Backdoor Criterion.ipynb](https://github.com/DataForScience/Causality/blob/master/3.3%20-%20Backdoor%20Criterion.ipynb)

3.4 - [Front-Door Criterion](https://medium.com/data-for-science/causal-inference-part-xii-front-door-criterion-38bec5172f3e) -- [3.4 - Front-Door Criterion.ipynb](https://github.com/DataForScience/Causality/blob/master/3.4%20-%20Front-Door%20Criterion.ipynb)

3.5 - [Conditional Interventions and Covariate-Specific Effects](https://medium.com/data-for-science/causal-inference-part-xiii-conditional-interventions-and-covariate-specific-effects-1c0126b8b996) -- [3.5 - Conditional Interventions and Covariate-Specific Effects.ipynb](https://github.com/DataForScience/Causality/blob/master/3.5%20-%20Conditional%20Interventions%20and%20Covariate-Specific%20Effects.ipynb)

3.6 - [Inverse Probability Weighing](https://medium.com/data-for-science/causal-inference-part-xiv-inverse-probability-weighing-f81680321427) -- [3.6 - Inverse Probability Weighing.ipynb](https://github.com/DataForScience/Causality/blob/master/3.6%20-%20Inverse%20Probability%20Weighing.ipynb)

---

For a more in-depth analysis, checkout Pearl's more technical book:

<p align="center">
<a href='https://amzn.to/2OSBP6u' alt='Judea Pearl — Causality'><img src='data/book2.jpeg' height=250></a>
 <br/>
  Amazon Affiliate Link: https://amzn.to/2OSBP6u
</p>

---

Sign up to the [Sunday Briefing](http://data4sci.com/newsletter) newsletter to be the first to know when we publish new posts:

<p align="center">
<a href='https://data4sci.ck.page/8a51c452bc' alt='Sunday Briefing Newsletter'><img src='data/newsletter.png' width=500></a>
</p>
