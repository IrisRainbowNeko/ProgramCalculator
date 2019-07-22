import pyqtgraph as pg
import array

from PyQt5.QtCore import Qt

class WaveShower():
    N = 50
    curve=None
    data = array.array('d', [0] * N)
    app=None
    plt=None
    win=None

    def __init__(self):
        self.app = pg.mkQApp()
        self.win = pg.GraphicsWindow()
        self.win.keyPressEvent= self.keyPressEvent
        self.win.resize(320, 230)

        self.plt = self.win.addPlot()
        self.plt.showGrid(x=True, y=True)
        self.plt.setRange(xRange=[0, self.N-1], yRange=[-1024, 1024], padding=0)
        self.curve = self.plt.plot(pen='y')

        #_thread.start_new_thread(self.win.show, tuple())
        #self.app.exec_()

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Q):
            global getwave
            getwave=False
            try:
                self.app.quit()
                self.win.close()
            except:
                pass

    def show(self):
        self.app.exec_()

    def update(self,value):
        if(not self.win.closed):
            self.data[:-1]=self.data[1:]
            self.data[-1]=value
            self.curve.setData(self.data)
