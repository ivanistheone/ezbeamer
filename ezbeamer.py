#!/usr/bin/env python
#
#
# produces a LaTeX beamer presentation for you
#
##############################################
import os,sys
import re
from string import Template

# if you don't have run install_argparse.sh
import argparse




PRESENTATION_INFO=Template(r"""
\title[$short_title]{$title}
\author[$author]{$author\\
\strut\\
\strut\\
\strut\\
Your University \\
Your department \\
                }
\date{\today}

\begin{document}

\tikzset{
    cnode/.style={isosceles triangle,
                isosceles triangle apex angle=60,thick,
                draw=blue!75, fill=blue!20,minimum height=6mm,inner sep=0.3mm},
    qnode/.style={circle,thick,draw=blue!75,fill=blue!20,minimum size=6mm,inner sep=0.3mm},
    every label/.style= {black, font=\footnotesize}
}


\begin{frame}
\titlepage
\end{frame}


""")



HEADER=Template(r"""\documentclass[10pt]{beamer}

\usepackage{beamerthemesplit}
%\mode<presentation>{\usetheme{Madrid}} % Either Madrid or Rochester

\usefonttheme{professionalfonts}
\usenavigationsymbolstemplate{}

\usepackage{graphicx}


\usepackage[utf8]{inputenc}
%\usepackage[T1]{fontenc}
\usepackage{palatino}
%\usepackage{euler}
%\usepackage{amsmath}
%\usepackage{amsthm}
%\usepackage{amssymb}
%\usepackage{amsthm,geometry}
%\usepackage[colorlinks=true]{hyperref}

\newtheorem{cor}{Corollary}
\newtheorem{lem}{Lemma}
\newtheorem{thm}{Theorem}
\newtheorem{defin}{Definition}
\newtheorem{proposition}{Proposition}

%polices
\newcommand{\msf}{\mathsf}
\newcommand{\mrm}{\mathrm}
\newcommand{\mbf}{\mathbf}
\newcommand{\mbb}{\mathbb}
\newcommand{\mcal}{\mathcal}
%polices

\newcommand{\bra}[1]{\langle #1|}
\newcommand{\ket}[1]{|#1 \rangle}
\newcommand{\braket}[2]{\langle #1|#2\rangle}
\newcommand{\ketbra}[1]{\ket{#1}\bra{#1}}
\newcommand{\ketb}[2]{\ket{#1}\bra{#2}}
\newcommand{\ident}{\mathbb{I}}
\DeclareMathOperator{\tr}{\mathrm{Tr}}
\DeclareMathOperator{\rank}{rank}
\DeclareMathOperator{\polylog}{polylog}
\newcommand{\mdag}{^{\dag}} % dag operator
\newcommand{\demi}{\frac{1}{2}}

\newcommand{\state}{{\rho^{AE}}}
\newcommand{\mixed}{\frac{\mathbb{I}}{d_{A}} \otimes \rho^E}
\newcommand{\tra}{\tr_A}
\newcommand{\cypher}{\mathcal{E}}

\newcommand{\mpr}{{\mrm{Pr}}}
\newcommand{\mtr}[1]{\mathrm{Tr}\left(#1\right)}%trace
\newcommand{\mtra}[1]{\mathrm{Tr}_{A}\left(#1\right)}%trace
\newcommand{\mtrb}[1]{\mathrm{Tr}_{B}\left(#1\right)}%trace
\newcommand{\p}{^{\prime}}


%Nombres
\newcommand{\mbR}{\mathbb{R}}
\newcommand{\mbZ}{\mathbb{Z}}
\newcommand{\mbQ}{\mathbb{Q}}
\newcommand{\mbC}{\mathbb{C}}
\newcommand{\mbN}{\mathbb{N}}
\newcommand{\mbI}{\mathbb{I}}
\newcommand{\mE}[1]{\mcal{E}(#1)}
\newcommand{\mO}[1]{\mcal{O}(#1)}
\newcommand{\mbE}{\mathbb{E}}
%Nombres

%notation de circuit
\newcommand{\mh}{\mathrm{H}}
\newcommand{\mx}{\mathrm{X}}
\newcommand{\my}{\mathrm{Y}}
\newcommand{\mzz}{\mathrm{Z}}
\newcommand{\ms}{\mathrm{S}}
\newcommand{\mt}{\mathrm{T}}
\newcommand{\mamp}{\frac{1}{\sqrt{2}}}
\newcommand{\cnot}{\mathrm{CNOT}}
\newcommand{\msx}{\sigma_{x}}
\newcommand{\msy}{\sigma_{y}}
\newcommand{\msz}{\sigma_{z}}


\setlength{\parindent}{0cm}
\setlength{\parskip}{2ex plus 0.5ex minus 0.5ex}


\newcommand{\aeq}{\approx_{(a)}}
\newcommand{\wtA}{\widetilde{A}}
\newcommand{\wtB}{\widetilde{B}}
\newcommand{\whA}{\widehat{A}}
\newcommand{\whB}{\widehat{B}}
\DeclareMathOperator{\Typ}{typ}

% ivan custom
\newcommand{\be}{\begin{equation}}
\newcommand{\ee}{\end{equation}}
\newcommand{\bea}{\begin{eqnarray}}
\newcommand{\eea}{\end{eqnarray}}
\newcommand{\e}{  \ensuremath{\mathcal E} }
\newcommand{\x}{  \ensuremath{\mathcal X} }
\newcommand{\y}{  \ensuremath{\mathcal Y} }
%\def \mcX{\mathcal{X} } (better no?)
\newcommand{\m}{  \ensuremath{\mathcal M} }
\newcommand{\otimesc}{\negthickspace\otimes\negthickspace}	%close verison of \otimes
\newcommand{\typ}{  \ensuremath{ T^{(n)}_\epsilon  } }
\newcommand{\jtyp}{  \ensuremath{ A^{(n)}_\epsilon  } }
%%% THEOREMS   %%%%%%%%%%%%%%
\theoremstyle{plain}
\newtheorem{Th}{Theorem}[section]
\newtheorem{Lem}[Th]{Lemma}
\newtheorem{Prop}[Th]{Proposition}
\newtheorem{Conj}[Th]{Conjecture}
\newtheorem{Cor}[Th]{Corollary}
\theoremstyle{definition}
\newtheorem{Ex}[Th]{Example}
\newtheorem{Def}[Th]{Definition}
\newtheorem{Rem}[Th]{Remark}
\newtheorem{Quest}[Th]{Question}
\newtheorem{prf}{Proof}
%%% MATH SETS %%%%%%%%%%%%%%
\def \Tr{\textup{Tr}}
\def \c{\mathbb{C}}
\def \z{\mathbb{Z}}
\def \r{\mathbb{R}}
\def \n{\mathbb{N}}
\def \p{\mathbb{P}}
\def \q{\mathbb{Q}}


\newcommand{\pymatgiven}[1]{
			\left[ \begin{array}{cccc}
				p(y_1|x_{#1}) & 0 			& \cdots 			& 0\\
				0 		& p(y_2|x_{#1}) 	& 	 			& 0 \\
				\vdots 	&  				& \ddots 			& \vdots \\
				0 		& 0 				& \cdots			& p(y_{\tiny |\mcal{Y}|}|x_{#1})
			\end{array} \right]
			}
\newcommand{\pymat}{
			\left[ \begin{array}{cccc}
				p_Y(y_1) 	& 0 			& \cdots 			& 0\\
				0 		& p_Y(y_2) 		&  				& 0 \\
				\vdots 	&  			& \ddots 			& \vdots \\
				0 		& 0 			& \cdots			& p_Y(y_{\small  |\mcal{Y}|})
			\end{array} \right]
			}
\newcommand{\pxmat}{
			\left[ \begin{array}{cccc}
				p_X(x_1) & 0 			& \cdots		& 0\\
				0 		& p_X(x_2) 		&  			& 0 \\
				\vdots 	&  			& \ddots 			& \vdots \\
				0 		& 0 			& \cdots			& p_X(x_{\small  |\mcal{X}|})
			\end{array} \right]
			}



\newcommand{\colvec}[1]{\left[\begin{array}{c} #1 \end{array}\right]}



\def\E{\mathcal{E}}
\def\cD{\mathcal{D}}
\def\cH{\mathcal{H}}
\def\cX{\mathcal{X}}
\def\cY{\mathcal{Y}}
\def\NN{\mathbb{N}}

\usepackage{tikz}
\usetikzlibrary{arrows,shapes,decorations,automata,backgrounds,petri}
\usetikzlibrary{shapes.gates.logic.US}
% http://tex.stackexchange.com/questions/13933/drawing-mechanical-systems-in-latex/13952#13952
\usetikzlibrary{calc,patterns,decorations.pathmorphing,decorations.markings}





%_____________________________________________________________________%
""")


