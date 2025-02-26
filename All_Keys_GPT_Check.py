directory='/home/ntlpt-52/work/IDP/Auto_Label/Trade_Finance/100_samples_data'

import json
from OCR_GPT import *
import jellyfish
import pandas as pd
import itertools
from logging_file import *
import os
import moment
import time
import glob

def GetLabelsFromFile(labels_file_path):
    with open(labels_file_path,'r') as f:
        labels_values=json.loads(f.read())
    f.close()
    if 'country_of_origin_origin_of_goods' in labels_values.keys():
        labels_values['country_of_origin_of_goods']=labels_values["country_of_origin_origin_of_goods"]
        del labels_values["country_of_origin_origin_of_goods"]
    if "payment_terms_terms_of_delivery_&_payment" in labels_values.keys():
        labels_values['payment_terms_of_delivery_&_payment']=labels_values["payment_terms_terms_of_delivery_&_payment"]
        del labels_values["payment_terms_terms_of_delivery_&_payment"]
    return labels_values

def convertGPTResponseToDict(response):
    response=response.splitlines()
    response=[ prediction for prediction in response if prediction.strip()]
    response_as_dictionary={}
    flag = True
    try:
        for prediction in response:
            prediction=prediction.split(":")
            key = prediction[0].strip().lower().replace(" ","_")
            value = prediction[1].strip()
            if not value:
               value="N/A" 
            response_as_dictionary[key]=value
        return response_as_dictionary
    except:
        return ""
    
def MatchGPTKeyswithLabels(response_dictionary,labels_values,file_name):
    keys_labels_matching_score={"Key":[],"PredictedValueFromGPT":[],"ValueGivenInFile":[],"levenshtein_distance":[]}
    correct_values_count=0
    keys_not_in_label_file=0
    threshold=5
    for key in response_dictionary.keys():
        keys_labels_matching_score["Key"].append(key)
        gpt_value= response_dictionary[key].lower()
        keys_labels_matching_score["PredictedValueFromGPT"].append(gpt_value)
        if key not in labels_values.keys():
            keys_labels_matching_score["ValueGivenInFile"].append("N/A")
            keys_labels_matching_score["levenshtein_distance"].append("N/A")
            keys_not_in_label_file+=1
        else: 
            given_value=labels_values[key][0][0].lower()
            keys_labels_matching_score["ValueGivenInFile"].append(given_value)
            leven_dist=jellyfish.levenshtein_distance(gpt_value,given_value)
            if leven_dist<=threshold:
                correct_values_count+= 1
            keys_labels_matching_score["levenshtein_distance"].append(leven_dist)

    print(keys_labels_matching_score)
    df = pd.DataFrame(data=keys_labels_matching_score)
    csv_file_directory="/home/ntlpt-52/work/IDP/Auto_Label/Trade_Finance/100_Samples_Key_Labels_Distance_Score/"+file_name+".csv"
    if not os.path.isdir("/home/ntlpt-52/work/IDP/Auto_Label/Trade_Finance/100_Samples_Key_Labels_Distance_Score"):
        os.mkdir("/home/ntlpt-52/work/IDP/Auto_Label/Trade_Finance/100_Samples_Key_Labels_Distance_Score")
    df.to_csv(csv_file_directory)  
    return correct_values_count,keys_not_in_label_file,df

