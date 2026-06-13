# Fișă rapidă

## Compilare

Compilarea trebuie pornită din directorul `thesis`.

| Scop | Comandă |
| --- | --- |
| Compilează `main.tex` | `./render.sh` |
| Curăță fișierele generate + compilează | `./render.sh -f` |
| Compilează un starter | `./render.sh -f --input bare_main_ro.tex` |

## Text

| Ce vrei | Scrii | Rezultat |
| --- | --- | --- |
| Bold | `\textbf{text}` | text îngroșat |
| Italic | `\textit{text}` | text înclinat |
| Monospace | `\texttt{text}` | caractere monospațiate |
| Text literal | `\verb!text!` | text fără interpretare LaTeX, folosit pentru cod |
| Link-uri | `\url{https://...}` | link clicabil, textul link-ului este propriu zis link-ul |
| Link-uri pe text | `\href{https://...}{text}` | link clicabil |
| Explicații în footer | `hello\footnote{explicație}` | numerotează itemii în footer automat per pagină |

## Text și referințe

| Ce vrei | Scrii | Rezultat |
| --- | --- | --- |
| Citare | `\cite{png_spec}` | sursă din `bibliography.bib` |
| Prescurtare | `\gls{PR}` | prima mențiune include definiția completă în paranteze și inserează link spre termen |
| Prescurtare scurtă | `\acrshort{PR}` | nu se extinde la definiția completă, utilă în titluri |
| Etichetă | `\label{my_label}` | țintă pentru referințe |
| Referințe la un obiect (imagine, tabel) | `\Obiectul{label_1}` | de ex. 'Imaginea 1.1' |
| Referințe la un obiect în cazul genitiv | `\unuiObiect{label_1}`, `\obiectului{label_1}` | 'imaginei 1.1' |
| Referințe la mai multe obiecte | `\obiectele{label_1}{label_2}` | 'imaginile 1.1 și 1.2' |
| Comandă în titlu | `\cprotect\section{Librăria \verb!minted!}` | necesar pentru `\verb` în titluri |

## Structura documentului

| Comandă | Folosire |
| --- | --- |
| `\titlePage` | inserarea foilor de titlu |
| `\tableofcontents` | inserarea cuprinsului |
| `\acronymsChapter` | inserarea listei de abrevieri |
| `\annotationChapter{ro}` | inserarea anotației în română |
| `\introChapter` | introducere |
| `\chapter{Titlu}\label{chapter_label}` | capitol numerotat |
| `\section{Titlu}` | secțiune |
| `\subsection{Titlu}` | subsecțiune |
| `\chapterConclusionSection{chapter_label}` | concluzii de capitol |
| `\finalConclusionChapter` sau `\finalConclusionChapter[Titlu]` | concluziile finale, cu validarea volumului oficial |
| `\unnumberedChapter{Titlu}` | capitol generic fără număr, se adaugă singur în cuprins și nu este validat ca volum |
| `\bibliographyChapter` | inserarea bibliografiei |
| `\appendixChapter` | începutul anexelor |
| `\section{Titlu}\label{appendix_label}` | anexă |
| `\declarationPage{}` | declarație |

## Inserări

| Ce vrei | Scrii |
| --- | --- |
| Cod numerotat: text direct | `\begin{code}[code_id]{js}{Inscripție}...\end{code}` |
| Cod direct nenumerotat în anexe | `\begin{codeWithoutLabel}{js}...\end{codeWithoutLabel}` |
| Cod numerotat: fișier întreg, eticheta este `../src/sourcefile.js` | `\insertCodeFile{js}{../src/sourcefile.js}{Inscripție}` |
| Cod numerotat: interval de linii | `\insertCodeFile[code_id][firstline=2,lastline=5]{java}{../src/sourcefile.java}{Inscripție}` |
| Cod numerotat: segment marcat | `\insertCodeSegment[code_id]{../src/sourcefile.zig}{example}{Inscripție}` |
| Cod nenumerotat în anexe | `\insertCodeFile*{java}{../src/sourcefile.java}` |
| Imagine numerotată, eticheta pentru referință este `interface.png` | `\insertImage{interface.png}{Inscripție}` |
| Imagine numerotată, eticheta pentru referință este `interface` | `\insertImage[interface]{interface.png}{Inscripție}` |
| Imagine nenumerotată | `\insertImage*{interface.png}{Inscripție}` |
| Tabel numerotat cu eticheta `table_id` | `\insertTable[table_id]{Inscripție}{\begin{tabular}{c c} A & B \end{tabular}}` |
| Tabel nenumerotat | `\insertTable*{Inscripție}{\begin{tabular}{c c} A & B \end{tabular}}` |

> Toate imaginile, tabelele și blocurile de cod trebuie menționate în text cu `\Cref`.
> Dacă este menționată întreaga anexă, elementele din ea pot rămâne nemenționate direct.
