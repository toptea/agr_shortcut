Quick Start
===============

Instead of manually navigating to different files, these can be open
more efficiently via the command line or via python console. Here are some
quick examples:


------------------
Drawing
------------------


a) Window Explorer
~~~~~~~~~~~~~~~~~~
    
    .. image:: ../image/dir_drawing.png
    
    
b) Command Line
~~~~~~~~~~~~~~~
    
    .. code-block:: powershell

        python -m shortcut drawing AGR1288-010-00
    
    
c) Python
~~~~~~~~~
    
    .. code-block:: python
    
        import shortcut
        shortcut.drawing('AGR1288-010-00')


------------------
Jobcard
------------------


a) Window Explorer
~~~~~~~~~~~~~~~~~~

    .. image:: ../image/dir_jobcard.png


b) Command Line
~~~~~~~~~~~~~~~

    .. code-block:: powershell
        
        python -m shortcut jobcard AGR1288-010-00


c) Python
~~~~~~~~~

    .. code-block:: python
    
        shortcut.jobcard('AGR1288-010-00')



------------------
PO
------------------


a) Window Explorer
~~~~~~~~~~~~~~~~~~

    .. image:: ../image/dir_purchase_order.png


b) Command Line
~~~~~~~~~~~~~~~

    .. code-block:: powershell
        
        python -m shortcut po 68628


c) Python
~~~~~~~~~

    .. code-block:: python
    
        shortcut.po(68628)


------------------
Sticker
------------------


a) Window Explorer
~~~~~~~~~~~~~~~~~~

    .. image:: ../image/dir_sticker.png


b) Command Line
~~~~~~~~~~~~~~~

     .. code-block:: powershell
        
        python -m shortcut sticker


c) Python
~~~~~~~~~

    .. code-block:: python
    
        shortcut.sticker()

