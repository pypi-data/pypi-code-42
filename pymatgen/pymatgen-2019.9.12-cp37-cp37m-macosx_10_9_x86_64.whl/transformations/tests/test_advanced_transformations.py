# coding: utf-8
# Copyright (c) Pymatgen Development Team.
# Distributed under the terms of the MIT License.

import unittest
import os
import json
import warnings
import numpy as np

from pymatgen import Lattice, Structure, Specie, Molecule
from pymatgen.transformations.standard_transformations import \
    OxidationStateDecorationTransformation, SubstitutionTransformation, \
    OrderDisorderedStructureTransformation, AutoOxiStateDecorationTransformation
from pymatgen.transformations.advanced_transformations import \
    SuperTransformation, EnumerateStructureTransformation, \
    MultipleSubstitutionTransformation, ChargeBalanceTransformation, \
    SubstitutionPredictorTransformation, MagOrderingTransformation, \
    DopingTransformation, _find_codopant, SlabTransformation, \
    MagOrderParameterConstraint, DisorderOrderedTransformation, \
    GrainBoundaryTransformation, CubicSupercellTransformation, \
    AddAdsorbateTransformation, SubstituteSurfaceSiteTransformation, \
    SQSTransformation

from monty.os.path import which
from pymatgen.io.vasp.inputs import Poscar
from pymatgen.io.cif import CifParser
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.analysis.energy_models import IsingModel
from pymatgen.analysis.gb.grain import GrainBoundaryGenerator
from pymatgen.util.testing import PymatgenTest
from pymatgen.core.surface import SlabGenerator
from pymatgen.io import atat

"""
Created on Jul 24, 2012
"""


__author__ = "Shyue Ping Ong"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"
__date__ = "Jul 24, 2012"


test_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                        'test_files')


def get_table():
    """
    Loads a lightweight lambda table for use in unit tests to reduce
    initialization time, and make unit tests insensitive to changes in the
    default lambda table.
    """
    data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                            'test_files', 'struct_predictor')
    json_file = os.path.join(data_dir, 'test_lambda.json')
    with open(json_file) as f:
        lambda_table = json.load(f)
    return lambda_table


enum_cmd = which('enum.x') or which('multienum.x')
makestr_cmd = which('makestr.x') or which('makeStr.x') or which('makeStr.py')
mcsqs_cmd = which('mcsqs')
enumlib_present = enum_cmd and makestr_cmd


