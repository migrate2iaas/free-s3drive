"""implements splash screen
taken from http://code.activestate.com/recipes/534124-elegant-tkinter-splash-screen/
"""

import time
try:
    import tkinter.tix as Tix
except ImportError: # Python 2
   import Tix


class SplashScreen( object ):
   def __init__( self, tkRoot, imageFilename, minSplashTime=0 ):
      self._root              = tkRoot
      self._image             = Tix.PhotoImage( file=imageFilename )
      self._splash            = None
      self._minSplashTime     = time.time() + minSplashTime
      
   def __enter__( self ):
      # Remove the app window from the display
      self._root.withdraw( )
      
      # Calculate the geometry to center the splash image
      scrnWt = self._root.winfo_screenwidth( )
      scrnHt = self._root.winfo_screenheight( )
      
      imgWt = self._image.width()
      imgHt = self._image.height()
      
      imgXPos = (scrnWt / 2) - (imgWt / 2)
      imgYPos = (scrnHt / 2) - (imgHt / 2)

      # Create the splash screen      
      self._splash = Tix.Toplevel()
      self._splash.overrideredirect(1)
      self._splash.geometry( '+%d+%d' % (imgXPos, imgYPos) )
      Tix.Label( self._splash, image=self._image, cursor='watch' ).pack( )

      # Force Tk to draw the splash screen outside of mainloop()
      self._splash.update( )
   
   def __exit__( self, exc_type, exc_value, traceback ):
      # Make sure the minimum splash time has elapsed
      timeNow = time.time()
      if timeNow < self._minSplashTime:
         time.sleep( self._minSplashTime - timeNow )

      del self._image
      
      # Destroy the splash window
      self._splash.destroy( )
      
      # Display the application window
      #self._root.deiconify( )

if __name__ == '__main__':
   tkRoot = Tix.Tk( )

   with SplashScreen( tkRoot, 'res/install.gif', 2.0 ):
      time.sleep(15)
      print("Ready...")

   tkRoot.mainloop( )
