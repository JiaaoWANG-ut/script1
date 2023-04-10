"""
This is an example of how to generate descriptors
The script downloads file specify input files (.vol files) and get Density: {2.2311},
and stores the value into a file example/{num}/{suffix}. 
Finally a {num}.tar.gz file is uploaded to HDFS
No recovery is guaranteed by the example.
"""

import re
import argparse

# def main(FLAGS):    
#     def descriptor_example(input_file:str) -> float:
    
    
    
file_text = open('1.res', "r").read()

#re_density = re.search(r'NAV_cm\^3/g: (.*?) ', file_text)
#re_density = re.search(r"NAV_cm^3/g: (\d+(?:\.\d+)?)", file_text)

#re_density = re.search(r'Unitcell_volume: (.*?) ', file_text)
#re_density = re.search(r'Density: (.*?) ', file_text)
#re_density = re.search(r'AV_A\^3: (.*?) ', file_text)
#re_density = re.search(r'AV_Volume_fraction: (.*?) ', file_text)
#re_density = re.search(r'AV_cm\^3/g: (.*?) ', file_text)
#re_density = re.search(r'NAV_A\^3 (.*?) ', file_text)

#re_density = re.search(r'NAV_cm\^3/g: (.*?) ', file_text)

#re_density = re.search(r'Number_of_channels: (.*?) ', file_text)
#re_density = re.search(r'Number_of_pockets: (.*?) ', file_text)

#file_text = open(input_file, "r").read()
re_density = re.split('\s+', file_text)[1]
print(float(re_density))

    


#    return float(density_text)


#     input_file = FLAGS.input
#     result = descriptor_example(input_file=input_file)
#     if isinstance(result, float):
#         print(result)
#     else:
#         raise RuntimeError("{output} is not a float number".format(output=result))


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="example of discriptor")
#     parser.add_argument("-input", help="File path")
#     FLAGS = parser.parse_args()
#     main(FLAGS)

