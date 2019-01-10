from django.db.models import Count
import numpy as np
import pandas as pd

from ratings.models import Game, Player, Rating
from utils.constants import (
    MAX_RATING_VALUE,
    MIN_RATING_VALUE,
)
from training.keras.utils.constants import (
    MIN_RATINGS_FOR_TRAINING,
)
from training.models import TrainedOnGame, TrainedOnPlayer

def _filter_by_sufficient_no_ratings(df):
    def _filter(key):
        counts = df[key].value_counts()
        ids = set(counts[counts >= MIN_RATINGS_FOR_TRAINING].index)
        return df[df[key].isin(ids)]
    df = _filter('player_id')
    df = _filter('game_id')
    return df.reset_index(drop=True)


def _to_trained_on(df, key, ModelClass, rebuild):
    ids = pd.Series(df[key].unique())
    if rebuild:
        ModelClass.objects.all().delete()
        trained_on = []
        for i, id_ in enumerate(ids):
            kwds = {'id_in_model': i, key: id_}
            trained_on.append(ModelClass(**kwds))
        ModelClass.objects.bulk_create(trained_on)
        id_to_model_indice = pd.Series(ids.index, index=ids)
    else:
        kwds = {'{}__in'.format(key): ids}
        trained_on = ModelClass.objects.all().filter(**kwds)
        trained_on_df = pd.DataFrame.from_records(trained_on.values())
        id_to_model_indice = pd.Series(
            list(trained_on_df.id_in_model), index=trained_on_df[key]
        )

    df.loc[:, key] = df[key].map(id_to_model_indice)
    df = df.dropna()
    return df


def load_dataset():
    qs = Rating.objects.all()
    df = pd.DataFrame.from_records(qs.values()).dropna()
    df = _filter_by_sufficient_no_ratings(df)
    return df


def to_keras_model_indices(df, rebuild_indices=False):
    df = _to_trained_on(df, 'game_id', TrainedOnGame, rebuild=rebuild_indices)
    df = _to_trained_on(df, 'player_id', TrainedOnPlayer, rebuild=rebuild_indices)
    return df
