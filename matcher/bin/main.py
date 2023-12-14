import argparse
from matcher.utils.parse_tsv import TsvIterator
from matcher.eval.eval import evaluate
import time

import multiprocessing

start_time = time.time()

# Logging Information
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')

file_handler = logging.FileHandler('main.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def process_chunk(chunk):
    tsv_iterator = TsvIterator(*chunk)
    results = []
    for comparison in tsv_iterator:
        # Add your processing logic for each comparison here
        results.append(comparison)
    return results

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

    #Output file with prediction
    tsv_iterator = TsvIterator(args.indir, args.outdir, args.method, args.threshold)

    ####################3
    chunk_size = 10000  # Adjust the chunk size as needed
    chunks = [(args.indir, args.outdir, args.method, args.threshold)] * chunk_size



    # Iterate through the file, and Comparison objects will be written to the output file
    index = 1
    logger.info("Iteration started")



    ######################
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())  # Adjust the number of processes as needed
    results = pool.map(process_chunk, chunks)

    pool.close()
    pool.join()


    # for comparison in tsv_iterator:
    #     if index % 10000 == 0:
    #         logger.info(f"Scoring {index} name pairs completed.")
    #     index += 1
    #     pass
    # logger.info(f"Completed with {index} iterations")



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

# python main.py -f ../../data/names.tsv -o ../../data/output_Exact.tsv -s Exact -t 0.5 -p Y -e Y -m f1
# python main.py -f ../../data/names.tsv -o ../../data/output_Jaccard.tsv -s Jaccard -t 0.5 -p Y -e Y -m f1
# python main.py -f ../../data/names.tsv -o ../../data/output_Leven.tsv -s Leven -t 0.5 -p Y -e Y -m f1
# python main.py -f ../../data/names.tsv -o ../../data/output_tfidf.tsv -s tfidf -t 0.5 -p Y -e Y -m f1
# python main.py -f ../../data/names.tsv -o ../../data/output_Bonus.tsv -s Bonus -t 0.5 -p Y -e Y -m f1


