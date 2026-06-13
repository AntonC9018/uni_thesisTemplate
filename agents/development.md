## Config development

- `/thesis/render.sh` is the build command.
  It should be used on the templates after changes to ensure 
  the changes worked and the templates still render.
  It must be run in `thesis` as the cwd.
- There are regression tests, see `tests`.
- Only rerun the tests that would be affected by changes. 
  Do a full test run only if prompted by the user.
- If you need a latex or a system package, pause the output and ask the user to install it.
  Add the package installation to `setup.sh`.
