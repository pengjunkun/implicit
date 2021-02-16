"""
An example based off the MovieLens 20M dataset.

This code will automatically download a HDF5 version of this
dataset when first run. The original dataset can be found here:
https://grouplens.org/datasets/movielens/.

Since this dataset contains explicit 5-star ratings, the ratings are
filtered down to positive reviews (4+ stars) to construct an implicit
dataset
"""

import argparse
import codecs
import logging
import time

import iqiyidata
import numpy as np
import tqdm

from implicit.als import AlternatingLeastSquares
from implicit.bpr import BayesianPersonalizedRanking
from implicit.datasets.movielens import get_movielens
from implicit.datasets.movielens import get_iqiyiData
from implicit.lmf import LogisticMatrixFactorization
from implicit.nearest_neighbours import (
    BM25Recommender,
    CosineRecommender,
    TFIDFRecommender,
    bm25_weight,
)

# config
LENGTH=10000
THRESHOLD=0.5

log = logging.getLogger("implicit")


# the main function of the demo
def calculate_similar_movies(output_filename, model_name="als",variant="1h"):
    # read in the input data file
    start = time.time()
    # titles, ratings = get_iqiyiData(variant)

    requests=iqiyidata.getData(variant)


    log.info("read data file in %s", time.time() - start)

    # generate a recommender model based off the input params
    if model_name == "als":
        model = AlternatingLeastSquares()

        # lets weight these models by bm25weight.
        log.debug("weighting matrix by bm25_weight")
        requests = (bm25_weight(requests, B=0.9) * 5).tocsr()

    elif model_name == "bpr":
        model = BayesianPersonalizedRanking()

    elif model_name == "lmf":
        model = LogisticMatrixFactorization()

    elif model_name == "tfidf":
        model = TFIDFRecommender()

    elif model_name == "cosine":
        model = CosineRecommender()

    elif model_name == "bm25":
        model = BM25Recommender(B=0.2)

    else:
        raise NotImplementedError("TODO: model %s" % model_name)

    # train the model
    log.debug("training model %s", model_name)
    start = time.time()
    model.fit(requests)
    log.debug("trained model '%s' in %s", model_name, time.time() - start)
    log.debug("calculating top movies")

    # the number of rating for one video
    user_count = np.ediff1d(requests.indptr)
    # sort the video from most popular to not popular
    to_generate = sorted(np.arange(requests.shape[0]), key=lambda x: -user_count[x])

    log.debug("calculating similar movies")
    with tqdm.tqdm(total=len(to_generate)) as progress:
        with codecs.open(output_filename, "w", "utf8") as o:
            for movieid in to_generate:
                # if this movie has no ratings, skip over (for instance 'Graffiti Bridge' has
                # no ratings > 4 meaning we've filtered out all data for it.
                if requests.indptr[movieid] != requests.indptr[movieid + 1]:
                    me = movieid
                    a=model.similar_items(movieid, LENGTH)
                    for other, score in a:
                        if score<THRESHOLD:
                            break
                        o.write("%s\t%s\t%s\n" % (me,other, "{:.3%}".format(score)))
                progress.update(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generates related items from the iqiyi traces",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--output",
        type=str,
        default="D:\\iqiyi_cluster.tsv",
        dest="outputfile",
        help="output file name",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="als",
        dest="model",
        help="model to calculate (als/bm25/tfidf/cosine)",
    )
    parser.add_argument(
        "--variant",
        type=str,
        default="24h",
        dest="variant",
        #could use test
        help="'1h', '3h','8h','24h'",
    )
    parser.add_argument(
        "--min_rating",
        type=float,
        default=4.0,
        dest="min_rating",
        help="Minimum rating to assume that a rating is positive",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    calculate_similar_movies(
        args.outputfile, model_name=args.model,
        # variant=args.variant
        variant=args.variant
    )
