"""
Credits:
Author: Santeri Heikkinen
Haravasto, Sprites - Mika Oja, Oulun yliopisto
"""

import random
import time
import pyglet
import haravasto

status = {
    "peli_status": True,
    "kentta": [],
    "liput": [],
    "miinat": [],
    "tyhjat": [],
    "kello": "",
    "vuosi": "",
    "minuutit": "",
    "vuoro_lkm": 0,
    "lopputulos": "",
    "kentta_koko": "",
    "miina_lkm": ""
}

hiiridata = {
    haravasto.HIIRI_VASEN: pyglet.window.mouse.LEFT,
    haravasto.HIIRI_KESKI: pyglet.window.mouse.MIDDLE,
    haravasto.HIIRI_OIKEA: pyglet.window.mouse.RIGHT
}

aika = {
    "aloitus": 0.0,
    "lopetus": 0.0
}

def alustus(): #resetoi eri sanakirjat pelin alkaessa 
    aika["aloitus"] = 0.0
    aika["lopetus"] = 0.0
    status["peli_status"] = True
    status["kentta"] = []
    status["liput"] = []
    status["miinat"] = []
    status["tyhjat"] = []
    status["vuoro_lkm"] = 0
    


def kasittele_hiiri(sij_x, sij_y, painike, muokkaus_nap):
    """
    Toimii pohjana kaikelle hiiren toiminnalle, joka on taas jaettu kahteen osaan:
    hiiren vasemman painikkeen toimintoihin sekä vastaavasti hiren oikean painikkeen
    toimintoihin.
    """
    liput = status["liput"]
    miinakentta = status["kentta"] #täytyvät olla mukana, jotta saadaan riittävät parametrit "kasittele_vasen" -funktiolle
    x = int(sij_x / 40) #jako, jotta toimii 40x40 spritejen kanssa          
    y = int(sij_y / 40)

    if status["peli_status"] == False: #tarkistetaan ensin voidaanko ottaa vastaan uusia painalluksia
        print("Peli on jo päättynyt. Aloita uusi peli.") #funktio ei mene painalluksia käsittelevään osaan
    else:
        if painike == hiiridata[haravasto.HIIRI_VASEN]: #jos vasen painike painettu
            kasittele_vasen(x, y, miinakentta, liput) #käsitellään kys painallus
        elif painike == hiiridata[haravasto.HIIRI_OIKEA]: #jos oikea painike painettu
            kasittele_oikea(x, y, miinakentta, liput) #käsitellään kys painallus
        if not status["tyhjat"]: #jos ei enää tyhjiä ruutuja jäljellä
            print("Onnittelut! Voitit pelin!")
            loppu_kasittely()
            aika["lopetus"] = time.time()
            rem = round(aika["lopetus"]-aika["aloitus"]) #ilman round -metodia ei toimi 
            min, sek = divmod(rem, 60)
            status["minuutit"] = "{:d}:{:02d}".format(min, sek)
            tilasto_kirjoitus() #kirjoittaa ylös pelin tiedot
    piirra_kentta()


def kasittele_oikea(x, y, miinakentta, liput):
    miinat = miina_laskuri(x, y, miinakentta)
    if miinakentta[y][x] == "0" or miinakentta[y][x] == str(miinat): #estää käyttäjää laittamasta lippua ei sallittuun paikkaan
        print("Et voi tehdä noin!")
    elif miinakentta[y][x] == " " or miinakentta[y][x] == "x":
        if (x, y) in liput: #jos ruudussa jo lippu
            liput.remove((x, y)) #päivitä tilanne
        else: #jos ruudussa ei ole lippua
            liput.append((x, y)) #päivitä tilanne
    

