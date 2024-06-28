import os
import pandas as pd
import xlsxwriter

def save_presence_matrix_and_plot(directory_path, excel_file_name='species_presence_matrix.xlsx'):
    # Load the Excel file
    excel_path = os.path.join(directory_path, excel_file_name)
    matrix = pd.read_excel(excel_path, index_col=0)  # Ensure the index (species names) is loaded correctly

    # Calculate the number of files each species is present in and sort in descending order
    presence_counts = (matrix == 'Y').sum(axis=1)
    presence_counts_sorted = presence_counts.sort_values(ascending=False)

    # Reorder the matrix according to the sorted presence counts
    matrix_sorted = matrix.loc[presence_counts_sorted.index]

    # Create a new Excel file for output with an embedded chart
    output_excel_path = os.path.join(directory_path, 'output_with_chart.xlsx')
    with pd.ExcelWriter(output_excel_path, engine='xlsxwriter') as writer:
        # Write the sorted presence counts and the reordered matrix to the Excel file
        presence_counts_sorted.to_excel(writer, sheet_name='Presence Counts')
        matrix_sorted.to_excel(writer, sheet_name='Sorted Matrix')

        # Access the xlsxwriter workbook and worksheet objects from the dataframe
        workbook = writer.book
        worksheet = writer.sheets['Presence Counts']

        # Create a chart object
        chart = workbook.add_chart({'type': 'bar'})

        # Configure the chart from the DataFrame data. Adjust the range accordingly
        # Ensure the sheet name is quoted if it contains spaces
        chart.add_series({
            'name': 'Presence Counts',
            'categories': f"='Presence Counts'!$A$2:$A${len(presence_counts_sorted) + 1}",
            'values': f"='Presence Counts'!$B$2:$B${len(presence_counts_sorted) + 1}",
        })

        # Set chart title and axis labels
        chart.set_title({'name': 'Number of Genes Each Species is Present In'})
        chart.set_x_axis({'name': 'Species Name'})
        chart.set_y_axis({'name': 'Number of Files'})

        # Insert the chart into the worksheet
        worksheet.insert_chart('D2', chart)

    return output_excel_path

# Usage
directory_path = '/Users/kshitij_mac/Desktop/9560/simplified_trees/'  # Adjusted to your specific path
output_path = save_presence_matrix_and_plot(directory_path)
print(f"Output with chart saved to: {output_path}")
