# coding: utf-8
# Copyright (c) Pymatgen Development Team.
# Distributed under the terms of the MIT License.

"""
This module defines the VaspInputSet abstract base class and a concrete
implementation for the parameters developed and tested by the core team
of pymatgen, including the Materials Virtual Lab, Materials Project and the MIT
high throughput project.  The basic concept behind an input set is to specify
a scheme to generate a consistent set of VASP inputs from a structure
without further user intervention. This ensures comparability across
runs.

Read the following carefully before implementing new input sets:

1. 99% of what needs to be done can be done by specifying user_incar_settings
   to override some of the defaults of various input sets. Unless there is an
   extremely good reason to add a new set, DO NOT add one. E.g., if you want
   to turn the hubbard U off, just set "LDAU": False as a user_incar_setting.
2. All derivative input sets should inherit from one of the usual MPRelaxSet or
   MITRelaxSet, and proper superclass delegation should be used where possible.
   In particular, you are not supposed to implement your own as_dict or
   from_dict for derivative sets unless you know what you are doing.
   Improper overriding the as_dict and from_dict protocols is the major
   cause of implementation headaches. If you need an example, look at how the
   MPStaticSet or MPNonSCFSets are constructed.

The above are recommendations. The following are UNBREAKABLE rules:

1. All input sets must take in a structure or list of structures as the first
   argument.
2. user_incar_settings, user_kpoints_settings and user_<whatever>_settings are
   ABSOLUTE. Any new sets you implement must obey this. If a user wants to
   override your settings, you assume he knows what he is doing. Do not
   magically override user supplied settings. You can issue a warning if you
   think the user is wrong.
3. All input sets must save all supplied args and kwargs as instance variables.
   E.g., self.my_arg = my_arg and self.kwargs = kwargs in the __init__. This
   ensures the as_dict and from_dict work correctly.
"""

import abc
import re
import glob
import shutil
import warnings
from itertools import chain
from copy import deepcopy
import numpy as np
from pathlib import Path
from monty.serialization import loadfn
from monty.io import zopen
from monty.dev import deprecated

from pymatgen.core.periodic_table import Specie, Element
from pymatgen.core.structure import Structure
from pymatgen.io.vasp.inputs import Incar, Poscar, Potcar, Kpoints, VaspInput
from pymatgen.io.vasp.outputs import Vasprun, Outcar
from pymatgen.io.lobster import Lobsterin
from monty.json import MSONable
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.symmetry.bandstructure import HighSymmKpath
from pymatgen.analysis.structure_matcher import StructureMatcher
from pymatgen.core.sites import PeriodicSite

__author__ = "Shyue Ping Ong, Wei Chen, Will Richards, Geoffroy Hautier, " \
             "Anubhav Jain"
__copyright__ = "Copyright 2011, The Materials Project"
__version__ = "1.0"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"
__date__ = "May 28 2016"

MODULE_DIR = Path(__file__).resolve().parent


class VaspInputSet(MSONable, metaclass=abc.ABCMeta):
    """
    Base class representing a set of Vasp input parameters with a structure
    supplied as init parameters. Typically, you should not inherit from this
    class. Start from DictSet or MPRelaxSet or MITRelaxSet.
    """

    @property
    @abc.abstractmethod
    def incar(self):
        """Incar object"""
        pass

    @property
    @abc.abstractmethod
    def kpoints(self):
        """Kpoints object"""
        pass

    @property
    @abc.abstractmethod
    def poscar(self):
        """Poscar object"""
        pass

    @property
    def potcar_symbols(self):
        """
        List of POTCAR symbols.
        """
        elements = self.poscar.site_symbols
        potcar_symbols = []
        settings = self._config_dict["POTCAR"]

        if isinstance(settings[elements[-1]], dict):
            for el in elements:
                potcar_symbols.append(settings[el]['symbol']
                                      if el in settings else el)
        else:
            for el in elements:
                potcar_symbols.append(settings.get(el, el))

        return potcar_symbols

    @property
    def potcar(self):
        """
        Potcar object.
        """
        return Potcar(self.potcar_symbols, functional=self.potcar_functional)

    @property  # type: ignore
    @deprecated(message="Use the get_vasp_input() method instead.")
    def all_input(self):
        """
        Returns all input files as a dict of {filename: vasp object}

        Returns:
            dict of {filename: object}, e.g., {'INCAR': Incar object, ...}
        """
        return {'INCAR': self.incar,
                'KPOINTS': self.kpoints,
                'POSCAR': self.poscar,
                'POTCAR': self.potcar}

    def get_vasp_input(self) -> VaspInput:
        """

        Returns:
            VaspInput
        """
        return VaspInput(incar=self.incar,
                         kpoints=self.kpoints,
                         poscar=self.poscar,
                         potcar=self.potcar)

    def write_input(self, output_dir,
                    make_dir_if_not_present=True, include_cif=False):
        """
        Writes a set of VASP input to a directory.

        Args:
            output_dir (str): Directory to output the VASP input files
            make_dir_if_not_present (bool): Set to True if you want the
                directory (and the whole path) to be created if it is not
                present.
            include_cif (bool): Whether to write a CIF file in the output
                directory for easier opening by VESTA.
        """
        vinput = self.get_vasp_input()
        vinput.write_input(
            output_dir, make_dir_if_not_present=make_dir_if_not_present)
        if include_cif:
            s = vinput["POSCAR"].structure
            fname = Path(output_dir) / ("%s.cif" % re.sub(r'\s', "", s.formula))
            s.to(filename=fname)

    def as_dict(self, verbosity=2):
        d = MSONable.as_dict(self)
        if verbosity == 1:
            d.pop("structure", None)
        return d


def _load_yaml_config(fname):
    config = loadfn(str(MODULE_DIR / ("%s.yaml" % fname)))
    config["INCAR"].update(loadfn(str(MODULE_DIR / "VASPIncarBase.yaml")))
    return config


