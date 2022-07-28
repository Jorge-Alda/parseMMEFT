# parseMMEFT

Parse the results of [MatchMakerEFT](https://ftae.ugr.es/matchmakereft) into Python objects.

## Usage

Download the `Python` script `parseMMEFT.py` and run the command

```bash
python3 parseMMEFT.py mymodel.dat mymodel.py
```

where `mymodel.dat` is the file created by MatchMakerEFT (typically called `MatchingResults.dat` in the folder `mymodel_MM`), and `mymodel.py` is the output created by `parseMMEFT`. The script `mymodel.py` can be used to interface directly with other packages, like `wilson`, `flavio` and `smelli`.

You can see `parseMMEFT` in action [here](https://github.com/Jorge-Alda/parseMMEFT/tree/main/example).
