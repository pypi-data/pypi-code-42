#!/usr/bin/env python

"""
Read protein match output produced by alignment-panel-civ.py and group it by
pathogen (either virus or bacteria).

This is currently only useful when you are matching against a subject protein
database whose titles have a pathogen accession number in the 5th |-separated
field, like this:

civ|GENBANK|YP_008686600.1|GENBANK|NC_022580.1|glycoprotein [pathogen name]
civ|GENBANK|YP_008686601.1|GENBANK|NC_022580.1|L protein [pathogen name]
civ|GENBANK|YP_008686602.1|GENBANK|NC_022581.1|nucleoprotein [pathogen name]

In this case, the first two matched subjects are from the same pathogen
(accession NC_022580.1). This script will gather those matches under their
common accession number and provides methods to print them.

Files with names in this format are generated by the make-protein-database.py
script in this directory and are used in databases such as RVDB.

Note that the *only* part of the title that is used in this script is the
pathogen accession number. The product (e.g., nucleoprotein) and pathogen name
are just there to ease human reading of the matches. The accession number is
looked up in a passed database (created with make-protein-database.py)

The script reads *file names* from standard input, and writes to standard
output.  Alternately, you can also provide file names on the command line.

Typical usage:

  $ find . -name summary-proteins |
        proteins-to-pathogens-civ.py --html [options] > index.html

Input files must contain lines in the following format:

0.01 58.9 58.9 1 1 1772 title
0.01 58.9 58.9 1 1 1772 title
0.09 51.8 57.4 2 2 3481 title

Fields must be whitespace separated. The seven fields are:

    Coverage
    Median bit score
    Best bit score
    Read count
    HSP count
    Protein length (in amino acids)
    Title (in the above-mentioned "protein name [pathogen name]" format)

"""

from __future__ import print_function
import argparse
import sys

# It's not clear that the PDF backend is the right choice here, but it
# works (i.e., the generation of PNG images works fine).
import matplotlib
matplotlib.use('PDF')

# These imports are here because dark.civ.proteins imports
# matplotlib.pyplot and we need to set the matplotlib backend before the
# import. So please don't move this import higher in this file.

from dark.civ.proteins import ProteinGrouper, SqliteIndex
from dark.taxonomy import Taxonomy