class DictSet(VaspInputSet):
    """
    Concrete implementation of VaspInputSet that is initialized from a dict
    settings. This allows arbitrary settings to be input. In general,
    this is rarely used directly unless there is a source of settings in yaml
    format (e.g., from a REST interface). It is typically used by other
    VaspInputSets for initialization.

    Special consideration should be paid to the way the MAGMOM initialization
    for the INCAR is done. The initialization differs depending on the type of
    structure and the configuration settings. The order in which the magmom is
    determined is as follows:

    1. If the site itself has a magmom setting, that is used.
    2. If the species on the site has a spin setting, that is used.
    3. If the species itself has a particular setting in the config file, that
       is used, e.g., Mn3+ may have a different magmom than Mn4+.
    4. Lastly, the element symbol itself is checked in the config file. If
       there are no settings, VASP's default of 0.6 is used.

    Args:
        structure (Structure): The Structure to create inputs for.
        config_dict (dict): The config dictionary to use.
        files_to_transfer (dict): A dictionary of {filename: filepath}. This
            allows the transfer of files from a previous calculation.
        user_incar_settings (dict): User INCAR settings. This allows a user
            to override INCAR settings, e.g., setting a different MAGMOM for
            various elements or species. Note that in the new scheme,
            ediff_per_atom and hubbard_u are no longer args. Instead, the
            config_dict supports EDIFF_PER_ATOM and EDIFF keys. The former
            scales with # of atoms, the latter does not. If both are
            present, EDIFF is preferred. To force such settings, just supply
            user_incar_settings={"EDIFF": 1e-5, "LDAU": False} for example.
            The keys 'LDAUU', 'LDAUJ', 'LDAUL' are special cases since
            pymatgen defines different values depending on what anions are
            present in the structure, so these keys can be defined in one
            of two ways, e.g. either {"LDAUU":{"O":{"Fe":5}}} to set LDAUU
            for Fe to 5 in an oxide, or {"LDAUU":{"Fe":5}} to set LDAUU to
            5 regardless of the input structure.

            If a None value is given, that key is unset. For example,
            {"ENCUT": None} will remove ENCUT from the incar settings.
        user_kpoints_settings (dict or Kpoints): Allow user to override kpoints
            setting by supplying a dict E.g., {"reciprocal_density": 1000}.
            User can also supply Kpoints object. Default is None.
        user_potcar_settings (dict: Allow user to override POTCARs. E.g.,
            {"Gd": "Gd_3"}. This is generally not recommended. Default is None.
        constrain_total_magmom (bool): Whether to constrain the total magmom
            (NUPDOWN in INCAR) to be the sum of the expected MAGMOM for all
            species. Defaults to False.
        sort_structure (bool): Whether to sort the structure (using the
            default sort order of electronegativity) before generating input
            files. Defaults to True, the behavior you would want most of the
            time. This ensures that similar atomic species are grouped
            together.
        potcar_functional (str): Functional to use. Default (None) is to use
            the functional in Potcar.DEFAULT_FUNCTIONAL. Valid values:
            "PBE", "PBE_52", "PBE_54", "LDA", "LDA_52", "LDA_54", "PW91",
            "LDA_US", "PW91_US".
        force_gamma (bool): Force gamma centered kpoint generation. Default
            (False) is to use the Automatic Density kpoint scheme, which
            will use the Gamma centered generation scheme for hexagonal
            cells, and Monkhorst-Pack otherwise.
        reduce_structure (None/str): Before generating the input files,
            generate the reduced structure. Default (None), does not
            alter the structure. Valid values: None, "niggli", "LLL".
        vdw: Adds default parameters for van-der-Waals functionals supported
            by VASP to INCAR. Supported functionals are: DFT-D2, undamped
            DFT-D3, DFT-D3 with Becke-Jonson damping, Tkatchenko-Scheffler,
            Tkatchenko-Scheffler with iterative Hirshfeld partitioning,
            MBD@rSC, dDsC, Dion's vdW-DF, DF2, optPBE, optB88, optB86b and
            rVV10.
        use_structure_charge (bool): If set to True, then the public
            variable used for setting the overall charge of the
            structure (structure.charge) is used to set the NELECT
            variable in the INCAR
            Default is False (structure's overall charge is not used)
        standardize (float): Whether to standardize to a primitive standard
            cell. Defaults to False.
        sym_prec (float): Tolerance for symmetry finding.
        international_monoclinic (bool): Whether to use international convention
            (vs Curtarolo) for monoclinic. Defaults True.
    """

    def __init__(self, structure, config_dict,
                 files_to_transfer=None, user_incar_settings=None,
                 user_kpoints_settings=None, user_potcar_settings=None,
                 constrain_total_magmom=False, sort_structure=True,
                 potcar_functional="PBE", force_gamma=False,
                 reduce_structure=None, vdw=None,
                 use_structure_charge=False, standardize=False, sym_prec=0.1,
                 international_monoclinic=True):
        if reduce_structure:
            structure = structure.get_reduced_structure(reduce_structure)
        if sort_structure:
            structure = structure.get_sorted_structure()

        self._structure = structure
        self._config_dict = deepcopy(config_dict)
        self.files_to_transfer = files_to_transfer or {}
        self.constrain_total_magmom = constrain_total_magmom
        self.sort_structure = sort_structure
        self.potcar_functional = potcar_functional
        self.force_gamma = force_gamma
        self.reduce_structure = reduce_structure
        self.user_incar_settings = user_incar_settings or {}
        self.user_kpoints_settings = user_kpoints_settings
        self.user_potcar_settings = user_potcar_settings
        self.vdw = vdw.lower() if vdw is not None else None
        self.use_structure_charge = use_structure_charge
        self.standardize = standardize
        self.sym_prec = sym_prec
        self.international_monoclinic = international_monoclinic

        if self.vdw:
            vdw_par = loadfn(str(MODULE_DIR / "vdW_parameters.yaml"))
            try:
                self._config_dict["INCAR"].update(vdw_par[self.vdw])
            except KeyError:
                raise KeyError("Invalid or unsupported van-der-Waals "
                               "functional. Supported functionals are "
                               "%s." % vdw_par.keys())
        if self.user_potcar_settings:
            warnings.warn(
                "Overriding POTCARs is generally not recommended as it "
                "significantly affect the results of calculations and "
                "compatibility with other calculations done with the same "
                "input set. In many instances, it is better to write a "
                "subclass of a desired input set and override the POTCAR in "
                "the subclass to be explicit on the differences.",
                BadInputSetWarning)
            for k, v in self.user_potcar_settings.items():
                self._config_dict["POTCAR"][k] = v

    @property
    def structure(self):
        if self.standardize and self.sym_prec:
            return standardize_structure(
                self._structure, sym_prec=self.sym_prec,
                international_monoclinic=self.international_monoclinic)
        else:
            return self._structure

    @property
    def incar(self):
        settings = dict(self._config_dict["INCAR"])
        for k, v in self.user_incar_settings.items():
            if v is None:
                try:
                    del settings[k]
                except KeyError:
                    settings[k] = v
            else:
                settings[k] = v
        structure = self.structure
        incar = Incar()
        comp = structure.composition
        elements = sorted([el for el in comp.elements if comp[el] > 0],
                          key=lambda e: e.X)
        most_electroneg = elements[-1].symbol
        poscar = Poscar(structure)
        hubbard_u = settings.get("LDAU", False)

        for k, v in settings.items():
            if k == "MAGMOM":
                mag = []
                for site in structure:
                    if hasattr(site, 'magmom'):
                        mag.append(site.magmom)
                    elif hasattr(site.specie, 'spin'):
                        mag.append(site.specie.spin)
                    elif str(site.specie) in v:
                        mag.append(v.get(str(site.specie)))
                    else:
                        mag.append(v.get(site.specie.symbol, 0.6))
                incar[k] = mag
            elif k in ('LDAUU', 'LDAUJ', 'LDAUL'):
                if hubbard_u:
                    if hasattr(structure[0], k.lower()):
                        m = dict([(site.specie.symbol, getattr(site, k.lower()))
                                  for site in structure])
                        incar[k] = [m[sym] for sym in poscar.site_symbols]
                    # lookup specific LDAU if specified for most_electroneg atom
                    elif most_electroneg in v.keys() and \
                            isinstance(v[most_electroneg], dict):
                        incar[k] = [v[most_electroneg].get(sym, 0)
                                    for sym in poscar.site_symbols]
                    # else, use fallback LDAU value if it exists
                    else:
                        incar[k] = [v.get(sym, 0)
                                    if isinstance(v.get(sym, 0), (float, int))
                                    else 0 for sym in poscar.site_symbols]
            elif k.startswith("EDIFF") and k != "EDIFFG":
                if "EDIFF" not in settings and k == "EDIFF_PER_ATOM":
                    incar["EDIFF"] = float(v) * structure.num_sites
                else:
                    incar["EDIFF"] = float(settings["EDIFF"])
            else:
                incar[k] = v

        has_u = hubbard_u and sum(incar['LDAUU']) > 0
        if has_u:
            # modify LMAXMIX if LSDA+U and you have d or f electrons
            # note that if the user explicitly sets LMAXMIX in settings it will
            # override this logic.
            if 'LMAXMIX' not in settings.keys():
                # contains f-electrons
                if any([el.Z > 56 for el in structure.composition]):
                    incar['LMAXMIX'] = 6
                # contains d-electrons
                elif any([el.Z > 20 for el in structure.composition]):
                    incar['LMAXMIX'] = 4
        else:
            for key in list(incar.keys()):
                if key.startswith('LDAU'):
                    del incar[key]

        if self.constrain_total_magmom:
            nupdown = sum([mag if abs(mag) > 0.6 else 0
                           for mag in incar['MAGMOM']])
            incar['NUPDOWN'] = nupdown

        if self.use_structure_charge:
            incar["NELECT"] = self.nelect

        if np.product(self.kpoints.kpts) < 4 and incar.get("ISMEAR", 0) == -5:
            incar["ISMEAR"] = 0

        if all([k.is_metal for k in structure.composition.keys()]):
            if incar.get("NSW", 0) > 0 and incar.get("ISMEAR", 1) < 1:
                warnings.warn("Relaxation of likely metal with ISMEAR < 1 "
                              "detected. Please see VASP recommendations on "
                              "ISMEAR for metals.", BadInputSetWarning)

        return incar

    @property
    def poscar(self):
        return Poscar(self.structure)

    @property
    def nelect(self):
        """
        Gets the default number of electrons for a given structure.
        """
        # if structure is not sorted this can cause problems, so must take
        # care to remove redundant symbols when counting electrons
        site_symbols = list(set(self.poscar.site_symbols))
        structure = self.structure
        nelect = 0.
        for ps in self.potcar:
            if ps.element in site_symbols:
                site_symbols.remove(ps.element)
                nelect += structure.composition.element_composition[
                              ps.element] * ps.ZVAL

        if self.use_structure_charge:
            return nelect - structure.charge
        else:
            return nelect

    @property
    def kpoints(self):
        """
        Writes out a KPOINTS file using the fully automated grid method. Uses
        Gamma centered meshes for hexagonal cells and Monk grids otherwise.

        Algorithm:
            Uses a simple approach scaling the number of divisions along each
            reciprocal lattice vector proportional to its length.
        """
        settings = self.user_kpoints_settings or self._config_dict["KPOINTS"]

        if isinstance(settings, Kpoints):
            return settings

        # If grid_density is in the kpoints_settings use
        # Kpoints.automatic_density
        if settings.get('grid_density'):
            return Kpoints.automatic_density(
                self.structure, int(settings['grid_density']),
                self.force_gamma)

        # If reciprocal_density is in the kpoints_settings use
        # Kpoints.automatic_density_by_vol
        elif settings.get('reciprocal_density'):
            return Kpoints.automatic_density_by_vol(
                self.structure, int(settings['reciprocal_density']),
                self.force_gamma)

        # If length is in the kpoints_settings use Kpoints.automatic
        elif settings.get('length'):
            return Kpoints.automatic(settings['length'])

        # Raise error. Unsure of which kpoint generation to use
        else:
            raise ValueError(
                "Invalid KPoint Generation algo : Supported Keys are "
                "grid_density: for Kpoints.automatic_density generation, "
                "reciprocal_density: for KPoints.automatic_density_by_vol "
                "generation, and length  : for Kpoints.automatic generation")

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__class__.__name__

    def write_input(self, output_dir,
                    make_dir_if_not_present=True, include_cif=False):
        super().write_input(
            output_dir=output_dir,
            make_dir_if_not_present=make_dir_if_not_present,
            include_cif=include_cif)
        for k, v in self.files_to_transfer.items():
            with zopen(v, "rb") as fin, \
                    zopen(str(Path(output_dir) / k), "wb") as fout:
                shutil.copyfileobj(fin, fout)


class MITRelaxSet(DictSet):
    """
    Standard implementation of VaspInputSet utilizing parameters in the MIT
    High-throughput project.
    The parameters are chosen specifically for a high-throughput project,
    which means in general pseudopotentials with fewer electrons were chosen.

    Please refer::

        A Jain, G. Hautier, C. Moore, S. P. Ong, C. Fischer, T. Mueller,
        K. A. Persson, G. Ceder. A high-throughput infrastructure for density
        functional theory calculations. Computational Materials Science,
        2011, 50(8), 2295-2310. doi:10.1016/j.commatsci.2011.02.023
    """
    CONFIG = _load_yaml_config("MITRelaxSet")

    def __init__(self, structure, **kwargs):
        super().__init__(structure, MITRelaxSet.CONFIG, **kwargs)
        self.kwargs = kwargs


class MPRelaxSet(DictSet):
    """
    Implementation of VaspInputSet utilizing parameters in the public
    Materials Project. Typically, the pseudopotentials chosen contain more
    electrons than the MIT parameters, and the k-point grid is ~50% more dense.
    The LDAUU parameters are also different due to the different psps used,
    which result in different fitted values.
    """
    CONFIG = _load_yaml_config("MPRelaxSet")

    def __init__(self, structure, **kwargs):
        super().__init__(structure, MPRelaxSet.CONFIG, **kwargs)
        self.kwargs = kwargs


class MPMetalRelaxSet(MPRelaxSet):
    """
    Implementation of VaspInputSet utilizing parameters in the public
    Materials Project, but with tuning for metals. Key things are a denser
    k point density, and a
    """
    CONFIG = _load_yaml_config("MPRelaxSet")

    def __init__(self, structure, **kwargs):
        super().__init__(structure, **kwargs)
        self._config_dict["INCAR"].update({
            "ISMEAR": 1,
            "SIGMA": 0.2
        })
        self._config_dict["KPOINTS"].update({
            "reciprocal_density": 200
        })
        self.kwargs = kwargs


