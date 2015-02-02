import sys
import json

States = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

Boundingboxs = [
    {"boundingbox":["30.1375217437744","35.0080299377441","-88.4731369018555","-84.8882446289062"],"display_name":"Alabama"},
    {"boundingbox":["31.3321762084961","37.0042610168457","-114.818359375","-109.045196533203"],"display_name":"Arizona"},
    {"boundingbox":["33.0041046142578","36.4996032714844","-94.6178131103516","-89.6422424316406"],"display_name":"Arkansas"},
    {"boundingbox":["32.5295219421387","42.0095024108887","-124.482009887695","-114.13077545166"],"display_name":"California"},
    {"boundingbox":["36.9924240112305","41.0023612976074","-109.060256958008","-102.041580200195"],"display_name":"Colorado"},
    {"boundingbox":["40.9667053222656","42.0505905151367","-73.7277755737305","-71.7869873046875"],"display_name":"Connecticut"},
    {"boundingbox":["38.4511260986328","39.8394355773926","-75.7890472412109","-74.9846343994141"],"display_name":"Delaware"},
    {"boundingbox":["24.3963069915771","31.0009689331055","-87.6349029541016","-79.9743041992188"],"lat":"27.7567667","lon":"-81.4639835","display_name":"Florida"},
    {"boundingbox":["30.3557567596436","35.0008316040039","-85.6051712036133","-80.7514266967773"],"lat":"32.3293809","lon":"-83.1137366","display_name":"Georgia"},
    {"boundingbox":["41.9880561828613","49.000846862793","-117.243034362793","-111.043563842773"],"lat":"43.6447642","lon":"-114.0154071","display_name":"Idaho"},
    {"boundingbox":["36.9701309204102","42.5083045959473","-91.513053894043","-87.0199203491211"],"lat":"40.0796319","lon":"-89.4339809","display_name":"Illinois"},
    {"boundingbox":["37.7717399597168","41.7613716125488","-88.0997085571289","-84.7845764160156"],"lat":"40.3270127","lon":"-86.1746933","display_name":"Indiana"},
    {"boundingbox":["40.3755989074707","43.5011367797852","-96.6397171020508","-90.1400604248047"],"lat":"41.9216734","lon":"-93.3122705","display_name":"Iowa"},
    {"boundingbox":["36.9930801391602","40.0030975341797","-102.0517578125","-94.5882034301758"],"lat":"38.27312","lon":"-98.5821872","display_name":"Kansas"},
    {"boundingbox":["36.4967155456543","39.1474609375","-89.5715103149414","-81.9645385742188"],"lat":"37.5726028","lon":"-85.1551411","display_name":"Kentucky"},
    {"boundingbox":["28.9210300445557","33.019458770752","-94.0431518554688","-88.817008972168"],"lat":"30.8703881","lon":"-92.007126","display_name":"Louisiana"},
    {"boundingbox":["42.9561233520508","47.4598426818848","-71.0841751098633","-66.9250717163086"],"lat":"45.709097","lon":"-68.8590201","display_name":"Maine"},
    {"boundingbox":["37.8856391906738","39.7229347229004","-79.4871978759766","-75.0395584106445"],"lat":"39.5162234","lon":"-76.9382069","display_name":"Maryland"},
    {"boundingbox":["41.1863288879395","42.8867149353027","-73.5081481933594","-69.8615341186523"],"lat":"42.3788774","lon":"-72.032366","display_name":"Massachusetts"},
    {"boundingbox":["41.6960868835449","48.3060646057129","-90.4186248779297","-82.122802734375"],"lat":"43.6211955","lon":"-84.6824346","display_name":"Michigan"},
    {"boundingbox":["43.4994277954102","49.3844909667969","-97.2392654418945","-89.4833831787109"],"lat":"45.9896587","lon":"-94.6113288","display_name":"Minnesota"},
    {"boundingbox":["30.1477890014648","34.9960556030273","-91.6550140380859","-88.0980072021484"],"lat":"32.9715645","lon":"-89.7348497","display_name":"Mississippi"},
    {"boundingbox":["35.9956817626953","40.6136360168457","-95.7741470336914","-89.0988388061523"],"lat":"38.7604815","lon":"-92.5617875","display_name":"Missouri"},
    {"boundingbox":["44.3582191467285","49.0011100769043","-116.050003051758","-104.039558410645"],"lat":"47.3752671","lon":"-109.6387579","display_name":"Montana"},
    {"boundingbox":["39.9999961853027","43.0017013549805","-104.053520202637","-95.3080520629883"],"lat":"41.7370229","lon":"-99.5873816","display_name":"Nebraska"},
    {"boundingbox":["35.0018730163574","42.0022087097168","-120.005729675293","-114.039642333984"],"lat":"39.5158825","lon":"-116.8537227","display_name":"Nevada"},
    {"boundingbox":["42.6970405578613","45.3057823181152","-72.55712890625","-70.534065246582"],"lat":"43.4849133","lon":"-71.6553992","display_name":"New Hampshire"},
    {"boundingbox":["38.7887535095215","41.3574256896973","-75.5633926391602","-73.8850555419922"],"lat":"40.0757384","lon":"-74.4041622","display_name":"New Jersey"},
    {"boundingbox":["31.3323001861572","37.0001411437988","-109.050178527832","-103.000862121582"],"lat":"34.5708167","lon":"-105.993007","display_name":"New Mexico"},
    {"boundingbox":["40.4773979187012","45.0158615112305","-79.7625122070312","-71.8527069091797"],"lat":"43.1561681","lon":"-75.8449946","display_name":"New York"},
    {"boundingbox":["33.7528762817383","36.5880393981934","-84.3218765258789","-75.4001159667969"],"lat":"35.6729639","lon":"-79.0392919","display_name":"North Carolina"},
    {"boundingbox":["45.9350357055664","49.0004920959473","-104.049270629883","-96.5543899536133"],"lat":"47.6201461","lon":"-100.540737","display_name":"North Dakota"},
    {"boundingbox":["38.4031982421875","42.3232383728027","-84.8203430175781","-80.5189895629883"],"lat":"40.2253569","lon":"-82.6881395","display_name":"Ohio"},
    {"boundingbox":["33.6191940307617","37.0021362304688","-103.002571105957","-94.4312133789062"],"lat":"34.9550817","lon":"-97.2684063","display_name":"Oklahoma"},
    {"boundingbox":["41.9917907714844","46.2991027832031","-124.703544616699","-116.463500976562"],"lat":"43.9792797","lon":"-120.737257","display_name":"Oregon"},
    {"boundingbox":["39.7197647094727","42.5146903991699","-80.5210876464844","-74.6894989013672"],"lat":"40.9699889","lon":"-77.7278831","display_name":"Pennsylvania"},
    {"boundingbox":["41.055534362793","42.018856048584","-71.9070053100586","-71.1204681396484"],"lat":"41.7962409","lon":"-71.5992372","display_name":"Rhode Island"},
    {"boundingbox":["32.0333099365234","35.2155418395996","-83.35400390625","-78.4992980957031"],"lat":"33.6874388","lon":"-80.4363743","display_name":"South Carolina"},
    {"boundingbox":["42.4798889160156","45.9454536437988","-104.05770111084","-96.4363327026367"],"lat":"44.6471761","lon":"-100.348761","display_name":"South Dakota"},
    {"boundingbox":["34.9829788208008","36.6781196594238","-90.310302734375","-81.6468963623047"],"lat":"35.7730076","lon":"-86.2820081","display_name":"Tennessee"},
    {"boundingbox":["25.8370609283447","36.5007057189941","-106.645652770996","-93.5078201293945"],"lat":"31.8160381","lon":"-99.5120986","display_name":"Texas"},
    {"boundingbox":["36.9979667663574","42.0013885498047","-114.053932189941","-109.041069030762"],"lat":"39.4225192","lon":"-111.7143584","display_name":"Utah"},
    {"boundingbox":["42.7269325256348","45.0166664123535","-73.437744140625","-71.4653549194336"],"lat":"44.5990718","lon":"-72.5002608","display_name":"Vermont"},
    {"boundingbox":["36.5407867431641","39.4660148620605","-83.6754150390625","-75.2312240600586"],"lat":"37.1232245","lon":"-78.4927721","display_name":"Virginia"},
    {"boundingbox":["45.5437202453613","49.00244140625","-124.836097717285","-116.917427062988"],"lat":"47.2868352","lon":"-120.2126139","display_name":"Washington"},
    {"boundingbox":["37.2014808654785","40.638801574707","-82.6447448730469","-77.7190246582031"],"lat":"38.4758406","lon":"-80.8408415","display_name":"West Virginia"},
    {"boundingbox":["42.491943359375","47.3025016784668","-92.8881149291992","-86.2495422363281"],"lat":"44.4308975","lon":"-89.6884637","display_name":"Wisconsin"},
    {"boundingbox":["40.9948768615723","45.0034217834473","-111.05689239502","-104.052154541016"],"lat":"43.1700264","lon":"-107.5685348","display_name":"Wyoming"},
    {"display_name":"Alaska", "boundingbox":["54.1","71.1","-167.9","-141.2"]},
    {"display_name":"Hawaii", "boundingbox":["18.8","22.2","-160.3","-154.8"]}]

