About
=====

ShaderLanguages is a `Sublime Text 2`_ syntax highlighting package for the
`High Level Shader Language`_, `OpenGL Shader Language`_, `CG C for Graphics`_ and
`Unity ShaderLab`_.

Installation
------------

This package has been submitted to the `Package Control`_ index and will hopefully soon be
available in the main list. You can then install it via the Command Palette (CTRL + Shift + P),
typing `install` and selecting `Package Control: Install Package`. In the subsequent popup text box
type `shader` and pick the `ShaderLanguages` package.

In the meantime, or if you do not use Package Control, download a `zip`_ or `tarball`_ archive,
extract the archive, rename the directory to `ShaderLanguages` and simply drop this directory into
your Sublime Text 2 Packages directory.

You are then able to set the syntax from the Command Palette.

Compiling CG Shaders
====

To successfully compile cg shaders, the `Nvidia CG Toolkit`_ must be installed and linked in the PATH environment variable.
(You must be able to run cgc from the console.)

NOTE
====

These syntax highlighting files are a work in progress and will still not highlight
all aspects of the shader language files. Please be patient.

License
=======

ShaderLanguages is released under the MIT license.

Copyright (c) 2012–2013 Jeroen Ruigrok van der Werven <asmodai@in-nomine.org>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

.. _Sublime Text 2: http://www.sublimetext.com/
.. _High Level Shader Language: http://en.wikipedia.org/wiki/High_Level_Shader_Language
.. _OpenGL Shader Language: http://en.wikipedia.org/wiki/GLSL
.. _Unity ShaderLab: http://docs.unity3d.com/Documentation/Components/SL-Reference.html
.. _CG C for Graphics: http://http.developer.nvidia.com/CgTutorial/cg_tutorial_chapter01.html
.. _Package Control: http://wbond.net/sublime_packages/package_control
.. _Nvidia CG Toolkit: https://developer.nvidia.com/cg-toolkit
.. _zip: https://bitbucket.org/asmodai/shaderlanguages/get/tip.zip
.. _tarball: https://bitbucket.org/asmodai/shaderlanguages/get/tip.tar.bz2