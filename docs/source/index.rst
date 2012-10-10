.. include:: <isogrk3.txt>

.. documentation master file, created by .. 
   sphinx-quickstart on Fri Oct 22 16:50:57 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.



.. contents::


``rnaseqlib``
=============

``rnaseqlib`` is a simple, lightweight pipeline for RNA-Seq analysis. 


Features
========

* Pipeline for analyzing RNA-Seq data:
  - Maps reads to genome and splice junctions
  - Computes basic quality control statistics
  - Outputs RPKM values for genes
* Includes support for Ribosome Footprinting data (Ribo-Seq) and CLIP (CLIP-Seq)


Updates
=======

**2012**

* ...


Installation
============

To install: ::

  easy_install rnaseqlib

For local installation, use: ::

  easy_install --user -U rnaseqlib


Testing ``rnaseqlib``
---------------------
.. _Testing rnaseqlib


Overview
========
.. _config:

Configuration
-------------


  [data]
  # directory where BAM files are
  bam_prefix = ./test-data/bam-data/
  # directory where MISO output is
  miso_prefix = ./test-data/miso-data/

  bam_files = [
      "heartWT1.sorted.bam",
      "heartWT2.sorted.bam",
      "heartKOa.sorted.bam",
      "heartKOb.sorted.bam"]

  miso_files = [
      "heartWT1",
      "heartWT2",
      "heartKOa",
      "heartKOb"]

  [plotting]
  # Dimensions of figure to be plotted (in inches)
  fig_width = 7
  fig_height = 5 
  # Factor to scale down introns and exons by
  intron_scale = 30
  exon_scale = 4
  # Whether to use a log scale or not when plotting
  logged = False 
  font_size = 6

  # Max y-axis
  ymax = 150

  # Whether to plot posterior distributions inferred by MISO
  show_posteriors = True 

  # Whether to show posterior distributions as bar summaries
  bar_posteriors = False

  # Whether to plot the number of reads in each junction
  number_junctions = True

  resolution = .5
  posterior_bins = 40
  gene_posterior_ratio = 5

  # List of colors for read denisites of each sample
  colors = [
      "#CC0011",
      "#CC0011",
      "#FF8800",
      "#FF8800"]

  # Number of mapped reads in each sample
  # (Used to normalize the read density for RPKM calculation)
  coverages = [
      6830944,
      14039751,
      4449737, 
      6720151]

  # Bar color for Bayes factor distribution
  # plots (--plot-bf-dist)
  # Paint them blue
  bar_color = "b"

  # Bayes factors thresholds to use for --plot-bf-dist
  bf_thresholds = [0, 1, 2, 5, 10, 20]

The above settings file specifies where the BAM files for each sample are (and their corresponding MISO output files) and also controls several useful plotting parameters. The parameters are:

 * ``bam_prefix``: directory where BAM files for the samples to plot are. These BAM files should be coordinate-sorted and indexed.
 * ``miso_prefix``: directory where MISO output directories are for the events to be plotted. For example, if plotting a skipped exon event for which the MISO output lives in ``/data/miso_output/SE/``, then ``miso_prefix`` should be set to ``/data/miso_output/SE``. 
 * ``bam_files``: list of BAM files for RNA-Seq samples in the order in which you'd like them to be plotted. Each value in the list should be a filename that resides in the directory specified by ``bam_prefix``.
 * ``miso_files``: list of MISO output directories for each sample. Should follow same order of samples as ``bam_files``. Each value in the list should be a MISO output directory that resides in the directory specified by ``miso_prefix``.

  .. note::
     ``sashimi_plot`` will look recursively in paths of ``miso_files`` to find the MISO output file (ending in ``.miso``) associated with the event that is being plotted. For example, if we have these settings: ::

         miso_prefix = /miso/output/
         miso_files = ['control']

     If our event is on a chromosome called ``chr7`` in the annotation, then the program will check every subdirectory of ``/miso/output/control`` for a directory called ``chr7``, and look for a file that has the form ``event_name.miso`` in that directory. If it cannot find such a directory in the first-level subdirectories, it will recurse into the subdirectories until it can find the file or until there are no more subdirectories to search.

