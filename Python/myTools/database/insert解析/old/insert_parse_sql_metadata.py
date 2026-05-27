import wx
import wx.grid
import sql_metadata

class MyFrame(wx.Frame):
    WD_PIX = 800
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "INSERT解析", size=(self.WD_PIX, 600))
        
        # 创建面板
        panel = wx.Panel(self, -1)

        # 创建文本框
        self.text_ctrl = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE, size=(self.WD_PIX, 100))

        # 创建按钮
        button = wx.Button(panel, -1, "解析")

        # 创建表格
        self.grid = wx.grid.Grid(panel)
        self.grid.CreateGrid(0, 0)
        self.grid.EnableEditing(False)
        
        
        # 布局
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text_ctrl, proportion=0, flag=wx.EXPAND|wx.ALL, border=5)
        sizer.Add(button, proportion=0, flag=wx.ALIGN_CENTER|wx.BOTTOM, border=5)
        sizer.Add(self.grid, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
        
        panel.SetSizer(sizer)
        
        # 绑定事件
        self.Bind(wx.EVT_BUTTON, self.OnParseButton, button)
    
    # 解析按钮事件处理函数
    def OnParseButton(self, event):
        # 获取文本框内容
        sql = self.text_ctrl.GetValue()
        # 解析sql语句
        data = []
        try:
            d = sql_metadata.Parser(sql).values_dict
            for key in d:
                data.append([key, d[key]])
        except:
            pass
        
        # 在表格中动态输出解析结果
        rows = len(data)
        cols = 2
        self.grid.ClearGrid()
        if self.grid.NumberRows>0:
            self.grid.DeleteRows(0, self.grid.NumberRows)
        if self.grid.NumberCols>0:
            self.grid.DeleteCols(0, self.grid.NumberCols)
        if rows > 0:
            self.grid.AppendCols(cols)
            self.grid.AppendRows(rows)
            for i in range(rows):
                for j in range(cols):
                    #print(i,j,data[i][j])
                    self.grid.SetCellValue(i, j, str(data[i][j]))
        
        # 设置列标签
        self.grid.SetColLabelValue(0, "字段")
        self.grid.SetColLabelValue(1, "值")
        
        # 设置列宽
        self.grid.SetRowLabelSize(50)
        self.grid.SetColSize(0, 150)
        self.grid.SetColSize(1, 300)

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show(True)
    app.MainLoop()