def kasittele_vasen(x, y, kentta, liput):  
    miinat = miina_laskuri(x, y, kentta)
    tyhja = status["tyhjat"]
    if kentta[y][x] == "x": #jos astutaan miinaan
        status["vuoro_lkm"] += 1 #vuorojen lkm nousee yhdellä
        print("Pahus! Astuit miinaan!")
        loppu_kasittely((x, y)) #tallentaa tiedon, jos voitit tai hävisit
        aika["lopetus"] = time.time()
        rem = round(aika["lopetus"]-aika["aloitus"]) #ilman round -metodia ei toimi 
        min, sek = divmod(rem, 60) #jaetaan 60:lla jotta saadaan minuutit, 
        status["minuutit"] = "{:d}:{:02d}".format(min, sek)
        tilasto_kirjoitus() #kirjoittaa ylös pelin tiedot
    elif kentta[y][x] == " " and 0 < miinat < 10: #jos tuntemattoman ruudun ympärillä miinoja
        status["vuoro_lkm"] += 1 #jos valitaan ruutu, jossa ei miinaa, mutta ympärillä miinoja
        if (x, y) in tyhja: #jos painettu ruutu oli tyhjä
            tyhja.remove((x, y)) #päivitä tilanne
        if (x, y) in liput: #jos painettu ruutu oli lippu
            liput.remove((x, y)) #päivitä tilanne
        kentta[y][x] = str(miinat) #asetetaan kentälle valittuun kohtaan miinojen lkm
    elif kentta[y][x] == " " and miinat == 0: #jos ei miinoja valitun ruudun ympärillä
        status["vuoro_lkm"] += 1 #jos valitaan ruutu, jossa ei miinaa, eikä miinoja ympärillä
        tulvataytto(kentta, x, y) #tulvatäyttö merkitsee jokaisen ympäröivän ruudun turvalliseksi
    else: #jos yritetään painaa vaikka jo tarkistettua ruutua
        print("Et voi tehdä noin!")


def loppu_kasittely(koord_pari=None):
    """Tarkistaa mahdollisen voiton tai tappion"""
    if koord_pari in status["miinat"]: #jos valitussa ruudussa miina
        status["peli_status"] = False #peli asetetaan päättyneeksi
        status["lopputulos"] = "Tappio" #kirjoitetaan ylös tappio
    elif not status["tyhjat"]: #tämä lohko suoritetaan, jos tyhjät ruudut loppuvat
        status["peli_status"] = False #peli asetetaan päättyneeksi
        status["lopputulos"] = "Voitto" #kirjoitetaan ylös voitto
        

def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()

    for rivi_i, sis_1 in enumerate(status["kentta"]): #'elamaa_pellolla' -tyylinen ratkaisu   
        for sarake_i, sis_2 in enumerate(sis_1): #käydään koko kenttä läpi yksitellen
            if status["kentta"][rivi_i][sarake_i] == "x" and status["peli_status"] == False: #tarkistetaan ensin mahdollinen tappio
                haravasto.lisaa_piirrettava_ruutu("x", sarake_i*40, rivi_i*40) #piirretään tappion aiheuttamaan ruutuun "x"
            elif (sarake_i, rivi_i) in status["liput"]: #jos ruudussa lippu
                haravasto.lisaa_piirrettava_ruutu("f", sarake_i*40, rivi_i*40)
            elif status["kentta"][rivi_i][sarake_i] == " ": #jos ruudussa tyhjä
                haravasto.lisaa_piirrettava_ruutu(" ", sarake_i*40, rivi_i*40)
            elif status["kentta"][rivi_i][sarake_i] == "x": #jos ruudussa miina
                haravasto.lisaa_piirrettava_ruutu(" ", sarake_i*40, rivi_i*40) #piilottaa miinan tuntemattomaksi pelaajalle
            else:
                haravasto.lisaa_piirrettava_ruutu(status["kentta"][rivi_i][sarake_i], #piirtää numeron jos miina lähellä
                sarake_i*40,
                rivi_i*40)    
                            
    haravasto.piirra_ruudut()


def miinoita(alue, vapaa, miinat):
    """
    Asettaa kentällä N kpl miinoja satunnaisiin paikkoihin.
    """
    for i in range(miinat): #toistaa "miinat" kertaa
        koord_pari = random.choice(vapaa) #satunnainen koordinaatti pari vapaista paikoista
        alue[koord_pari[1]][koord_pari[0]] = "x" #miina koord_parin osoittamaan paikkaan
        status["miinat"].append((koord_pari)) #lisätään miinoitetun ruudun paikka sanakirjaan
        vapaa.remove(koord_pari) #poisto vapaitten listasta mihin asetettu miina
        

