"""This module provides different metric functions. A metric can be defined by a keyword (str) or a callable. If it is a keyword it has to be available in ``tensorflow.keras`` or in ``deephyper.netrics``. The loss functions availble in ``deephyper.metrics`` are:
* Sparse Perplexity: ``sparse_perplexity``
* R2: ``r2``
* AUC ROC: ``auroc``
* AUC Precision-Recall: ``aucpr``
"""
from collections import OrderedDict

import tensorflow as tf
from deephyper.search import util

def r2(y_true, y_pred):
    SS_res = tf.keras.backend.sum(tf.keras.backend.square(y_true - y_pred), axis=0)
    SS_tot = tf.keras.backend.sum(
        tf.keras.backend.square(y_true - tf.keras.backend.mean(y_true, axis=0)), axis=0
    )
    output_scores = 1 - SS_res / (SS_tot + tf.keras.backend.epsilon())
    r2 = tf.keras.backend.mean(output_scores)
    return r2


def mae(y_true, y_pred):
    return tf.keras.metrics.mean_absolute_error(y_true, y_pred)

def mse(y_true, y_pred):
    return tf.keras.metrics.mean_squared_error(y_true, y_pred)

def acc(y_true, y_pred):
    return tf.keras.metrics.categorical_accuracy(y_true, y_pred)


def sparse_perplexity(y_true, y_pred):
    cross_entropy = tf.keras.losses.sparse_categorical_crossentropy(y_true, y_pred)
    perplexity = tf.pow(2.0, cross_entropy)
    return perplexity

metrics_func = OrderedDict()
metrics_func["mean_absolute_error"] = metrics_func["mae"] = mae
metrics_func["r2"] = r2
metrics_func["mean_squared_error"] = metrics_func["mse"] = mse
metrics_func["accuracy"] = metrics_func["acc"] = acc
metrics_func["sparse_perplexity"] = sparse_perplexity

metrics_obj = OrderedDict()
metrics_obj["auroc"] = lambda : tf.keras.metrics.AUC(name="auroc", curve="ROC")
metrics_obj["aucpr"] = lambda : tf.keras.metrics.AUC(name="aucpr", curve="PR")


def selectMetric(name: str):
    """Return the metric defined by name.

    Args:
        name (str): a string referenced in DeepHyper, one referenced in keras or an attribute name to import.

    Returns:
        str or callable: a string suppossing it is referenced in the keras framework or a callable taking (y_true, y_pred) as inputs and returning a tensor.
    """
    if metrics_func.get(name) == None and metrics_obj.get(name) == None:
        try:
            return util.load_attr_from(name)
        except:
            return name  # supposing it is referenced in keras metrics
    else:
        if name in metrics_func:
            return metrics_func[name]
        else:
            return metrics_obj[name]()