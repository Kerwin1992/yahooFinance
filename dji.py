# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('WXAgg')
import wx
import urllib
import re
import time
from custom_dialogs import ConfigureData
from selenium import webdriver

class StockFrame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, size=(500, 600))
        #创建一个状态栏，添加File,About,Quit等item，一个图形界面一般都需要这些元素
        self.CreateStatusBar()

        menuBar = wx.MenuBar()

        filemenu = wx.Menu()
        menuBar.Append(filemenu, "&File")

        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program")
        filemenu.AppendSeparator()

        menuQuit = filemenu.Append(wx.ID_EXIT, "Q&uit", " Terminate the program")
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.onQuit, menuQuit)
        self.SetMenuBar(menuBar)

        #textField
        panel = wx.Panel(self)

        codeSizer = wx.BoxSizer(wx.HORIZONTAL)
        labelText = wx.StaticText(panel, label="Stock Code:")
        codeSizer.Add(labelText, 0, wx.ALIGN_BOTTOM)
        codeSizer.Add((10, 10))
        addressText = wx.TextCtrl(panel, value='AAPL')
        addressText.SetSize(addressText.GetBestFittingSize())
        codeSizer.Add(addressText)

        #画列表框图
        self.list = wx.ListCtrl(panel, wx.NewId(), style=wx.LC_REPORT)
        self.list.InsertColumn(0, "Symbol")
        self.list.InsertColumn(1, "Name")
        self.list.InsertColumn(2, "Last Trade")

        pos = self.list.InsertStringItem(0, "--")
        self.list.SetStringItem(pos, 1, "loading...")
        self.list.SetStringItem(pos, 2, "--")
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnClick, self.list)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(codeSizer, 0, wx.ALL, 10)
        vsizer.Add(self.list, -1, wx.ALL | wx.EXPAND, 10)
        # panel.SetSizer(self.sizer)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add((10, 10))
        buttonQuit = wx.Button(panel, -1, "Quit")
        self.Bind(wx.EVT_BUTTON, self.onQuit, buttonQuit)
        buttonQuit.SetDefault()
        hsizer.Add(buttonQuit, 1)

        buttonRefresh = wx.Button(panel, -1, "Refresh")
        self.Bind(wx.EVT_BUTTON, self.onRefresh, buttonRefresh)
        hsizer.Add(buttonRefresh, 1)
        # self.buttonGroupSizer.Layout()
        # self.buttonGroupSizer.Fit(self)
        vsizer.Add(hsizer, 0, wx.ALIGN_BOTTOM)
        # self.sizer.Layout()
        # vsizer.Fit(self)

        # self.buttonGroupSizer.Fit(self)
        ###self.SetSizer(self.buttonGroupSizer)
        panel.SetSizerAndFit(vsizer)
        panel.Layout()
        # self.Show(True)

        '''frameSizer = wx.BoxSizer(wx.VERTICAL)
        frameSizer.Add(panel)
        self.SetSizerAndFit(frameSizer)
        self.Layout()
        self.Fit()'''
    #将数据载入图形界面
    def setData(self, data):
        self.list.ClearAll()
        self.list.InsertColumn(0, "Symbol")
        self.list.InsertColumn(1, "Name")
        self.list.InsertColumn(2, "Last Trade")
        pos = 0
        for row in data:
            # This one looks neater but cannot replace the "&amp;"
            # self.list.Append(row)
            pos = self.list.InsertStringItem(pos + 1, row[0])
            self.list.SetStringItem(pos, 1, row[1].replace("&amp;", "&"))
            self.list.SetColumnWidth(1, -1)
            self.list.SetStringItem(pos, 2, row[2])
            if (pos % 2 == 0):
                # Get the item at a specific index:
                # item = self.list.GetItem(pos)
                self.list.SetItemBackgroundColour(pos, (134, 225, 249))
                # Set new look and feel back to the list
                # self.list.SetItem(item)
        self.FitInside()
        pass

    def GetAllSelected(self):
        selection = []

        # start at -1 to get the first selected item
        current = -1
        while True:
            next = self.GetNextSelected(current)
            if next == -1:
                return selection

            selection.append(self.list.GetItemText(next))
            current = next

    def GetNextSelected(self, current):
        return self.list.GetNextItem(current,
                                     wx.LIST_NEXT_ALL,
                                     wx.LIST_STATE_SELECTED)

    def OnClick(self, event):
        codes = self.GetAllSelected()
        print "code in DJI", codes
        ConfigureData(codes)

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "A small text editor", "About Sample Editor", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def onQuit(self, event):
        self.Close()
        self.Destroy()

    def onRefresh(self, event):
        pass


app = wx.App(False)
top = StockFrame("Dow Jones Industrial Average (^DJI)")
top.Show(True)

#采用谷歌的自动化工具
driver = webdriver.Chrome()
driver.get('https://finance.yahoo.com/quote/%5EDJA')
#找到并自动点击Components项
element = driver.find_element_by_link_text('Components')
webdriver.ActionChains(driver).click(element).perform()
time.sleep(5)
#转码
dStr = driver.page_source.encode('utf-8')
#正则表达式获取成分股中所需要的参数
m = re.findall(r'<td class="Py.*?><.*?>(.*?)</a></td>.*?>(.*?)</td>.*?>(.*?)</td>.*?</tr>', dStr)
if m:
    print m
    # print"\n"
    print len(m)
    top.setData(m)
else:
    wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)

driver.close()
app.MainLoop()