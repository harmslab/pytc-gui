==============================
pytc-gui programming reference
==============================

pytc-gui is written using :code:`pyqt5`.  

Coding guidelines
-----------------

.. sourcecode:: python

    class SomeWidget(QW.QWidget):
        """
        Do widget-y thing.
        """

        def __init__(self,parent,fit,*args,**kwargs):   

            super().__init__() 
            self._parent = parent
            self._fit = fit 

+ :code:`self._parent` is the parent widget to the current widget.
+ :code:`self._fit` is the :code:`FitContainer` instance created by the initial
  :code:`MainWindow` instance and then passed to all other widgets.  Accessing
  :code:`self._fit` thus allows all of the widgets to synchronize their
  behavior.
