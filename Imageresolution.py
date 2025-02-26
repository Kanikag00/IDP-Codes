import PIL
from PIL import Image
import glob
import pandas as pd
  
image_directory="/home/ntlpt-52/work/IDP/Auto_Label/Trade_Finance/Trade_Finance_Actual_Data/Images/"
resolution_dict={"ImageFileName":[],"Width":[],"Height":[]}
for file in glob.glob(image_directory+"*"):
    img = PIL.Image.open(file)
    # fetching the dimensions
    wid, hgt = img.size
    resolution_dict["ImageFileName"].append(file)
    resolution_dict["Width"].append(wid)
    resolution_dict["Height"].append(hgt)

resolution_df = pd.DataFrame(resolution_dict)
overall_resolution_info=open("/home/ntlpt-52/work/IDP/Auto_Label/Trade_Finance/Trade_Finance_Actual_Data/Overall_Resolution.txt","w")
overall_resolution_info.writelines("Minimum width and height = "+str(resolution_df['Width'].min())+"x"+str(resolution_df['Height'].min())+"\n")
overall_resolution_info.writelines("Maximum width and height = "+str(resolution_df['Width'].max())+"x"+str(resolution_df['Height'].max())+"\n")
overall_resolution_info.writelines("Median of width and height = "+str(resolution_df['Width'].median())+"x"+str(resolution_df['Height'].median())+"\n")
overall_resolution_info.writelines("Mean width and height = "+str(resolution_df['Width'].mean())+"x"+str(resolution_df['Height'].mean())+"\n")
overall_resolution_info.close()
resolution_df.to_csv("/home/ntlpt-52/work/IDP/Auto_Label/Trade_Finance/Trade_Finance_Actual_Data/Images_resolution.csv")

    