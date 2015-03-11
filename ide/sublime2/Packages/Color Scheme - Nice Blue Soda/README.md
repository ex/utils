Sublime-Text-2
==============

Currently I just released my first Color Scheme.
Please notice, that is my very first work.
Feedback is always welcome.

You can even fork this and improve it your way. Feel free.

# Screens
![Example 1](https://bitbucket.org/DanielSiepmann/color-scheme-nice-blue-soda/raw/default/Docs/Example%201.png "Example 1 with HTML, CSS and PHP.")
![Example 2](https://bitbucket.org/DanielSiepmann/color-scheme-nice-blue-soda/raw/default/Docs/Example%202.png "Example 2 with HTML, CSS and PHP.")
![Example Diff](https://bitbucket.org/DanielSiepmann/color-scheme-nice-blue-soda/raw/default/Docs/Example%20Diff.png "Example 3 with Diff.")

# Supported
Currently tested / supported:

- Languages
    - HTML
    - CSS
    - XML
    - JavaScript (not well done)
    - TypoScript (not well done)
    - JSON (not well done)
    - PHP
    - PHPDoc
    - Markdown
    - Markup
    - Diff
- Plugins
    - SublimeLinter
    - Bracket Highlighter
    - Shell command output
    - PlainTasks (not well done, just initial)
    - QuickCal (https://github.com/facelessuser/QuickCal)
- Core
    - Find in Files Result
    

# Installation

After "installing" the scheme, you have to configure Sublime Text to use this scheme:

    "color_scheme": "Packages/color-scheme-nice-blue-soda/Nice Blue Soda.tmTheme",

## Unix like systems
The CLI way

    cd ~/.config/sublime-text-2/Package
    hg clone ssh://hg@bitbucket.org/DanielSiepmann/color-scheme-nice-blue-soda


## Mac
The CLI way

    cd ~/Library/Application Support/Sublime Text 2/Packages
    hg clone ssh://hg@bitbucket.org/DanielSiepmann/color-scheme-nice-blue-soda

As a GUI for Mac you can use the nice and free [SourceTree][].

## Windows
On Windows you can do the same way as for Unix.
As a GUI for Windows you can use the free [TortoiseHg][].

## PlainTasks
PlainTasks plugin has it's own Color Scheme. But you can change the file to use inside the settings.
Just add this to the plugin settings:

    "color_scheme": "Packages/color-scheme-nice-blue-soda/Nice Blue Soda.tmTheme",

# Additions

Works very well with the nice [Sublime Text 2](http://www.sublimetext.com/) Theme [Soda Dark](https://github.com/buymeasoda/soda-theme/#design) (used for the Screens too).