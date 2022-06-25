import unittest
from datetime import datetime
from statistics import mean
from typing import Dict

from src.features.FeatureSelector import FeatureSelector
from src.biosignals.Timeseries import Timeseries


class FeatureSelectorTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.initial = datetime(2000, 1, 1, 0, 0, 0)
        cls.sf = 1
        cls.n_features = 3

        cls.samples = [ [0.2, 0.4, 0.6, 0.4, 0.2, 0.4, 0.1, 0.15],
                        [0.7, 0.1, 0.8, 0.9, 0.3, 0.6, 0.3, 0.91],
                        [0.3, 0.75, 0.8, 0.92, 0.4, 0.1, 0.3, 1.] ]

        cls.avg = [mean(cls.samples[0]), mean(cls.samples[1]), mean(cls.samples[2])]

        cls.features = {}
        cls.feature_names = ('mean', 'variance', 'deviation')
        for i in range(cls.n_features):
            f = Timeseries([Timeseries.Segment(cls.samples[i], cls.initial, cls.sf), ], True, cls.sf)
            cls.features[cls.feature_names[i]] = f


    def test_select_based_on_average_being_higher_than(self):

        def selection_function(segment: Timeseries.Segment) -> bool:
            if mean(segment.samples) > 0.5:
                print('keep')
                return True  # A selection function should evaluate some criteria and return True if the feature is to be kept.

        extractor = FeatureSelector(selection_function, name='My third pipeline unit!')
        selected_features = extractor.apply(self.features)
        print(self.avg)

        self.assertIsInstance(selected_features, Dict)
        self.assertEqual(len(selected_features), 2)
        self.assertTrue('variance' in selected_features)
        self.assertTrue('deviation' in selected_features)
        self.assertEqual(selected_features['variance'].segments[0].samples, self.samples[1])
        self.assertEqual(selected_features['deviation'].segments[0].samples, self.samples[2])



if __name__ == '__main__':
    unittest.main()