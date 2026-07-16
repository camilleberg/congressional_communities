
import plotly.graph_objects as go

from graph_programs.custom_colors import custom_continuous

def make_female_percentage_graph():

    # initilaiizing the figure
    fig_percent = go.Figure()
    

    # vertical line at 50 percent
    fig_percent.add_shape(
        type="line",
        x0=50, y0=0.5,
        x1=50, y1=1.5,
        line=dict(color="grey", width=1.5, dash="solid")
    )
    fig_percent.add_hline(y=1, line_width=1.5, line_dash="solid", line_color="grey")


    # makinf the background transparent
    fig_percent.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})

    # making cleaner
    fig_percent.update_layout(
        title=dict(text="Female percentage by region"),
        width=350,
        height=225,
        legend_itemclick=False,
        xaxis=dict(range=[0, 100], title="% female", 
                tickmode='array', tickvals=[0, 50, 100], 
                ticktext=['0%', '50%', '100%']),  # custom ticks for y-axis),
        yaxis=dict(visible=False, range=[0, 2]),
    )

    # getting rid of grid lines
    fig_percent.update_xaxes(showgrid=False)
    fig_percent.update_yaxes(showgrid=False)

    return fig_percent
    

# update on click 
def update_female_percentage_graph(demographics_data, geoids_df, fig_percent):
    fig_percent.data = ()  # clear traces from the previous click before redrawing

    if geoids_df.empty:
        return fig_percent

    plt_data = {"female_percent": [], "GEOID": []}

    for GEOID in geoids_df["GEOID"]:
        plt_data["female_percent"].append(
            demographics_data.loc[(demographics_data.GEOID == GEOID)]["D049FEMALE_PERCENT"].values[0]
        )
        plt_data["GEOID"].append(GEOID)
        cmin = min(plt_data["female_percent"])
        cmax = max(plt_data["female_percent"])

    for geoid, pct in zip(plt_data["GEOID"], plt_data["female_percent"]):
        fig_percent.add_trace(
            go.Scatter(
                x=[pct], y=[1], mode="markers",
                marker=dict(
                    color=[pct], 
                    cmin=cmin, 
                    cmax=cmax,
                    colorscale=custom_continuous, 
                    size=15),
                name=str(geoid),
            )
        )

    return fig_percent

    
def reset_female_percentage_graph(fig_percent):
    fig_percent.data = ()  # clear traces from the previous click before redrawing
    return fig_percent