if __name__ == "__main__":
    directory= "/home/ntlpt-52/work/IDP/Auto_Label/Trade_Finance/100_samples_data/"
    #-----------------------------------checking all the labels available----------------------------------------------------------------------------
    all_labels_file="/home/ntlpt-52/work/IDP/Auto_Label/Trade_Finance/Trade_Finance_Actual_Data/classes.txt"
    with open(all_labels_file,'r') as f:
        lines=f.read()
    f.close()
    lines=lines.splitlines()
    all_labels=[]
    for line in lines:
        if line=='country_of_origin_origin_of_goods':
            line="country_of_origin_of_goods"
        elif line=="payment_terms_terms_of_delivery_&_payment":
            line="payment_terms_of_delivery_&_payment"
        all_labels.append(line.replace("_"," "))
    # print(all_labels)
    label_query= ", ".join(all_labels)
    #------------------------------------------------------------------------------------------------------------------------------------------------

    metrics_dict={"ImagePath":[],"Number of keys predicted by GPT":[],"Number of keys predicted not in Label File":[],"Number of keys accurately predicted":[],"Accuracy- CoorectlyPredicted/Available Keys":[],"levenshtein_distance_median":[],"levenshtein_distance_90th_percentile":[]}
    index=0

    #-----------------------------------------------------------logs_directory----SetLoggingSettings--------------------------------------------------------------------------
    todays_date = moment.unix(time.time(), utc=True).locale('Asia/Kolkata').format("YYYY-MM-DD_HH-mm-ss")
    logs_directory= "/home/ntlpt-52/work/IDP/Auto_Label/Trade_Finance/Experiment_logs/100_samples_data_logs/"
    if os.path.isdir(logs_directory):
        lst = os.listdir(logs_directory)
        number_files = len(lst)
    else :
        os.makedirs(logs_directory)
        number_files=0
    log_file_name="{}_{}".format(todays_date,number_files+1)
    log_file_path=os.path.join(logs_directory,log_file_name)
    set_basic_config_for_logging(log_file_path)
    logger=get_logger_object_and_setting_the_loglevel()
    #----------------------------------------------------------------Iterating all images-------------------------------------------------------------------------
    for image_file_path in glob.glob(directory+"*.png"):
        print(image_file_path)
        label_file_path=image_file_path.split(".")[0]+"_labels.txt"
        image_file_name=image_file_path.split("/")[-1].split(".")[0]
        labels_values = GetLabelsFromFile(label_file_path)
       
        # print(label_query)
        text_from_ocr=OCR_Text_Extraction(image_file_path)
        # print(text_from_ocr)
        try:
            response_from_GPT=GPT_Key_Value_Pair_Extraction(label_query,text_from_ocr)
        except:
            break
        print(response_from_GPT)
        #---------------------------------------------------------Logging-------------------------------------------------------------------------------------------
        logger.info("Indexxx - "+str(index))
        logger.info('Image Path= '+image_file_path)
        logger.info("ouput from OCR = "+ text_from_ocr)
        logger.debug("output from OpenAI = "+response_from_GPT)
        logger.debug("-----------------------------------------------------")
        logger.debug("/n/n")
        #------------------------------------------------------------------Logging Done--------------------------------------------------------------------------
        dict_var = convertGPTResponseToDict(response_from_GPT)
        if not dict_var:
            index+=1
            continue
        print(dict_var)
        correct_values_count,keys_not_in_label_file,key_label_dataframe=MatchGPTKeyswithLabels(dict_var,labels_values,image_file_name)
    #--------------------------------------------------------------Metrics CSV----------------------------------------------------------------------------------
        metrics_dict["ImagePath"].append(image_file_name)
        metrics_dict["Number of keys predicted by GPT"].append(len(dict_var.keys()))
        metrics_dict["Number of keys predicted not in Label File"].append(keys_not_in_label_file)
        metrics_dict["Number of keys accurately predicted"].append(correct_values_count)
        metrics_dict["Accuracy- CoorectlyPredicted/Available Keys"].append(correct_values_count/(len(dict_var.keys())-keys_not_in_label_file)*100)
        metrics_dict["levenshtein_distance_median"].append(key_label_dataframe[key_label_dataframe['levenshtein_distance']!="N/A"]['levenshtein_distance'].median())
        metrics_dict["levenshtein_distance_90th_percentile"].append(key_label_dataframe[key_label_dataframe['levenshtein_distance']!="N/A"]['levenshtein_distance'].quantile(0.9))

        index+=1
            
    metrics_dataframe=pd.DataFrame(metrics_dict)
    logger.info("-----------------------------------------Total Metrics---------------------------------------------")
    logger.info("Total Accuracy Average= "+str(metrics_dataframe["Accuracy- CoorectlyPredicted/Available Keys"].mean()))
    logger.info("Total Levenshtein Distance Median= "+str(metrics_dataframe["levenshtein_distance_median"].median()))
    logger.info("---------------------------------------------------------------------------------------------------")
    metrics_dataframe.to_csv("/home/ntlpt-52/work/IDP/Auto_Label/Trade_Finance/100_Sample_Metrics.csv") 


