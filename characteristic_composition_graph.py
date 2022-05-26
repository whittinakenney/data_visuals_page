import pandas as pd
import plotly.graph_objects as go

data = pd.read_csv("uberProj/N-Factor_RandomGenerated .csv")

x = list(data["PersonID"])
sig_vector = [.25, .25, .25, .25] #must be same size as number of characteristics and add to 1

characteristics = list(data.columns[1:])
unit_column_vectors = []

for m in range(len(characteristics)): #scales each column vectors by sig_vector
    column_m_times_sig_m = data[characteristics[m]] * sig_vector[m]
    unit_column_vectors.append(column_m_times_sig_m)

for n in range(len(characteristics)): #takes every person except the first and finds its characteristic composition
    if n == 0:
        fig = go.Figure(go.Bar(x=x, y=unit_column_vectors[n], name = characteristics[n]))
    else:
        fig.add_trace(go.Bar(x=x, y=unit_column_vectors[n], name = characteristics[n]))

fig.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'},
                  title = "Total Confidence for Each Person's ID")
