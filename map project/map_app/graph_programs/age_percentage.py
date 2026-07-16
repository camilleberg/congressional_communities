import plotly.graph_objects as go
from graph_programs.custom_colors import custom_continuous

def make_age_percentage_graph():
    fig_age = go.Figure()

    # making backgroufn transparent
    fig_age.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
        
    # getting rid of grid lines
    fig_age.update_xaxes(showgrid=False)
    fig_age.update_yaxes(showgrid=False)

    fig_age.update_layout(
        yaxis=dict(range=[0, 45]),
    )
    
    return fig_age 

# update on click
def update_age_percentage_graph(demographics_data, geoids_df, fig_age, age_brackets):
    fig_age.data = ()  # clear traces from the previous click before redrawing

    if geoids_df.empty:
        return fig_age

    # indexes the data at GEOID
    demo_indexed = demographics_data.set_index("GEOID")
    # filters in specific GEOIDS 
    subset = demo_indexed.loc[geoids_df["GEOID"], age_brackets]
    # builds out dictiornary 
    plt_data = {"GEOID": subset.index.tolist(), **{age: subset[age].tolist() for age in age_brackets}}

    for i, geoid in enumerate(plt_data['GEOID']):
        y_values = [plt_data[age][i] for age in age_brackets]
        fig_age.add_trace(
            go.Scatter(
                x=age_brackets,
                y=y_values,
                name=str(geoid),
                mode='lines', 
                hovertemplate= (
                    "%{y} % <br>" 
                    "<extra></extra>"  # <extra></extra> removes the secondary side-box (trace name)
                )
            )
        )
        
    fig_age.update_layout(hovermode='x unified')
    
    return fig_age

def reset_age_percentage_graph(fig_age):
    fig_age.data = ()  # clear traces from the previous click before redrawing
    return fig_age