class MPHSERelaxSet(DictSet):
    """
    Same as the MPRelaxSet, but with HSE parameters.
    """
    CONFIG = _load_yaml_config("MPHSERelaxSet")

    def __init__(self, structure, **kwargs):
        super().__init__(structure, MPHSERelaxSet.CONFIG, **kwargs)
        self.kwargs = kwargs


class MPStaticSet(MPRelaxSet):
    """
    Run a static calculation.

    Args:
        structure (Structure): Structure from previous run.
        prev_incar (Incar): Incar file from previous run.
        prev_kpoints (Kpoints): Kpoints from previous run.
        lepsilon (bool): Whether to add static dielectric calculation
        reciprocal_density (int): For static calculations, we usually set the
            reciprocal density by volume. This is a convenience arg to change
            that, rather than using user_kpoints_settings. Defaults to 100,
            which is ~50% more than that of standard relaxation calculations.
        small_gap_multiply ([float, float]): If the gap is less than
            1st index, multiply the default reciprocal_density by the 2nd
            index.
        **kwargs: kwargs supported by MPRelaxSet.
    """

    def __init__(self, structure, prev_incar=None, prev_kpoints=None,
                 lepsilon=False, lcalcpol=False, reciprocal_density=100,
                 small_gap_multiply=None, **kwargs):
        super().__init__(structure, **kwargs)
        if isinstance(prev_incar, str):
            prev_incar = Incar.from_file(prev_incar)
        if isinstance(prev_kpoints, str):
            prev_kpoints = Kpoints.from_file(prev_kpoints)

        self.prev_incar = prev_incar
        self.prev_kpoints = prev_kpoints
        self.reciprocal_density = reciprocal_density
        self.kwargs = kwargs
        self.lepsilon = lepsilon
        self.lcalcpol = lcalcpol
        self.small_gap_multiply = small_gap_multiply

    @property
    def incar(self):
        parent_incar = super().incar
        incar = Incar(self.prev_incar) if self.prev_incar is not None else \
            Incar(parent_incar)

        incar.update(
            {"IBRION": -1, "ISMEAR": -5, "LAECHG": True, "LCHARG": True,
             "LORBIT": 11, "LVHAR": True, "LWAVE": False, "NSW": 0,
             "ICHARG": 0, "ALGO": "Normal"})

        if self.lepsilon:
            incar["IBRION"] = 8
            incar["LEPSILON"] = True

            # LPEAD=T: numerical evaluation of overlap integral prevents
            # LRF_COMMUTATOR errors and can lead to better expt. agreement
            # but produces slightly different results
            incar["LPEAD"] = True

            # Note that DFPT calculations MUST unset NSW. NSW = 0 will fail
            # to output ionic.
            incar.pop("NSW", None)
            incar.pop("NPAR", None)

        if self.lcalcpol:
            incar["LCALCPOL"] = True

        for k in ["MAGMOM", "NUPDOWN"] + list(self.kwargs.get(
                "user_incar_settings", {}).keys()):
            # For these parameters as well as user specified settings, override
            # the incar settings.
            if parent_incar.get(k, None) is not None:
                incar[k] = parent_incar[k]
            else:
                incar.pop(k, None)

        # use new LDAUU when possible b/c the Poscar might have changed
        # representation
        if incar.get('LDAU'):
            u = incar.get('LDAUU', [])
            j = incar.get('LDAUJ', [])
            if sum([u[x] - j[x] for x, y in enumerate(u)]) > 0:
                for tag in ('LDAUU', 'LDAUL', 'LDAUJ'):
                    incar.update({tag: parent_incar[tag]})
            # ensure to have LMAXMIX for GGA+U static run
            if "LMAXMIX" not in incar:
                incar.update({"LMAXMIX": parent_incar["LMAXMIX"]})

        # Compare ediff between previous and staticinputset values,
        # choose the tighter ediff
        incar["EDIFF"] = min(incar.get("EDIFF", 1), parent_incar["EDIFF"])
        return incar

    @property
    def kpoints(self):
        self._config_dict["KPOINTS"]["reciprocal_density"] = \
            self.reciprocal_density
        kpoints = super().kpoints

        # Prefer to use k-point scheme from previous run
        # except for when lepsilon = True is specified
        if self.prev_kpoints and self.prev_kpoints.style != kpoints.style:
            if (self.prev_kpoints.style == Kpoints.supported_modes.Monkhorst) \
                    and (not self.lepsilon):
                k_div = [kp + 1 if kp % 2 == 1 else kp
                         for kp in kpoints.kpts[0]]
                kpoints = Kpoints.monkhorst_automatic(k_div)
            else:
                kpoints = Kpoints.gamma_automatic(kpoints.kpts[0])
        return kpoints

    def override_from_prev_calc(self, prev_calc_dir='.'):
        """
        Update the input set to include settings from a previous calculation.

        Args:
            prev_calc_dir (str): The path to the previous calculation directory.

        Returns:
            The input set with the settings (structure, k-points, incar, etc)
            updated using the previous VASP run.
        """
        vasprun, outcar = get_vasprun_outcar(prev_calc_dir)

        self.prev_incar = vasprun.incar
        self.prev_kpoints = vasprun.kpoints

        if self.standardize:
            warnings.warn("Use of standardize=True with from_prev_run is not "
                          "recommended as there is no guarantee the copied "
                          "files will be appropriate for the standardized "
                          "structure.")

        self._structure = get_structure_from_prev_run(vasprun, outcar)

        # multiply the reciprocal density if needed
        if self.small_gap_multiply:
            gap = vasprun.eigenvalue_band_properties[0]
            if gap <= self.small_gap_multiply[0]:
                self.reciprocal_density = (self.reciprocal_density *
                                           self.small_gap_multiply[1])

        return self

    @classmethod
    def from_prev_calc(cls, prev_calc_dir, **kwargs):
        """
        Generate a set of Vasp input files for static calculations from a
        directory of previous Vasp run.

        Args:
            prev_calc_dir (str): Directory containing the outputs(
                vasprun.xml and OUTCAR) of previous vasp run.
            **kwargs: All kwargs supported by MPStaticSet, other than prev_incar
                and prev_structure and prev_kpoints which are determined from
                the prev_calc_dir.
        """
        input_set = cls(_dummy_structure, **kwargs)
        return input_set.override_from_prev_calc(prev_calc_dir=prev_calc_dir)


class MPHSEBSSet(MPHSERelaxSet):
    """
    Implementation of a VaspInputSet for HSE band structure computations.
    Remember that HSE band structures must be self-consistent in VASP. A
    band structure along symmetry lines for instance needs BOTH a uniform
    grid with appropriate weights AND a path along the lines with weight 0.

    Thus, the "Uniform" mode is just like regular static SCF but allows
    adding custom kpoints (e.g., corresponding to known VBM/CBM) to the
    uniform grid that have zero weight (e.g., for better gap estimate).

    The "Gap" mode behaves just like the "Uniform" mode, however, if starting
    from a previous calculation, the VBM and CBM k-points will automatically
    be added to ``added_kpoints``.

    The "Line" mode is just like Uniform mode, but additionally adds
    k-points along symmetry lines with zero weight.

    Args:
        structure (Structure): Structure to compute
        user_incar_settings (dict): A dict specifying additional incar
            settings
        added_kpoints (list): a list of kpoints (list of 3 number list)
            added to the run. The k-points are in fractional coordinates
        mode (str): "Line" - generate k-points along symmetry lines for
            bandstructure. "Uniform" - generate uniform k-points grid.
        reciprocal_density (int): k-point density to use for uniform mesh.
        copy_chgcar (bool): Whether to copy the CHGCAR of a previous run.
        kpoints_line_density (int): k-point density for high symmetry lines
        **kwargs (dict): Any other parameters to pass into DictSet.

    """

    def __init__(self, structure, user_incar_settings=None, added_kpoints=None,
                 mode="Gap", reciprocal_density=None, copy_chgcar=True,
                 kpoints_line_density=20, **kwargs):
        super().__init__(structure, **kwargs)
        self.user_incar_settings = user_incar_settings or {}
        self._config_dict["INCAR"].update({
            "NSW": 0,
            "ISMEAR": 0,
            "SIGMA": 0.05,
            "ISYM": 3,
            "LCHARG": False,
            "NELMIN": 5
        })
        self.added_kpoints = added_kpoints if added_kpoints is not None else []
        self.mode = mode

        if (not reciprocal_density or
                "reciprocal_density" not in self.user_kpoints_settings):
            self.reciprocal_density = 50
        else:
            self.reciprocal_density = reciprocal_density or \
                                      self.user_kpoints_settings['reciprocal_density']

        self.kpoints_line_density = kpoints_line_density
        self.copy_chgcar = copy_chgcar

    @property
    def kpoints(self):
        kpts = []
        weights = []
        all_labels = []
        structure = self.structure

        # for both modes, include the Uniform mesh w/standard weights
        grid = Kpoints.automatic_density_by_vol(structure,
                                                self.reciprocal_density).kpts
        ir_kpts = SpacegroupAnalyzer(structure, symprec=0.1) \
            .get_ir_reciprocal_mesh(grid[0])
        for k in ir_kpts:
            kpts.append(k[0])
            weights.append(int(k[1]))
            all_labels.append(None)

        # for both modes, include any user-added kpoints w/zero weight
        for k in self.added_kpoints:
            kpts.append(k)
            weights.append(0.0)
            all_labels.append("user-defined")

        # for line mode only, add the symmetry lines w/zero weight
        if self.mode.lower() == "line":
            kpath = HighSymmKpath(structure)
            frac_k_points, labels = kpath.get_kpoints(
                line_density=self.kpoints_line_density,
                coords_are_cartesian=False)

            for k in range(len(frac_k_points)):
                kpts.append(frac_k_points[k])
                weights.append(0.0)
                all_labels.append(labels[k])

        comment = ("HSE run along symmetry lines"
                   if self.mode.lower() == "line"
                   else "HSE run on uniform grid")

        return Kpoints(comment=comment,
                       style=Kpoints.supported_modes.Reciprocal,
                       num_kpts=len(kpts), kpts=kpts, kpts_weights=weights,
                       labels=all_labels)

    def override_from_prev_calc(self, prev_calc_dir='.'):
        """
        Update the input set to include settings from a previous calculation.

        Args:
            prev_calc_dir (str): The path to the previous calculation directory.

        Returns:
            The input set with the settings (structure, k-points, incar, etc)
            updated using the previous VASP run.
        """
        vasprun, outcar = get_vasprun_outcar(prev_calc_dir)

        self._structure = get_structure_from_prev_run(vasprun, outcar)

        # note: recommend not standardizing the cell because we want to retain
        # k-points
        if self.standardize:
            warnings.warn("Use of standardize=True with from_prev_calc is not "
                          "recommended as there is no guarantee the copied "
                          "files will be appropriate for the standardized "
                          "structure.")

        if self.mode.lower() == "gap":
            added_kpoints = []

            bs = vasprun.get_band_structure()
            vbm, cbm = bs.get_vbm()["kpoint"], bs.get_cbm()["kpoint"]
            if vbm:
                added_kpoints.append(vbm.frac_coords)
            if cbm:
                added_kpoints.append(cbm.frac_coords)

            self.added_kpoints.extend(added_kpoints)

        files_to_transfer = {}
        if self.copy_chgcar:
            chgcars = sorted(glob.glob(str(Path(prev_calc_dir) / "CHGCAR*")))
            if chgcars:
                files_to_transfer["CHGCAR"] = str(chgcars[-1])

        self.files_to_transfer.update(files_to_transfer)

        return self

    @classmethod
    def from_prev_calc(cls, prev_calc_dir, **kwargs):
        """
        Generate a set of Vasp input files for HSE calculations from a
        directory of previous Vasp run.

        Args:
            prev_calc_dir (str): Directory containing the outputs
                (vasprun.xml and OUTCAR) of previous vasp run.
            **kwargs: All kwargs supported by MPHSEBSStaticSet, other than
                prev_structure which is determined from the previous calc dir.
        """
        input_set = cls(_dummy_structure, **kwargs)
        return input_set.override_from_prev_calc(prev_calc_dir=prev_calc_dir)


