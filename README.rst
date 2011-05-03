


ez beamer
=========


Purpose
-------

Generate the latex source code for a LaTeX beamer 
presentation from a simple `outline` input format
where sections/subsections and frames are 
indicated by their indentation level.


Prereqs
-------
  * pdflatex installed on your machine



Example 0
---------


The outline file
::

    Section
        Subsection
            Slide 1
                \begin{itemize}
                    \item one
                    \item two
                \end{itemize}
            Slide 2

Will be rendered to .tex with the appropriate 
headers and \frame and \frametitle tags.
::

    \section{Section}
        \subsection{Subsection}
            \frame{
                \frametitle{Slide 1}
                \begin{itemize}
                    \item one
                    \item two
                \end{itemize}
            }

            \frame{
                \frametitle{Slide 2}
            }


Example 1
---------

Running the command:
::

    ./ezbeamer.py --name test2 --title "Some title" --short_title ttq --author "Ivan Savov" --outline ./outline.txt 
    
produces the file outline_result.pdf 



Current status
--------------
Works, I might do lists (enumerate/itemize) 
and shortcuts for \includegraphics, but it is very
usable as is...


stay tuned for the web-interface for this script ;)