def get_state(lon,lat):
    for bounding in Boundingboxs:
        lat1,lat2,lon1,lon2=bounding["boundingbox"]
        if lon>=lon1 and lon<=lon2 and lat>=lat1 and lat<=lat2:
            stateName = bounding["display_name"]
            return [state for state, name in States.items() if name == stateName]
    return []

def nameToState(name):
    for state,stateName in States.items():
        if stateName==name:
            return state
    return ""    

def get_location(tw):
    states=[]
    place = tw.get("place",{})
    if not (place=={} or place ==None):
        country_code = place.get("country_code","")
        if country_code.encode('utf-8') == 'US':
            full_name = place.get("full_name","")
            if not full_name=="":
                if not full_name.find(',')==-1:
                    city, state=full_name.split(", ")
                    if not state.strip()=="USA":
                        states.append(state.strip())
                        return states
                    else:
                        state=nameToState(city.strip())
                        if not state=="":
                            states.append(state)
                            return states

    coords = tw.get("coordinates","")
    if not (coords=="" or coords==None):
        if coords["type"].lower()=="point":
            lon,lat=coords["coordinates"]
            return get_state(lon,lat)

    return []

def rank_states(states):
    maxscore=-100
    scores={}
    for state, (sent,num) in states.items():
        score = float(sent)/float(num)
        scores[state]= score
        if score > maxscore:
            maxscore = score

    return [state for state, score in scores.items() if score == maxscore][0]

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2]) #.readlines()

    scores = {} # initialize an empty dictionary
    happyscores = {}
    for line in sent_file:
         term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
         scores[term] = int(score)  # Convert the score to an integer.

    for line in tweet_file:
	tweet=json.loads(line)
#        print tweet.get("place",None)
	sentiment=0
	for term in tweet.get("text","").encode('utf-8').translate(None,"!\"#$%&()*+,-./:;<=>?@[\]^_`{|}~").lower().split():
            sentiment=sentiment+scores.get(term,0)
        for state in  get_location(tweet):
            sent,num = happyscores.get(state,(0,0))
            happyscores[state] = (sent+sentiment, num+1)

    print rank_states(happyscores)
    
if __name__ == '__main__':
    main()