class MPNonSCFSet(MPRelaxSet):
    """
    Init a MPNonSCFSet. Typically, you would use the classmethod
    from_prev_calc to initialize from a previous SCF run.

    Args:
        structure (Structure): Structure to compute
        prev_incar (Incar/string): Incar file from previous run.
        mode (str): Line, Uniform or Boltztrap mode supported.
        nedos (int): nedos parameter. Default to 2001.
        reciprocal_density (int): density of k-mesh by reciprocal
            volume (defaults to 100)
        sym_prec (float): Symmetry precision (for Uniform mode).
        kpoints_line_density (int): Line density for Line mode.
        optics (bool): whether to add dielectric function
        copy_chgcar: Whether to copy the old CHGCAR when starting from a
            previous calculation.
        nbands_factor (float): Multiplicative factor for NBANDS when starting
            from a previous calculation. Choose a higher number if you are
            doing an LOPTICS calculation.
        small_gap_multiply ([float, float]): When starting from a previous
            calculation, if the gap is less than 1st index, multiply the default
            reciprocal_density by the 2nd index.
        **kwargs: kwargs supported by MPRelaxSet.
    """

    def __init__(self, structure, prev_incar=None,
                 mode="line", nedos=2001, reciprocal_density=100, sym_prec=0.1,
                 kpoints_line_density=20, optics=False, copy_chgcar=True,
                 nbands_factor=1.2, small_gap_multiply=None, **kwargs):
        super().__init__(structure, **kwargs)
        if isinstance(prev_incar, str):
            prev_incar = Incar.from_file(prev_incar)
        self.prev_incar = prev_incar
        self.kwargs = kwargs
        self.nedos = nedos
        self.reciprocal_density = reciprocal_density
        self.sym_prec = sym_prec
        self.kpoints_line_density = kpoints_line_density
        self.optics = optics
        self.mode = mode.lower()
        self.copy_chgcar = copy_chgcar
        self.nbands_factor = nbands_factor
        self.small_gap_multiply = small_gap_multiply

        if self.mode.lower() not in ["line", "uniform", "boltztrap"]:
            raise ValueError("Supported modes for NonSCF runs are 'Line', "
                             "'Uniform' and 'Boltztrap!")

        if (self.mode.lower() != "uniform" or nedos < 2000) and optics:
            warnings.warn("It is recommended to use Uniform mode with a high "
                          "NEDOS for optics calculations.")

    @property
    def incar(self):
        incar = super().incar
        if self.prev_incar is not None:
            incar.update({k: v for k, v in self.prev_incar.items()})

        # Overwrite necessary INCAR parameters from previous runs
        incar.update({"IBRION": -1, "LCHARG": False, "LORBIT": 11,
                      "LWAVE": False, "NSW": 0, "ISYM": 0, "ICHARG": 11})

        if self.mode.lower() == 'uniform':
            # use tetrahedron method for DOS and optics calculations
            incar.update({"ISMEAR": -5})
        else:
            # if line mode, can't use ISMEAR=-5; also use small sigma to avoid
            # partial occupancies for small band gap materials.
            # finally, explicit k-point generation (needed for bolztrap mode)
            # is incompatible with ISMEAR = -5.
            incar.update({"ISMEAR": 0, "SIGMA": 0.01})

        incar.update(self.kwargs.get("user_incar_settings", {}))

        if self.mode.lower() in "uniform":
            # Set smaller steps for DOS and optics output
            incar["NEDOS"] = self.nedos

        if self.optics:
            incar["LOPTICS"] = True

        incar.pop("MAGMOM", None)

        return incar

    @property
    def kpoints(self):
        if self.mode.lower() == "line":
            kpath = HighSymmKpath(self.structure)
            frac_k_points, k_points_labels = kpath.get_kpoints(
                line_density=self.kpoints_line_density,
                coords_are_cartesian=False)
            kpoints = Kpoints(
                comment="Non SCF run along symmetry lines",
                style=Kpoints.supported_modes.Reciprocal,
                num_kpts=len(frac_k_points),
                kpts=frac_k_points, labels=k_points_labels,
                kpts_weights=[1] * len(frac_k_points))
        elif self.mode.lower() == "boltztrap":
            kpoints = Kpoints.automatic_density_by_vol(self.structure,
                                                       self.reciprocal_density)
            mesh = kpoints.kpts[0]
            ir_kpts = SpacegroupAnalyzer(
                self.structure,
                symprec=self.sym_prec).get_ir_reciprocal_mesh(mesh)
            kpts = []
            weights = []
            for k in ir_kpts:
                kpts.append(k[0])
                weights.append(int(k[1]))
            kpoints = Kpoints(comment="Non SCF run on uniform grid",
                              style=Kpoints.supported_modes.Reciprocal,
                              num_kpts=len(ir_kpts),
                              kpts=kpts, kpts_weights=weights)
        else:
            self._config_dict["KPOINTS"]["reciprocal_density"] = \
                self.reciprocal_density
            kpoints = super().kpoints

        # override pymatgen kpoints if provided
        user_kpoints = self.kwargs.get("user_kpoints_settings", None)
        if isinstance(user_kpoints, Kpoints):
            kpoints = user_kpoints

        return kpoints

    def override_from_prev_calc(self, prev_calc_dir='.'):
        """
        Update the input set to include settings from a previous calculation.

        Args:
            prev_calc_dir (str): The path to the previous calculation directory.

        Returns:
            The input set with the settings (structure, k-points, incar, etc)
            updated using the previous VASP run.
        """
        vasprun, outcar = get_vasprun_outcar(prev_calc_dir)

        self.prev_incar = vasprun.incar

        # Get a Magmom-decorated structure
        self._structure = get_structure_from_prev_run(vasprun, outcar)

        if self.standardize:
            warnings.warn("Use of standardize=True with from_prev_run is not "
                          "recommended as there is no guarantee the copied "
                          "files will be appropriate for the standardized"
                          " structure. copy_chgcar is enforced to be false.")
            self.copy_chgcar = False

        # Turn off spin when magmom for every site is smaller than 0.02.
        if outcar and outcar.magnetization:
            site_magmom = np.array([i['tot'] for i in outcar.magnetization])
            ispin = 2 if np.any(site_magmom[np.abs(site_magmom) > 0.02]) else 1

        elif vasprun.is_spin:
            ispin = 2

        else:
            ispin = 1

        nbands = int(np.ceil(vasprun.parameters["NBANDS"] * self.nbands_factor))
        self.prev_incar.update({"ISPIN": ispin, "NBANDS": nbands})

        files_to_transfer = {}

        if self.copy_chgcar:
            chgcars = sorted(glob.glob(str(Path(prev_calc_dir) / "CHGCAR*")))
            if chgcars:
                files_to_transfer["CHGCAR"] = str(chgcars[-1])

        self.files_to_transfer.update(files_to_transfer)

        # multiply the reciprocal density if needed:
        if self.small_gap_multiply:
            gap = vasprun.eigenvalue_band_properties[0]
            if gap <= self.small_gap_multiply[0]:
                self.reciprocal_density = (self.reciprocal_density *
                                           self.small_gap_multiply[1])
                self.kpoints_line_density = (self.kpoints_line_density *
                                             self.small_gap_multiply[1])

        return self

    @classmethod
    def from_prev_calc(cls, prev_calc_dir, **kwargs):
        """
        Generate a set of Vasp input files for NonSCF calculations from a
        directory of previous static Vasp run.

        Args:
            prev_calc_dir (str): The directory contains the outputs(
                vasprun.xml and OUTCAR) of previous vasp run.
            **kwargs: All kwargs supported by MPNonSCFSet, other than structure,
                prev_incar and prev_chgcar which are determined from the
                prev_calc_dir.
        """
        input_set = cls(_dummy_structure, **kwargs)
        return input_set.override_from_prev_calc(prev_calc_dir=prev_calc_dir)


