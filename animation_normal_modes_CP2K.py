# Load modules
import numpy as np
from itertools import cycle
from collections import namedtuple


# Functions
def read_cp2k_molden_file(filename, natoms, title="NModes"):
    """ Reads the CP2K vibration output and splits it in 5 sections:
    
    - title : title section (optional)
    - atomtypes : iteratable
        list of atomtypes.
    - coords : np.array
        array of coordinates
    - intensities : list
        list of intensities of the normal modes
    - vibrations : list of np.array
        list of arrays of modifications to apply to coordinates
      
    ( str, int, title=str ) --> ( namedtuple( coords, title, atomtypes, intensities, vibrations ) )
    
    Usage:
    read_cp2k_molden_file("DA.TS.freq-VIBRATIONS-1.mol", 24)
    """
    
    # Intensities
    vib = False
    vibrations = []
    
    # Coordinates
    xyz = False
    count = 0 
    coords = np.zeros([natoms, 3], dtype="float64")
    atomtypes = []
    
    # Vibrations
    mod = False
    mcount = 0
    modifications = []
    m = np.zeros([natoms, 3], dtype="float64")
    
    # Read file
    lines = [line.rstrip('\n') for line in open(filename)]
    
    for line in lines:
        # Split lines
        line = line.split()
        
        # Initiate the vib flag
        if "[FREQ]" in line:
            vib = True
            xyz = False
            mod = False 
        
        # Read intensities when vib is True
        elif vib: 
            if "[FR-COORD]" in line: 
                vib = False
                xyz = True
                mod = False
            else:
                vibrations.append(float(line[0]))
        
        # Read coordinates and atomtypes when xyz is True
        elif xyz:
            if "[FR-NORM-COORD]" in line: 
                vib = False
                xyz = False
                mod = True
            else:
                if count < natoms:
                    atomtypes.append(line[0])
                    coords[count][:] = list(map(float, line[1:4]))
            count += 1
        
        # Read vibration coordinates when mod is True
        elif mod:
            if "vibration" in line:
                if "1" not in line:
                    modifications.append(m)
                mcount = 0
                m = np.zeros([natoms, 3], dtype="float64")
            else:
                if mcount < natoms:
                    m[mcount][:] = list(map(float, line[0:3]))
                    mcount += 1
    
    # save as namedtuple
    return namedtuple(title, ["title", "coords", "atomtypes", "intensities", "vibrations"])         (title, coords, atomtypes, vibrations, modifications)


def generate_animation_normal_modes(tup, vib, n):
    """ Morph coordinates using the normal modes vibratios vectors. 
    
    - title : title section (optional)
    - atomtypes : iteratable
        list of atomtypes.
    - coords : list of np.array
        list of arrays of modifications to apply to coordinates
    
    ( namedTuples, int, int ) --> ( namedtuple( coords, title, atomtypes ) ) 
    
    Usage:
    generate_animation_normal_modes(nmodes, 0, 10)
    """
    
    # Gather information of the system:
    #       Coordinates & vibrations
    coords = tup.coords
    vibration = tup.vibrations[vib]
    
    # List to store the new coordinates
    new_coords = []
    
    # Generate coordinates
    for m in range(-n, n, 1):
        tmp = coords + m * 0.1 * vibration
        new_coords.append(tmp)
        
    # save as namedtuple
    return namedtuple("Vibration"+str(vib+1), ["title", "coords", "atomtypes"])         ("Vibration "+str(vib+1), new_coords, tup.atomtypes)

    

def write_multiple_XYZ_file( filename, tup ):
    """ Writes a multiple XYZ file with structures for each normal mode. 
    Adapted from pele.utils.xyz.
    https://github.com/pele-python/pele/blob/master/pele/utils/xyz.py
      
    ( str, namedtuple ) --> None
    
    Usage:
    write_multiple_XYZ_file("test.xyz", nmodes)
    """
    
    # correction factor
    f = 1.3/2.5
    
    # open file for writing coordinates
    fout = open(filename, "w")
    
    # for structures:
    for s in tup.coords:
        fout.write("%d\n%s\n" % (s.size / 3, tup.title))
        for x, atomtype in zip(s.reshape(-1, 3), cycle(tup.atomtypes)):
            fout.write("%s %.12g %.12g %.12g\n" % (atomtype, x[0]*f, x[1]*f, x[2]*f))
    
    # Close output file
    fout.close()
    


# Main
nmodes = read_cp2k_molden_file("DA.TS.freq-VIBRATIONS-1.mol",  24)

for i in range(69):
    kk = generate_animation_normal_modes(nmodes, 0, 10)
    write_multiple_XYZ_file("Vibrations/DA.vibrations"+str(i)+".xyz", kk)





# In[ ]:



