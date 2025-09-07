import pandas as pd
import streamlit as st
from io import BytesIO

def transform_wide_to_long(df):
    """
    Transforms a wide-format DataFrame with repeating columns into a long-format DataFrame.
    """
    # This is the same transformation logic as before, just placed in a function.
    # The list of columns and logic remains unchanged.
    static_cols = [
        'submissiondate', 'q1_enum_name', 'calc_date', 'calc_start_time', 'village_name',
        'farmer_id', 'farmer_name', 'phone_number', 'total_acres', 'plots', 'sowing_date',
        'transplant_date', 'harvest_date', 'no_of_plots', 'name_cnf', 'phone_reenter',
        'alt_phone', 'b4_plot_serials', 'total_plots', 'first_visit', 'a1_sowing_cnf',
        'a2a_sw_date', 'a2b_sw_date', 'a3_dsr', 'a4_dsr_type', 'a7_seed', 'a7_seed_oth',
        'a8_duration', 'a9_training', 'b1_area_cnf', 'b2_area_enter', 'b2_area_enter_1',
        'b2_area_enter_2', 'b2_enter_acres', 'b2_enter_guntas', 'b3_plots_cnf',
        'd10_window', 'd11_window_end', 'd12_rain', 'd13_tillering', 'd14_uneven',
        'fertilizer_date', 'e1_window', 'e2_dw_date', 'e3_dw_number', 'e4_fruits_id',
        'comments', 'instanceid', 'formdef_version', 'key', 'date_only', 'date_num',
        'dup_flag', 'visit_gap', 'daily_unique_farmers', 'depth', 'drying_event'
    ]

    max_plots = 0
    for col in df.columns:
        if col.startswith('this_plot_id_'):
            try:
                plot_num = int(col.split('_')[-1])
                if plot_num > max_plots:
                    max_plots = plot_num
            except ValueError:
                continue

    long_data = []

    plot_col_patterns = [
        'this_plot_id', 'this_plot_label1', 'w3w_link', 'w3w_latlong', 'to_be_updated',
        'message', 'w3w_okay', 'new_plot_entr', 'new_w3w_link', 'scto_lat', 'scto_lon',
        'scto_alt', 'scto_acc', 'final_w3w_link', 'w3w_corrected'
    ]
    
    pipe_col_patterns = [
        'this_plot_id2', 'this_plot_label2', 'b8a_plot_awd', 'b8b_plot_dsr',
        'b9_field_dsr_indi', 'b9_field_dsr_indi_1', 'b9_field_dsr_indi_2',
        'b9_field_dsr_indi_3', 'b9_field_dsr_indi_4', 'b9_field_dsr_indi__996',
        'b9_oth', 'awd_plot', 'dsr_plot', 'c1_pipe_status', 'c2_pipe_distance',
        'pipe_image', 'd1_soil', 'd2_soil_removal', 'd3_wl_status', 'd4_wl_above',
        'd5_wl_below', 'd5_pipe_image', 'd6_pipeslatitude', 'd6_pipeslongitude',
        'd6_pipesaltitude', 'd6_pipesaccuracy', 'd8_puddles', 'd9_cracks'
    ]

    for _, row in df.iterrows():
        for i in range(1, max_plots + 1):
            plot_id_col = f'this_plot_id_{i}'
            if pd.notna(row.get(plot_id_col)):
                new_row = {}
                
                for col in static_cols:
                    new_row[col] = row.get(col)
                
                for pattern in plot_col_patterns:
                    col_name = f'{pattern}_{i}'
                    if col_name in row:
                        new_row[pattern] = row[col_name]
                
                for pattern in pipe_col_patterns:
                    col_name = f'{pattern}_{i}'
                    if col_name in row:
                        new_row[pattern] = row[col_name]
                
                long_data.append(new_row)

    return pd.DataFrame(long_data)

# Streamlit UI
st.title("Wide to Long Data Transformer")

uploaded_file = st.file_uploader("Upload your wide-format CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Read the file based on its type
    try:
        if uploaded_file.name.endswith('.csv'):
            df_wide = pd.read_csv(uploaded_file, low_memory=False)
        else:
            df_wide = pd.read_excel(uploaded_file)
        
        st.write("Original Data:")
        st.dataframe(df_wide.head())

        # Perform the transformation
        df_long = transform_wide_to_long(df_wide)
        
        st.success("Transformation successful! 🎉")
        st.write("Transformed Data:")
        st.dataframe(df_long.head())

        # Provide the download button
        csv_buffer = BytesIO()
        df_long.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        st.download_button(
            label="Download Transformed CSV",
            data=csv_buffer,
            file_name="transformed_data.csv",
            mime="text/csv",
        )
        
    except Exception as e:
        st.error(f"An error occurred: {e}")