class MPSOCSet(MPStaticSet):
    """
    An input set for running spin-orbit coupling (SOC) calculations.

    Args:
        structure (Structure): the structure must have the 'magmom' site
            property and each magnetic moment value must have 3
            components. eg: ``magmom = [[0,0,2], ...]``
        saxis (tuple): magnetic moment orientation
        copy_chgcar: Whether to copy the old CHGCAR. Defaults to True.
        nbands_factor (float): Multiplicative factor for NBANDS. Choose a
            higher number if you are doing an LOPTICS calculation.
        reciprocal_density (int): density of k-mesh by reciprocal volume.
        small_gap_multiply ([float, float]): If the gap is less than
            1st index, multiply the default reciprocal_density by the 2nd
            index.
        magmom (list[list[float]]): Override for the structure magmoms.
        **kwargs: kwargs supported by MPStaticSet.
    """

    def __init__(self, structure, saxis=(0, 0, 1), copy_chgcar=True,
                 nbands_factor=1.2, reciprocal_density=100,
                 small_gap_multiply=None, magmom=None, **kwargs):

        if (not hasattr(structure[0], "magmom") and
                not isinstance(structure[0].magmom, list)):
            raise ValueError(
                "The structure must have the 'magmom' site "
                "property and each magnetic moment value must have 3 "
                "components. eg:- magmom = [0,0,2]")

        super().__init__(structure, reciprocal_density=reciprocal_density,
                         **kwargs)
        self.saxis = saxis
        self.copy_chgcar = copy_chgcar
        self.nbands_factor = nbands_factor
        self.small_gap_multiply = small_gap_multiply
        self.magmom = magmom

    @property
    def incar(self):
        incar = super().incar
        if self.prev_incar is not None:
            incar.update({k: v for k, v in self.prev_incar.items()})

        # Overwrite necessary INCAR parameters from previous runs
        incar.update({"ISYM": -1, "LSORBIT": "T", "ICHARG": 11,
                      "SAXIS": list(self.saxis)})
        incar.update(self.kwargs.get("user_incar_settings", {}))

        return incar

    def override_from_prev_calc(self, prev_calc_dir='.'):
        """
        Update the input set to include settings from a previous calculation.

        Args:
            prev_calc_dir (str): The path to the previous calculation directory.

        Returns:
            The input set with the settings (structure, k-points, incar, etc)
            updated using the previous VASP run.
        """
        vasprun, outcar = get_vasprun_outcar(prev_calc_dir)

        self.prev_incar = vasprun.incar

        # Remove magmoms from previous INCAR, since we will prefer
        # the final calculated magmoms
        # TODO: revisit in context of MPStaticSet incar logic
        if 'MAGMOM' in self.prev_incar:
            del self.prev_incar['magmom']

        # Get a magmom-decorated structure
        self._structure = get_structure_from_prev_run(vasprun, outcar)
        if self.standardize:
            warnings.warn("Use of standardize=True with from_prev_run is not "
                          "recommended as there is no guarantee the copied "
                          "files will be appropriate for the standardized"
                          " structure. copy_chgcar is enforced to be false.")
            self.copy_chgcar = False

        # override magmom if provided
        if self.magmom:
            self._structure = self._structure.copy(
                site_properties={"magmom": self.magmom})

        # magmom has to be 3D for SOC calculation.
        if hasattr(self._structure[0], "magmom"):
            if not isinstance(self._structure[0].magmom, list):
                self._structure = self._structure.copy(
                    site_properties={"magmom": [[0, 0, site.magmom]
                                                for site in self._structure]})
        else:
            raise ValueError("Neither the previous structure has magmom "
                             "property nor magmom provided")

        nbands = int(np.ceil(vasprun.parameters["NBANDS"] * self.nbands_factor))
        self.prev_incar.update({"NBANDS": nbands})

        files_to_transfer = {}
        if self.copy_chgcar:
            chgcars = sorted(glob.glob(str(Path(prev_calc_dir) / "CHGCAR*")))
            if chgcars:
                files_to_transfer["CHGCAR"] = str(chgcars[-1])

        self.files_to_transfer.update(files_to_transfer)

        # multiply the reciprocal density if needed:
        if self.small_gap_multiply:
            gap = vasprun.eigenvalue_band_properties[0]
            if gap <= self.small_gap_multiply[0]:
                self.reciprocal_density = (self.reciprocal_density *
                                           self.small_gap_multiply[1])

        return self

    @classmethod
    def from_prev_calc(cls, prev_calc_dir, **kwargs):
        """
        Generate a set of Vasp input files for SOC calculations from a
        directory of previous static Vasp run. SOC calc requires all 3
        components for MAGMOM for each atom in the structure.

        Args:
            prev_calc_dir (str): The directory contains the outputs(
                vasprun.xml and OUTCAR) of previous vasp run.
            **kwargs: All kwargs supported by MPSOCSet, other than structure,
                prev_incar and prev_chgcar which are determined from the
                prev_calc_dir.
        """
        input_set = cls(_dummy_structure, **kwargs)
        return input_set.override_from_prev_calc(prev_calc_dir=prev_calc_dir)


class MPNMRSet(MPStaticSet):
    """
    Init a MPNMRSet.

    Args:
        structure (Structure): Structure to compute
        mode (str): The NMR calculation to run
                        "cs": for Chemical Shift
                        "efg" for Electric Field Gradient
        isotopes (list): list of Isotopes for quadrupole moments
        prev_incar (Incar): Incar file from previous run.
        reciprocal_density (int): density of k-mesh by reciprocal
                                volume (defaults to 100)
        **kwargs: kwargs supported by MPStaticSet.
    """

    def __init__(self, structure, mode="cs", isotopes=None,
                 prev_incar=None, reciprocal_density=100, **kwargs):
        self.mode = mode
        self.isotopes = isotopes if isotopes else []
        super().__init__(structure, prev_incar=prev_incar,
                         reciprocal_density=reciprocal_density, **kwargs)

    @property
    def incar(self):
        incar = super().incar

        if self.mode.lower() == "cs":
            incar.update({"LCHIMAG": True,
                          "EDIFF": -1.0e-10,
                          "ISYM": 0,
                          "LCHARG": False,
                          "LNMR_SYM_RED": True,
                          "NELMIN": 10,
                          "NSLPLINE": True,
                          "PREC": "ACCURATE",
                          "SIGMA": 0.01})
        elif self.mode.lower() == "efg":

            isotopes = {ist.split("-")[0]: ist for ist in self.isotopes}

            quad_efg = [
                Specie(p).get_nmr_quadrupole_moment(isotopes.get(p, None)) for p
                in self.poscar.site_symbols]

            incar.update({"ALGO": "FAST",
                          "EDIFF": -1.0e-10,
                          "ISYM": 0,
                          "LCHARG": False,
                          "LEFG": True,
                          "QUAD_EFG": quad_efg,
                          "NELMIN": 10,
                          "PREC": "ACCURATE",
                          "SIGMA": 0.01})
        incar.update(self.kwargs.get("user_incar_settings", {}))

        return incar


class MVLElasticSet(MPRelaxSet):
    """
    MVL denotes VASP input sets that are implemented by the Materials Virtual
    Lab (http://www.materialsvirtuallab.org) for various research.

    This input set is used to calculate elastic constants in VASP. It is used
    in the following work::

        Z. Deng, Z. Wang, I.-H. Chu, J. Luo, S. P. Ong.
        “Elastic Properties of Alkali Superionic Conductor Electrolytes
        from First Principles Calculations”, J. Electrochem. Soc.
        2016, 163(2), A67-A74. doi: 10.1149/2.0061602jes

    To read the elastic constants, you may use the Outcar class which parses the
    elastic constants.

    Args:
        scale (float): POTIM parameter. The default of 0.015 is usually fine,
            but some structures may require a smaller step.
        user_incar_settings (dict): A dict specifying additional incar
            settings.
    """

    def __init__(self, structure, potim=0.015, **kwargs):
        super().__init__(structure, **kwargs)
        self._config_dict["INCAR"].update({"IBRION": 6, "NFREE": 2,
                                           "POTIM": potim})
        self._config_dict["INCAR"].pop("NPAR", None)