def miina_laskuri(x, y, kentta):
    """
    Laskee valitun ruudun ympäriltä maksimissaan 9 ruudun alueen pitäen huolen, että
    pysytään silti sallitun alueen sisällä. Jos valittu ruutu 
    itsessään sisältää jo miinan tämä lasketaan myös mukaan.
    """
    miinat = 0 #asetetaan miinat alussa nollaan
    for i in range(y - 1, y + 2): #'o_luokkaista_toimintaa' -tyylinen ratkaisu
        for j in range(x - 1, x + 2):
            if -1 < i < len(kentta) and -1 < j < len(kentta[0]): 
                if kentta[i][j] == "x":
                    miinat += 1 #joka kierroksella miina lisää
    return miinat


def tulvataytto(kentta, aloitus_x, aloitus_y):
    """
    Merkitsee planeetalla olevat tuntemattomat alueet turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä.
    """
    t_lista = status["tyhjat"] #alustetaan tarvittavat listat selkeyden vuoksi
    l_lista = status["liput"]
    
    #if kentta[aloitus_y][aloitus_x] != "x":
    tulva = [(aloitus_x, aloitus_y)]
    while tulva:
        koord_pari = tulva.pop()
        miinat = miina_laskuri(koord_pari[0], koord_pari[1], kentta) #laskuri laskee valitun ruudun ympäriltä miinat
        if miinat == 0: #jos miinoja ei ympäriltä löydy
            if koord_pari in t_lista: #jos valittu ruutu tyhjä
                t_lista.remove(koord_pari) #päivitä tilanne
            if koord_pari in l_lista: #jos valitussa ruudussa lippu
                l_lista.remove(koord_pari) #päivitä tilanne
            kentta[koord_pari[1]][koord_pari[0]] = "0" #merkitse kyseinen koordinaatti turvalliseksi 

            for y in range(koord_pari[1] - 1, koord_pari[1] + 2): #tarkistetaan valitun ruudun ympäristö
                for x in range(koord_pari[0] - 1, koord_pari[0] + 2):
                    if -1 < y < len(kentta) and -1 < x < len(kentta[0]):
                        if kentta[y][x] == " ": #jos ruutuja ei ole jo "avattu"
                            tulva.append((x, y)) #seuraava syöte ylemmälle koodilohkolle täytettäväksi                     
        else: #jos miinoja löytyy
            kentta[koord_pari[1]][koord_pari[0]] = str(miinat) #merkitään kys ruutuun ympäröivien miinojen lkm
            if koord_pari in t_lista: #jos valittu ruutu tyhjä
                t_lista.remove(koord_pari) #päivitä tilanne


def main():
    """
    Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen piirtokäsittelijän.
    """
    print("\nTervetuloa Miinantallaajan pariin!\n\nVoit valita seuraavista vaihtoehdoista:\n", end="")
    print("[1] - Aloita uusi peli\n[2] - Katsele tilastoja\n[3] - Poistu\n")
    while True:
        try:
            kayt_valinta = int(input("Valinnat (1-3): ").strip())
        except (ValueError, TypeError):
            print("\nSyötä vain kokonaislukuja (1-3), kiitos!")
        except (KeyboardInterrupt):
            print("\n\nHei hei!")
            break
        else:
            if kayt_valinta == 1:
                try:
                    leveys = int(input("Syötä haluamasi pelialueen leveys: ").strip())
                    korkeus = int(input("Syötä haluamasi pelikentän korkeus: ").strip())
                    miinojen_lkm = int(input("Syötä tahtomasi pelikentän miinojen lukumäärä: ").strip())
                except (ValueError, TypeError):
                    print("\nSyötä leveys, korkeus, miinojen lukumäärä kokonaislukuina, kiitos!\n")
                else:
                    if leveys < 2 or korkeus < 2:
                        print("\nKentän täytyy olla vähintään 2 ruutua korkea/leveä!\n")
                    elif leveys > 25:
                        print("\nTästä kentästä tulisi valtava! Kokeile jotain hieman hillitympää!\n")
                    elif miinojen_lkm <= 0:
                        print("\nEihän miinantallaajaa voi pelata ilman miinoja!\n") 
                    elif miinojen_lkm >= (leveys*korkeus):
                        print("\nKentällä on liian monta miinaa!\n")
                    else:
                        kaynnistys(leveys, korkeus, miinojen_lkm) #määrittelee perusehdot ja käynnistää pelin
            elif kayt_valinta == 2:
                tilasto_luku() #nimensä mukaisesti lukee tiedoston menneistä peleistä
            elif kayt_valinta == 3:
                print("\nHei hei!") #rikkoo main loopin
                break
            else: #jos valittiin jotain muuta kuin annettuja vaihtoehtoja
                print("Valitse kokonaisluku väliltä (1-3)!")

                
