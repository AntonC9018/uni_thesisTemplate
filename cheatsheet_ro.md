# Fișă rapidă pentru șablon

## Pornire

1. Copiați `thesis/bare_main_ro.tex` în `thesis/main.tex`.
2. Completați metadatele de la începutul fișierului: autor, titlu, conducător, program, tipul lucrării.
3. Compilați din directorul `thesis`:

```sh
./render.sh --force --input main.tex
```

## Metadate utile

- `\docTitleRo` - titlul lucrării.
- `\docTypeRoDefinit`, `\docTypeRoNedefinit`, `\docTypeRoDativ` - formele gramaticale ale tipului lucrării.
- `\studentTypeRo` - textul pentru autor pe foaia de titlu, de exemplu `student`, `absolvent`, `masterand`.
- `\uniGroupName`, `\authorName`, `\conducatorName`, `\conducatorTitleRo` - datele pentru foaia de titlu.
- `\github` și `\conferencesList` - linkul sursei și conferințele raportate.

## Prescurtări

Definiți prescurtările înainte de `\begin{document}`:

```tex
\acro{PNG}{Portable Network Graphics}
\acro[url]{URL}{Uniform Resource Locator}
```

În text folosiți `\ac{PNG}`, `\acrshort{PNG}` sau `\gls{PNG}`. Prescurtările nemenționate nu apar în lista de abrevieri.

## Citări și bibliografie

Adăugați sursele în `thesis/bibliography.bib`, apoi citați-le în text:

```tex
Text citat dintr-o sursă\cite{cheia_sursei}.
Text citat dintr-o pagină concretă\cite[12]{cheia_sursei}.
```

Bibliografia este inserată cu `\bibliographyChapter`.

## Tabele și imagini

Folosiți variantele numerotate când elementul este referit în text:

```tex
\Cref{schema_interfata} prezintă schița interfeței.

\insertImage[schema_interfata]{interface_sketch.png}{Schița interfeței}
```

Pentru tabele:

```tex
\Cref{tabel_date} prezintă datele.

\insertTable[tabel_date]{Date experimentale}{%
  \begin{tabular}{c c}
    A & B \\
  \end{tabular}
}
```

Folosiți `\insertImage*` și `\insertTable*` doar pentru elemente nenumerotate, la care nu faceți referință directă.

## Referințe la anexe

După `\appendixChapter`, fiecare anexă cu `\label{...}` trebuie referită în text cu `\ref{...}`, `\cref{...}` sau `\Cref{...}`.
Elementele numerotate din anexă sunt acoperite de referința la întreaga anexă; referiți-le direct doar când le discutați separat.
Această excepție se aplică numai anexelor. Imaginile și tabelele numerotate din textul principal trebuie referite direct.

Dacă o etichetă din anexă nu este referită, PDF-ul afișează un avertisment roșu lângă element, iar logul LaTeX conține un avertisment `Package config Warning`.

## Ghilimele

Folosiți `\enquote{...}` pentru ghilimele adaptate limbii documentului:

```tex
\enquote{acesta este un citat scurt}
```

## Cod

Pentru un fișier întreg:

```tex
\inputminted{zig}{../src/sourcefile.zig}
```

Pentru un interval de linii:

```tex
\inputminted[firstline=2,lastline=5]{zig}{../src/sourcefile.zig}
```

Pentru un segment marcat în fișier, folosiți:

```tex
\inputMintedSegment{../src/sourcefile.zig}{example}
```