* ``fig_width``: output figure's width (in inches.)
 * ``fig_height``: output figure's height (in inches.)
 * ``exon_scale`` / ``intron_scale``: factor by which to scale down exons and introns, respectively.
 * ``logged``: whether to log the RNA-Seq read densities (set to ``False`` for linear scaling)
 * ``ymax``: maximum value of y-axis for RNA-Seq read densities. If not given, then the highest y-axis value across all samples will be set for each, resulting in comparable y-scaling.
 * ``show_posteriors``: plot MISO posterior distributions if ``True``, do not if ``False``
 * ``bar_posteriors``: plot MISO posterior distributions not as histograms, but as a horizontal bar that simply shows the mean and confidence intervals of the distribution in each sample.
 * ``colors``: Colors to use for each sample. Colors should be listed in same order as ``bam_files`` and ``miso_files`` lists.
 * ``coverages``: Number of mapping reads in each sample, for use when when computing normalized (i.e. RPKM) RNA-Seq read densities. Should be listed in same order as ``bam_files`` and ``miso_files``. These numbers correspond to the "per million" denominators used for calculating RPKM.

**Additional parameters (all optional):**

 * ``sample_labels``: a list of string labels for each sample. By default, ``sashimi_plot`` will use the BAM filename from ``bam_files`` as the label for the sample. This option provides alternative labels. Note that ``sample_labels`` must have the same number of entries as ``bam_files``.
 * ``reverse_minus``: specifies whether minus strand (``-``) event isoforms are to be plotted in same direction as plus strand events. By default, set to ``False``, meaning minus strand events will be plotted in direction opposite to plus strand events.
 * ``nxticks``: number of x-axis ticks to plot
 * ``nyticks``: number of y-axis ticks to plot

.. note::
  For junction visualization, ``sashimi_plot`` currently uses only reads that cross *a single* junction. If a read crosses multiple exon-exon junctions, it is currently skipped, although MISO will use such a read in isoform estimation if it consistent with the given isoform annotation. Also, ``sashimi_plot`` currently ignores reads containing insertions or deletions and does not visualize sequence mismatches.
 
Command-line options
--------------------

