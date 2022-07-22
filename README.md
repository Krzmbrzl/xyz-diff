# xyz-diff

Python3 script for producing nicely formatted diffs of [XYZ files](https://en.wikipedia.org/wiki/XYZ_file_format).

The script always diffs exactly two molecular geometries given as XYZ files. The output consists of as many lines as there are atoms in the diffed
geometries. Each line consists of four parts:
```
<element> <xDiff> <yDiff> <zDiff>
```
where `<element>` is either the element symbol of the respective atom, if the atom type was identical in both files or of the form `<leftElement> ->
<rightElement>`, if the atom type at this position differed between the files. `<xDiff>`, `<yDiff>` and `<zDiff>` are the differences in the
respective cartesian coordinates.

Example:
```
O         +0.00000000   +0.00000000   -0.01143253  
O         +0.00000000   -0.00000000   +0.01143253  
Cu -> Co  -0.01804938   +0.00829356   +0.00000000  
Cu        +0.01804938   -0.00829356   +0.00000000  
N         -0.04042133   +0.03424848   +0.00000000  
N         +0.04042133   -0.03424848   +0.00000000  
N         -0.02848896   -0.00191986   +0.01590888  
N         -0.02848896   -0.00191986   -0.01590888  
N         +0.02848896   +0.00191986   +0.01590888  
N         +0.02848896   +0.00191986   -0.01590888  
H         -0.04673929   +0.02155138   +0.00000000  
H         +0.04673929   -0.02155138   +0.00000000  
H         -0.04417332   +0.03825913   +0.00254647  
H         -0.04417332   +0.03825913   -0.00254647  
H         +0.04417332   -0.03825913   +0.00254647  
H         +0.04417332   -0.03825913   -0.00254647  
H         -0.02376989   -0.00091570   +0.01582489  
H         -0.02376989   -0.00091570   -0.01582489  
H         +0.02376989   +0.00091570   +0.01582489  
H         +0.02376989   +0.00091570   -0.01582489  
H         -0.02343687   -0.00428525   +0.01206063  
H         -0.02343687   -0.00428525   -0.01206063  
H         +0.02343687   +0.00428525   +0.01206063  
H         +0.02343687   +0.00428525   -0.01206063  
H         -0.03131781   -0.00348489   +0.01817259  
H         -0.03131781   -0.00348489   -0.01817259  
H         +0.03131781   +0.00348489   +0.01817259  
H         +0.03131781   +0.00348489   -0.01817259
```

By default the cartesian differences are color-coded such that zero is printed in a grey-ish color and the biggest absolute difference is highlighted
in a red-ish tone. All other differences are colored somewhere between these extrema using their absolute value as input for deciding which color to
use for them.

If you prefer a monochrome (no colors) output, use the `--monochrome` option.

