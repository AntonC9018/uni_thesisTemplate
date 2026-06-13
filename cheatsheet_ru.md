# Краткая памятка

## Компиляция

Компиляция должна запускаться из директории `thesis`.

| Цель | Команда |
| --- | --- |
| Скомпилировать `main.tex` | `./render.sh` |
| Скомпилировать после очистки сгенерированных файлов | `./render.sh -f` |
| Скомпилировать стартовый файл | `./render.sh -f --input bare_main_ru.tex` |

## Текст и ссылки

| Что нужно | Команда | Результат |
| --- | --- | --- |
| Жирный текст | `\textbf{text}` | выделение жирным |
| Курсив | `\textit{text}` | наклонный текст |
| Monospace | `\texttt{text}` | равноширные символы |
| Дословный текст | `\verb!text!` | текст без LaTeX-интерпретации, используется для кода |
| Цитирование | `\cite{png_spec}` | источник из `bibliography.bib` |
| Сокращение | `\gls{PR}` | первое упоминание будет содержать полное определение в скобках, вставит ссылку на этот термин |
| Короткое сокращение | `\acrshort{PR}` | не раскрывается до полного определения, полезно в заголовках |
| Метка | `\label{my_label}` | цель для ссылок |
| Ссылка с большой буквы | `\Cref{my_label}` | начало предложения |
| Ссылка с маленькой буквы | `\cref{my_label}` | внутри предложения |
| Команда в заголовке | `\cprotect\section{Библиотека \verb|minted|}` | нужно для `\verb` в заголовках |

## Структура документа

| Команда | Использование |
| --- | --- |
| `\titlePage` | вставка титульных листов |
| `\tableofcontents` | вставка содержания |
| `\acronymsChapter` | вставка списка сокращений |
| `\introChapter` | введение |
| `\chapter{Название}\label{chapter_label}` | нумерованная глава |
| `\section{Название}` | раздел |
| `\subsection{Название}` | подраздел |
| `\chapterConclusionSection{chapter_label}` | выводы к главе |
| `\unnumberedChapter{Название}` | глава без номера, сама добавляется в содержание |
| `\bibliographyChapter` | вставка библиографии |
| `\appendixChapter` | начало приложений |
| `\section{Название}\label{appendix_label}` | приложение |
| `\declarationPage{}` | декларация |

## Вставки

| Что нужно | Команда |
| --- | --- |
| Нумерованный код: прямой текст | `\begin{code}[code_id]{zig}{Надпись}...\end{code}` |
| Прямой ненумерованный код в приложениях | `\begin{codeWithoutLabel}{text}...\end{codeWithoutLabel}` |
| Нумерованный код: весь файл, метка `../src/sourcefile.zig` | `\insertCodeFile{zig}{../src/sourcefile.zig}{Надпись}` |
| Нумерованный код: диапазон строк | `\insertCodeFile[code_id][firstline=2,lastline=5]{zig}{../src/sourcefile.zig}{Надпись}` |
| Нумерованный код: отмеченный сегмент | `\insertCodeSegment[code_id]{../src/sourcefile.zig}{example}{Надпись}` |
| Ненумерованный код в приложениях | `\insertCodeFile*{zig}{../src/sourcefile.zig}` |
| Нумерованная картинка, метка для обращения - `interface.png` | `\insertImage{interface.png}{Надпись}` |
| Нумерованная картинка, метка для обращения `interface` | `\insertImage[interface]{interface.png}{Надпись}` |
| Ненумерованная картинка | `\insertImage*{interface.png}{Надпись}` |
| Нумерованная таблица с меткой `table_id` | `\insertTable[table_id]{Надпись}{\begin{tabular}{c c} A & B \end{tabular}}` |
| Ненумерованная таблица | `\insertTable*{Надпись}{\begin{tabular}{c c} A & B \end{tabular}}` |

> Все картинки, таблицы и блоки кода должны быть упомянуты в тексте, используя `\Cref`.
> Если упомянуто все приложение, можно не упоминать картинки изнутри.
> 
> Вы увидите ошибки, если это не будет выполнено.
