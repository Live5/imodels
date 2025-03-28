from typing import List

from sklearn.base import ClassifierMixin, RegressorMixin

from imodels.rule_set.rule_fit import RuleFit
from imodels.util.convert import itemsets_to_rules
from imodels.util.extract import extract_fpgrowth


class FPLasso(RuleFit):

    def __init__(self,
                 minsupport=0.1,
                 maxcardinality=2,
                 disc_strategy='mdlp',
                 disc_kwargs={},
                 verbose=False,
                 n_estimators=100,
                 tree_size=4,
                 sample_fract='default',
                 max_rules=2000,
                 memory_par=0.01,
                 tree_generator=None,
                 lin_trim_quantile=0.025,
                 lin_standardise=True,
                 exp_rand_tree_size=True,
                 include_linear=True,
                 alpha=None,
                 random_state=None):
        super().__init__(n_estimators,
                         tree_size,
                         sample_fract,
                         max_rules,
                         memory_par,
                         tree_generator,
                         lin_trim_quantile,
                         lin_standardise,
                         exp_rand_tree_size,
                         include_linear,
                         alpha,
                         random_state)
        self.disc_strategy = disc_strategy
        self.disc_kwargs = disc_kwargs
        self.minsupport = minsupport
        self.maxcardinality = maxcardinality
        self.verbose = verbose

    def fit(self, X, y=None, feature_names=None, undiscretized_features=[]):
        self.undiscretized_features = undiscretized_features
        super().fit(X, y, feature_names=feature_names)
        return self

    def _extract_rules(self, X, y) -> List[str]:
        itemsets = extract_fpgrowth(X, y,
                                    feature_names=self.feature_placeholders,
                                    minsupport=self.minsupport,
                                    maxcardinality=self.maxcardinality,
                                    undiscretized_features=self.undiscretized_features,
                                    disc_strategy=self.disc_strategy,
                                    disc_kwargs=self.disc_kwargs,
                                    verbose=self.verbose)[0]
        return itemsets_to_rules(itemsets)


class FPLassoRegressor(FPLasso, RegressorMixin):
    def _init_prediction_task(self):
        self.prediction_task = 'regression'


class FPLassoClassifier(FPLasso, ClassifierMixin):
    def _init_prediction_task(self):
        self.prediction_task = 'classification'
