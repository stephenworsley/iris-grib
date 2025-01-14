# Copyright iris-grib contributors
#
# This file is part of iris-grib and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""
Test function
:func:`iris_grib._load_convert.product_definition_template_6`.

"""

# import iris_grib.tests first so that some things can be initialised
# before importing anything else.
import iris_grib.tests as tests

from copy import deepcopy
from unittest import mock

from iris.coords import DimCoord

from iris_grib._load_convert import product_definition_template_6


class Test(tests.IrisGribTest):
    def setUp(self):
        def func(s, m, f):
            return m['cell_methods'].append(self.cell_method)

        module = 'iris_grib._load_convert'
        self.patch('warnings.warn')
        this = '{}.product_definition_template_0'.format(module)
        self.cell_method = mock.sentinel.cell_method
        self.patch(this, side_effect=func)
        self.metadata = {'factories': [], 'references': [],
                         'standard_name': None,
                         'long_name': None, 'units': None, 'attributes': {},
                         'cell_methods': [], 'dim_coords_and_dims': [],
                         'aux_coords_and_dims': []}

    def _check(self, request_warning):
        this = 'iris_grib._load_convert.options'
        with mock.patch(this, warn_on_unsupported=request_warning):
            metadata = deepcopy(self.metadata)
            percentile = 50
            section = {'percentileValue': percentile}
            forecast_reference_time = mock.sentinel.forecast_reference_time
            # The called being tested.
            product_definition_template_6(section, metadata,
                                          forecast_reference_time)
            expected = deepcopy(self.metadata)
            expected['cell_methods'].append(self.cell_method)
            percentile = DimCoord(percentile,
                                  long_name='percentile',
                                  units='%')
            expected['aux_coords_and_dims'].append((percentile, None))
            self.assertEqual(metadata, expected)

    def test_pdt_no_warn(self):
        self._check(False)

    def test_pdt_warn(self):
        self._check(True)


if __name__ == '__main__':
    tests.main()
