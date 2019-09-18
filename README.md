# CP2K_normal_modes

**Description**: Python script to animate the normal modes found by the CP2K calculations

**Author**: Salomé Llabrés Prat, PhD

**Version**: 1.2

**Dependencies**:
-  Python3 (argparse, numpy, itertools and collections)

---

## About:

**CP2K_normal_modes** is a Python3 script that reads the CP2K vibration molden output (.mol) and creates XYZ file for each vibration found by CP2K. 

---

## Usage: 

```javascript
usage: animation_normal_modes_CP2K.py [-h] -i INPUT -o OUTPUT -f NFRAMES

Read MOLDEN file and write a multiple XYZ for each vibration.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        CP2K MOLDEN frequency MOL file.
  -o OUTPUT, --output OUTPUT
                        Base name for the vibration output files.
  -f NFRAMES, --nframes NFRAMES
                        Number of frames to describe the vibrations.
```

---

## Output:

```javascript
Number of atoms found: 24.
Number of vibrations found: 69.

Read CP2K frequency file.

Write multiple XYZ files for all the vibrations.
```


---

**To implement:**

- [ ] Write only selected vibrations. 

