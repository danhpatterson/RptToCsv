#SSMS Outputs files by default as .rpt, column aligned format.
#Pass in the input file, second parameter: either a filepath or 'df' to return a pandas Dataframe

#main('test.rpt','folder/filename.csv')
# dataframe=main('test.rpt','df')
def main(file,output='df'): 
    
    #We read in the first two lines, containing the headers and column lengths
    f = open(file, "r")
    counter=1
    for x in f:
        if counter==1:
            headers=x
        elif counter==2:
            line=x
            break
        counter+=1
        
    #Get the column headers from the first line
    new_columns=[]
    column_headers=headers.split()
    for field in column_headers:
        #This is a weird quirk that seems to affect the first header, usually the  field
        if 'ï»¿' in field:
            new_columns.append(field.replace('ï»¿',''))
        else:
            new_columns.append(field)
        
    #Get the column widths from the second line('Dashes and space separators')
    column_widths=[]
    line_split=line.split()
    for item in line_split:
        #Need to account for the space, therefore adding 1 to column length
        length=len(item)+1
        column_widths.append(length)
        
    #Read in the file using our above specs
    df=pd.read_fwf(file,names=new_columns,widths=column_widths,skiprows=[0,1])
    #Drops empty rows where all fields are empty-- this is a standard ouput of .rpt files
    df=df.dropna(how='all')
    
    if output=='df':
      return df
    else:
      #Save filepath
      if '.csv' not in output:
        output=output+'.csv'
      df.to_csv(output)
