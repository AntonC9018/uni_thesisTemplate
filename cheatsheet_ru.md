# Краткая памятка

## Компиляция

| Цель | Команда |
| --- | --- |
| Скомпилировать `main.tex` | `cd thesis && ./render.sh --input main.tex` |
| Скомпилировать после очистки сгенерированных файлов | `cd thesis && ./render.sh -f --input main.tex` |
| Длинный вариант `-f` | `cd thesis && ./render.sh --force --input main.tex` |
| Скомпилировать стартовый файл | `cd thesis && ./render.sh -f --input bare_main_ru.tex` |

## Текст и ссылки

| Что нужно | Команда | Результат |
| --- | --- | --- |
| Жирный текст | `\textbf{text}` | выделение жирным |
| Курсив | `\textit{text}` | наклонный текст |
| Monospace | `\texttt{text}` | технический текст |
| Дословный текст | `\verb!text!` | текст без LaTeX-интерпретации |
| Цитирование | `\cite{png_spec}` | источник из `bibliography.bib` |
| Термин из глоссария | `\gls{PR}` | термин / сокращение |
| Короткое сокращение | `\acrshort{PR}` | только краткая форма |
| Метка | `\label{my_label}` | цель для ссылок |
| Ссылка с большой буквы | `\Cref{my_label}` | начало предложения |
| Ссылка с маленькой буквы | `\cref{my_label}` | внутри предложения |

## Структура документа

| Порядок | Команда | Использование |
| --- | --- | --- |
| 1 | `\titlePage` | титульные листы |
| 2 | `\tableofcontents` | содержание |
| 3 | `\acronymsChapter` | список сокращений |
| 4 | `\introChapter` | введение |
| 5 | `\chapter{Название}\label{chapter_label}` | нумерованная глава |
| 6 | `\section{Название}` | раздел |
| 7 | `\subsection{Название}` | подраздел |
| 8 | `\chapterConclusionSection{chapter_label}` | выводы к главе |
| 9 | `\unnumberedChapter{Название}` | глава без номера |
| 10 | `\bibliographyChapter` | библиография |
| 11 | `\appendixChapter` | начало приложений |
| 12 | `\section{Название}\label{appendix_label}` | приложение |
| 13 | `\declarationPage{}` | декларация автора |

## Вставки

| Что нужно | Команда |
| --- | --- |
| Код: весь файл | `\inputminted{zig}{../src/sourcefile.zig}` |
| Код: диапазон строк | `\inputminted[firstline=2,lastline=5]{zig}{../src/sourcefile.zig}` |
| Код: отмеченный сегмент | `\inputMintedSegment{../src/sourcefile.zig}{example}` |
| Код: дословный текст | `\begin{verbatim}...\end{verbatim}` |
| Нумерованная картинка, label = файл | `\insertImage{interface.png}{Caption}` |
| Нумерованная картинка, свой label | `\insertImage[interface]{interface.png}{Caption}` |
| Ненумерованная картинка | `\insertImage*{interface.png}{Caption}` |
| Нумерованная таблица | `\insertTable[data_table]{Caption}{\begin{tabular}{c c} A & B \end{tabular}}` |
| Ненумерованная таблица | `\insertTable*{Caption}{\begin{tabular}{c c} A & B \end{tabular}}` |
| Правило для картинок/таблиц | в тексте: `\Cref{label}` перед элементом |
| Правило для приложений | `\ref{appendix_label}` может покрыть элементы внутри приложения |
