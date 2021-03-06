##
## Main driver for running RNA-Seq pipeline
##
import os
import sys
import time

import rnaseqlib
import rnaseqlib.utils as utils
import rnaseqlib.settings as settings
import rnaseqlib.Pipeline as rna_pipeline
import rnaseqlib.RNABase as rna_base

def run_pipeline(settings_filename,
                 output_dir):
    """
    Run pipeline on all samples given settings file.
    """
    # Create pipeline instance
    pipeline = rna_pipeline.Pipeline(settings_filename,
                                     output_dir)
    # Run pipeline
    pipeline.run()

    
def run_on_sample(sample_label,
                  settings_filename,
                  output_dir):
    """
    Run pipeline on one particular sample.
    """
    pipeline = rna_pipeline.Pipeline(settings_filename,
                                     output_dir,
                                     curr_sample=sample_label)
    pipeline.run_on_sample(sample_label)


def check_requirements():
    print "Checking that all required programs are available..."
    # Utilities that need to be on path for pipeline to run
    REQUIRED_PROGRAMS = [# UCSC utils
                         "genePredToGtf",
                         # Tophat/Bowtie
                         "bowtie-build",
                         "tophat",
                         # Bedtools
                         "intersectBed",
                         "subtractBed",
                         "sortBed",
                         "mergeBed",
                         "tagBam",
                         # Related utils
                         "gtf2gff3.pl",
                         # Unix utils
                         "gunzip",
                         "wget",
                         "cat",
                         "zcat",
                         "cut"]
    found_all = True
    for program in REQUIRED_PROGRAMS:
        if utils.which(program) is None:
            print "WARNING: Cannot find required program \'%s\' " \
                  "on your path.  Please install it or add it. " \
                  "to your path if already installed." %(program)
            if program == "genePredToGtf":
                genePredToGtf_msg()
            elif program == "gtf2gff3.pl":
                gtf2gff3_msg()
            print "  - Proceeding anyway..."
            found_all = False
    if found_all:
        print "Found all required programs."
    else:
        # Do not proceed if programs not found.
        sys.exit(1)


def gtf2gff3_msg():
    print "To get gtf2gff3.pl, see: "
    print "http://cpansearch.perl.org/src/LDS/GBrowse-2.12/bin/gtf2gff3.pl"
    
        
def genePredToGtf_msg():
    print "To install genePredToGtf, download the executable for your OS " \
          "from: "
    print "http://hgdownload.cse.ucsc.edu/admin/exe/"
    print "And place the executable in your PATH."


def initialize_pipeline(genome,
                        output_dir,
                        init_params={}):
    """
    Initialize the pipeline.
    """
    # Check for required programs
    check_requirements()
    base_obj = rna_base.RNABase(genome, output_dir,
                                init_params=init_params)
    base_obj.initialize()


def greeting(parser=None):
    print "rnaseqlib: a lightweight pipeline for RNA-Seq analysis"
    print "=" * 10
    if parser is not None:
        parser.print_help()
    
    
def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--run", dest="run", action="store_true",
                      default=False,
                      help="Run pipeline.")
    parser.add_option("--run-on-sample", dest="run_on_sample", nargs=1, default=None,
                      help="Run on a particular sample. Takes as input the sample label.")
    parser.add_option("--settings", dest="settings", nargs=1,
                      default=None,
                      help="Settings filename.")
    parser.add_option("--init", dest="initialize", nargs=1, default=None,
                      help="Initialize the pipeline. Takes as input a genome, "
                      "e.g. mm9 or hg18")
    parser.add_option("--output-dir", dest="output_dir", nargs=1,
                      default=None,
                      help="Output directory.")
    ##
    ## Options related to --init
    ##
    parser.add_option("--frac-constitutive", dest="frac_constitutive",
                      nargs=1, default=0.7, type="float",
                      help="Fraction (number between 0 and 1) of " \
                      "transcripts that an exon can be in to be considered " \
                      "constitutive. Default is 0.7 (i.e. 70% of " \
                      "transcripts.) [OBSOLETE]")
    parser.add_option("--constitutive-exon-diff", dest="constitutive_exon_diff",
                      nargs=1, default=10, type="int",
                      help="Number of \'wiggle\' bases by which an exon can " \
                      "differ in order to be considered constitutive. By " \
                      "default set to 10. [OBSOLETE]")
    (options, args) = parser.parse_args()

    greeting()

    if options.output_dir == None:
        print "Error: need --output-dir argument."
        parser.print_help()
        sys.exit(1)
        
    output_dir = utils.pathify(options.output_dir)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    settings_filename = None
    if options.run:
        if options.settings == None:
            # Running of pipeline requires settings filename
            print "Error: need --settings"
            parser.print_help()
            sys.exit(1)
        settings_filename = utils.pathify(options.settings)
        run_pipeline(settings_filename,
                     output_dir)

    if options.run_on_sample is not None:
        if options.settings == None:
            # Running of pipeline requires settings filename
            print "Error: need --settings"
            parser.print_help()
            sys.exit(1)
        settings_filename = utils.pathify(options.settings)
        sample_label = options.run_on_sample
        run_on_sample(sample_label, settings_filename,
                      output_dir)

    if options.initialize is not None:
        # Parse initialization-related settings
        frac_constitutive = float(options.frac_constitutive)
        constitutive_exon_diff = int(options.constitutive_exon_diff)
        init_params = {"frac_constitutive": frac_constitutive,
                       "constitutive_exon_diff": constitutive_exon_diff}
        genome = options.initialize
        initialize_pipeline(genome,
                            output_dir,
                            init_params=init_params)
    

if __name__ == '__main__':
    main()