class MVLGWSet(DictSet):
    """
    MVL denotes VASP input sets that are implemented by the Materials Virtual
    Lab (http://www.materialsvirtuallab.org) for various research. This is a
    flexible input set for GW calculations.

    Note that unlike all other input sets in this module, the PBE_54 series of
    functional is set as the default. These have much improved performance for
    GW calculations.

    A typical sequence is mode="STATIC" -> mode="DIAG" -> mode="GW" ->
    mode="BSE". For all steps other than the first one (static), the
    recommendation is to use from_prev_calculation on the preceding run in
    the series.

    Args:
        structure (Structure): Input structure.
        prev_incar (Incar/string): Incar file from previous run.
        mode (str): Supported modes are "STATIC" (default), "DIAG", "GW",
            and "BSE".
        nbands (int): For subsequent calculations, it is generally
            recommended to perform NBANDS convergence starting from the
            NBANDS of the previous run for DIAG, and to use the exact same
            NBANDS for GW and BSE. This parameter is used by
            from_previous_calculation to set nband.
        potcar_functional (str): Defaults to "PBE_54".
        copy_wavecar: Whether to copy the old WAVECAR, WAVEDER and associated
            files when starting from a previous calculation.
        nbands_factor (int): Multiplicative factor for NBANDS when starting
            from a previous calculation. Only applies if mode=="DIAG".
            Need to be tested for convergence.
        ncores (int): Numbers of cores used for the calculation. VASP will alter
            NBANDS if it was not dividable by ncores. Only applies if
            mode=="DIAG".
        **kwargs: All kwargs supported by DictSet. Typically,
            user_incar_settings is a commonly used option.
    """
    CONFIG = _load_yaml_config("MVLGWSet")

    SUPPORTED_MODES = ("DIAG", "GW", "STATIC", "BSE")

    def __init__(self, structure, prev_incar=None, nbands=None,
                 potcar_functional="PBE_54", reciprocal_density=100,
                 mode="STATIC", copy_wavecar=True, nbands_factor=5, ncores=16,
                 **kwargs):
        super().__init__(structure, MVLGWSet.CONFIG, **kwargs)
        self.prev_incar = prev_incar
        self.nbands = nbands
        self.potcar_functional = potcar_functional
        self.reciprocal_density = reciprocal_density
        self.mode = mode.upper()
        if self.mode not in MVLGWSet.SUPPORTED_MODES:
            raise ValueError("%s not one of the support modes : %s" %
                             (self.mode, MVLGWSet.SUPPORTED_MODES))
        self.kwargs = kwargs
        self.copy_wavecar = copy_wavecar
        self.nbands_factor = nbands_factor
        self.ncores = ncores

    @property
    def kpoints(self):
        """
        Generate gamma center k-points mesh grid for GW calc,
        which is requested by GW calculation.
        """
        return Kpoints.automatic_density_by_vol(self.structure,
                                                self.reciprocal_density,
                                                force_gamma=True)

    @property
    def incar(self):
        parent_incar = super().incar
        incar = Incar(self.prev_incar) if self.prev_incar is not None else \
            Incar(parent_incar)

        if self.mode == "DIAG":
            # Default parameters for diagonalization calculation.
            incar.update({
                "ALGO": "Exact",
                "NELM": 1,
                "LOPTICS": True,
                "LPEAD": True
            })
        elif self.mode == "GW":
            # Default parameters for GW calculation.
            incar.update({
                "ALGO": "GW0",
                "NELM": 1,
                "NOMEGA": 80,
                "ENCUTGW": 250
            })
            incar.pop("EDIFF", None)
            incar.pop("LOPTICS", None)
            incar.pop("LPEAD", None)
        elif self.mode == "BSE":
            # Default parameters for BSE calculation.
            incar.update({
                "ALGO": "BSE",
                "ANTIRES": 0,
                "NBANDSO": 20,
                "NBANDSV": 20
            })

        if self.nbands:
            incar["NBANDS"] = self.nbands

        # Respect user set INCAR.
        incar.update(self.kwargs.get("user_incar_settings", {}))

        return incar

    def override_from_prev_calc(self, prev_calc_dir='.'):
        """
        Update the input set to include settings from a previous calculation.

        Args:
            prev_calc_dir (str): The path to the previous calculation directory.

        Returns:
            The input set with the settings (structure, k-points, incar, etc)
            updated using the previous VASP run.
        """
        vasprun, outcar = get_vasprun_outcar(prev_calc_dir)
        self.prev_incar = vasprun.incar
        self._structure = vasprun.final_structure

        if self.standardize:
            warnings.warn("Use of standardize=True with from_prev_run is not "
                          "recommended as there is no guarantee the copied "
                          "files will be appropriate for the standardized "
                          "structure.")

        self.nbands = int(vasprun.parameters["NBANDS"])
        if self.mode.upper() == "DIAG":
            self.nbands = int(np.ceil(self.nbands * self.nbands_factor /
                                      self.ncores) * self.ncores)

        # copy WAVECAR, WAVEDER (derivatives)
        files_to_transfer = {}
        if self.copy_wavecar:
            for fname in ("WAVECAR", "WAVEDER", "WFULL"):
                w = sorted(glob.glob(str(Path(prev_calc_dir) / (fname + "*"))))
                if w:
                    if fname == "WFULL":
                        for f in w:
                            fname = Path(f).name
                            fname = fname.split(".")[0]
                            files_to_transfer[fname] = f
                    else:
                        files_to_transfer[fname] = str(w[-1])

        self.files_to_transfer.update(files_to_transfer)

        return self

    @classmethod
    def from_prev_calc(cls, prev_calc_dir, mode="DIAG", **kwargs):
        """
        Generate a set of Vasp input files for GW or BSE calculations from a
        directory of previous Exact Diag Vasp run.

        Args:
            prev_calc_dir (str): The directory contains the outputs(
                vasprun.xml of previous vasp run.
            mode (str): Supported modes are "STATIC", "DIAG" (default), "GW",
                and "BSE".
            **kwargs: All kwargs supported by MVLGWSet, other than structure,
                prev_incar and mode, which are determined from the
                prev_calc_dir.
        """
        input_set = cls(_dummy_structure, mode=mode, **kwargs)
        return input_set.override_from_prev_calc(prev_calc_dir=prev_calc_dir)


class MVLSlabSet(MPRelaxSet):
    """
    Class for writing a set of slab vasp runs,
    including both slabs (along the c direction) and orient unit cells (bulk),
    to ensure the same KPOINTS, POTCAR and INCAR criterion.

    Args:
        k_product: default to 50, kpoint number * length for a & b directions,
            also for c direction in bulk calculations
        bulk (bool): Set to True for bulk calculation. Defaults to False.
        **kwargs: Other kwargs supported by :class:`DictSet`.
    """

    def __init__(self, structure, k_product=50, bulk=False,
                 auto_dipole=False, set_mix=True, sort_structure=True,
                 **kwargs):
        super().__init__(structure, **kwargs)

        if sort_structure:
            structure = structure.get_sorted_structure()

        self.k_product = k_product
        self.bulk = bulk
        self.auto_dipole = auto_dipole
        self.kwargs = kwargs
        self.set_mix = set_mix
        self.kpt_calc = None

        slab_incar = {"EDIFF": 1e-4, "EDIFFG": -0.02, "ENCUT": 400,
                      "ISMEAR": 0, "SIGMA": 0.05, "ISIF": 3}
        if not self.bulk:
            slab_incar["ISIF"] = 2
            slab_incar["LVTOT"] = True
            if self.set_mix:
                slab_incar["AMIN"] = 0.01
                slab_incar["AMIX"] = 0.2
                slab_incar["BMIX"] = 0.001
            slab_incar["NELMIN"] = 8
            if self.auto_dipole:
                weights = [s.species.weight for s in structure]
                center_of_mass = np.average(structure.frac_coords,
                                            weights=weights, axis=0)

                slab_incar["IDIPOL"] = 3
                slab_incar["LDIPOL"] = True
                slab_incar["DIPOL"] = center_of_mass

        self._config_dict["INCAR"].update(slab_incar)

    @property
    def kpoints(self):
        """
        k_product, default to 50, is kpoint number * length for a & b
            directions, also for c direction in bulk calculations
        Automatic mesh & Gamma is the default setting.
        """

        # To get input sets, the input structure has to has the same number
        # of required parameters as a Structure object (ie. 4). Slab
        # attributes aren't going to affect the VASP inputs anyways so
        # converting the slab into a structure should not matter

        kpt = super().kpoints
        kpt.comment = "Automatic mesh"
        kpt.style = 'Gamma'

        # use k_product to calculate kpoints, k_product = kpts[0][0] * a
        lattice_abc = self.structure.lattice.abc
        kpt_calc = [int(self.k_product / lattice_abc[0] + 0.5),
                    int(self.k_product / lattice_abc[1] + 0.5), 1]

        self.kpt_calc = kpt_calc
        # calculate kpts (c direction) for bulk. (for slab, set to 1)
        if self.bulk:
            kpt_calc[2] = int(self.k_product / lattice_abc[2] + 0.5)

        kpt.kpts[0] = kpt_calc

        return kpt

    def as_dict(self, verbosity=2):
        d = MSONable.as_dict(self)
        if verbosity == 1:
            d.pop("structure", None)
        return d


class MVLGBSet(MPRelaxSet):
    """
    Class for writing a vasp input files for grain boundary calculations, slab
    or bulk.

    Args:
        structure(Structure): provide the structure
        k_product: Kpoint number * length for a & b directions, also for c
            direction in bulk calculations. Default to 40.
        slab_mode (bool): Defaults to False. Use default (False) for a
            bulk supercell. Use True if you are performing calculations on a
            slab-like (i.e., surface) of the GB, for example, when you are
            calculating the work of separation.
        is_metal (bool): Defaults to True. This determines whether an ISMEAR of
            1 is used (for metals) or not (for insulators and semiconductors)
            by default. Note that it does *not* override user_incar_settings,
            which can be set by the user to be anything desired.
        **kwargs:
            Other kwargs supported by :class:`MPRelaxSet`.
    """

    def __init__(self, structure, k_product=40, slab_mode=False, is_metal=True,
                 **kwargs):
        super().__init__(structure, **kwargs)
        self.k_product = k_product
        self.slab_mode = slab_mode
        self.is_metal = is_metal

    @property
    def kpoints(self):
        """
        k_product, default to 40, is kpoint number * length for a & b
        directions, also for c direction in bulk calculations
        Automatic mesh & Gamma is the default setting.
        """

        # To get input sets, the input structure has to has the same number
        # of required parameters as a Structure object.

        kpt = super().kpoints
        kpt.comment = "Generated by pymatgen's MVLGBSet"
        kpt.style = 'Gamma'

        # use k_product to calculate kpoints, k_product = kpts[0][0] * a
        lengths = self.structure.lattice.abc
        kpt_calc = [int(self.k_product / lengths[0] + 0.5),
                    int(self.k_product / lengths[1] + 0.5),
                    int(self.k_product / lengths[2] + 0.5)]

        if self.slab_mode:
            kpt_calc[2] = 1

        kpt.kpts[0] = kpt_calc

        return kpt

    @property
    def incar(self):
        incar = super().incar

        # The default incar setting is used for metallic system, for
        # insulator or semiconductor, ISMEAR need to be changed.
        incar.update({
            "LCHARG": False,
            "NELM": 60,
            "PREC": "Normal",
            "EDIFFG": -0.02,
            "ICHARG": 0,
            "NSW": 200,
            "EDIFF": 0.0001
        })

        if self.is_metal:
            incar["ISMEAR"] = 1
            incar["LDAU"] = False

        if self.slab_mode:
            # for clean grain boundary and bulk relaxation, full optimization
            # relaxation (ISIF=3) is used. For slab relaxation (ISIF=2) is used.
            incar["ISIF"] = 2
            incar["NELMIN"] = 8

        incar.update(self.user_incar_settings)

        return incar


class MVLRelax52Set(DictSet):
    """
    Implementation of VaspInputSet utilizing the public Materials Project
    parameters for INCAR & KPOINTS and VASP's recommended PAW potentials for
    POTCAR.

    Keynotes from VASP manual:
        1. Recommended potentials for calculations using vasp.5.2+
        2. If dimers with short bonds are present in the compound (O2, CO,
            N2, F2, P2, S2, Cl2), it is recommended to use the h potentials.
            Specifically, C_h, O_h, N_h, F_h, P_h, S_h, Cl_h
        3. Released on Oct 28, 2018 by VASP. Please refer to VASP
            Manual 1.2, 1.3 & 10.2.1 for more details.

    Args:
        structure (Structure): input structure.
        potcar_functional (str): choose from "PBE_52" and "PBE_54".
        **kwargs: Other kwargs supported by :class:`DictSet`.
    """
    CONFIG = _load_yaml_config("MVLRelax52Set")

    def __init__(self, structure, potcar_functional="PBE_52", **kwargs):
        if potcar_functional not in ["PBE_52", "PBE_54"]:
            raise ValueError("Please select from PBE_52 and PBE_54!")

        super().__init__(structure, MVLRelax52Set.CONFIG,
                         potcar_functional=potcar_functional, **kwargs)
        self.kwargs = kwargs