``sashimi_plot/plot.py`` takes the following arguments: ::

  --plot-posterior
                        Plot the posterior distribution. Takes as input a raw
                        MISO output file (.miso)
  --plot-insert-len
                        Plot the insert length distribution from a given
                        insert length (*.insert_len) filename. Second
                        argument is a settings filename.
  --plot-bf-dist
                        Plot Bayes factor distributon. Takes the arguments:
                        (1) Bayes factor filename (*.miso_bf) settings
                        filename, (2) a settings filename.
  --plot-event
                        Plot read densities and MISO inferences for a given
                        alternative event. Takes the arguments: (1) event name
                        (i.e. the ID= of the event based on MISO gff3
                        annotation file, (2) directory where MISO output is
                        for that event type (e.g. if event is a skipped exon,
                        provide the directory where the output for all SE
                        events are), (3) path to plotting settings file.
  --output-dir
                        Output directory.



.. _plotting:

Visualizing and plotting MISO output
====================================

MISO comes with several built-in utilities for plotting its output, which all make use of the Python ``matplotlib`` environment package. These can be accessed through the ``plot.py`` utility.


Customizing the appearance of MISO estimates alongside raw RNA-Seq data
-----------------------------------------------------------------------

In the main example of ``--plot-event`` shown above, the MISO posterior distributions are shown fully as a histogram. Sometimes it's easier to compare a group of samples by just comparing the mean expression level (along with confidence intervals) in each sample, without plotting the entire distribution. Using the ``bar_posteriors`` option in the settings file, this can be done. Setting: ::

  bar_posteriors = True

yields the plot below:

.. image:: images/plot_event_bar_posteriors.png
  :scale: 80%
  :align: center
  :alt: Showing summaries of MISO posterior distributions as horizontal bars

The mean of each sample's posterior distribution over |Psi| is shown as a circle, with horizontal error bars extending to the upper and lower bounds of the confidence interval in each sample. Since the x-axis remains fixed in all samples, this makes it easy to visually compare the means of all samples and the overlap between their confidence intervals.

Plotting the distribution of events with Bayes factors
------------------------------------------------------

It is often useful to plot the distribution of events that meet various Bayes factor thresholds. For any Bayes factor threshold, we can compute the number of events that meet that threshold in a given comparison file and visualize this as a distribution. The option ``--plot-bf-dist`` does this, as follows: ::

  plot.py --plot-bf-dist control_vs_knockdown.miso_bf settings.txt --output-dir plots/

This will plot the distribution of events meeting various Bayes factors thresholds in the file ``control_vs_knockdown.miso_bf`` (outputted by calling ``--compare-samples`` in MISO) using the plotting settings file ``settings.txt``, and output the resulting plot to ``plots/``. The resulting plot will look like:
 
  .. figure:: images/bf_dist.png
      :scale: 50%
      :figclass: align-center
      :align: center
      :alt: Distribution of events meeting various Bayes factor thresholds

      *Distribution of events meeting various Bayes factor thresholds*

This figure shows the number of events (in logarithmic scale) in the ``.miso_bf`` file that have Bayes factor greater than or equal to 0, greater than or equal to 1, greater than or equal to 2, etc. all the way to events with Bayes factor greater than or equal to 20. 

The title of the plot says how many of the events in the input ``.miso_bf`` file were used in plotting the distribution. In the above example all 5231 entries in the file were used, but if the lowest Bayes factor threshold for the x-axis was set to be 2, for example, then only a subset of the entries would be plotted since there are events with Bayes factor less than 2. 

The color of the bars used in the plot and Bayes factor thresholds for the x-axis can be customized through the setting file options ``bar_color`` and ``bf_thresholds``, respectively. The default settings are: ::

  # Color of bar for --plot-bf-dist
  bar_color = "b"

  # Bayes factor thresholds for --plot-bf-dist
  bf_thresholds = [0, 1, 2, 5, 10, 20]


Plotting MISO estimates individually
------------------------------------

We can visualize posterior distributions as histograms using the ``--plot-posterior`` argument to ``plot.py``. For example, to plot the MISO posterior distribution of our example event in the ``heartKOa`` sample, run: ::

  python plot.py --plot-posterior "test-data/miso-data/heartKOa/chr17/chr17:45816186:45816265:-@chr17:45815912:45815950:-@chr17:45814875:45814965:-.miso" --output-dir test-plot

This will produce a PDF plot that looks like this:

.. image:: images/posterior_plot1.png
  :scale: 50%
  :align: center
  :alt: sashimi_plot of posterior distribution


Plotting insert length distributions and summary statistics
-----------------------------------------------------------

For paired-end RNA-Seq samples, we can visualize the insert length distribution. This distribution is informative about the quality of the RNA-Seq sample, since it can tell us how precisely or cleanly the insert length of interest was selected during the RNA-Seq library preparation. This distribution is also used by `MISO`_ in order to assign read pairs to isoforms, and so the tighter this distribution is, the more confident we can be in assigning read pairs to isoforms based on their insert length.

The distribution can be plotted using the ``--plot-insert-len`` option, which takes as input: (1) an insert length file (ending in ``.insert_len``) produced by MISO and (2) a plotting settings filename. For example: ::

  python plot.py --plot-insert-len sample.insert_len settings.txt --output-dir plots/

will produce a histogram of the insert length in ``sample.insert_len`` and place it in the ``plots`` directory. The histogram might look like this: 

.. image:: images/insert-length-dist.png
  :scale: 50%
  :align: center
  :alt: Insert length distribution plotted from a MISO insert length file


Frequently Asked Questions (FAQ)
================================

1. **I'd like to plot RNA-Seq data for my own annotations, which are not part of the MISO events. Can this be done?** 
Yes. ``sashimi_plot`` can plot any event, as long as it is specified in the GFF3 format and indexed by the ``index_gff.py`` script that we provide. See :ref:`indexing-annotation`.

2. **I get the error that the** ``.positions`` **field is undefined.** 
This is caused by using an older version of the `pysam`_ module. Upgrading to version 0.6 or higher fixes the issue.


.. note:: 
  Section under construction

.. _refs:
.. _katz:


Authors
=======

* Main feature (``--plot-event``) written by Eric T. Wang and Yarden Katz.
* Other features written by Yarden Katz.

Acknowledgements
================

Thanks to:

* Vincent Butty (MIT)
* Michael Lovci (UCSD)
* Sol Katzman (UCSC)
* Mohini Jangi (MIT)
* Paul Boutz (MIT)
* Sean O'Keeffe (Columbia)


References
==========

1. Katz Y, Wang ET, Airoldi EM, Burge CB. (2010). `Analysis and design of RNA sequencing experiments for identifying isoform regulation`_. Nature Methods 7, 1009-1015.

2. Wang ET, Sandberg R, Luo S, Khrebtukova I, Zhang L, Mayr C, Kingsmore SF, Schroth GP, Burge CB. (2008). Alternative Isoform Regulation in Human Tissue Transcriptomes. Nature 456, 470-476

.. _Analysis and design of RNA sequencing experiments for identifying isoform regulation: http://www.nature.com/nmeth/journal/v7/n12/full/nmeth.1528.html

Related software
----------------

* `IGV`_: Visualizer of mapped reads (e.g. BAM files). Displays junction reads. 

.. _MISO: http://genes.mit.edu/burgelab/miso/
.. _UCSC Genome Browser: http://genome.ucsc.edu/
.. _BioMart: http://www.ensembl.org/biomart/martview 
.. _A Practical Course in Bayesian Graphical Modeling: http://www.socsci.uci.edu/~mdlee/bgm.html
.. _Python 2.6: http://www.python.org
.. _Numpy: http://www.numpy.org
.. _Scipy: http://www.scipy.org
.. _matplotlib: http://matplotlib.sourceforge.net/
.. _simplejson: http://code.google.com/p/simplejson
.. _jsonpickle: http://jsonpickle.github.com
.. _pygsl: http://pygsl.sourceforge.net
.. _GSL: http://www.gnu.org/software/gsl
.. _samtools: http://samtools.sourceforge.net/
.. _pysam: http://code.google.com/p/pysam/
.. _Spliced Alignment/MAP (SAM): http://samtools.sourceforge.net/SAM1.pdf
.. _SAM: http://samtools.sourceforge.net/SAM1.pdf
.. _GFF: http://www.sequenceontology.org/gff3.shtml
.. _Drosophila melanogaster alternative events (modENCODE): http://genes.mit.edu/burgelab/miso/annotations/modENCODE_alt_events.zip
.. _Mouse genome (mm9) alternative events: http://genes.mit.edu/burgelab/miso/annotations/mm9_alt_events.zip
.. _Human genome (hg18) alternative events: http://genes.mit.edu/burgelab/miso/annotations/hg18_alt_events.zip
.. _Human genome (hg19) alternative events: http://genes.mit.edu/burgelab/miso/annotations/hg19_alt_events.zip
.. _Indexed mm9 annotations: http://genes.mit.edu/burgelab/miso/annotations/mm9/pickled/
.. _Indexed hg18 annotations: http://genes.mit.edu/burgelab/miso/annotations/hg18/pickled/
.. _Bowtie: http://bowtie-bio.sourceforge.net/
.. _Tophat: http://tophat.cbcb.umd.edu/
.. _IGV: http://www.broadinstitute.org/igv/
.. _Cufflinks: http://cufflinks.cbcb.umd.edu/
.. _PolyA DB: http://polya.umdnj.edu/polyadb/
.. _repository: https://github.com/yarden/MISO
.. _Perl script: http://seqanswers.com/forums/showthread.php?t=3201&highlight=GFF3
.. _miso-users: http://mailman.mit.edu/mailman/listinfo/miso-users
.. _White House adopts MISO: http://www.mediabistro.com/fishbowldc/white-house-soup-of-the-day-64_b53593#.Tp2c76k31tA.gmail

.. Indices and tables
.. ^^^^^^^^^^^^^^^^^^

.. * :ref:`genindex`
.. * :ref:`search`

