import requests
import requests_cache
import json
import datetime as dt
from matplotlib import pyplot as plt
plt.close('all')

#Call the APIs
requests_cache.install_cache('cv19erl', expire_after = 3600) #to avoid too many requests
API_hystory = 'https://geodaten.erlangen.de/opendata/api/v1/corona?api_key=db065a8e-68b2-4dae-b94b-d7c3376f6185'
landkreisObjectId = '282' #Erlangen
API_fresh = 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=OBJECTID%20%3E%3D%20'+landkreisObjectId+'%20AND%20OBJECTID%20%3C%3D%20'+landkreisObjectId+'&outFields=OBJECTID,death_rate,cases,deaths,cases_per_100k,cases_per_population,BL,BL_ID,county,last_update,cases7_per_100k,recovered,cases7_bl_per_100k,cases7_per_100k_txt,cases7_lk&outSR=4326&f=json'
response_hystory = requests.get(API_hystory)
data_hystory = response_hystory.json()
response_fresh = requests.get(API_fresh)
data_fresh = response_fresh.json()

# Take and format the hystorical data
#FIXME the date is managed in a sporty way, it combines dates from the APIs with local date.
deaths = [int(i['deaths']) for i in data_hystory]
dates = [i['stand'] for i in data_hystory]
cases = [int(i['cases']) for i in data_hystory]
cases100k7 = [i['cases7_per_100k'] for i in data_hystory]
dates = [dt.datetime.strptime(i, '%Y-%m-%dT%H:%M:%S.%fZ').date() for i in dates]

# format and appends the fresh data
data_fresh = data_fresh['features'][0]['attributes']
dates.append(dt.date.today() - dt.timedelta(days=1))
cases.append(data_fresh['cases'])
cases100k7.append(data_fresh['cases7_per_100k'])
deaths.append(data_fresh['deaths'])

# print(json.dumps(data2, sort_keys=True, indent=4))

#plot the data
plt.plot(dates,deaths,label='deaths',color='k')
plt.plot(dates,cases100k7,label='cases/100k/7',color='b')
plt.plot(dates[-1],deaths[-1],marker='o',color='k')
plt.plot(dates[-1],cases100k7[-1],marker='o',color='b')

#formatting the graph
today=dt.date.today().strftime("%d %m %Y")
plt.title('Covid Erlangen {}'.format(today))
plt.grid()
plt.legend()
plt.ylim(bottom=0)
plt.gcf().autofmt_xdate()

#adding the color bands
a,b=plt.gca().get_xlim()
c,d=plt.gca().get_ylim()
plt.fill_between((a,b),35,50,color='green',alpha=0.2)
plt.fill_between((a,b),50,100,color='orange',alpha=0.2)
plt.fill_between((a,b),100,d,color='red',alpha=0.2)
plt.xlim(a,b)
plt.ylim(c,d)

#save the figure
plt.savefig('covidplot{}.png'.format(today), bbox_inches=0, dpi=600)
plt.show()
