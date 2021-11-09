# Importing library
import cv2
import pandas as pd
import os
from geopy.geocoders import Nominatim
import geopy.distance
from pathlib import Path
from pyzbar.pyzbar import decode
from countryinfo import CountryInfo
code_path=Path(__file__).resolve().parent
project_path=code_path.parent
data_path=project_path/"data"

def BarcodeDecoder(image,user_location="Brussels,Belgium"):
    country_list=pd.read_excel(os.path.join(data_path,"country_code.xlsx"))

    #First 3 digits= country of origin
    barcode_data, barcode_type=BarcodeReader(image)
    try:
        barcode_data=str(int(barcode_data))
    except:
        pass
    if barcode_type=="EAN13":
        len_barcode=len(barcode_data)
        if len_barcode==13:
            barcode_data='00'+str(barcode_data)
        elif len_barcode==14:
            barcode_data='0'+str(barcode_data)
        elif len_barcode==15:
            barcode_data=str(barcode_data)
        else:
            target_location=''
        try:
            country_code=int(barcode_data[:3])
            country_list=country_list.loc[country_list['Code'] == country_code]
            country=country_list["Country"].values[0]
            capital = CountryInfo(country).capital()
            target_location=capital+","+country
        except:
            target_location = ''
    else:
        target_location=''
    if target_location !='':
        distance=compute_product_distance(target_location, user_location)
        output ="Your product travelled for "+str(int(distance))+ " kilometers , all the way from "+country + "! "
    else:
        output=" We couldn't compute the country of origin of your product. Probably a galaxy far far away though. Buy local ! "
    return output

def compute_product_distance(target_location,user_location):
    # instantiate a new Nominatim client
    app = Nominatim(user_agent="tutorial")
    location = app.geocode(target_location).raw
    latitude=location['lat']
    longitude=location['lon']
    coords_1=[latitude,longitude]
    location_user = app.geocode(user_location).raw
    latitude_user=location_user['lat']
    longitude_user=location_user['lon']
    coords_2=[latitude_user,longitude_user]
    kilometers=geopy.distance.geodesic(coords_1, coords_2).km
    return kilometers

# Make one method to decode the barcode
def BarcodeReader(image):
    # read the image in numpy array using cv2
    img = cv2.imread(image)

    # Decode the barcode image
    detectedBarcodes = decode(img)

    # If not detected then print the message
    if not detectedBarcodes:
        print("Barcode Not Detected or your barcode is blank/corrupted!")
        barcode_data=""
        barcode_type=""
    else:

        # Traverse through all the detected barcodes in image
        for barcode in detectedBarcodes:

            # Locate the barcode position in image
            (x, y, w, h) = barcode.rect

            # Put the rectangle in image using
            # cv2 to heighlight the barcode
            cv2.rectangle(img, (x - 10, y - 10),
                          (x + w + 10, y + h + 10),
                          (255, 0, 0), 2)

            if barcode.data != "":
                # Print the barcode data
                barcode_data=barcode.data
                barcode_type=barcode.type
    return barcode_data,barcode_type

    # Display the image
    '''cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''


if __name__ == "__main__":
    # Take the image from user
    image = os.path.join(data_path,"barcode4.jfif")
    output=BarcodeDecoder(image)
    print(output)
