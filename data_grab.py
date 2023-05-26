import json
import requests
import pandas as pd
import ssl
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

# Get names and addresses
acc_url = "https://www.queensu.ca/facilities/accessibility/building-directory"

data = pd.read_html(acc_url)[0]
# Get the link table. Pandas doesn't preserve hyperlinks.
sp_acc = BeautifulSoup(requests.get(acc_url).text, 'html.parser')
link_table = \
    [
        [
            [
                item['href'] for item in td.find_all('a')
            ]
            for td in tr.find_all('td')
        ]
        for tr in sp_acc.find_all('table')[0].find_all('tr')
    ]

for x in range(len(data)):
    # Generate Tag (there are many inconsistent tags that were accounted for).
    d_name = str(data.iloc[x, 0]).lower().replace(" ", "-")
    name = str(data.iloc[x,0]).replace("Lab", "Laboratory").replace(" Le-Caine", "-LeCaine")

    match d_name:
        case "the-university-club":
            d_name = "university-club-queens"
        case "the-law-building":
            d_name = "law-building"
        case "school-of-kinesiology-and-health-studies":
            d_name = "kinesiology-and-health-studies-school"
        case "richardson-lab":
            name = "Richardson Laboratory"
            d_name = "richardson-laboratory"
        case "richardson-stadium":
            d_name = "george-richardson-memorial-stadium"
        case "queen's-centre-/-athletics-and-recreation-centre-(arc)":
            name = "Queen's Athletics Recreation Centre"
            d_name = "athletics-and-recreation-centre-arc"
        case "new-medical-building":
            d_name = "school-medicine-building"
        case "louise-d.-acton-building":
            d_name = "louise-d-acton-building"
        case "joseph-s.-stauffer-library":
            d_name = "stauffer-library"
        case "john-watson-hall":
            d_name = "watson-hall"
        case "isabel-bader-centre-for-performing-arts":
            d_name = "isabel-bader-centre-performing-arts"
        case "harrison-le-caine-hall":
            d_name = "harrison-lecaine-hall"
        case "the-grad-club":
            d_name = "grad-club"
        case "four-directions-indigenous-student-centre":
            d_name = "four-directions"
        case "flemming-hall---stewart-pollock-wing":
            d_name = "fleming-hall"
        case "flemming-hall:-jemmet-wing":
            d_name = "fleming-hall"
        case "donald-gordon-centre":
            d_name = "donald-gordon-conference-centre"
        case "chernoff-hall-&-auditorium":
            d_name = "chernoff-hall"
        case "biosciences-complex-&-earl-hall":
            d_name = "biosciences-complex"
        case "asus-offices":
            d_name = "arts-and-science-undergraduate-society-asus"
        case "office-of-advancement,-faculty-of-health-sciences-building":
            d_name = "health-sciences-faculty"
        case "environmental-health-&-safety-building":
            d_name = "ehs-building"
        case "bruce-wing":
            d_name = "miller-hall"
        case "78-barrie-street":
            d_name = "administrative-offices"
        case "macklem-house":
            d_name = "katherine-bermingham-macklem-house"
        case "184-union-st":
            d_name = "queens_daycare"
            name = "Queen's Day Care Centre"
        case "186-barrie-st":
            d_name = "186-barrie-street"

    # Get expected encyclopedia entry.
    url = "https://www.queensu.ca/encyclopedia" + "/" + d_name[0] + "/" + d_name

    # The one building where it's entry doesn't start with its alphabetical beginning.
    if d_name == "katherine-bermingham-macklem-house":
        url = "https://www.queensu.ca/encyclopedia/m/katherine-bermingham-macklem-house"
    req_response = requests.get(url)
    z = 0
    text = ""
    images = []
    alts = []
    links = []

    # If the expected entry exists.
    if req_response.status_code == 200:
        soup = BeautifulSoup(req_response.text, 'html.parser')

        text = [i.text for i in soup.find_all('article')[0].find_all('p')]
        # Get all images in the page.
        for item in soup.find_all('img'):
            # Ignore SVGs (menu icons, queen's logo, etc.)
            if str(item)[len(item) - 6:len(item) - 3] != "svg":
                out_str = str("/images/buildings/" + d_name + "-" + str(z) + ".jpg")
                img_str = str("./public/images/buildings/" + d_name + "-" + str(z) + ".jpg")
                try:
                    # Try to write the image to local storage.
                    with open(img_str, 'wb') as handler:
                        handler.write(requests.get(("https://www.queensu.ca" + item['src'])).content)
                        images.append(out_str)
                        alts.append(item['alt'])
                        z += 1
                        # Get the alt text (wouldn't be much of an accessibility app if visually-impaired can't use it)
                except:
                    try:
                        # Accounting for some WebPublish 2 legacy formatting.
                        with open(img_str, 'wb') as handler:
                            handler.write(requests.get(("https://www.queensu.ca" + item['data-src'])).content)
                            images.append(out_str)
                            alts.append(item['alt'])
                            z += 1
                    except Exception as e:
                        print(e)
    else:
        url = ""
        text = name
        
    if len(images) == 0:
        # If no images found, use one of the ones I downloaded manually.
        images.append("/images/buildings/" + d_name + ".jpg")
        alts.append("Street view of " + str(data.iloc[x, 0]) + ".")


    # Get accessibility description
    sp_2 = BeautifulSoup(requests.get("https://www.queensu.ca" + link_table[x + 1][0][0]).text, 'html.parser')
    
    acc_des = []
    location = ""
    entrances = []
    elevators = ""
    corridors = ""
    wayfinding = ""
    washrooms = ""
    fountains = ""
    classrooms = ""
    services = ""
    parking = ""

    for i in sp_2.find_all('article')[0].find_all('p'):
        p = i.text.replace("\u00a0", " ")
        
        if p.find("Location") != -1:
            location = p.replace("Location: ", "")
        elif p.find("Entrances") != -1 or \
            (p.find("North") != -1 and p.find("Northern") == -1) or \
            (p.find("East")  != -1 and p.find("Eastern")  == -1) or \
            (p.find("West")  != -1 and p.find("Western")  == -1 and p.find("Street West")  == -1) or \
            (p.find("South") != -1 and p.find("Southern") == -1) or \
            p.find("Other Entrances") != -1 or \
            p.find("Alternative Entrance") != -1 or \
            p.find("Other entrances") != -1:

            entrances.append(p.replace("Entrances: ", ""))
        elif p.find("Corridor") != -1 or p.find("Corridors") != -1:
            corridors = p.replace("Corridors: ", "")
        elif p.find("Wayfinding") != -1:
            wayfinding = p.replace("Wayfinding: ", "")
        elif p.find("Washrooms") != -1:
            washrooms = p.replace("Washrooms: ", "")
        elif p.find("Water Fountain") != -1:
            fountains = p.replace("Water Fountain: ", "")
        elif p.find("Classrooms") != -1:
            classrooms = p.replace("Classrooms: ", "")
        elif p.find("Services") != -1:
            services = p.replace("Services: ", "")
        elif p.find("Parking") != -1:
            parking = p.replace("Parking: ", "")
        elif p.find("Elevators") != -1:
            elevators = p.replace("Elevators: ", "")
        else:
            acc_des.append(p)
    
    print(name + " " + str(data.iloc[x, 1]))

    # Convert shortened Google Maps links to long-form.
    shorturl = link_table[x + 1][4][len(link_table[x + 1][4]) - 1]
    session = requests.Session()
    resp = session.head(shorturl, allow_redirects=True)
    longurl = resp.url
    if(d_name == 'chernoff-hall'):
        longurl = "https://www.google.ca/maps/place//@44.2246547,-76.4993621,18z"
    # Get Coordinates From Google Maps
    temp = longurl.split('/')[6].replace('@','').split(',')
    latg = float(temp[0])
    long = float(temp[1]) + .0021

    # Get co-ordinates (with name)
    coord_resp = requests.get(("http://localhost:8081/?addressdetails=1&q=" + name.replace("ASUS Offices", "ASUS Core") + ",+kingston,+ontario&format=json&limit=1").lower().replace(" ", "+"), headers=headers)
    coord_resp = coord_resp.json()

    # If grabbing with the name failed, grab with just address (may not be centred correctly)
    if (coord_resp == []):
        coord_resp = requests.get(("http://localhost:8081/?addressdetails=1&q=" + str(data.iloc[x, 1]) + ",+kingston&format=json&limit=1").lower().replace(" ", "+"), headers=headers)
        coord_resp = coord_resp.json()
    
    lat = 0.0
    lon = 0.0

    # Take the average of results (potentially increasing accuracy)
    for i in coord_resp:
        lat += float(i["lat"])
        lon += float(i["lon"])
    
    # Handle divide by zero
    if (coord_resp != []):
        lat = lat/len(coord_resp)
        lon = lon/len(coord_resp)

    dictionary = {
        "name": name,
        "coords": [lat, lon] if (coord_resp != []) else [latg, long],
        "addr": str(data.iloc[x, 1]),
        "images": [{'src':images[i], 'alt':alts[i]} for i in range(len(images))],
        "desc": [i for i in text if (i != "")],
        "location" : location,
        "entrances" : [i for i in entrances if ("Entrances" not in i)],
        "corridors" : corridors,
        "wayfinding" : wayfinding,
        "washrooms" : washrooms,
        "fountains" : fountains,
        "classrooms" : classrooms,
        "elevators" : elevators,
        "services" : services,
        "parking" : parking,
        "desc_src": url,
        "access": [st for st in acc_des if ("Link to " not in st) and ("Floor Plans" not in st) and ("Site Plans" not in st) and ("Floor Plan" not in st) and ("Site Plan" not in st)],
        "map": shorturl
    }

    with open(str("./buildings/" + d_name + ".json"), "w") as outfile:
        json.dump(dictionary, outfile)
