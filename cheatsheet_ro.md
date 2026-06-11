# Fișă rapidă

## Compilare

| Scop | Comandă |
| --- | --- |
| Compilează `main.tex` | `cd thesis && ./render.sh --input main.tex` |
| Compilează după curățarea fișierelor generate | `cd thesis && ./render.sh -f --input main.tex` |
| Echivalent lung pentru `-f` | `cd thesis && ./render.sh --force --input main.tex` |
| Compilează un starter | `cd thesis && ./render.sh -f --input bare_main_ro.tex` |

## Text și referințe

| Ce vrei | Scrii | Rezultat |
| --- | --- | --- |
| Bold | `\textbf{text}` | text îngroșat |
| Italic | `\textit{text}` | text înclinat |
| Monospace | `\texttt{text}` | text tehnic |
| Text literal | `\verb!text!` | text fără interpretare LaTeX |
| Citare | `\cite{png_spec}` | sursă din `bibliography.bib` |
| Termen din glosar | `\gls{PR}` | termen / prescurtare |
| Prescurtare scurtă | `\acrshort{PR}` | doar forma scurtă |
| Etichetă | `\label{my_label}` | țintă pentru referințe |
| Referință cu literă mare | `\Cref{my_label}` | început de propoziție |
| Referință cu literă mică | `\cref{my_label}` | în interiorul propoziției |

## Structura documentului

| Ordine | Comandă | Folosire |
| --- | --- | --- |
| 1 | `\titlePage` | foi de titlu |
| 2 | `\tableofcontents` | cuprins |
| 3 | `\acronymsChapter` | lista abrevierilor |
| 4 | `\introChapter` | introducere |
| 5 | `\chapter{Titlu}\label{chapter_label}` | capitol numerotat |
| 6 | `\section{Titlu}` | secțiune |
| 7 | `\subsection{Titlu}` | subsecțiune |
| 8 | `\chapterConclusionSection{chapter_label}` | concluzii de capitol |
| 9 | `\unnumberedChapter{Titlu}` | capitol fără număr |
| 10 | `\bibliographyChapter` | bibliografie |
| 11 | `\appendixChapter` | începe anexele |
| 12 | `\section{Titlu}\label{appendix_label}` | anexă |
| 13 | `\declarationPage{}` | declarația autorului |

## Inserări

| Ce vrei | Scrii |
| --- | --- |
| Cod: fișier întreg | `\inputminted{zig}{../src/sourcefile.zig}` |
| Cod: interval de linii | `\inputminted[firstline=2,lastline=5]{zig}{../src/sourcefile.zig}` |
| Cod: segment marcat | `\inputMintedSegment{../src/sourcefile.zig}{example}` |
| Cod: text literal | `\begin{verbatim}...\end{verbatim}` |
| Imagine numerotată, label = fișier | `\insertImage{interface.png}{Caption}` |
| Imagine numerotată, label custom | `\insertImage[interface]{interface.png}{Caption}` |
| Imagine nenumerotată | `\insertImage*{interface.png}{Caption}` |
| Tabel numerotat | `\insertTable[data_table]{Caption}{\begin{tabular}{c c} A & B \end{tabular}}` |
| Tabel nenumerotat | `\insertTable*{Caption}{\begin{tabular}{c c} A & B \end{tabular}}` |
| Regula pentru imagini/tabele | în text: `\Cref{label}` înainte de element |
| Regula pentru anexe | `\ref{appendix_label}` poate acoperi elementele din anexă |
