# -*- coding: UTF-8 -*z

# wxPython module
import wx
# Matplotlib Figure object
from matplotlib.figure import Figure
# Matplotlib font manager
import matplotlib.font_manager as font_manager
# import the WxAgg FigureCanvas object, that binds Figure to
# WxAgg backend. In this case, this is also a wxPanel
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
# used to obtain CPU usage information
import psutil as p
# wxWidgets object ID for the timer
TIMER_ID = wx.NewId()
# number of data points
POINTS = 300
class PlotFigure(wx.Frame):
    """Matplotlib wxFrame with animation effect"""
    def __init__(self):
        # initialize the super class
        wx.Frame.__init__(self, None, wx.ID_ANY, title="CPU Usage Monitor", size=(600, 400))
        # Matplotlib Figure
        self.fig = Figure((6, 4), 100)
        # bind the Figure to the backend specific canvas
        self.canvas = FigureCanvas(self, wx.ID_ANY, self.fig)
        # add a subplot
        self.ax = self.fig.add_subplot(111)

        # limit the X and Y axes dimensions
        # we prefer 2 separate functions for clarity
        self.ax.set_ylim([0, 100])
        self.ax.set_xlim([0, POINTS])
        # but we want a "frozen" window (defined by y/xlim functions)
        self.ax.set_autoscale_on(False)
        # we do not want ticks on X axis
        self.ax.set_xticks([])
        # we want a tick every 10 point on Y (101 is to have 100 too)
        self.ax.set_yticks(range(0, 101, 10))
        # disable autoscale, since we don't want the Axes to adapt
        # draw a grid (it will be only for Y)
        self.ax.grid(True)
        # generates first "empty" plots
        self.user = [None] * POINTS
        self.nice = [None] * POINTS
        self.sys = [None] * POINTS
        self.idle = [None] * POINTS
        self.l_user,=self.ax.plot(range(POINTS),self.user,label='User%')
        self.l_nice,=self.ax.plot(range(POINTS),self.nice,label='Nice%')
        self.l_sys, =self.ax.plot(range(POINTS),self.sys, label='Sys%')
        self.l_idle,=self.ax.plot(range(POINTS),self.idle,label='Idle%')
        # add the legend
        self.ax.legend(loc='upper center',ncol=4,prop=font_manager.FontProperties(size=10))
        # force a draw on the canvas()
        # trick to show the grid and the legend
        self.canvas.draw()
        # save the clean background - everything but the line
        # is drawn and saved in the pixel buffer background
        self.bg = self.canvas.copy_from_bbox(self.ax.bbox)
        # take a snapshot of CPU usage, needed for the update algorithm


        self.before = self.prepare_cpu_usage()
        # bind events coming from timer with id = TIMER_ID
        # to the onTimer callback function
        wx.EVT_TIMER(self, TIMER_ID, self.onTimer)


    def prepare_cpu_usage(self):
        """helper function to return CPU usage info"""
        # get the CPU times using psutil module
        t = p.cpu_times()
        # return only the values we're interested in
        if hasattr(t, 'nice'):
            return [t.user, t.nice, t.system, t.idle]
        else:
            # special case for Windows, without 'nice' value
            return [t.user, 0, t.system, t.idle]

    def get_cpu_usage(self):
        """Compute CPU usage comparing previous and currentmeasurements"""
        # take the current CPU usage information
        now = self.prepare_cpu_usage()
        # compute deltas between current and previous measurements
        delta = [now[i]-self.before[i] for i in range(len(now))]
        # compute the total (needed for percentages calculation)
        total = sum(delta)
        # save the current measurement to before object
        self.before = now
        # return the percentage of CPU usage for our 4 categories
        return [(100.0*dt)/total for dt in delta]

    def onTimer(self, evt):
        """callback function for timer events"""
        # get the CPU usage information
        tmp = self.get_cpu_usage()
        # restore the clean background, saved at the beginning
        self.canvas.restore_region(self.bg)
        # update the data
        self.user = self.user[1:] + [tmp[0]]
        self.nice = self.nice[1:] + [tmp[1]]
        self.sys = self.sys[1:] + [tmp[2]]
        self.idle = self.idle[1:] + [tmp[3]]
        # update the plot
        self.l_user.set_ydata(self.user)
        self.l_nice.set_ydata(self.nice)
        self.l_sys.set_ydata( self.sys)
        self.l_idle.set_ydata(self.idle)
        # just draw the "animated" objects
        self.ax.draw_artist(self.l_user)
        self.ax.draw_artist(self.l_nice)
        self.ax.draw_artist(self.l_sys)
        self.ax.draw_artist(self.l_idle)
        # "blit" the background with the animated lines
        self.canvas.blit(self.ax.bbox)

if __name__ == '__main__':
    # create the wrapping application
    app = wx.App()
    # instantiate the Matplotlib wxFrame object
    frame = PlotFigure()
    # Initialize the timer - wxPython requires this to be connected to
    # the receiving event handler
    t = wx.Timer(frame, TIMER_ID)
    t.Start(50)
    # show the frame
    frame.Show()
    # start application event loop processing
    app.MainLoop()

