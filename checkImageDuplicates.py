#<----------------------------------------------------------For Two Images with ImageHash-------------------------------------------------------------------------
# from PIL import Image
# import imagehash
# import sys
# from pympler import asizeof

# hash0 = imagehash.average_hash(Image.open('/home/ntlpt-52/work/IDP/Auto_Label/Trade_Finance/Master_Data/Packing_List_705_page_0.png')) 
# hash1 = imagehash.average_hash(Image.open('/home/ntlpt-52/work/IDP/Auto_Label/Trade_Finance/Master_Data/Packing_List_706_page_3.png')) 
# cutoff = 5  # maximum bits that could be different between the hashes. 
# print("hash0",hash0)
# print("hash1",hash1)
# print("SIZE 0",sys.getsizeof(hash0))
# print(asizeof.asizeof(hash0))
# print("SIZE 1",sys.getsizeof(hash1))
# print(asizeof.asizeof(hash1))
# print("Difference",hash0-hash1)
# if hash0 - hash1 < cutoff:
#   print('images are similar')
# else:
#   print('images are not similar')
import json
import shutil
from imagededup.methods import *
from imagededup.utils import plot_duplicates
from logging_file import *
import os
import moment
import time

# phasher = CNN()
# phasher = WHash()
# phasher = AHash()
phasher = PHash()
# phasher = DHash()
image_directory='/home/ntlpt-52/Downloads/FIlflan/TradeDocuments_Images/COVERING_SCHEDULE/Cleaned_images'
unique_duplicates_images_directory='/home/ntlpt-52/Downloads/FIlflan/TradeDocuments_Images/COVERING_SCHEDULE/Unique_Cleaned'
if not os.path.isdir(unique_duplicates_images_directory):
    os.makedirs(unique_duplicates_images_directory)
encodings = phasher.encode_images(image_dir=image_directory)
duplicates = phasher.find_duplicates(encoding_map=encodings,max_distance_threshold=0)
unique_images=[]
duplicate_images=[]
SameDuplicatesInMoreThanOneImage={}
for key in duplicates.keys():
    if key not in duplicate_images:
        # unique_fodler_path=unique_duplicates_images_directory+"/"+key.split(".")[0]+"/Unique"
        # duplicates_folder_path=unique_duplicates_images_directory+"/"+key.split(".")[0]+"/Duplicates"
        unique_fodler_path =unique_duplicates_images_directory
        if not os.path.isdir(unique_fodler_path):
            os.makedirs(unique_fodler_path)
        # if not os.path.isdir(duplicates_folder_path):
        #     os.makedirs(duplicates_folder_path)
        shutil.copy(image_directory+"/"+key, unique_fodler_path+"/"+key)
        unique_images.append(key)
        for image in duplicates[key]:
            # shutil.copy(image_directory+"/"+image, duplicates_folder_path+"/"+image)
            if image in duplicate_images:
                if image not in SameDuplicatesInMoreThanOneImage.keys():
                    SameDuplicatesInMoreThanOneImage[image]=[key]
                else:
                    SameDuplicatesInMoreThanOneImage[image].append(key)
            else:
                duplicate_images.append(image)

        # plot_duplicates(image_dir='/home/ntlpt-52/work/IDP/Auto_Label/Trade_Finance/Trade_Finance_Actual_Data/link_trade_finance/0_79',
        #         duplicate_map=duplicates,
        #         filename=key)

#-------------------------------------------------------------Logging-------------------------------------------------------------------------------------------------
todays_date = moment.unix(time.time(), utc=True).locale('Asia/Kolkata').format("YYYY-MM-DD_HH-mm-ss")
logs_directory= "/home/ntlpt-52/work/IDP/Auto_Label/Trade_Finance/Experiment_logs/Covering_Schedule_Cleaned"
if os.path.isdir(logs_directory):
    lst = os.listdir(logs_directory)
    number_files = len(lst)
else :
    os.makedirs(logs_directory)
    number_files=0
log_file_name="{}_{}_{}_{}".format(image_directory.split("/")[-1],"Phash",todays_date,number_files+1)
log_file_path=os.path.join(logs_directory,log_file_name)
set_basic_config_for_logging(log_file_path)
logger=get_logger_object_and_setting_the_loglevel()
logger.info("Number of images in directory = "+str(len(os.listdir(image_directory))))
logger.info('Duplicates = '+json.dumps(duplicates))
logger.info("Unique Images = "+str(unique_images))
logger.info("Length of Unique Images = "+str(len(unique_images)))
logger.info("Length of Unique Images without repetition = "+str(len(set(unique_images))))
logger.info("Duplicate Images = "+str(duplicate_images))
logger.info("Length of Duplicate Images = "+str(len(duplicate_images)))
logger.info("Length of Duplicate Images without repetition = "+str(len(set(duplicate_images))))
logger.info("Same duplicates in more than One Images : "+json.dumps(SameDuplicatesInMoreThanOneImage))
logger.debug("-----------------------------------------------------")
logger.debug("/n/n")