PAPER_MID=Template(r"""

\section{Introduction}

\section{Results}

""")




FOOTER=Template(r"""

\begin{frame}
	\frametitle{The end}
	\begin{center}
		\huge thank you for your attention!
	\end{center}
\end{frame}




%\subsection{References}

%\frame[shrink=0.1]{
%	\begin{thebibliography}{9} \label{referencess}
%	\bibitem[C\&T]{coverthomas}		T.~M.~Cover and J.~A.~Thomas, {\em Elements of Information Theory}, New York: Wiley, ~1991.
%	\bibitem[N\&C]{nielsenchuang} 	M.~Nielsen, I.~Chuang, {Quantum computation and quantum information}, {2004}, {Cambridge}.
%	\bibitem[DHW03]{afamily} 		I. Devetak, A.W. Harrow, A. Winter,
%									\emph{A family of quantum protocols},
%									quant-ph/0308044.
%	\bibitem[YDH05]{macapacity} 	J.~Yard, I.~Devetak, P.~Hayden. \emph{Capacity Theorems for Quantum Multiple Access Channels:
%									Classical-Quantum and Quantum-Quantum Capacity Regions}, quant-ph/0501045.
%	\bibitem[ADHW06]{motherofall} 	A.~Abeyesinghe, I.~Devetak, P.~Hayden, A.~Winter,
%									\emph{The mother of all protocols: Restructuring quantum information's family tree},
%									quant-ph/0606225
%	\bibitem[C\&T]{coverthomas}		T.~M.~Cover and J.~A.~Thomas, {\em Elements of Information Theory}, New York: Wiley, ~1991.
%	\bibitem[N\&C]{nielsenchuang} 	M.~Nielsen, I.~Chuang, {Quantum computation and quantum information}, {2004}, {Cambridge}.
%	\bibitem[DHW03]{afamily} 		I. Devetak, A.W. Harrow, A. Winter,
%									\emph{A family of quantum protocols},
%									quant-ph/0308044.
%	\bibitem[YDH05]{macapacity} 	J.~Yard, I.~Devetak, P.~Hayden. \emph{Capacity Theorems for Quantum Multiple Access Channels:
%									Classical-Quantum and Quantum-Quantum Capacity Regions}, quant-ph/0501045.
%	\bibitem[ADHW06]{motherofall} 	A.~Abeyesinghe, I.~Devetak, P.~Hayden, A.~Winter,
%									\emph{The mother of all protocols: Restructuring quantum information's family tree},
%									quant-ph/0606225
%	\end{thebibliography}
%}



\end{document}

""")