class MITNEBSet(MITRelaxSet):
    """
    Class for writing NEB inputs. Note that EDIFF is not on a per atom
    basis for this input set.

    Args:
        unset_encut (bool): Whether to unset ENCUT.
        **kwargs: Other kwargs supported by :class:`DictSet`.
    """

    def __init__(self, structures, unset_encut=False, **kwargs):
        if len(structures) < 3:
            raise ValueError("You need at least 3 structures for an NEB.")
        kwargs["sort_structure"] = False
        super().__init__(structures[0], **kwargs)
        self.structures = self._process_structures(structures)
        self.unset_encut = False
        if unset_encut:
            self._config_dict["INCAR"].pop("ENCUT", None)

        if "EDIFF" not in self._config_dict["INCAR"]:
            self._config_dict["INCAR"]["EDIFF"] = self._config_dict[
                "INCAR"].pop("EDIFF_PER_ATOM")

        # NEB specific defaults
        defaults = {'IMAGES': len(structures) - 2, 'IBRION': 1, 'ISYM': 0,
                    'LCHARG': False, "LDAU": False}
        self._config_dict["INCAR"].update(defaults)

    @property
    def poscar(self):
        return Poscar(self.structures[0])

    @property
    def poscars(self):
        return [Poscar(s) for s in self.structures]

    @staticmethod
    def _process_structures(structures):
        """
        Remove any atom jumps across the cell
        """
        input_structures = structures
        structures = [input_structures[0]]
        for s in input_structures[1:]:
            prev = structures[-1]
            for i in range(len(s)):
                t = np.round(prev[i].frac_coords - s[i].frac_coords)
                if np.any(np.abs(t) > 0.5):
                    s.translate_sites([i], t, to_unit_cell=False)
            structures.append(s)
        return structures

    def write_input(self, output_dir, make_dir_if_not_present=True,
                    write_cif=False, write_path_cif=False,
                    write_endpoint_inputs=False):
        """
        NEB inputs has a special directory structure where inputs are in 00,
        01, 02, ....

        Args:
            output_dir (str): Directory to output the VASP input files
            make_dir_if_not_present (bool): Set to True if you want the
                directory (and the whole path) to be created if it is not
                present.
            write_cif (bool): If true, writes a cif along with each POSCAR.
            write_path_cif (bool): If true, writes a cif for each image.
            write_endpoint_inputs (bool): If true, writes input files for
                running endpoint calculations.
        """
        output_dir = Path(output_dir)
        if make_dir_if_not_present and not output_dir.exists():
            output_dir.mkdir(parents=True)
        self.incar.write_file(str(output_dir / 'INCAR'))
        self.kpoints.write_file(str(output_dir / 'KPOINTS'))
        self.potcar.write_file(str(output_dir / 'POTCAR'))

        for i, p in enumerate(self.poscars):
            d = output_dir / str(i).zfill(2)
            if not d.exists():
                d.mkdir(parents=True)
            p.write_file(str(d / 'POSCAR'))
            if write_cif:
                p.structure.to(filename=str(d / '{}.cif'.format(i)))
        if write_endpoint_inputs:
            end_point_param = MITRelaxSet(
                self.structures[0],
                user_incar_settings=self.user_incar_settings)

            for image in ['00', str(len(self.structures) - 1).zfill(2)]:
                end_point_param.incar.write_file(
                    str(output_dir / image / 'INCAR'))
                end_point_param.kpoints.write_file(
                    str(output_dir / image / 'KPOINTS'))
                end_point_param.potcar.write_file(
                    str(output_dir / image / 'POTCAR'))
        if write_path_cif:
            sites = set()
            lat = self.structures[0].lattice
            for site in chain(*(s.sites for s in self.structures)):
                sites.add(
                    PeriodicSite(site.species, site.frac_coords, lat))
            nebpath = Structure.from_sites(sorted(sites))
            nebpath.to(filename=str(output_dir / 'path.cif'))


class MITMDSet(MITRelaxSet):
    """
    Clas for writing a vasp md run. This DOES NOT do multiple stage
    runs.

    Args:
        structure (Structure): Input structure.
        start_temp (int): Starting temperature.
        end_temp (int): Final temperature.
        nsteps (int): Number of time steps for simulations. NSW parameter.
        time_step (int): The time step for the simulation. The POTIM
            parameter. Defaults to 2fs.
        spin_polarized (bool): Whether to do spin polarized calculations.
            The ISPIN parameter. Defaults to False.
        **kwargs: Other kwargs supported by :class:`DictSet`.
    """

    def __init__(self, structure, start_temp, end_temp, nsteps, time_step=2,
                 spin_polarized=False, **kwargs):
        # MD default settings
        defaults = {'TEBEG': start_temp, 'TEEND': end_temp, 'NSW': nsteps,
                    'EDIFF_PER_ATOM': 0.000001, 'LSCALU': False,
                    'LCHARG': False,
                    'LPLANE': False, 'LWAVE': True, 'ISMEAR': 0,
                    'NELMIN': 4, 'LREAL': True, 'BMIX': 1,
                    'MAXMIX': 20, 'NELM': 500, 'NSIM': 4, 'ISYM': 0,
                    'ISIF': 0, 'IBRION': 0, 'NBLOCK': 1, 'KBLOCK': 100,
                    'SMASS': 0, 'POTIM': time_step, 'PREC': 'Low',
                    'ISPIN': 2 if spin_polarized else 1,
                    "LDAU": False}

        super().__init__(structure, **kwargs)

        self.start_temp = start_temp
        self.end_temp = end_temp
        self.nsteps = nsteps
        self.time_step = time_step
        self.spin_polarized = spin_polarized
        self.kwargs = kwargs

        # use VASP default ENCUT
        self._config_dict["INCAR"].pop('ENCUT', None)

        if defaults['ISPIN'] == 1:
            self._config_dict["INCAR"].pop('MAGMOM', None)
        self._config_dict["INCAR"].update(defaults)

    @property
    def kpoints(self):
        return Kpoints.gamma_automatic()


class MPMDSet(MPRelaxSet):
    """
    This a modified version of the old MITMDSet pre 2018/03/12.

    This set serves as the basis for the amorphous skyline paper.

    (1) Aykol, M.; Dwaraknath, S. S.; Sun, W.; Persson, K. A. Thermodynamic
        Limit for Synthesis of Metastable Inorganic Materials. Sci. Adv. 2018,
        4 (4).

    Class for writing a vasp md run. This DOES NOT do multiple stage runs.
    Precision remains normal, to increase accuracy of stress tensor.

    Args:
        structure (Structure): Input structure.
        start_temp (int): Starting temperature.
        end_temp (int): Final temperature.
        nsteps (int): Number of time steps for simulations. NSW parameter.
        time_step (int): The time step for the simulation. The POTIM
            parameter. Defaults to 2fs.
        spin_polarized (bool): Whether to do spin polarized calculations.
            The ISPIN parameter. Defaults to False.
        **kwargs: Other kwargs supported by :class:`DictSet`.
    """

    def __init__(self, structure, start_temp, end_temp, nsteps,
                 spin_polarized=False, **kwargs):

        # MD default settings
        defaults = {'TEBEG': start_temp, 'TEEND': end_temp, 'NSW': nsteps,
                    'EDIFF_PER_ATOM': 0.00001, 'LSCALU': False,
                    'LCHARG': False,
                    'LPLANE': False, 'LWAVE': True, 'ISMEAR': 0,
                    'NELMIN': 4, 'LREAL': True, 'BMIX': 1,
                    'MAXMIX': 20, 'NELM': 500, 'NSIM': 4, 'ISYM': 0,
                    'ISIF': 0, 'IBRION': 0, 'NBLOCK': 1, 'KBLOCK': 100,
                    'SMASS': 0, 'POTIM': 2, 'PREC': 'Normal',
                    'ISPIN': 2 if spin_polarized else 1,
                    "LDAU": False, 'ADDGRID': True}

        if Element('H') in structure.species:
            defaults['POTIM'] = 0.5
            defaults['NSW'] = defaults['NSW'] * 4

        super().__init__(structure, **kwargs)

        self.start_temp = start_temp
        self.end_temp = end_temp
        self.nsteps = nsteps
        self.spin_polarized = spin_polarized
        self.kwargs = kwargs

        # use VASP default ENCUT
        self._config_dict["INCAR"].pop('ENCUT', None)

        if defaults['ISPIN'] == 1:
            self._config_dict["INCAR"].pop('MAGMOM', None)
        self._config_dict["INCAR"].update(defaults)

    @property
    def kpoints(self):
        return Kpoints.gamma_automatic()


class MVLNPTMDSet(MITMDSet):
    """
    Class for writing a vasp md run in NPT ensemble.

    Notes:
        To eliminate Pulay stress, the default ENCUT is set to a rather large
        value of ENCUT, which is 1.5 * ENMAX.

    Args:
        structure (Structure): input structure.
        start_temp (int): Starting temperature.
        end_temp (int): Final temperature.
        nsteps(int): Number of time steps for simulations. NSW parameter.
        time_step (int): The time step for the simulation. The POTIM
            parameter. Defaults to 2fs.
        spin_polarized (bool): Whether to do spin polarized calculations.
            The ISPIN parameter. Defaults to False.
        **kwargs: Other kwargs supported by :class:`DictSet`.
    """

    def __init__(self, structure, start_temp, end_temp, nsteps, time_step=2,
                 spin_polarized=False, **kwargs):
        user_incar_settings = kwargs.get("user_incar_settings", {})

        # NPT-AIMD default settings
        defaults = {"IALGO": 48,
                    "ISIF": 3,
                    "LANGEVIN_GAMMA": [10] * structure.ntypesp,
                    "LANGEVIN_GAMMA_L": 1,
                    "MDALGO": 3,
                    "PMASS": 10,
                    "PSTRESS": 0,
                    "SMASS": 0}

        defaults.update(user_incar_settings)
        kwargs["user_incar_settings"] = defaults

        super().__init__(structure, start_temp, end_temp,
                         nsteps, time_step, spin_polarized, **kwargs)

        # Set NPT-AIMD ENCUT = 1.5 * VASP_default
        enmax = [self.potcar[i].keywords['ENMAX']
                 for i in range(structure.ntypesp)]
        encut = max(enmax) * 1.5
        self._config_dict["INCAR"]["ENCUT"] = encut


