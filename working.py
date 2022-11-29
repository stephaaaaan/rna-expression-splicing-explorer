import pandas as pd
import plotly.graph_objects as go

x = pd.read_csv('~/Desktop/alternative_splicing_data.csv')
e1 = int(x.loc[1209:].loc[1209]['event position'].split('-')[0])
s1 = e1 - 100
s2_e2 = x.loc[1209:].loc[1209]['event position'].split('-')[1]
s2 = int(s2_e2.split(':')[0])
e2 = int(s2_e2.split(':')[1])
s3 = int(x.loc[1209:].loc[1209]['event position'].split('-')[2])
e3 = s3 + 100
fig = go.Figure(go.Scatter(x=[s1,s1,e1,e1,s1,None,s2,s2,e2,e2,s2,None,s3,s3,e3,e3,s3], y=[0,1,1,0,0,None,0,1,1,0,0,None,0,1,1,0,0], fill="toself"))


fig.add_shape(type="path",
    path=f"M {e1},0 Q {(e1+s3)/2},-1 {s3},0",
    line=dict(color="RoyalBlue",width=50)
)
fig.add_shape(type="path",
    path=f"M {e1},1 Q {(e1+s2)/2},2 {s2},1",
    line=dict(color="RoyalBlue",width=50)
)
fig.add_shape(type="path",
    path=f"M {e2},1 Q {(e2+s3)/2},2 {s3},1",
    line=dict(color="RoyalBlue",width=50)
)

'''fig.update_layout(
    shapes=[dict(
            type="path",
            path=f"M {e1},1 Q {(e1+s3)/2},2 {s3},1",
            line_color="RoyalBlue",
            width= 20
        )]
)'''
fig.show()