def ezbeamer_create_latex( args ):
    """ parses an `outline` file and prepares a LaTeX beamer presentation.

        This is a section
            This is a subsection
                Frame title
                    Some content
                    in the fame like this
                Next frame title
            Another subsection
        Another section
    """
    print "ezbeamer ********************************** *** ** * "

    if not args.name:
        name = raw_input("Give me a name for the folder. (no spaces)\n> ")
    else:
        name = args.name

    # make a de dir
    if not os.path.exists(name):
        os.mkdir(name)
    #os.chdir(name)
    texfile = open(name+"/"+name+".tex","w")

    #generic beamer header
    head= HEADER.substitute()
    texfile.write(head)


    # info
    if not args.author:
        args.author = raw_input("What is your name? \n> ")
    if not args.title:
        args.title = raw_input("What is the title of the presentation? \n> ")
    if not args.short_title:
        args.short_title = raw_input("What is a short title (abbreviation) for the presentation? \n> ")
    info = PRESENTATION_INFO.substitute(title = args.title,
                                        author = args.author,
                                        short_title = args.short_title)
    texfile.write(info)


    if not args.outline:

        print "You didn't specify an outline file :(  "
        print " .... you are missing all the EZ part, "
        print "      but I respect your use of beamer "
        print "      so I will make ane empty .tex file "
        print "      for you -- you can start from there"
        print "                                         "
        print "      You are cool!                      "
        print "                                         "


    else:
        # indentation-based outline parser
        # thx http://stackoverflow.com/questions/2268532/grab-a-lines-whitespace-indention-with-python/2268559#2268559
        lead_sp = re.compile(r"\s*")
        comment = re.compile(r"\s*#")
        frame_title =  re.compile("\s*([^\[]*)(\s*\[(.*)\])?") 

        outline = open(args.outline, 'r')

        state = 'out'
        # "out'       = outside of slide
        # 'inslide'   = within a \frame
        # 'itemize'   = within an \itemize    *
        # 'enumerate' = within an \enumerate  -

        for line in outline.readlines():

            if comment.match(line):    # python style comments
                continue

            # find indentation:
            lsp = lead_sp.match(line).group()

            if state=='inslide' and not (lsp.startswith(" "*12) or lsp.startswith("\t\t\t")):
                texfile.write("\t"*2 + "\\end{frame}\n\n" )
                state='out'
                # slide closing

            if len(line.strip())==0:                     # skip blank lines
                continue

            if len(lsp)==0:
                texfile.write("\\section{"+line.strip()+"}\n\n")
            if lsp in [" "*4, "\t"]:
                texfile.write(lsp+"\\subsection{"+line.strip()+"}\n\n")
            if lsp in [" "*8, "\t\t"]:
                m = frame_title.match(line)
                ft = m.groups()[0].strip()
                if m.groups()[1]:
                    opts = m.groups()[2]
                    texfile.write(lsp+"\\begin{frame}["+opts+"]\n"+lsp+"\t\\frametitle{"+ft+"}\n")
                else:
                    texfile.write(lsp+"\\begin{frame}\n"+lsp+"\t\\frametitle{"+ft+"}\n")
                state='inslide'
            if lsp.startswith(" "*12) or lsp.startswith("\t\t\t"):

                if state!='inslide':
                    print "skipping line ", line.strip(), " doesn't seem to below to any slide "
                else:
                    texfile.write(line)
                    state='inslide'

        foot = FOOTER.substitute()
        texfile.write(foot)


        texfile.close()

    print "done"
    print "Look for a directory called " + name + " and the .tex file inside"
    print "to typeset to PDF run:     pdflatex " + name +".tex"
    print "thank you come again... ivan.savov gmail com"


if __name__=="__main__":

    parser = argparse.ArgumentParser(description='ezbeamer -- for LaTeX beamer presentations.')
    parser.add_argument('--outline', help='Paper outline.txt (noindend=sec_title, 1-indent=subsec, 2-indent=frametitle, 3-indent=slidecontnets)')

    parser.add_argument('--name', help='Name of presentation (for dirname).')
    parser.add_argument('--title', help='Presentation long title')
    parser.add_argument('--short_title', help='Short title')
    parser.add_argument('--author', help='Author')

    args = parser.parse_args()
    ezbeamer_create_latex( args )

    #print "This will give you a simple tex file in a subdirectory"
    #print "of the current directory called PaperName"








