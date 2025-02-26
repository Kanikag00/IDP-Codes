import pytesseract
from PIL import Image
import openai

def OCR_Text_Extraction(image_path):
    text_portion = pytesseract.image_to_string(Image.open(image_path))
    return text_portion

def GPT_Key_Value_Pair_Extraction(labels_to_extract,text_portion):
    openai.api_key = ""
    first: str = "Extract "+labels_to_extract
    data: str = text_portion
    end: str = "All Extracted Details are :" 

    # print(f"{first}\n\n{data}\n\n{end}")

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{first}\n\n{data}\n\n{end}",
        temperature=0.2,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # print(print(response.choices[0]['text']))
    print(response)
    return response.choices[0]['text']





if __name__ == "__main__":
    # image_path: str = "/media/tarun/D1/IDP_poc/image2text/sample/Packing_List_39_page_1.png"
    image_path: str = "/home/ntlpt-52/work/IDP/Clusters/Images/19_141/IM-000000011378729-AP_page_1.png"

    text_portion = pytesseract.image_to_string(Image.open(image_path))
    print(text_portion)
    # exit("++++++++++++++")
    # kanika account
    openai.api_key = ""
    # first: str = "Extract Exporter Name, buyer name, consignee name, net weight in kgs, bin, total, IEC,
    # country of " \ "origin, state of origin, box size, quantity, description of goods, Fir #, part no:" data: str =
    # text_portion end: str = "exporter name, buyer name, consignee name, net weight in kgs, bin, total, IEC:,
    # country of origin, " \ "state of origin:, box size, quantity, description of goods, Fir #:, part no:"
    

    first: str = "Extract Billing details,Shipping details,Dates,Order Details,Invoice details,Items details,Total Amount,Quantity,Discounts,bank details etc  "
    data: str = text_portion
    end: str = "All Extracted Details are :" 

    print(f"{first}\n\n{data}\n\n{end}")

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{first}\n\n{data}\n\n{end}",
        temperature=0.2,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # print(print(response.choices[0]['text']))

    print(response)
