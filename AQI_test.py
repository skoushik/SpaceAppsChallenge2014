import urllib
from xml.etree.ElementTree import parse
import datetime
import h5py


#today = datetime.utcnow().strftime("%Y-%m-%d")
today = datetime.date.today()
BASE_URL="http://modwebsrv.modaps.eosdis.nasa.gov/axis2/services/MODAPSservices/"

fivedays = datetime.timedelta(days=5)

def genericRequest(method, **kargs):
  retList = []

  url = BASE_URL + method
  if len(kargs) > 0:
    url += "?"

    for key, value in kargs.items():
      url += key + "=" + str(value) + "&"  # Extra & on the end doesn't seem to hurt anything

  root = parse(urllib.urlopen(url)).getroot()

  for element in root:
    retList.append(element.text)

  return retList

files = genericRequest("searchForFiles", product="MOD04_L2", 
                             # collection="5", 
                             start=str(today-fivedays), 
                             stop=str(today), 
                             north="43", south="33", 
                             west="-107", east="-93", 
                             coordsOrTiles="coords", dayNightBoth="DNB")

fileIDstr = ",".join(files)
fileUrls = genericRequest("getFileUrls", fileIds = fileIDstr)


for url in fileUrls:
	filename = url.split("/")[-1]
	urllib.urlretrieve(url,filename)
