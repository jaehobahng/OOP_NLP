import argparse
from matcher.utils.parse_tsv import TsvIterator
from matcher.eval.eval import evaluate
import multiprocessing
import time

start_time = time.time()

# Logging Information
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')

file_handler = logging.FileHandler('main.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def process_comparison(comparison):
    # Your code for processing each comparison goes here
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Code to make corpus " "for assignment 4"
    )
    parser.add_argument("-f", "--indir", required=True, help="Input data directory")
    parser.add_argument("-o", "--outdir", required=True, help="Output data directory")
    parser.add_argument("-s", "--method", required=True, help="Scoring method")
    parser.add_argument("-t", "--threshold", required=True, help="Threshold")
    parser.add_argument("-p", "--pri", required=True, help="Print Y/N")

    parser.add_argument("-e", "--evalu", required=True, help="Evaluate Y/N")
    parser.add_argument("-m", "--evalmeth", required=True, help="Evaluation method")
    

    args = parser.parse_args()

    # Create a pool of worker processes
    # num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=5)

    #Output file with prediction
    tsv_iterator = TsvIterator(args.indir, args.outdir, args.method, args.threshold)

    # Use multiprocessing to parallelize the loop processing
    results = pool.map(process_comparison, tsv_iterator)

    import pandas as pd
    df = pd.read_csv(args.outdir, delimiter='\t',header=None, names=['PersonLabel','AliasLabel','Prediction','Score'])


    if args.pri == 'Y':
        print(df.head())
    elif args.pri == 'N':
        pass
    else:
        ValueError("Only 'Y' and 'N' values must be given as inputs")


    if args.evalu == 'Y':
        eval_score = evaluate(df.Prediction,args.evalmeth)
        print(args.evalmeth, '=', eval_score)
    elif args.evalu == 'N':
        pass
    else:
        ValueError("Only 'Y' and 'N' values must be given as inputs")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")

# python main_multi.py -f ../../data/names.tsv -o ../../data/output_Exact.tsv -s Exact -t 0.5 -p Y -e Y -m f1
# python main_multi.py -f ../../data/names.tsv -o ../../data/output_Jaccard.tsv -s Jaccard -t 0.5 -p Y -e Y -m f1
# python main.py -f ../../data/names.tsv -o ../../data/output_Leven.tsv -s Leven -t 0.5 -p Y -e Y -m f1
# python main.py -f ../../data/names.tsv -o ../../data/output_tfidf.tsv -s tfidf -t 0.5 -p Y -e Y -m f1
# python main_multi.py -f ../../data/names.tsv -o ../../data/output_Bonus.tsv -s Bonus -t 0.5 -p Y -e Y -m f1

"""
python main.py 
-f <path_to_dataset> 
-s <scoring_algorithm> 
-e <flag_whether_to_evaluate>
-p <flag_whether_to_print_results>

"""