class MVLScanRelaxSet(MPRelaxSet):
    """
    Class for writing a relax input set using Strongly Constrained and
    Appropriately Normed (SCAN) semilocal density functional.

    Notes:
        1. This functional is only available from VASP.5.4.3 upwards.

        2. Meta-GGA calculations require POTCAR files that include
        information on the kinetic energy density of the core-electrons,
        i.e. "PBE_52" or "PBE_54". Make sure the POTCAR including the
        following lines (see VASP wiki for more details):

            $ grep kinetic POTCAR
            kinetic energy-density
            mkinetic energy-density pseudized
            kinetic energy density (partial)

    Args:
        structure (Structure): input structure.
        potcar_functional (str): choose from "PBE_52" and "PBE_54".
        vdw (str): set "rVV10" to enable SCAN+rVV10, which is a versatile
            van der Waals density functional by combing the SCAN functional
            with the rVV10 non-local correlation functional.
        **kwargs: Other kwargs supported by :class:`DictSet`.
    """

    def __init__(self, structure, potcar_functional="PBE_52", **kwargs):
        if potcar_functional not in ["PBE_52", "PBE_54"]:
            raise ValueError("SCAN calculations required PBE_52 or PBE_54!")

        super().__init__(structure, potcar_functional=potcar_functional,
                         **kwargs)

        self._config_dict["INCAR"].update({"ADDGRID": True,
                                           "EDIFF": 1e-05,
                                           "EDIFFG": -0.05,
                                           "LASPH": True,
                                           "LDAU": False,
                                           "METAGGA": "SCAN",
                                           "NELM": 200})


class LobsterSet(MPRelaxSet):
    CONFIG = _load_yaml_config("MPRelaxSet")
    """
    Input set to prepare VASP runs that can be digested by Lobster (See cohp.de)

    Args:
        structure (Structure): input structure.
        isym (int): ISYM entry for INCAR, only isym=-1 and isym=0 are allowed
        ismear (int): ISMEAR entry for INCAR, only ismear=-5 and ismear=0 are allowed
        reciprocal_density (int): density of k-mesh by reciprocal volume
        potcar_functional (string): only PBE_54, PBE_52 and PBE are recommended at the moment
        **kwargs: Other kwargs supported by :class:`DictSet`.

    """

    def __init__(self, structure: Structure, isym=-1, ismear=-5, reciprocal_density=None, potcar_functional="PBE_54",
                 **kwargs):
        warnings.warn("Make sure that all parameters are okay! This is a brand new implementation.")

        if not (isym == -1 or isym == 0):
            raise ValueError("Lobster cannot digest WAVEFUNCTIONS with symmetry")
        if not (ismear == -5 or ismear == 0):
            raise ValueError("Lobster usually works with ismear=-5 or ismear=0")

        # newest potcars are preferred
        super().__init__(structure, potcar_functional=potcar_functional, **kwargs)

        # reciprocal density
        if self.user_kpoints_settings is not None:
            if (not reciprocal_density or "reciprocal_density" not in self.user_kpoints_settings):
                # test, if this is okay
                self.reciprocal_density = 310
            else:
                self.reciprocal_density = reciprocal_density or \
                                          self.user_kpoints_settings['reciprocal_density']
        else:
            if (not reciprocal_density):
                # test, if this is okay
                self.reciprocal_density = 310
            else:
                self.reciprocal_density = reciprocal_density

        # might need to be adapted in the future
        ediff_per_atom = 5e-05

        self.isym = isym
        self.ismear = ismear
        # predefined basis! Check if the basis is okay! (charge spilling and bandoverlaps!)
        basis = Lobsterin._get_basis(structure=structure,
                                     potcar_symbols=self.potcar_symbols)
        lobsterin = Lobsterin(settingsdict={"basisfunctions": basis})
        nbands = lobsterin._get_nbands(structure=structure)

        update_dict = {"EDIFF_PER_ATOM": ediff_per_atom, "NSW": 0, "LWAVE": True, "ISYM": isym, "NBANDS": nbands,
                       "IBRION": -1, "ISMEAR": ismear, "LORBIT": 11, "ICHARG": 0, "ALGO": "Normal"}

        self._config_dict["INCAR"].update(update_dict)
        self._config_dict["KPOINTS"].update({"reciprocal_density": self.reciprocal_density})


def get_vasprun_outcar(path, parse_dos=True, parse_eigen=True):
    path = Path(path)
    vruns = list(glob.glob(str(path / "vasprun.xml*")))
    outcars = list(glob.glob(str(path / "OUTCAR*")))

    if len(vruns) == 0 or len(outcars) == 0:
        raise ValueError(
            "Unable to get vasprun.xml/OUTCAR from prev calculation in %s" %
            path)
    vsfile_fullpath = str(path / "vasprun.xml")
    outcarfile_fullpath = str(path / "OUTCAR")
    vsfile = vsfile_fullpath if vsfile_fullpath in vruns else sorted(vruns)[-1]
    outcarfile = outcarfile_fullpath if outcarfile_fullpath in outcars else \
        sorted(outcars)[-1]
    return (Vasprun(vsfile, parse_dos=parse_dos, parse_eigen=parse_eigen),
            Outcar(outcarfile))


def get_structure_from_prev_run(vasprun, outcar=None):
    """
    Process structure from previous run.

    Args:
        vasprun (Vasprun): Vasprun that contains the final structure
            from previous run.
        outcar (Outcar): Outcar that contains the magnetization info from
            previous run.

    Returns:
        Returns the magmom-decorated structure that can be passed to get
        Vasp input files, e.g. get_kpoints.
    """
    structure = vasprun.final_structure

    site_properties = {}
    # magmom
    if vasprun.is_spin:
        if outcar and outcar.magnetization:
            site_properties.update({"magmom": [i['tot']
                                               for i in outcar.magnetization]})
        else:
            site_properties.update({"magmom": vasprun.parameters['MAGMOM']})
    # ldau
    if vasprun.parameters.get("LDAU", False):
        for k in ("LDAUU", "LDAUJ", "LDAUL"):
            vals = vasprun.incar[k]
            m = {}
            l_val = []
            s = 0
            for site in structure:
                if site.specie.symbol not in m:
                    m[site.specie.symbol] = vals[s]
                    s += 1
                l_val.append(m[site.specie.symbol])
            if len(l_val) == len(structure):
                site_properties.update({k.lower(): l_val})
            else:
                raise ValueError("length of list {} not the same as"
                                 "structure".format(l_val))

    return structure.copy(site_properties=site_properties)


def standardize_structure(structure, sym_prec=0.1,
                          international_monoclinic=True):
    """
    Get the symmetrically standardized structure.

    Args:
        structure (Structure): The structure.
        sym_prec (float): Tolerance for symmetry finding for standardization.
        international_monoclinic (bool): Whether to use international
            convention (vs Curtarolo) for monoclinic. Defaults True.

    Returns:
        The symmetrized structure.
    """
    sym_finder = SpacegroupAnalyzer(structure, symprec=sym_prec)
    new_structure = sym_finder.get_primitive_standard_structure(
        international_monoclinic=international_monoclinic)

    # the primitive structure finding has had several bugs in the past
    # defend through validation
    vpa_old = structure.volume / structure.num_sites
    vpa_new = new_structure.volume / new_structure.num_sites

    if abs(vpa_old - vpa_new) / vpa_old > 0.02:
        raise ValueError(
            "Standardizing cell failed! VPA old: {}, VPA new: {}".format(
                vpa_old, vpa_new))

    sm = StructureMatcher()
    if not sm.fit(structure, new_structure):
        raise ValueError(
            "Standardizing cell failed! Old structure doesn't match new.")

    return new_structure


class BadInputSetWarning(UserWarning):
    pass


def batch_write_input(structures, vasp_input_set=MPRelaxSet, output_dir=".",
                      make_dir_if_not_present=True, subfolder=None,
                      sanitize=False, include_cif=False, **kwargs):
    """
    Batch write vasp input for a sequence of structures to
    output_dir, following the format output_dir/{group}/{formula}_{number}.

    Args:
        structures ([Structure]): Sequence of Structures.
        vasp_input_set (VaspInputSet): VaspInputSet class that creates
            vasp input files from structures. Note that a class should be
            supplied. Defaults to MPRelaxSet.
        output_dir (str): Directory to output files. Defaults to current
            directory ".".
        make_dir_if_not_present (bool): Create the directory if not present.
            Defaults to True.
        subfolder (callable): Function to create subdirectory name from
            structure. Defaults to simply "formula_count".
        sanitize (bool): Boolean indicating whether to sanitize the
            structure before writing the VASP input files. Sanitized output
            are generally easier for viewing and certain forms of analysis.
            Defaults to False.
        include_cif (bool): Whether to output a CIF as well. CIF files are
            generally better supported in visualization programs.
        **kwargs: Additional kwargs are passed to the vasp_input_set class
            in addition to structure.
    """
    output_dir = Path(output_dir)
    for i, s in enumerate(structures):
        formula = re.sub(r'\s+', "", s.formula)
        if subfolder is not None:
            subdir = subfolder(s)
            d = output_dir / subdir
        else:
            d = output_dir / '{}_{}'.format(formula, i)
        if sanitize:
            s = s.copy(sanitize=True)
        v = vasp_input_set(s, **kwargs)
        v.write_input(str(d), make_dir_if_not_present=make_dir_if_not_present,
                      include_cif=include_cif)


_dummy_structure = Structure([1, 0, 0, 0, 1, 0, 0, 0, 1], ['I'], [[0, 0, 0]],
                             site_properties={"magmom": [[0, 0, 1]]})
