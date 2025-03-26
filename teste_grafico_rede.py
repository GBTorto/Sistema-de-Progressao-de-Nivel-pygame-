import plotly.express as px
import pandas as pd

df = pd.DataFrame(dict(
    r=[2, 5, 2, 2, 3, 9],
    theta=['processing cost', 'mechanical properties', 'chemical stability',
           'thermal stability', 'device integration', "nome"]))

fig = px.line_polar(df, r='r', theta='theta', line_close=True)
fig.update_traces(fill='toself')

# Remover apenas a linha circular onde ficavam os números
fig.update_layout(
    polar=dict(
        radialaxis=dict(showticklabels=False, linecolor="rgba(0,0,0,0)")
    )
)

fig.show()
