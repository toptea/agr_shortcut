shortcut 
========

This package provide simple shortcuts that helps the user navigate to
files and folders more quickly. 


Quick Start
-----------

Instead of manually navigating to different files, these can be open
more efficiently via the command line or via python console. Here are some
quick examples:


**Command Line:**
    
    .. code-block:: powershell

        python -m shortcut --help

        python -m shortcut drawing AGR1288-010-00
        python -m shortcut jobcard AGR1288-010-00
        python -m shortcut po 68628
        python -m shortcut sticker

        python -m shortcut new_jobcard AGR-1288 AGR1288-010-00 44080
        python -m shortcut dubs AGR-1288 AGR1288-010-00
    
    
**Python:**
    
    .. code-block:: python
    
        import shortcut
        shortcut.drawing('AGR1288-010-00')
        shortcut.jobcard('AGR1288-010-00')
        shortcut.po(68628)
        shortcut.sticker()


Documentation
-------------

Temporary docs can be found at:

doc/_build/html/index.html