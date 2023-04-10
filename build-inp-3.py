##Automatically Generate CP2K AIMD inpfile
##JIAAO WANG@UTAUSTIN
##CHECK LINUX ENV MUST CONTAIN Multiwfn
##MUST RUN UNDER LINUX ENV
##wangjiaao0720@utexas.edu
import os
import subprocess
import argparse
import sys
#import line_profiler


def coordinate(file_name):
    

    if os.path.exists("../inptemp.inp"):
        f = open("../inptemp.inp").readlines()
    else:
        print("inptemp not found ,please generatre inptemp in the /.. path")
        sys.exit()
    coordinate_list=[]
    startread=False
    for line in f:
        if line == '  &SUBSYS\n':
            startread=True
          #  print(line)


        if startread==True:
            coordinate_list.append(line)

        if line == '    &COORD\n':
            startread=False
            break
         #   print(line)




    input_str=open(file_name).readlines()

        #print(input_str)

        #output = []
    output_str = ''
    for line in input_str:
        if line.startswith("ATOM"):
            tokens = line.split()

            element=tokens[2][0].upper() + tokens[2][1:].lower()
            #print(element)    
            output_str += "      "+element+"   "+str(float(tokens[5]))+"   "+str(float(tokens[6]))+"   "+str(float(tokens[7]))+"\n"
    
    #print(output_str)

        #output_str += f"Si\t{tokens[5]:.8f}\t{tokens[6]:.8f}\t{tokens[7]:.8f}\n"

                #.append(output_str)
    #print(len(output_str))
    coordinate_list.append(output_str)



    for line in f:
        if line == '    &END COORD\n':
            startread=True
           # print(line)


        if startread==True:
            coordinate_list.append(line)

        if line == '  &END SUBSYS\n':
            startread=False
            break
            #print(line)


    
    
    
    print("Coordination Part Successfully Generated")
    
    return coordinate_list
    
    
    

def main(file):
    subprocess.call('rm *.inp', shell=True)
    global file_name
    filename=file.input

    before_coor=['#Generated by Jiaao_Wang_UTAUSTIN_Henkelman_Group\n', '&GLOBAL\n', '  PROJECT '+filename+'\n', '  PRINT_LEVEL MEDIUM\n', '  RUN_TYPE MD\n', '&END GLOBAL\n', '\n', '&FORCE_EVAL\n', '  METHOD Quickstep\n', '\n']
    
    
    coordinate_list=coordinate(filename)
    
    
    after_coor=['\n', '  &DFT\n', '    BASIS_SET_FILE_NAME  BASIS_MOLOPT\n', '    POTENTIAL_FILE_NAME  GTH_POTENTIALS\n', '#   WFN_RESTART_FILE_NAME Layer-RESTART.wfn\n', '   # CHARGE    0 #Net charge\n', '    #MULTIPLICITY    1 #Spin multiplicity\n', '    UKS\n', '    &QS\n', '      #METHOD GPW\n', '      EPS_DEFAULT 1E-10 #This is default. Set all EPS_xxx to values such that the energy will be correct up to this value\n', '      EXTRAPOLATION ASPC #Extrapolation for wavefunction during e.g. MD. ASPC is default, PS also be used\n', '      EXTRAPOLATION_ORDER 3 #Order for PS or ASPC extrapolation. 3 is default\n', '    &END QS\n', '    &POISSON\n', '      PERIODIC XYZ #Direction(s) of PBC for calculating electrostatics\n', '      PSOLVER PERIODIC #The way to solve Poisson equation\n', '    &END POISSON\n', '    &XC\n', '      &XC_FUNCTIONAL PBE\n', '      &END XC_FUNCTIONAL\n', '      &VDW_POTENTIAL\n', '        POTENTIAL_TYPE PAIR_POTENTIAL\n', '        &PAIR_POTENTIAL\n', '          PARAMETER_FILE_NAME dftd3.dat\n', '          TYPE DFTD3\n', '          REFERENCE_FUNCTIONAL PBE\n', '        &END PAIR_POTENTIAL\n', '      &END VDW_POTENTIAL\n', '    &END XC\n', '    &MGRID\n', '      CUTOFF 500\n', '      REL_CUTOFF 50\n', '    &END MGRID\n', '    &SCF\n', '      MAX_SCF 150 #Should be set to a small value (e.g. 30) if enabling outer SCF\n', '      MAX_SCF_HIST 1\n', '\n', '      &OT\n', '        PRECONDITIONER FULL_KINETIC #FULL_SINGLE_INVERSE is also worth to try. FULL_ALL is better but quite expensive for large system\n', '        MINIMIZER DIIS #CG is worth to consider in difficult cases\n', '        LINESEARCH 2PNT #1D line search algorithm for CG. 2PNT is default, 3PNT is better but more costly. GOLD is best but very expensive\n', '      &END OT\n', '\n', '      &PRINT\n', '        &RESTART #Use "&RESTART OFF" can prevent generating wfn file\n', '          BACKUP_COPIES 0 #Maximum number of backup copies of wfn file\n', '        &END RESTART\n', '      &END PRINT\n', '    &END SCF\n', '  &END DFT\n', '  &PRINT\n', '    &FORCES ON\n', '  &END FORCES\n', '  &END PRINT\n', '&END FORCE_EVAL\n', '\n', '&MOTION\n', '  &MD\n', '    ENSEMBLE LANGEVIN\n', '    STEPS 0     \n', '    TIMESTEP 1 #fs. Decrease it properly for high temperature simulation\n', '    TEMPERATURE 800 #Initial and maintained temperature (K)\n', '    &LANGEVIN\n', '            GAMMA 0.01\n', '            NOISY_GAMMA 2.2E-4\n', '    &END LANGEVIN\n', '    &THERMAL_REGION\n', '            DO_LANGEVIN_DEFAULT F     \n', '            &PRINT\n', '                    &LANGEVIN_REGIONS\n', '                    &END LANGEVIN_REGIONS\n', '            &END PRINT\n', '    &END THERMAL_REGION\n', '    #&THERMOSTAT\n', '    # TYPE GLE\n', '    #&END THERMOSTAT\n', '  &END MD\n', '\n', '  &PRINT\n', '    &TRAJECTORY\n', '      &EACH\n', '        MD     1 #Output frequency of geometry\n', '      &END EACH\n', '      FORMAT pdb\n', '    &END TRAJECTORY\n', '    &VELOCITIES\n', '      &EACH\n', '       MD     1 #Output frequency of velocity\n', '      &END EACH\n', '    &END VELOCITIES\n', '    &RESTART\n', '      BACKUP_COPIES 0 #Maximum number of backing up restart file\n', '      &EACH\n', '        MD 1 #Frequency of updating last restart file\n', '      &END EACH\n', '    &END RESTART\n', '  &END PRINT\n', '&END MOTION\n']
    
    #subprocess.call('rm *.inp', shell=True)
    #print(filename.split(".")[1]+)
    output=filename.split(".")[0]+".inp"
    f = open(output, "w+")
    f.truncate(0)
    #f.close()
    
    
    #f = open(output, "a")
    f.writelines(before_coor)
    #f.close()
    
    #f = open(output, "a")
    f.writelines(coordinate_list)
    f.writelines(after_coor)
    f.close()
    
    print("\n"+output+" Successfully Generated")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="check cif lattice, if not reach value, supercell it until to get it")
    parser.add_argument("-input", help="input: filename in pdb file,relative")
    #parser.add_argument("-num", help="withdraw number, can be 'all' or a number")

    fileinput = parser.parse_args()

    main(fileinput)


#subprocess.call('rm *.inp', shell=True)