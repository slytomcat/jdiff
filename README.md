# json diff

Finds the difference between two JSON-files ignoring the attributes sequence in json-objects and sequence of arrays' elements (if it is not disabled by command line option).

Mandatory parameters: 
- path to original JSON-file (first file)
- path to new JSON-file (second file)

The option `-o` or `--keep_arrays_order` allows to keep arrays element's order during comparaation. The ojbjects coparison is not affected by this option.

The items are marked by `+` sign in result when they are exist in the first file but not exist in the second one. The items marked by `-` sing when they are exist in second file but not exist in the fist one. Equaul items are not marked.

Two JSON-objects `{"a":1,"b":2}` and `{"b":2,"a":1}` are equal (formatting has no matter). 

Without `-o` option two JSON-arrays `[1,2]` and `[2,1]` are considered as equal (formatting has no matter).

With `-o` option the arrays `[1,2]` and `[2,1]` are not equal. 
```
  [
-     1  
+     2
-     2
+     1
  ]
```
Only arrays `[1,2]` and `[1,2]` are equal. 

## Usage:

```
python3 jdiff.py <original JSON file> <new JSON file> [--keep_arrays_order|-o]
```

Comparison results are printed out to stdout. Use output redirection to store the result into a file. For example:
```
python3 jdiff.py a.json b.json > result.diff
```

## Examples

Example of work (sample files are available in repo):
```
python3 jdiff.py a.json b.json > result.diff
```
![Screenshot](https://github.com/slytomcat/jdiff/blob/master/Screenshot)

Example of work with `-o` option (considering the arrays order)
```
python3 jdiff.py a.json b.json -o > result.diff
```
![Screenshot_o](https://github.com/slytomcat/jdiff/blob/master/Screenshot_o)
