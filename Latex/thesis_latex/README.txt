LaTeX Thesis Template v.1.4.x

Copyright (C) 2004-2011
Institute for Dynamic Systems and Control, ETH Zurich

Original contribution by Eric Mueller (IMRT), 2004/04/02

Currently maintained by Soren Ebbesen (IDSC), sebbesen@idsc.mavt.ethz.ch

=========================================
Change log:
=========================================
-----------------------------------------
Version 1.4.1: 2014/13/03, Soren Ebbesen.
-----------------------------------------

* Minor bug-fixes

-----------------------------------------
Version 1.4.0: 2011/23/03, Soren Ebbesen.
-----------------------------------------

Major cahnges:

* Re-written in English

* Usepackages moved to ethidsc.sty

* Enables options st, bt, and mt

* Included mcode.sty for .m code formatting in documents


-----------------------------------------
Version 1.2.2: 2009/25/06, Soren Ebbesen.
-----------------------------------------

Major changes:

* none

Minor changes:

* Swapped page number and page title when using fancy header such that the page number is placed on the left of left-pages (even pages) and on the right side on right-pages (odd pages).

* Some additional efforts in the transition to a purely English template.

-----------------------------------------
Version 1.2.1: 2009/10/06, Soren Ebbesen.
-----------------------------------------

Major changes:

* none

Minor changes:

* Added sections on how to work with units and including code. Modified section on how to include graphics.

-----------------------------------------
Version 1.2.0: 2009/29/05, Soren Ebbesen.
-----------------------------------------

Major changes:

* Removed option ("dt" or "st") in  \usepackage[options]{ethidsc}. Instead the command \type{ARG} was created which is invoked by \maketitle. ARG is any string and intended to describe the type of report. Example \type{Master Thesis}. This is equivalent to \usepackage[dt]{ethidsc} in older versions. The motivation for this change was to remove the restriction

* Replaced file 'bibliography.tex' with 'bibliography.bib'. The .bib file is most conveniently created by a dedicated program for organizing references (such as Jabref (free), Bibdesk (free), or Endnote).  

* Replaced IMRT logo with IDSC logo.

* Translated last page to english. (German translation is still available using the \usepackage[german]{ethidsc}).

* Updated the text "statment regarding plagiarism" (last page) to reflect the official statement as of "Decreed in November 2008 by the Rector, ETH Zurich". This text is now See [http://www.ethz.ch/students/semester/plagiarism_s_en.pdf]

Minor changes:

* Renamed style-file ethimrt.sty to ethidsc.sty

* Renamed file Bericht.tex to Report.tex

* Replaced "H.P.Geering" with "R.D'Andrea"

* Included the hyperref package to enable hyperlinks within the PDF.

* Change name of template from "LaTeX -Template für Semester- und Diplomarbeiten" to "LaTeX Thesis Template v.1.2".

To do:

* Write and include introduction to organizing references using dedicated tools such as Jabref.