def main(db, taxdb, args):
    grouper = ProteinGrouper(db, taxdb,
                             assetDir=args.assetDir,
                             sampleName=args.sampleName,
                             sampleNameRegex=args.sampleNameRegex,
                             format_=args.format,
                             saveReadLengths=args.showReadLengths,
                             titleRegex=args.titleRegex,
                             negativeTitleRegex=args.negativeTitleRegex,
                             pathogenDataDir=args.pathogenDataDir)

    if args.filenames:
        filenames = args.filenames
    else:
        filenames = (line[:-1] for line in sys.stdin)

    for filename in filenames:
        with open(filename) as fp:
            grouper.addFile(filename, fp)

    if args.html:
        print(grouper.toHTML(
            args.pathogenPanelFilename,
            minProteinFraction=args.minProteinFraction,
            pathogenType=args.pathogenType,
            title=args.title, preamble=args.preamble,
            sampleIndexFilename=args.sampleIndexFilename,
            omitVirusLinks=args.omitVirusLinks))
    else:
        print(grouper.toStr(
            title=args.title, preamble=args.preamble,
            pathogenType=args.pathogenType))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Group proteins by the pathogen they're from.")

    parser.add_argument(
        'filenames', nargs='*',
        help=('File names to read input from. The input will typically be '
              'generated by alignment-panel-civ.py'))

    parser.add_argument(
        '--proteinGenomeDatabase', required=True,
        help=('The filename of an Sqlite3 database holding protein and '
              'genome information, as built by make-protein-database.py'))

    parser.add_argument(
        '--taxonomyDatabase', required=True,
        help=('The file holding the sqlite3 taxonomy database. See '
              'https://github.com/acorg/ncbi-taxonomy-database for how to '
              'build one.'))

    # A mutually exclusive group for either --sampleName or --sampleNameRegex
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        '--sampleName',
        help=('An (optional) sample name. Use when all input files are for a '
              'single sample. Cannot be used with --sampleNameRegex.'))

    group.add_argument(
        '--sampleNameRegex',
        help=('An (optional) regular expression that can be used to extract a '
              'short sample name from full sample file name.  The regular '
              'expression must have a matching group (delimited by '
              'parentheses) that captures the part of the file name that '
              'should be used as the sample name.'))

    parser.add_argument(
        '--pathogenPanelFilename',
        help=('An (optional) filename to write a pathogen-sample panel PNG '
              'image to.'))

    parser.add_argument(
        '--sampleIndexFilename',
        help=('An (optional) filename to write a sample index file to. '
              'Lines in the file will have an integer index, a space, and '
              'then the sample name. Only produced if --html is used '
              '(because the pathogen-NNN-sample-MMM.fastq are only written '
              'in that case).'))

    parser.add_argument(
        '--html', default=False, action='store_true',
        help='If specified, output HTML instead of plain text.')

    parser.add_argument(
        '--format', default='fasta', choices=('fasta', 'fastq'),
        help=('Give the format of the sequence files written by '
              'alignment-panel-civ.py.'))

    parser.add_argument(
        '--minProteinFraction', type=float, default=0.0,
        help=('The minimum fraction of proteins in a pathogen that must be '
              'matched by a particular sample in order for that pathogen to '
              'be displayed for that sample.'))

    parser.add_argument(
        '--pathogenType', default='viral', choices=('bacterial', 'viral'),
        help=('Specify the pathogen type. This option only affects the '
              'language used in HTML output.'))

    parser.add_argument(
        '--showReadLengths', default=False, action='store_true',
        help=('If specified, the HTML output (use --html to get this) will '
              'contain the lengths of all reads that match proteins for a '
              'pathogen.'))

    parser.add_argument(
        '--assetDir', default='out',
        help=('The output directory where noninteractive-alignment-panel.py '
              'put its plots and FASTA/FASTQ files.'))

    parser.add_argument(
        '--pathogenDataDir', default='pathogen-data',
        help=('The directory where per-pathogen information (e.g., collected '
              'reads across all samples) should be written.'))

    parser.add_argument(
        '--title', default='Summary of pathogens',
        help='The title to show at the top of the output.')

    parser.add_argument(
        '--preamble',
        help='Optional preamble text to show after the title.')

    parser.add_argument(
        '--titleRegex', default=None,
        help='A regex that pathogen names must match.')

    parser.add_argument(
        '--negativeTitleRegex', default=None,
        help='a regex that pathogen names must not match.')

    parser.add_argument(
        '--omitVirusLinks', default=False, action='store_true',
        help=('If specified, the HTML output (use --html to get this) for '
              'viruses will not contain links to ICTV and ViralZone. '
              'This should be used when working with viruses that do not yet '
              'have names that can be looked up.'))

    args = parser.parse_args()

    if not args.html:
        if args.sampleIndexFilename:
            print('It does not make sense to use --sampleIndexFilename '
                  'without also using --html', file=sys.stderr)
            sys.exit(1)
        if args.omitVirusLinks:
            print('It does not make sense to use --omitVirusLinks '
                  'without also using --html', file=sys.stderr)
            sys.exit(1)

    if args.omitVirusLinks and args.pathogenType != 'viral':
        print('The --omitVirusLinks option only makes sense with '
              '--pathogenType viral', file=sys.stderr)
        sys.exit(1)

    with SqliteIndex(args.proteinGenomeDatabase) as db, \
            Taxonomy(args.taxonomyDatabase) as taxdb:
        main(db, taxdb, args)
