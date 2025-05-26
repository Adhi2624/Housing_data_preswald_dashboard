from preswald import connect, get_df, query, table, text, plotly,slider,selectbox
import plotly.express as px
import pandas as pd


connect() 
df = get_df("Housing")

numeric_columns = ['price', 'area', 'bedrooms', 'bathrooms', 'stories', 'parking']
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col] = df[col].fillna(df[col].median())
categorical_columns = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea', 'furnishingstatus']
for col in categorical_columns:
    df[col] = df[col].fillna('Unknown')

columns=['bedrooms', 'bathrooms', 'stories', 'parking','mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea', 'furnishingstatus']

text("# Housing Price Dashboard")
minval=min(df["area"])
maxval=max(df['area'])
sliderData=slider(label='slider for area',min_val=int(minval),max_val=int(maxval))



sql = f"""
SELECT CAST(price AS FLOAT) AS price,
       CAST(area AS FLOAT) AS area,
       CAST(bedrooms AS FLOAT) AS bedrooms,
       CAST(bathrooms AS FLOAT) AS bathrooms,
       CAST(stories AS FLOAT) AS stories,
       mainroad,
       guestroom,
       basement,
       hotwaterheating,
       airconditioning,
       CAST(parking AS FLOAT) AS parking,
       prefarea,
       furnishingstatus
FROM Housing
WHERE CAST(area AS FLOAT) > {sliderData}
"""
filtered_df = query(sql, "Housing")




# text(f"Showing {len(filtered_df)} houses with area greater than {sliderData} sq ft")
table(filtered_df, title="Filtered Housing Data")

text("# Choose based on which category you want differnce",size=2.0)
opt=selectbox(label='options',default='bedrooms',options=columns)

fig = px.scatter(
        df,
        x="area",
        y="price",
        color=opt,
        size="bedrooms",
        title=f"Area vs. Price by {opt} Status",
        labels={"area": "Area (sq ft)", "price": "Price ($)", "furnishingstatus": "Furnishing Status"}
    )
plotly(fig)
