#Import thư viện
import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
#khai báo biến
i =1
#Tạo hàng đợi hai đầu có 20 phần tử
X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)
Z = deque(maxlen=20)
Z.append(1)
#Tạo một lớp app, tạo layout cho lớp
app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.H1('Biểu đồ nhịp tim và nồng độ oxi trong máu'),	#Tạo thẻ H1 
        dcc.Graph(id='live-graph', animate=True),				#Id hình, chế độ ảnh động
        dcc.Interval(
            id='graph-update',
            interval=1*1000
        ),
    ]
)
#tạo một decorator
@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_scatter():
    global i
    YY = []
    ZZ = []
    graph_data = open('example.txt','r').read()	#lấy dữ liệu
    lines = graph_data.split("\n")
	#Thêm dữ liệu vào hàng đợi
    for line in lines:
        if len(line) > 1:
            xs,ys,zs = line.split(',')
            YY.append(int(ys))
            ZZ.append(int(zs))
    X.append(X[-1]+1)
    Y.append(YY[i])
    Z.append(ZZ[i])
    i = i+1
	#Tiến hành vẽ
    data1 = plotly.graph_objs.Scatter(
            x=list(X),      		#Trục x
            y=list(Z),				#Trục y
            name='Nồng độ oxi',		#Tên đường thẳng
            mode= 'lines+markers'	#Kiểu: đường thẳng, dấu chấm.
            )
    data = plotly.graph_objs.Scatter(
            x=list(X),				#Trục x
            y=list(Y),				#Trục y
            name='Nhịp tim',		#Tên đường thẳng
            mode= 'lines+markers'	#Kiểu: đường thẳng, dấu chấm.
            )
	#Trả về tham số mà hàm yêu cầu
    return {'data': [data1,data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y)-10,max(Z)+10]),)} 
if __name__ == '__main__':
    app.run_server(debug=True)	#Chạy server