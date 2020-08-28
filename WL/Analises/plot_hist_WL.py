import pandas as pd
#https://plotly.com/
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

df = pd.read_csv('./Historico_WL.dat', delimiter='\t')

fig = px.scatter(x = df['Nome'], y = df['G0C0T90'])
fig.update_layout(title='Historico Teste Winston-Lutz', plot_bgcolor='rgb(230, 230,230)',showlegend=True)
fig.show()

df['Nome'] = df['Nome'].map(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))
plt.plot(df['Nome'],df['G0C0T270'])
plt.gcf().autofmt_xdate()
plt.show()