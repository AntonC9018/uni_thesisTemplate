# USM Latex Template

This repository contains an opinionated Latex template configured according to USM standards.

# Usage

## Cloning the Repository

Use `git` to get a local copy of this repository.
Install `git` if you don't have it yet.

```shell
cd ~
git clone https://github.com/AntonC9018/uni_thesisTemplate
cd uni_thesisTemplate
```

> Note that it is very important to have the project be a git repository!
> Some features may not work otherwise.

## Installation

### Windows

> [There's a video in russian.](https://youtu.be/TGKnbUBJUOU)

For Windows users, it is highly recommended to use WSL.
For installation instructions, see [this](https://learn.microsoft.com/en-us/windows/wsl/install).

Once you got WSL, refer to the [Ubuntu](#Ubuntu) section for further instructions.

Now, the template may work on Windows without WSL.
The reason it's not recommended is because Latex is known
to cause issues on Windows because of incorrect package versions.
Latex on Linux is more stable in this regard.

### Ubuntu

Run `sudo ./setup.sh`.

> The installation will take 10-15 minutes and will take up around 6GB of storage.
>
> The reason is that dealing with texlive dependencies comes with a lot of complexity,
> there being no standard solution for having a needed set of packages be installed automatically.
> A good solution that minimizes the installation size 
> would require a lot of development time and resources.
> This is why the setup script installs the `texlive-full` distribution.

## Compiling the Thesis

1. **Choose Your Language:** Rename the main `.tex` file 
   corresponding to your language (`ru`/`ro`).

   ```shell
   mv thesis/bare_main_ro.tex thesis/main.tex
   ```

2. **Compile the PDF:**

   ```shell
   cd thesis
   ./render.sh
   ```

## But I don't know Latex...

Here's an overview of the process:
- There's the **source file**, which is the `main.tex` file;
- There's the **Latex compiler**, which *compiles* it to make a PDF;
- The PDF is output in the same directory as the `main.tex` file, you can view it normally in the browser.

I suggest you look through `main.tex` and correlate 
this source file with what you see in the PDF.
Play around with it, see how changes in the source file affect the PDF, 
see what errors the compiler gives.
You will be able to learn most of what you need to write your work like this.

## Notes on prompting the AI

I know most of you won't even bother looking through the examples in the file
and will go straight into copy-pasting AI generated text into your document.
If you do, at least add the example file into the context 
by copy-pasting it into the prompt alongside yours.
This will significantly improve the chances of your document compiling properly.

## The compile script doesn't work after changes

In this case, you should clear the latex cache.
To recompile having cleared the cache, run `./render.sh -f`.

> Note that clearing the cache relies on `git`, 
> so you **must have your project be a git repository.**


