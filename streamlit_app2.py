import pandas as pd
import streamlit as st
import plotly.express as px

#Configuration page of streamlit, change title, page icon and layout.
#Link page for emogi https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard",
                   page_icon=":bar_chart:",
                   layout='wide')

#----Read Excel with pandas----
@st.cache_data
def get_data_from_excel():
    df=pd.read_excel(
        io='supermarkt_sales.xlsx',
        engine='openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows=1000,
    )
    # Add 'Hour' column to dataframe
    df['Hour']=pd.to_datetime(df.Time,format="%H:%M:%S").dt.hour
    return df
df=get_data_from_excel()
#----SIDEBAR----
st.sidebar.header('Please Filter Here:')

#----Filters----
city=st.sidebar.multiselect(
    "Select the City:",
    options=df['City'].unique(),
    default=df['City'][0]
)

customer_type=st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df['Customer_type'].unique(),
    default=df['Customer_type'][0]
)

gender=st.sidebar.multiselect(
    "Select the City:",
    options=df['Gender'].unique(),
    default=df['Gender'][0]
)

Hour=st.sidebar.multiselect(
    "Select a Hour",
    options=df['Hour'].unique(),
    default=df['Hour'][0]
)
#----Fin Filters----
#----Fin SIDEBAR----
try:
    df_selection = df.query(
        "City == @city | Customer_type ==@customer_type | Gender == @gender | Hour == @Hour"
    )
except:
    df_selection = df.query()


#----Main Page----
st.title(":bar_chart: Sales Dasboard")
st.markdown("##") #El numeral da un salto de linea

#----TOP KPI'S----
total_sales=int(df_selection["Total"].sum())
average_rating=round(df_selection["Rating"].mean(),1)
start_rating=":star:"*int(round(average_rating,0))
average_sale_by_transaction=round(df_selection["Total"].mean(),2)

left_column,middle_column,right_column=st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US ${total_sales:,}")
with middle_column:
    st.subheader("Average Rating")
    st.subheader(f"{average_rating} {start_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US ${average_sale_by_transaction}")

st.markdown("----")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).agg({"Total":"sum"}).sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

#SALES BY HOUR [BAR CHART]
sales_by_hour = df_selection.groupby(by=["Hour"]).agg({"Total":"sum"}).sort_values(by="Total")
fig_hourly_sales=px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

#CONTAINER CHARTS
left_column,right_column=st.columns(2)
left_column.plotly_chart(fig_hourly_sales,use_container_width=True)
right_column.plotly_chart(fig_product_sales,use_container_width=True)

#----HIDE STREAMLIT STYLE----
hide_st_style="""
            <style>
            #MainMenu {visibility:hidden;}
            footer {visibility:hidden;}
            header {visibility:hidden;}
            </style>
"""
st.markdown(hide_st_style,unsafe_allow_html=True)
#----Print dataframe for screen----
#st.dataframe(df_selection)
