# Example for parseMMEFT

In this folder you can find the files to compute a physical observable, starting from the NP Lagrangian.
We will compute the Lepton Flavour-Violating BR for the process mu -> e gamma in the scotogenic model ([arXiv:hep-ph/0601225](http://arxiv.org/abs/hep-ph/0601225), [arXiv:2004.05172 [hep-ph]](http://arxiv.org/abs/2004.05172)), as in the course ["Computing tools for the SMEFT" (SMEFT'22 Physics School, Siegen, Germany) by Avelino Vicente](https://ific.uv.es/~montesin/siegen2022.html).

The files are:

* [scotogenic.fr](https://github.com/Jorge-Alda/parseMMEFT/blob/main/example/scotogenic.fr): FeynRules file with the definition of the Lagrangian.
* [scotogenic.dat](https://github.com/Jorge-Alda/parseMMEFT/blob/main/example/scotogenic.dat): File created by `MatchMakerEFT` containing the `Mathematica` replacement rules for each Wilson coefficient.
* [scotogenic.py](https://github.com/Jorge-Alda/parseMMEFT/blob/main/example/scotogenic.py): `Python` script created by `parseMMEFT` with the functions to calculate the Wilson coefficients.
* [sminputs.py](https://github.com/Jorge-Alda/parseMMEFT/blob/main/example/sminputs.py): `Python` script to obtain the SM Lagrangian parameters at the high scale in the SM and SMEFT. Requires [`wilson`](https://wilson-eft.github.io/).
* [test.ipynb](https://github.com/Jorge-Alda/parseMMEFT/blob/main/example/test.ipynb): Jupyter notebook demostrating the use of `scotogenic.py`. Requires [`flavio`](http://flav-io.github.io/).
