import csv, operator
import pandas as pd
import pandas as pd2
from google.cloud import storage
import os
import codecs

def process_file(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    l_state = ''
    old_name_file = ''
    name_file = ''
    j = 0
    i = 1
    l_project = 'veronica-olea-02'
    file_tmp = 'data.csv'
    folder = '/tmp'
    l_file_tmp = folder + '/' + file_tmp
    l_file_sort = folder + '/' + 'data_sort.csv'
    client = storage.Client(project=l_project)
    blob_name = 'to-process/airports.csv'
    bucket = client.get_bucket('ejercicio-01')

    blob = bucket.blob(blob_name)
    if blob.exists():
        #sort file
    	blob.download_to_filename(l_file_tmp)
    	data_tmp = pd.read_csv(l_file_tmp,
                    names=['IATA','AIRPORT','CITY','STATE','COUNTRY','LATITUDE','LONGITUDE'],
                    index_col=['STATE'])
    	df = pd.DataFrame(data_tmp)
    	df.sort_index(inplace=True)
    	df.to_csv(l_file_sort)
        #read file to process
    	ifile  = open(l_file_sort, "rb")
    	data_file = csv.reader(codecs.iterdecode(ifile, 'utf-8'))
        #asign record for fist file
    	df2 = pd2.DataFrame(columns = ('STATE', 'IATA', 'AIRPORT', 'CITY', 'COUNTRY', 'LATITUDE', 'LONGITUDE'))
    	next(data_file)
        #read records to processs
    	for reg in data_file:
	        if l_state == '' or l_state != reg[0]:
                #name for new file
	            l_state = reg[0]
                name_file = 'airport_by_state_' + str(i) + '.csv'
            	i = i + 1
            	if old_name_file == '':
                	old_name_file = name_file
                	j = 1
			
            	if old_name_file != name_file:
                    #upload file by group
                	df2.to_csv( folder + '/' + old_name_file)
                	blob_2 = bucket.blob('processed/' + old_name_file)
                	with open(folder + '/' + old_name_file, 'rb') as grouped:
                    	blob_2.upload_from_file(grouped)
                    	grouped.close()
                    
                	os.remove(folder + '/' + old_name_file)
                	old_name_file = name_file
                	j = 1
                    #header for new file
                	df2 = pd2.DataFrame(columns = ( 'STATE', 'IATA', 'AIRPORT', 'CITY', 'COUNTRY', 'LATITUDE', 'LONGITUDE'))
                #asign first record to file
            	df2.loc[j] = reg
		
        	else:
                #asign record to file
            	j = j  + 1
            	df2.loc[j] = reg
        #delete files
    	blob.delete()
    	csvarchivo.close()
    	os.remove(l_file_tmp)
    	os.remove(l_file_sort)
    
