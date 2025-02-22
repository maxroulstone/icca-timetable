import streamlit as st
import pandas as pd
import get_personal_timetable


all_groups = list(pd.read_csv('data/timetable.csv')['group'].unique())

# Sample data
data = {
    'Item': all_groups,
}
df = pd.DataFrame(data)

# Streamlit UI
st.title('ICCA Personal Timetable')

# Multi-select box
selected_items = st.multiselect('Select items:', df['Item'])

# Filter dataframe based on selection
filtered_df = get_personal_timetable.get_personal_timetable(selected_items)

# Display filtered dataframe
st.write('Personal Table:')
st.dataframe(filtered_df, width=1000)

# Convert filtered dataframe to ics format
ics_data = get_personal_timetable.csv_to_ics(filtered_df)


if not filtered_df.empty:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.download_button(
            label='Download Timetable as ICS',
            data=ics_data,
            file_name='timetable.ics',
            mime='text/calendar'
        )

    with col2:
        st.download_button(
            label='Download Timetable as CSV',
            data=filtered_df.to_csv(index=False),
            file_name='timetable.csv',
            mime='text/csv'
        )
else:
    st.write('No items selected.')
