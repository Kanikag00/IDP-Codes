import json
import shutil
from imagededup.methods import CNN,WHash,AHash,PHash,DHash
import os
from collections import defaultdict
from operator import itemgetter


class Deduplicate:

    def get_hashing_object(hash_method : str):
        if hash_method == "CNN":
            return CNN()
        elif hash_method =="WHash":
            return WHash()
        elif hash_method=="AHash" : 
            return AHash()
        elif hash_method== "PHash" : 
            return PHash()
        elif hash_method=="DHash" : 
            return DHash()

    def save_unique_and_duplicates(uniques : list,duplicates : list ,source_dir : str,output_dir : str, only_uniques : bool) -> None:
        unique_output_dir = os.path.join(output_dir,"Unique_Images")
        os.makedirs(unique_output_dir,exist_ok=True)
        for unq_img in uniques:
            shutil.copy(os.path.join(source_dir,unq_img),os.path.join(unique_output_dir,unq_img))
        if only_uniques:
            return 
        duplicate_output_dir = os.path.join(output_dir,"Duplicate_Images")
        os.makedirs(duplicate_output_dir,exist_ok=True)
        for dup_img in duplicates:
            shutil.copy(os.path.join(source_dir,dup_img),os.path.join(duplicate_output_dir,dup_img))
        
    def save_unique_and_bucketed_duplicates(uniques : list ,duplicates_per_image : dict, source_dir : str,output_dir : str) -> None:
        unique_output_dir = os.path.join(output_dir,"Unique_Images")
        os.makedirs(unique_output_dir,exist_ok=True)
        dup_images = []
        for unq_img in uniques:
            shutil.copy(os.path.join(source_dir,unq_img),os.path.join(unique_output_dir,unq_img))
            duplicate_output_dir = os.path.join(output_dir,"Duplicate_Images",unq_img.replace(".png","")+"_"+str(len(duplicates_per_image[unq_img])))
            os.makedirs(duplicate_output_dir,exist_ok=True)
            for dup in duplicates_per_image[unq_img]:
                shutil.copy(os.path.join(source_dir,dup),os.path.join(duplicate_output_dir,dup))
            
    def perform_hashing(hash_method : str ,image_source_dir : str ,threshold : int ,handle_multiple_duplicates: bool):
        hasher = Deduplicate.get_hashing_object(hash_method)
        encodings = hasher.encode_images(image_dir=image_source_dir)
        complete_duplicates_dict= hasher.find_duplicates(encoding_map=encodings , max_distance_threshold=threshold,scores=True)
        unique_images,duplicate_images,duplicates_for_unique_images = Deduplicate.find_unique_and_duplicates(complete_duplicates_dict,
                                                                                                             handle_multiple_duplicates)
        
        return unique_images,duplicate_images,duplicates_for_unique_images

    def find_unique_and_duplicates(complete_duplicates_dict : dict,handle_multiple_duplicates : list):
        unique_images=[]
        duplicate_images=[]
        duplicates_for_unique_images_dict = defaultdict(list)
        same_duplicate_for_multiple_images = []
        try:
            for img in complete_duplicates_dict:
                if img not in duplicate_images:
                    unique_images.append(img)
                    for dup in complete_duplicates_dict[img]:
                        # dup is a tuple (Image_Name, Hamming Distance in Hashes of Images)
                        if dup[0] in duplicate_images and dup[0] not in same_duplicate_for_multiple_images:
                            same_duplicate_for_multiple_images.append(dup[0])
                        duplicate_images.append(dup[0])
                        duplicates_for_unique_images_dict[img].append(dup[0])
        except:
            pass
        
        duplicate_images=set(duplicate_images)
        
        if handle_multiple_duplicates:
            duplicates_for_unique_images_dict = Deduplicate.remove_multiple_duplicates(complete_duplicates_dict,
                                                                                       duplicates_for_unique_images_dict,
                                                                                       same_duplicate_for_multiple_images,
                                                                                       unique_images)

        return unique_images,duplicate_images,duplicates_for_unique_images_dict
    
    def remove_multiple_duplicates(complete_duplicates_dict : dict, duplicates_for_unique_dict : dict, multiple_occuring_duplicates : list,unique_images_list : list) -> dict:
        
        for image in multiple_occuring_duplicates:
            try:                    
                unique_images_with_this_duplicate = [dup for dup in complete_duplicates_dict[image] if dup[0] in unique_images_list]
                #To get the name of image with minimum Hamming Distance between hashes
                
                min_distance_img = max(unique_images_with_this_duplicate,key=itemgetter(1))[0]  
                
                for unq in unique_images_with_this_duplicate:
                    if unq[0] != min_distance_img:
                        duplicates_for_unique_dict[unq[0]].remove(image)
            except : 
                pass
        
        return duplicates_for_unique_dict


    def perform_operation(json_data:dict):
        images_source_dir = json_data["Input_Images_Dir"]
        hash_method = json_data["Hash_Method"]
        threshold = eval(json_data["Max_Difference_Threshold"])
        saving_method = json_data['Output_Option']
        output_dir = json_data["Output_Dir"]
        handle_multiple_duplicates = eval(json_data["Handle_Multiple_Duplicates"])
        unique_images,duplicate_images,duplicates_for_unique_images = Deduplicate.perform_hashing(hash_method,
                                                                                                  images_source_dir,
                                                                                                  threshold,
                                                                                                  handle_multiple_duplicates)
        if saving_method == "Save_Only_Uniques":
            Deduplicate.save_unique_and_duplicates(unique_images,duplicate_images,images_source_dir,output_dir,only_uniques=True)
        elif saving_method == "Save_Uniques_and_Duplicates":
            Deduplicate.save_unique_and_duplicates(unique_images,duplicate_images,images_source_dir,output_dir,only_uniques=False)
        elif saving_method == "Save_Uniques_and_Bucketed_Duplicates" :
            Deduplicate.save_unique_and_bucketed_duplicates(unique_images,duplicates_for_unique_images,images_source_dir,output_dir)

        count = {
            'unique_images':len(unique_images),
            'duplicate_images':len(duplicate_images)
        }
        return count,duplicates_for_unique_images
        