def kaynnistys(leveys, korkeus, miinojen_lkm):

    kentan_luonti(leveys, korkeus)
    miinoita(status["kentta"], status["tyhjat"], miinojen_lkm)
    status["vuosi"] = time.strftime("%Y-%m-%d") #tallennetaan sanakirjaan nykyinen hetki vuosi-kk-päivä
    status["kello"] = time.strftime("%H:%M:%S") #tallennetaan sanakirjaan nykyinen kellonaika
    status["miina_lkm"] = str(miinojen_lkm) 
    status["kentta_koko"] = "{leveys}x{korkeus}".format(leveys=leveys, korkeus=korkeus)
    aika["aloitus"] = time.time() #metodi time-moduulista alkaa laskemaan aikaa sekunneissa. HUOM täytyy muuntaa.
    
    haravasto.luo_ikkuna(leveys*40, korkeus*40)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    #haravasto.aseta_nappain_kasittelija(kasittele_nappain)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aloita()
    alustus()


def kentan_luonti(leveys, korkeus):
    kentta = []
    #alla oleva miinoitus_tuokio -tyylinen koodipätkä
    for rivi in range(korkeus): 
        kentta.append([])
        for sarake in range(leveys):
            kentta[-1].append(" ")
    status["kentta"] = kentta #luotu kenttä globaaliksi muuttujaksi

    tyhjat = [] 
    #sama juttu kuin ylempänä, mutta vain tyhjille ruuduille
    for rivi_2 in range(leveys):
        for sarake_2 in range(korkeus):
            tyhjat.append((rivi_2, sarake_2)) #lisätään kaikki yllä olevat ruudut 'tyhjiin'
    status["tyhjat"] = tyhjat #tyhjä kenttä globaaliksi muuttujat

def tilasto_kirjoitus():
    try:
        with open("tilasto.txt", "a") as f: #luo tai lisää tiedoston "tilasto.txt" loppuun vaaditut tiedot
            f.write("{kello}, {vuosi}, {minuutit}, {vuoro_lkm}, {lopputulos}, {kentta_koko}, {miina_lkm}\n".format(
                kello=status["kello"], #tallennetaan vaaditut tiedot
                vuosi=status["vuosi"],
                minuutit=status["minuutit"],
                vuoro_lkm=status["vuoro_lkm"],
                lopputulos=status["lopputulos"],
                kentta_koko=status["kentta_koko"],
                miina_lkm=status["miina_lkm"]
            ))

    except (FileNotFoundError, IOError): #omituisista virheistä annetaan palaute
        print("Jotain meni pieleen tiedoston käsittelyssä!")

def tilasto_luku():
    try:
        with open("tilasto.txt", "r") as r: #samankaltainen koodipätkä 4. materiaalista
            sisalto = r.readlines() #tallennetaan tilasto.txt sisalto muuttujaan
            for indeksi, rivi in enumerate(sisalto): #käydään sisallön jokainen alkio läpi
                kello, vuosi, minuutit, vuoro_lkm, lopputulos, kentta_koko, miina_lkm = rivi.split(",") 
                print("\nPeli [{indeksi}]: {ksto} - {klo} | Aika: {min} | Vuoroja: {vro} | Koko: {kent} | Miinoja: {lkm} | Tulos: {tls}".format(
                    indeksi=indeksi + 1, #käsitellään ja sijoitetaan muuttujat
                    ksto=vuosi.strip(),
                    klo=kello.strip(),
                    min=minuutit.strip(),
                    vro=vuoro_lkm.strip(),
                    kent=kentta_koko.strip(),
                    lkm=miina_lkm.strip(),
                    tls=lopputulos.strip()        
                ))
    except (FileNotFoundError, IOError): #omituisista virheistä annetaan palaute
        print("Tiedostoa ei ole.")



if __name__ == "__main__":
    haravasto.lataa_kuvat("spritet")

    main()