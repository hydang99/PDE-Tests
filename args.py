import argparse

def argument_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # ***************************************************
    # Rename file images
    # ***************************************************
    parser.add_argument('--rename_src','-rs', type=str,default='datasets/dataset_before/',
                        help="Source directory to rename")
    parser.add_argument('--dest_org','-do', type=str,default='datasets/images/',
                        help = "Destination directory for original image")
    parser.add_argument('--dest_label','-dl', type=str,default='datasets/labels_unconverted/',
                        help = "Destination directory for unconverted image")
    parser.add_argument('--dest_converted','-dc', type=str,default='datasets/mask_gt_converted/',
                        help = "Destination directory for converted image")
    return parser
def dataset_rename(parsed_args):
    """Build for rename_dataset.py from the parsed command-line arguments"""
    return {
        'rename_src': parsed_args.rename_src,
        'dest_org': parsed_args.dest_org,
        'dest_label': parsed_args.dest_label,
    }
def dataset_convert(parsed_args):
    return{
        'src_label':parsed_args.dest_label,
        'dir_dest': parsed_args.dest_converted

    }