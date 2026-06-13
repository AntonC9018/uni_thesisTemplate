# Fișă rapidă

## Compilare

Compilarea trebuie pornită din directorul `thesis`.

| Scop | Comandă |
| --- | --- |
| Compilează `main.tex` | `./render.sh` |
| Compilează după curățarea fișierelor generate | `./render.sh -f` |
| Compilează un starter | `./render.sh -f --input bare_main_ro.tex` |

## Text și referințe

| Ce vrei | Scrii | Rezultat |
| --- | --- | --- |
| Bold | `\textbf{text}` | text îngroșat |
| Italic | `\textit{text}` | text înclinat |
| Monospace | `\texttt{text}` | caractere monospațiate |
| Text literal | `\verb!text!` | text fără interpretare LaTeX, folosit pentru cod |
| Citare | `\cite{png_spec}` | sursă din `bibliography.bib` |
| Prescurtare | `\gls{PR}` | prima mențiune include definiția completă în paranteze și inserează link spre termen |
| Prescurtare scurtă | `\acrshort{PR}` | nu se extinde la definiția completă, utilă în titluri |
| Etichetă | `\label{my_label}` | țintă pentru referințe |
| Referință cu literă mare | `\Cref{my_label}` | început de propoziție |
| Referință cu literă mică | `\cref{my_label}` | în interiorul propoziției |
| Comandă în titlu | `\cprotect\section{Librăria \verb|minted|}` | necesar pentru `\verb` în titluri |

## Structura documentului

| Comandă | Folosire |
| --- | --- |
| `\titlePage` | inserarea foilor de titlu |
| `\tableofcontents` | inserarea cuprinsului |
| `\acronymsChapter` | inserarea listei de abrevieri |
| `\introChapter` | introducere |
| `\chapter{Titlu}\label{chapter_label}` | capitol numerotat |
| `\section{Titlu}` | secțiune |
| `\subsection{Titlu}` | subsecțiune |
| `\chapterConclusionSection{chapter_label}` | concluzii de capitol |
| `\unnumberedChapter{Titlu}` | capitol fără număr, se adaugă singur în cuprins |
| `\bibliographyChapter` | inserarea bibliografiei |
| `\appendixChapter` | începutul anexelor |
| `\section{Titlu}\label{appendix_label}` | anexă |
| `\declarationPage{}` | declarație |

## Inserări

| Ce vrei | Scrii |
| --- | --- |
| Cod numerotat: text direct | `\insertCode[code_id]{zig}{Inscripție}{...}` |
| Cod direct nenumerotat în anexe | `\insertCode*{...}` |
| Cod numerotat: fișier întreg, eticheta este `../src/sourcefile.zig` | `\insertCodeFile{zig}{../src/sourcefile.zig}{Inscripție}` |
| Cod numerotat: interval de linii | `\insertCodeFile[code_id][firstline=2,lastline=5]{zig}{../src/sourcefile.zig}{Inscripție}` |
| Cod numerotat: segment marcat | `\insertCodeSegment[code_id]{../src/sourcefile.zig}{example}{Inscripție}` |
| Cod nenumerotat în anexe | `\insertCodeFile*{zig}{../src/sourcefile.zig}` |
| Imagine numerotată, eticheta pentru referință este `interface.png` | `\insertImage{interface.png}{Inscripție}` |
| Imagine numerotată, eticheta pentru referință este `interface` | `\insertImage[interface]{interface.png}{Inscripție}` |
| Imagine nenumerotată | `\insertImage*{interface.png}{Inscripție}` |
| Tabel numerotat cu eticheta `table_id` | `\insertTable[table_id]{Inscripție}{\begin{tabular}{c c} A & B \end{tabular}}` |
| Tabel nenumerotat | `\insertTable*{Inscripție}{\begin{tabular}{c c} A & B \end{tabular}}` |

> Toate imaginile, tabelele și blocurile de cod trebuie menționate în text cu `\Cref`.
> Dacă este menționată întreaga anexă, elementele din ea pot rămâne nemenționate direct.
