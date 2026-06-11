The repo contains latex template config for Moldova State University.

- `/setup.sh`
- `/thesis` is the directory with the `config.sty` (the most important file)
  and the templates named `bare_main_ro.tex` and `bare_main_ru.tex`.
  In order to use the template, the user would start by cloning it and
  renaming one of these files to `main.tex` to build upon.
- `/thesis/render.sh` is the build command.
  It should be used on the templates after changes to ensure 
  the changes worked and the templates still render.
  It must be run in `thesis` as the cwd.
- There are regression tests that must be run, see `tests`.