class SuperTransformationTest(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter("ignore")

    def tearDown(self):
        warnings.simplefilter("default")

    def test_apply_transformation(self):
        tl = [SubstitutionTransformation({"Li+": "Na+"}),
              SubstitutionTransformation({"Li+": "K+"})]
        t = SuperTransformation(tl)
        coords = list()
        coords.append([0, 0, 0])
        coords.append([0.375, 0.375, 0.375])
        coords.append([.5, .5, .5])
        coords.append([0.875, 0.875, 0.875])
        coords.append([0.125, 0.125, 0.125])
        coords.append([0.25, 0.25, 0.25])
        coords.append([0.625, 0.625, 0.625])
        coords.append([0.75, 0.75, 0.75])

        lattice = Lattice([[3.8401979337, 0.00, 0.00],
                           [1.9200989668, 3.3257101909, 0.00],
                           [0.00, -2.2171384943, 3.1355090603]])
        struct = Structure(lattice, ["Li+", "Li+", "Li+", "Li+", "Li+", "Li+",
                                     "O2-", "O2-"], coords)
        s = t.apply_transformation(struct, return_ranked_list=True)

        for s_and_t in s:
            self.assertEqual(s_and_t['transformation']
                             .apply_transformation(struct),
                             s_and_t['structure'])

    @unittest.skipIf(not enumlib_present, "enum_lib not present.")
    def test_apply_transformation_mult(self):
        # Test returning multiple structures from each transformation.
        disord = Structure(np.eye(3) * 4.209, [{"Cs+": 0.5, "K+": 0.5}, "Cl-"],
                           [[0, 0, 0], [0.5, 0.5, 0.5]])
        disord.make_supercell([2, 2, 1])

        tl = [EnumerateStructureTransformation(),
              OrderDisorderedStructureTransformation()]
        t = SuperTransformation(tl, nstructures_per_trans=10)
        self.assertEqual(len(t.apply_transformation(disord,
                                                    return_ranked_list=20)), 8)
        t = SuperTransformation(tl)
        self.assertEqual(len(t.apply_transformation(disord,
                                                    return_ranked_list=20)), 2)


class MultipleSubstitutionTransformationTest(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter("ignore")

    def tearDown(self):
        warnings.simplefilter("default")

    def test_apply_transformation(self):
        sub_dict = {1: ["Na", "K"]}
        t = MultipleSubstitutionTransformation("Li+", 0.5, sub_dict, None)
        coords = list()
        coords.append([0, 0, 0])
        coords.append([0.75, 0.75, 0.75])
        coords.append([0.5, 0.5, 0.5])
        coords.append([0.25, 0.25, 0.25])
        lattice = Lattice([[3.8401979337, 0.00, 0.00],
                           [1.9200989668, 3.3257101909, 0.00],
                           [0.00, -2.2171384943, 3.1355090603]])
        struct = Structure(lattice, ["Li+", "Li+", "O2-", "O2-"], coords)
        self.assertEqual(len(t.apply_transformation(struct,
                                                    return_ranked_list=True)),
                         2)


class ChargeBalanceTransformationTest(unittest.TestCase):

    def test_apply_transformation(self):
        t = ChargeBalanceTransformation('Li+')
        coords = list()
        coords.append([0, 0, 0])
        coords.append([0.375, 0.375, 0.375])
        coords.append([.5, .5, .5])
        coords.append([0.875, 0.875, 0.875])
        coords.append([0.125, 0.125, 0.125])
        coords.append([0.25, 0.25, 0.25])
        coords.append([0.625, 0.625, 0.625])
        coords.append([0.75, 0.75, 0.75])

        lattice = Lattice([[3.8401979337, 0.00, 0.00],
                           [1.9200989668, 3.3257101909, 0.00],
                           [0.00, -2.2171384943, 3.1355090603]])
        struct = Structure(lattice, ["Li+", "Li+", "Li+", "Li+", "Li+", "Li+",
                                     "O2-", "O2-"], coords)
        s = t.apply_transformation(struct)

        self.assertAlmostEqual(s.charge, 0, 5)


@unittest.skipIf(not enumlib_present, "enum_lib not present.")
class EnumerateStructureTransformationTest(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter("ignore")

    def tearDown(self):
        warnings.simplefilter("default")

    def test_apply_transformation(self):
        enum_trans = EnumerateStructureTransformation(refine_structure=True)
        enum_trans2 = EnumerateStructureTransformation(refine_structure=True,
                                                      sort_criteria="nsites")
        p = Poscar.from_file(os.path.join(test_dir, 'POSCAR.LiFePO4'),
                             check_for_POTCAR=False)
        struct = p.structure
        expected_ans = [1, 3, 1]
        for i, frac in enumerate([0.25, 0.5, 0.75]):
            trans = SubstitutionTransformation({'Fe': {'Fe': frac}})
            s = trans.apply_transformation(struct)
            oxitrans = OxidationStateDecorationTransformation(
                {'Li': 1, 'Fe': 2, 'P': 5, 'O': -2})
            s = oxitrans.apply_transformation(s)
            alls = enum_trans.apply_transformation(s, 100)
            self.assertEqual(len(alls), expected_ans[i])
            self.assertIsInstance(trans.apply_transformation(s), Structure)
            for ss in alls:
                self.assertIn("energy", ss)
            alls = enum_trans2.apply_transformation(s, 100)
            self.assertEqual(len(alls), expected_ans[i])
            self.assertIsInstance(trans.apply_transformation(s), Structure)
            for ss in alls:
                self.assertIn("num_sites", ss)

        # make sure it works for non-oxidation state decorated structure
        trans = SubstitutionTransformation({'Fe': {'Fe': 0.5}})
        s = trans.apply_transformation(struct)
        alls = enum_trans.apply_transformation(s, 100)
        self.assertEqual(len(alls), 3)
        self.assertIsInstance(trans.apply_transformation(s), Structure)
        for s in alls:
            self.assertNotIn("energy", s)

    def test_max_disordered_sites(self):
        l = Lattice.cubic(4)
        s_orig = Structure(l, [{"Li": 0.2, "Na": 0.2, "K": 0.6}, {"O": 1}],
                           [[0, 0, 0], [0.5, 0.5, 0.5]])
        est = EnumerateStructureTransformation(max_cell_size=None,
                                               max_disordered_sites=5)
        dd = est.apply_transformation(s_orig, return_ranked_list=100)
        self.assertEqual(len(dd), 9)
        for d in dd:
            self.assertEqual(len(d["structure"]), 10)

    def test_to_from_dict(self):
        trans = EnumerateStructureTransformation()
        d = trans.as_dict()
        trans = EnumerateStructureTransformation.from_dict(d)
        self.assertEqual(trans.symm_prec, 0.1)


class SubstitutionPredictorTransformationTest(unittest.TestCase):
    def test_apply_transformation(self):
        t = SubstitutionPredictorTransformation(threshold=1e-3, alpha=-5,
                                                lambda_table=get_table())
        coords = list()
        coords.append([0, 0, 0])
        coords.append([0.75, 0.75, 0.75])
        coords.append([0.5, 0.5, 0.5])
        lattice = Lattice([[3.8401979337, 0.00, 0.00],
                           [1.9200989668, 3.3257101909, 0.00],
                           [0.00, -2.2171384943, 3.1355090603]])
        struct = Structure(lattice, ['O2-', 'Li1+', 'Li1+'], coords)

        outputs = t.apply_transformation(struct, return_ranked_list=True)
        self.assertEqual(len(outputs), 4, 'incorrect number of structures')

    def test_as_dict(self):
        t = SubstitutionPredictorTransformation(threshold=2, alpha=-2,
                                                lambda_table=get_table())
        d = t.as_dict()
        t = SubstitutionPredictorTransformation.from_dict(d)
        self.assertEqual(t.threshold, 2,
                         'incorrect threshold passed through dict')
        self.assertEqual(t._substitutor.p.alpha, -2,
                         'incorrect alpha passed through dict')


@unittest.skipIf(not enumlib_present, "enum_lib not present.")
class MagOrderingTransformationTest(PymatgenTest):

    def setUp(self):

        latt = Lattice.cubic(4.17)
        species = ["Ni", "O"]
        coords = [[0, 0, 0],
                  [0.5, 0.5, 0.5]]
        self.NiO = Structure.from_spacegroup(225, latt, species, coords)

        latt = Lattice([[2.085, 2.085, 0.0],
                        [0.0, -2.085, -2.085],
                        [-2.085, 2.085, -4.17]])
        species = ["Ni", "Ni", "O", "O"]
        coords = [[0.5, 0, 0.5],
                  [0, 0, 0],
                  [0.25, 0.5, 0.25],
                  [0.75, 0.5, 0.75]]
        self.NiO_AFM_111 = Structure(latt, species, coords)
        self.NiO_AFM_111.add_spin_by_site([-5, 5, 0, 0])

        latt = Lattice([[2.085, 2.085, 0],
                        [0, 0, -4.17],
                        [-2.085, 2.085, 0]])
        species = ["Ni", "Ni", "O", "O"]
        coords = [[0.5, 0.5, 0.5],
                  [0, 0, 0],
                  [0, 0.5, 0],
                  [0.5, 0, 0.5]]
        self.NiO_AFM_001 = Structure(latt, species, coords)
        self.NiO_AFM_001.add_spin_by_site([-5, 5, 0, 0])

        parser = CifParser(os.path.join(test_dir, 'Fe3O4.cif'))
        self.Fe3O4 = parser.get_structures()[0]
        trans = AutoOxiStateDecorationTransformation()
        self.Fe3O4_oxi = trans.apply_transformation(self.Fe3O4)

        parser = CifParser(os.path.join(test_dir, 'Li8Fe2NiCoO8.cif'))
        self.Li8Fe2NiCoO8 = parser.get_structures()[0]
        self.Li8Fe2NiCoO8.remove_oxidation_states()
        warnings.simplefilter("ignore")

    def tearDown(self):
        warnings.simplefilter("default")

    def test_apply_transformation(self):
        trans = MagOrderingTransformation({"Fe": 5})
        p = Poscar.from_file(os.path.join(test_dir, 'POSCAR.LiFePO4'),
                             check_for_POTCAR=False)
        s = p.structure
        alls = trans.apply_transformation(s, 10)
        self.assertEqual(len(alls), 3)
        f = SpacegroupAnalyzer(alls[0]["structure"], 0.1)
        self.assertEqual(f.get_space_group_number(), 31)

        model = IsingModel(5, 5)
        trans = MagOrderingTransformation({"Fe": 5},
                                          energy_model=model)
        alls2 = trans.apply_transformation(s, 10)
        # Ising model with +J penalizes similar neighbor magmom.
        self.assertNotEqual(alls[0]["structure"], alls2[0]["structure"])
        self.assertEqual(alls[0]["structure"], alls2[2]["structure"])

        s = self.get_structure('Li2O')
        # Li2O doesn't have magnetism of course, but this is to test the
        # enumeration.
        trans = MagOrderingTransformation({"Li+": 1}, max_cell_size=3)
        alls = trans.apply_transformation(s, 100)
        # TODO: check this is correct, unclear what len(alls) should be
        self.assertEqual(len(alls), 12)

        trans = MagOrderingTransformation({"Ni": 5})
        alls = trans.apply_transformation(self.NiO.get_primitive_structure(),
                                          return_ranked_list=10)
        self.assertEqual(self.NiO_AFM_111.lattice, alls[0]["structure"].lattice)
        self.assertEqual(self.NiO_AFM_001.lattice, alls[1]["structure"].lattice)

    def test_ferrimagnetic(self):
        trans = MagOrderingTransformation({"Fe": 5}, order_parameter=0.75,
                                          max_cell_size=1)
        p = Poscar.from_file(os.path.join(test_dir, 'POSCAR.LiFePO4'),
                             check_for_POTCAR=False)
        s = p.structure
        a = SpacegroupAnalyzer(s, 0.1)
        s = a.get_refined_structure()
        alls = trans.apply_transformation(s, 10)
        self.assertEqual(len(alls), 1)

    def test_as_from_dict(self):
        trans = MagOrderingTransformation({"Fe": 5}, order_parameter=0.75)
        d = trans.as_dict()
        # Check json encodability
        s = json.dumps(d)
        trans = MagOrderingTransformation.from_dict(d)
        self.assertEqual(trans.mag_species_spin, {"Fe": 5})
        from pymatgen.analysis.energy_models import SymmetryModel
        self.assertIsInstance(trans.energy_model, SymmetryModel)

    def test_zero_spin_case(self):
        # ensure that zero spin case maintains sites and formula
        s = self.get_structure('Li2O')
        trans = MagOrderingTransformation({"Li+": 0.0}, order_parameter=0.5)
        alls = trans.apply_transformation(s)
        Li_site = alls.indices_from_symbol('Li')[0]
        # Ensure s does not have a spin property
        self.assertFalse('spin' in s.sites[Li_site].specie._properties)
        # ensure sites are assigned a spin property in alls
        self.assertTrue('spin' in alls.sites[Li_site].specie._properties)
        self.assertEqual(alls.sites[Li_site].specie._properties['spin'], 0)

    def test_advanced_usage(self):

        # test spin on just one oxidation state
        magtypes = {"Fe2+": 5}
        trans = MagOrderingTransformation(magtypes)
        alls = trans.apply_transformation(self.Fe3O4_oxi)
        self.assertIsInstance(alls, Structure)
        self.assertEqual(str(alls[0].specie), "Fe2+,spin=5")
        self.assertEqual(str(alls[2].specie), "Fe3+")

        # test multiple order parameters
        # this should only order on Fe3+ site, but assign spin to both
        magtypes = {"Fe2+": 5, "Fe3+": 5}
        order_parameters = [
            MagOrderParameterConstraint(1, species_constraints="Fe2+"),
            MagOrderParameterConstraint(0.5, species_constraints="Fe3+")
        ]
        trans = MagOrderingTransformation(magtypes, order_parameter=order_parameters)
        alls = trans.apply_transformation(self.Fe3O4_oxi)
        # using this 'sorted' syntax because exact order of sites in first
        # returned structure varies between machines: we just want to ensure
        # that the order parameter is accurate
        self.assertEqual(sorted([str(alls[idx].specie) for idx in range(0,2)]),
                         sorted(["Fe2+,spin=5", "Fe2+,spin=5"]))
        self.assertEqual(sorted([str(alls[idx].specie) for idx in range(2, 6)]),
                         sorted(["Fe3+,spin=5", "Fe3+,spin=5",
                                 "Fe3+,spin=-5", "Fe3+,spin=-5"]))
        self.assertEqual(str(alls[0].specie), "Fe2+,spin=5")

        # this should give same results as previously
        # but with opposite sign on Fe2+ site
        magtypes = {"Fe2+": -5, "Fe3+": 5}
        order_parameters = [
            MagOrderParameterConstraint(1, species_constraints="Fe2+"),
            MagOrderParameterConstraint(0.5, species_constraints="Fe3+")
        ]
        trans = MagOrderingTransformation(magtypes, order_parameter=order_parameters)
        alls = trans.apply_transformation(self.Fe3O4_oxi)
        self.assertEqual(sorted([str(alls[idx].specie) for idx in range(0,2)]),
                         sorted(["Fe2+,spin=-5", "Fe2+,spin=-5"]))
        self.assertEqual(sorted([str(alls[idx].specie) for idx in range(2, 6)]),
                         sorted(["Fe3+,spin=5", "Fe3+,spin=5",
                                 "Fe3+,spin=-5", "Fe3+,spin=-5"]))

        # while this should order on both sites
        magtypes = {"Fe2+": 5, "Fe3+": 5}
        order_parameters = [
            MagOrderParameterConstraint(0.5, species_constraints="Fe2+"),
            MagOrderParameterConstraint(0.25, species_constraints="Fe3+")
        ]
        trans = MagOrderingTransformation(magtypes, order_parameter=order_parameters)
        alls = trans.apply_transformation(self.Fe3O4_oxi)
        self.assertEqual(sorted([str(alls[idx].specie) for idx in range(0,2)]),
                         sorted(["Fe2+,spin=5", "Fe2+,spin=-5"]))
        self.assertEqual(sorted([str(alls[idx].specie) for idx in range(2, 6)]),
                         sorted(["Fe3+,spin=5", "Fe3+,spin=-5",
                                 "Fe3+,spin=-5", "Fe3+,spin=-5"]))

        # add coordination numbers to our test case
        # don't really care what these are for the test case
        cns = [6, 6, 6, 6, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0]
        self.Fe3O4.add_site_property('cn', cns)

        # this should give FM ordering on cn=4 sites, and AFM ordering on cn=6 sites
        magtypes = {"Fe": 5}
        order_parameters = [
            MagOrderParameterConstraint(0.5, species_constraints="Fe",
                                        site_constraint_name="cn", site_constraints=6),
            MagOrderParameterConstraint(1.0, species_constraints="Fe",
                                        site_constraint_name="cn", site_constraints=4)
        ]
        trans = MagOrderingTransformation(magtypes, order_parameter=order_parameters)
        alls = trans.apply_transformation(self.Fe3O4)
        alls.sort(key=lambda x: x.properties['cn'], reverse=True)
        self.assertEqual(sorted([str(alls[idx].specie) for idx in range(0, 4)]),
                         sorted(["Fe,spin=-5", "Fe,spin=-5",
                                 "Fe,spin=5", "Fe,spin=5"]))
        self.assertEqual(sorted([str(alls[idx].specie) for idx in range(4,6)]),
                         sorted(["Fe,spin=5", "Fe,spin=5"]))

        # now ordering on both sites, equivalent to order_parameter = 0.5
        magtypes = {"Fe2+": 5, "Fe3+": 5}
        order_parameters = [
            MagOrderParameterConstraint(0.5, species_constraints="Fe2+"),
            MagOrderParameterConstraint(0.5, species_constraints="Fe3+")
        ]
        trans = MagOrderingTransformation(magtypes, order_parameter=order_parameters)
        alls = trans.apply_transformation(self.Fe3O4_oxi, return_ranked_list=10)
        struct = alls[0]["structure"]
        self.assertEqual(sorted([str(struct[idx].specie) for idx in range(0,2)]),
                         sorted(["Fe2+,spin=5", "Fe2+,spin=-5"]))
        self.assertEqual(sorted([str(struct[idx].specie) for idx in range(2, 6)]),
                         sorted(["Fe3+,spin=5", "Fe3+,spin=-5",
                                 "Fe3+,spin=-5", "Fe3+,spin=5"]))
        self.assertEqual(len(alls), 4)

        # now mixed orderings where neither are equal or 1
        magtypes = {"Fe2+": 5, "Fe3+": 5}
        order_parameters = [
            MagOrderParameterConstraint(0.5, species_constraints="Fe2+"),
            MagOrderParameterConstraint(0.25, species_constraints="Fe3+")
        ]
        trans = MagOrderingTransformation(magtypes, order_parameter=order_parameters)
        alls = trans.apply_transformation(self.Fe3O4_oxi, return_ranked_list=100)
        struct = alls[0]["structure"]
        self.assertEqual(sorted([str(struct[idx].specie) for idx in range(0,2)]),
                         sorted(["Fe2+,spin=5", "Fe2+,spin=-5"]))
        self.assertEqual(sorted([str(struct[idx].specie) for idx in range(2, 6)]),
                         sorted(["Fe3+,spin=5", "Fe3+,spin=-5",
                                 "Fe3+,spin=-5", "Fe3+,spin=-5"]))
        self.assertEqual(len(alls), 2)

        # now order on multiple species
        magtypes = {"Fe2+": 5, "Fe3+": 5}
        order_parameters = [
            MagOrderParameterConstraint(0.5, species_constraints=["Fe2+", "Fe3+"]),
        ]
        trans = MagOrderingTransformation(magtypes, order_parameter=order_parameters)
        alls = trans.apply_transformation(self.Fe3O4_oxi, return_ranked_list=10)
        struct = alls[0]["structure"]
        self.assertEqual(sorted([str(struct[idx].specie) for idx in range(0,2)]),
                         sorted(["Fe2+,spin=5", "Fe2+,spin=-5"]))
        self.assertEqual(sorted([str(struct[idx].specie) for idx in range(2, 6)]),
                         sorted(["Fe3+,spin=5", "Fe3+,spin=-5",
                                 "Fe3+,spin=-5", "Fe3+,spin=5"]))
        self.assertEqual(len(alls), 6)


@unittest.skipIf(not enumlib_present, "enum_lib not present.")
class DopingTransformationTest(PymatgenTest):

    def setUp(self):
        warnings.simplefilter("ignore")

    def tearDown(self):
        warnings.simplefilter("default")

    def test_apply_transformation(self):
        structure = PymatgenTest.get_structure("LiFePO4")
        a = SpacegroupAnalyzer(structure, 0.1)
        structure = a.get_refined_structure()
        t = DopingTransformation("Ca2+", min_length=10)
        ss = t.apply_transformation(structure, 100)
        self.assertEqual(len(ss), 1)

        t = DopingTransformation("Al3+", min_length=15, ionic_radius_tol=0.1)
        ss = t.apply_transformation(structure, 100)
        self.assertEqual(len(ss), 0)

        # Aliovalent doping with vacancies
        for dopant, nstructures in [("Al3+", 2), ("N3-", 235), ("Cl-", 8)]:
            t = DopingTransformation(dopant, min_length=4, alio_tol=1,
                                     max_structures_per_enum=1000)
            ss = t.apply_transformation(structure, 1000)
            self.assertEqual(len(ss), nstructures)
            for d in ss:
                self.assertEqual(d["structure"].charge, 0)

        # Aliovalent doping with codopant
        for dopant, nstructures in [("Al3+", 3), ("N3-", 37), ("Cl-", 37)]:
            t = DopingTransformation(dopant, min_length=4, alio_tol=1,
                                     codopant=True,
                                     max_structures_per_enum=1000)
            ss = t.apply_transformation(structure, 1000)
            self.assertEqual(len(ss), nstructures)
            for d in ss:
                self.assertEqual(d["structure"].charge, 0)

        # Make sure compensation is done with lowest oxi state
        structure = PymatgenTest.get_structure("SrTiO3")
        t = DopingTransformation("Nb5+", min_length=5, alio_tol=1,
                                 max_structures_per_enum=1000,
                                 allowed_doping_species=["Ti4+"])
        ss = t.apply_transformation(structure, 1000)
        self.assertEqual(len(ss), 3)
        for d in ss:
            self.assertEqual(d["structure"].formula, "Sr7 Ti6 Nb2 O24")

    def test_as_from_dict(self):
        trans = DopingTransformation("Al3+", min_length=5, alio_tol=1,
                                     codopant=False, max_structures_per_enum=1)
        d = trans.as_dict()
        # Check json encodability
        s = json.dumps(d)
        trans = DopingTransformation.from_dict(d)
        self.assertEqual(str(trans.dopant), "Al3+")
        self.assertEqual(trans.max_structures_per_enum, 1)

    def test_find_codopant(self):
        self.assertEqual(_find_codopant(Specie("Fe", 2), 1), Specie("Cu", 1))
        self.assertEqual(_find_codopant(Specie("Fe", 2), 3), Specie("In", 3))


class SlabTransformationTest(PymatgenTest):

    def test_apply_transformation(self):
        s = self.get_structure("LiFePO4")
        trans = SlabTransformation([0, 0, 1], 10, 10, shift = 0.25)
        gen = SlabGenerator(s, [0, 0, 1], 10, 10)
        slab_from_gen = gen.get_slab(0.25)
        slab_from_trans = trans.apply_transformation(s)
        self.assertArrayAlmostEqual(slab_from_gen.lattice.matrix, 
                                    slab_from_trans.lattice.matrix)
        self.assertArrayAlmostEqual(slab_from_gen.cart_coords, 
                                    slab_from_trans.cart_coords)

        fcc = Structure.from_spacegroup("Fm-3m", Lattice.cubic(3), ["Fe"],
                                        [[0, 0, 0]])
        trans = SlabTransformation([1, 1, 1], 10, 10)
        slab_from_trans = trans.apply_transformation(fcc)
        gen = SlabGenerator(fcc, [1, 1, 1], 10, 10)
        slab_from_gen = gen.get_slab()
        self.assertArrayAlmostEqual(slab_from_gen.lattice.matrix,
                                    slab_from_trans.lattice.matrix)
        self.assertArrayAlmostEqual(slab_from_gen.cart_coords, 
                                    slab_from_trans.cart_coords)



class GrainBoundaryTransformationTest(PymatgenTest):
    def test_apply_transformation(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            Al_bulk = Structure.from_spacegroup("Fm-3m", Lattice.cubic(2.8575585),
                                                ["Al"], [[0, 0, 0]])
            gb_gen_params_s5 = {"rotation_axis": [1, 0, 0], "rotation_angle": 53.13010235415599,
                                "expand_times": 3, "vacuum_thickness": 0.0, "normal": True,
                                "plane": [0, -1, -3], 'rm_ratio': 0.6}
            gbg = GrainBoundaryGenerator(Al_bulk)
            gb_from_generator = gbg.gb_from_parameters(**gb_gen_params_s5)
            gbt_s5 = GrainBoundaryTransformation(**gb_gen_params_s5)
            gb_from_trans = gbt_s5.apply_transformation(Al_bulk)
            self.assertArrayAlmostEqual(gb_from_generator.lattice.matrix,
                                        gb_from_trans.lattice.matrix)
            self.assertArrayAlmostEqual(gb_from_generator.cart_coords,
                                        gb_from_trans.cart_coords)


class DisorderedOrderedTransformationTest(PymatgenTest):

    def test_apply_transformation(self):

        # non-sensical example just for testing purposes
        struct = self.get_structure('BaNiO3')

        trans = DisorderOrderedTransformation()
        output = trans.apply_transformation(struct)

        self.assertFalse(output.is_ordered)
        self.assertDictEqual(output[-1].species.as_dict(),
                             {'Ni': 0.5, 'Ba': 0.5})

@unittest.skipIf(not mcsqs_cmd, "mcsqs not present.")
class SQSTransformationTest(PymatgenTest):

    def test_apply_transformation(self):

        # non-sensical example just for testing purposes
        self.pztstrings = np.load(os.path.join(test_dir, "mcsqs/pztstrings.npy"), allow_pickle=True)
        self.struct = self.get_structure('Pb2TiZrO6')

        trans = SQSTransformation({2:6, 3:4}, supercell = [2,1,1], total_atoms = None, search_time = 0.01)
        struct = self.struct.copy()
        struct.replace_species({'Ti': {'Ti':0.5, 'Zr':0.5 }, 'Zr': {'Ti':0.5, 'Zr':0.5}})
        sqs = trans.apply_transformation(struct)
        self.assertEqual(atat.Mcsqs(sqs).to_string() in self.pztstrings, True)
        os.remove('sqscell.out')
        os.remove('rndstrgrp.out')
        os.remove('bestcorr.out')
        os.remove('rndstr.in')
        os.remove('sym.out')
        os.remove('mcsqs.log')
        os.remove('bestsqs.out')
        os.remove('clusters.out')

class CubicSupercellTransformationTest(PymatgenTest):

    def test_apply_transformation(self):

        structure = self.get_structure('TlBiSe2')
        min_atoms = 100
        max_atoms = 1000
        num_nn_dists = 5

        # Test the transformation without constraining trans_mat to be diagonal
        supercell_generator = CubicSupercellTransformation(min_atoms=min_atoms,
                                                           max_atoms=max_atoms,
                                                           num_nn_dists=num_nn_dists)
        superstructure = supercell_generator.apply_transformation(structure)

        num_atoms = superstructure.num_sites
        self.assertTrue(num_atoms>=min_atoms)
        self.assertTrue(num_atoms<=max_atoms)
        self.assertTrue(supercell_generator.smallest_dim >=
                        num_nn_dists*supercell_generator.nn_dist)
        self.assertArrayAlmostEqual(superstructure.lattice.matrix[0],
                                    [1.49656087e+01, -1.11448000e-03, 9.04924836e+00])
        self.assertArrayAlmostEqual(superstructure.lattice.matrix[1],
                                    [-0.95005506, 14.95766342, 10.01819773])
        self.assertArrayAlmostEqual(superstructure.lattice.matrix[2],
                                    [3.69130000e-02, 4.09320200e-02, 5.90830153e+01])
        self.assertEqual(superstructure.num_sites, 448)
        self.assertArrayEqual(supercell_generator.trans_mat,
                              np.array([[4, 0, 0],
                                        [1, 4, -4],
                                        [0, 0, 1]]))

        # Test the diagonal transformation
        structure2 = self.get_structure('Si')
        sga = SpacegroupAnalyzer(structure2)
        structure2 = sga.get_primitive_standard_structure()
        structure2.to("poscar", filename="POSCAR-orig_si")
        diagonal_supercell_generator = CubicSupercellTransformation(min_atoms=min_atoms,
                                                                    max_atoms=max_atoms,
                                                                    num_nn_dists=num_nn_dists,
                                                                    force_diagonal_transformation=True)
        superstructure2 = diagonal_supercell_generator.apply_transformation(structure2)
        superstructure2.to("poscar", filename="POSCAR-diag_si")
        self.assertArrayEqual(diagonal_supercell_generator.trans_mat,
                              np.array([[4, 0, 0],
                                        [0, 4, 0],
                                        [0, 0, 4]]))


class AddAdsorbateTransformationTest(PymatgenTest):

    def test_apply_transformation(self):

        co = Molecule(["C", "O"], [[0, 0, 0], [0, 0, 1.23]])
        trans = AddAdsorbateTransformation(co)
        pt = Structure(Lattice.cubic(5), ["Pt"], [[0, 0, 0]])  # fictitious
        slab = SlabTransformation([0, 0, 1], 20, 10).apply_transformation(pt)
        out = trans.apply_transformation(slab)

        self.assertEqual(out.composition.reduced_formula, "Pt4CO")


class SubstituteSurfaceSiteTransformationTest(PymatgenTest):

    def test_apply_transformation(self):

        trans = SubstituteSurfaceSiteTransformation("Au")
        pt = Structure(Lattice.cubic(5), ["Pt"], [[0, 0, 0]])  # fictitious
        slab = SlabTransformation([0, 0, 1], 20, 10).apply_transformation(pt)
        out = trans.apply_transformation(slab)

        self.assertEqual(out.composition.reduced_formula, "Pt3Au")


if __name__ == "__main__":
    unittest.main()
