import os
from termcolor import colored
from torch.utils.data import Dataset
import torch
from PIL import Image
import json 
from transformers import LayoutLMv2Processor
from itertools import chain
from torch.utils.data import DataLoader
from tqdm import tqdm
import glob
import pandas
from Stratified_Split import StratifiedSplit

class PackingList_Dataset(Dataset):
    def __init__(self,image_directory,list_of_images,words=None,boxes=None,labels=None,processor=None,max_length=512,label2id=None):
        """
		Args:
			image_dir (string): Directory with all the document images.
			processor (LayoutLMv2Processor): Processor to prepare the text + image.
            words : list of list of tokens
            boxes : list of list of bounding boxes respective of each token
            labels : list of list of all labels
		"""
        self.image_dir = image_directory
        self.image_file_names = list_of_images
        self.processor = processor
        self.words=words
        self.boxes=boxes
        self.labels=labels
        self.label2id=label2id
	
    def __len__(self):
        return len(self.image_file_names)
    
    def __getitem__(self,idx):

        # image = Image.open(os.path.join(self.image_dir,self.image_file_names[idx])).convert("RGB")


        # words=self.words[idx] 
        # boxes=self.boxes[idx]
        # labels=self.labels[idx]
    
        # assert len(words)==len(boxes)==len(labels)

        
        # word_labels=[self.label2id[label] for label in labels]

        # print(colored(f"words are: {words}", "green"))
        # print(colored(f"label/home/ntlpt-52/work/IDP/Dataset_code/Master_Datas are: {labels}", "green"))
        # print(colored(f"boxes are: {boxes}", "green"))

        # assert len(words) == len(boxes) == len(word_labels)

        # # use processor to prepare everything
        # encoded_inputs = self.processor(image, words, boxes=boxes, word_labels=word_labels,
        #                                 padding="max_length", truncation=True,
        #                                 return_tensors="pt")

        # # remove batch dimension
        # for k, v in encoded_inputs.items():
        #     encoded_inputs[k] = v.squeeze()

        # assert encoded_inputs.input_ids.shape == torch.Size([512])
        # assert encoded_inputs.attention_mask.shape == torch.Size([512])
        # assert encoded_inputs.token_type_ids.shape == torch.Size([512])
        # assert encoded_inputs.bbox.shape == torch.Size([512, 4])
        # assert encoded_inputs.image.shape == torch.Size([3, 224, 224])
        # assert encoded_inputs.labels.shape == torch.Size([512])

        # return encoded_inputs
        return self.image_file_names[idx]
    
if __name__ == '__main__':
    image_directory = "/home/ntlpt-52/work/IDP/Dataset_code/Master_Data"
    images_layoutLabels= pandas.read_csv("/home/ntlpt-52/work/IDP/Dataset_code/ImagesAndLayoutLabels.csv")
    packing_list_data = PackingList_Dataset(image_directory=image_directory,list_of_images=images_layoutLabels["images"],labels=images_layoutLabels["layout_labels"])
    split_object= StratifiedSplit(packing_list_data,images_layoutLabels["layout_labels"])
    # train_data, train_labels, test_data, _ = split_object.test_stratified_split(testfraction=0.2, random_state=1)
    train_data, train_labels, eval_data,eval_labels, test_data, _ = split_object.test_eval_stratified_split(testfraction=0.2,evalfraction=0.3,random_state=1)
    # print("TestData-------------",test_data.__len__())
    # print("evaldata--------------",eval_data.__len__())
    # print("evalLabels-----------",eval_labels)
    # print("traindata---------------",train_data.__len__())
    # print("trainlabels------------",train_labels)