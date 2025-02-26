from Images_DeDuplication import Deduplicate
import argparse


if __name__ == "__main__":

    _parser = argparse.ArgumentParser()
    _parser.add_argument(
        "-img",
        "--image_dir",
        type=str,
        help="Directory containing images",
        default='/home/ntlpt-52/work/IDP/Auto_Label/Trade_Finance/Images_To_DEDUP/Test_Image_Set/'
    )
    _parser.add_argument(
        "-hash",
        "--hash_method",
        type=str,
        help="Hash Method to use ['PHash','DHash','AHash','WHash','CNN']",
        default='PHash'
    )
    _parser.add_argument(
        "-thresh",
        "--max_difference_threshold",
        type=str,
        help="Hamming distance between two images below which retrieved duplicates are valid.",
        default=10
    )
    _parser.add_argument(
        "-om",
        "--output_method",
        type=str,
        help="['Save_Only_Uniques','Save_Uniques_and_Duplicates','Save_Uniques_and_Bucketed_Duplicates']",
        default='Save_Only_Uniques'
    )
    _parser.add_argument(
        '-od',
        "--output_dir",
        type=str,
        help="Directory to save output",
        default=''
    )
    _parser.add_argument(
        '-hmd',
        "--handle_multiple_duplicates",
        type=str,
        help="True or False",
        default='False'
    )

    args = _parser.parse_args()

    config = {
            "Input_Images_Dir":args.image_dir,
            "Hash_Method":args.hash_method,
            "Max_Difference_Threshold":args.max_difference_threshold,
            "Output_Option":args.output_method,
            "Output_Dir":args.output_dir,
            "Handle_Multiple_Duplicates":args.handle_multiple_duplicates
    }

    count,duplicates_per_unique_image = Deduplicate.perform_operation(config)

    print(count)
    print(duplicates_per_unique_image)
