from typing import Any
import pandas as pd
import plotly.express as px

def generate_terminal_chart(data: pd.DataFrame, target_metric: str, plot_type: str) -> Any:
    # Colors for the terminal UI
    wall_street_colors = ["#00FF66", "#FF3366", "#00FFFF", "#FFFF33", "#FF9900", "#CC66FF"]

    fig_args = dict(
        data_frame=data,
        x="Date",
        y=target_metric,
        color="Ticker",
        template="plotly_dark",
        color_discrete_sequence=wall_street_colors,
    )

    # Generate the appropriate figure type
    if plot_type == "Time Series (Line)":
        fig = px.line(**fig_args)
        fig.update_traces(line=dict(width=3), selector=dict(type="scatter"))
    else:
        fig = px.bar(**fig_args, barmode="group")

    # Use the trace name directly, which is automatically set to the Ticker
    fig.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>Value: %{y:,.2f}<extra></extra>"
    )

    fig.update_layout(
        hovermode="x unified",
        dragmode="pan",
        plot_bgcolor="#11151F",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=True, gridcolor="#242B3D", zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#242B3D", zeroline=True, zerolinecolor="#8A93A6"),
    )

    return fig