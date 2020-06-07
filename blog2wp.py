#!/usr/bin/python
# -*- coding: utf-8 -*-

#  blog2wp.py
#
#
# Martin Rybensky
#

verze = '2020-02-27_01'


import sys, os, urllib2, datetime, time, urlparse

tento_rok = str(datetime.datetime.now().year)
tento_mesic = str(datetime.datetime.now().month)

##########################################################################################
# DEFINICE FUNKCI


##############################
# prevoddata - funkce prevadejici tvary datumu z blog.cz 
# na standardni yyyy-mm-dd hh:mm:ss
##############################

def prevoddata(fujdatum,debug):

    # Před 10 minutami
    # Dnes v 10:21
    # Včera v 10:21
    #
    #
    # 12. června 2017 v 10:21

    if debug:
        sys.stdout.write('datum puvodni: ' + fujdatum + ' | ')

    # inicializace promennych
    rok = ''
    mesic = ''
    den = ''
    cas = ''
    wpdatum = ''
    dneska = datetime.datetime.today()
    vcera = datetime.datetime.today() - datetime.timedelta(days=1)

    # spinavy workaround kvuli par divnym datumum
    if '</div>' in fujdatum:
        fujdatum = fujdatum.rsplit('</div>',1)[0]

    # mesice
    if 'ledna' in fujdatum:
        mesic = '01'
        rok = fujdatum.split('ledna ',1)[1]
        rok = rok.split(' ',1)[0]
    elif 'února' in fujdatum:
        mesic = '02'
        rok = fujdatum.split('února ',1)[1]
        rok = rok.split(' ',1)[0]
    elif 'března' in fujdatum:
        mesic = '03'
        rok = fujdatum.split('března ',1)[1]
        rok = rok.split(' ',1)[0]
    elif 'dubna' in fujdatum:
        mesic = '04'
        rok = fujdatum.split('dubna ',1)[1]
        rok = rok.split(' ',1)[0]
    elif 'května' in fujdatum:
        mesic = '05'
        rok = fujdatum.split('května ',1)[1]
        rok = rok.split(' ',1)[0]
    elif 'června' in fujdatum:
        mesic = '06'
        rok = fujdatum.split('června ',1)[1]
        rok = rok.split(' ',1)[0]
    elif 'července' in fujdatum:
        mesic = '07'
        rok = fujdatum.split('července ',1)[1]
        rok = rok.split(' ',1)[0]
    elif 'srpna' in fujdatum:
        mesic = '08'
        rok = fujdatum.split('srpna ',1)[1]
        rok = rok.split(' ',1)[0]
    elif 'září' in fujdatum:
        mesic = '09'
        rok = fujdatum.split('září ',1)[1]
        rok = rok.split(' ',1)[0]
    elif 'října' in fujdatum:
        mesic = '10'
        rok = fujdatum.split('října ',1)[1]
        rok = rok.split(' ',1)[0]
    elif 'listopadu' in fujdatum:
        mesic = '11'
        rok = fujdatum.split('listopadu ',1)[1]
        rok = rok.split(' ',1)[0]
    elif 'prosince' in fujdatum:
        mesic = '12'
        rok = fujdatum.split('prosince ',1)[1]
        rok = rok.split(' ',1)[0]
    elif 'Dnes' in fujdatum:
        den = dneska.day
        den = str(den)
        den = den.zfill(2)
        mesic = dneska.month
        mesic = str(mesic)
        mesic = mesic.zfill(2)
        rok = dneska.year
    elif 'Včera' in fujdatum:
        den = vcera.day
        den = str(den)
        den = den.zfill(2)
        mesic = vcera.month
        mesic = str(mesic)
        mesic = mesic.zfill(2)
        rok = vcera.year
    elif 'Pondělí' in fujdatum:
        pondeli = dneska - datetime.timedelta(days=dneska.weekday())
        den = pondeli.day
        den = str(den)
        den = den.zfill(2)
        mesic = pondeli.month
        mesic = str(mesic)
        mesic = mesic.zfill(2)
        rok = pondeli.year

    elif 'Úterý' in fujdatum:
        pondeli = dneska - datetime.timedelta(days=dneska.weekday())
        utery = pondeli + datetime.timedelta(days=1)
        if utery > dneska:
            utery = pondeli - datetime.timedelta(days=6)
        den = utery.day
        den = str(den)
        den = den.zfill(2)
        mesic = utery.month
        mesic = str(mesic)
        mesic = mesic.zfill(2)
        rok = utery.year

    elif 'Středa' in fujdatum:
        pondeli = dneska - datetime.timedelta(days=dneska.weekday())
        streda = pondeli + datetime.timedelta(days=2)
        if streda > dneska:
            streda = pondeli - datetime.timedelta(days=5)
        den = streda.day
        den = str(den)
        den = den.zfill(2)
        mesic = streda.month
        mesic = str(mesic)
        mesic = mesic.zfill(2)
        rok = streda.year

    elif 'Čtvrtek' in fujdatum:
        pondeli = dneska - datetime.timedelta(days=dneska.weekday())
        ctvrtek = pondeli + datetime.timedelta(days=3)
        if ctvrtek > dneska:
            ctvrtek = pondeli - datetime.timedelta(days=4)
        den = ctvrtek.day
        den = str(den)
        den = den.zfill(2)
        mesic = ctvrtek.month
        mesic = str(mesic)
        mesic = mesic.zfill(2)
        rok = ctvrtek.year


    elif 'Pátek' in fujdatum:
        pondeli = dneska - datetime.timedelta(days=dneska.weekday())
        patek = pondeli + datetime.timedelta(days=4)
        if patek > dneska:
            patek = pondeli - datetime.timedelta(days=3)
        den = patek.day
        den = str(den)
        den = den.zfill(2)
        mesic = patek.month
        mesic = str(mesic)
        mesic = mesic.zfill(2)
        rok = patek.year

    elif 'Sobota' in fujdatum:
        pondeli = dneska - datetime.timedelta(days=dneska.weekday())
        sobota = pondeli + datetime.timedelta(days=5)
        if sobota > dneska:
            sobota = pondeli - datetime.timedelta(days=2)
        den = sobota.day
        den = str(den)
        den = den.zfill(2)
        mesic = sobota.month
        mesic = str(mesic)
        mesic = mesic.zfill(2)
        rok = sobota.year


    elif 'Neděle' in fujdatum:
        pondeli = dneska - datetime.timedelta(days=dneska.weekday())
        nedele = pondeli + datetime.timedelta(days=6)
        if nedele > dneska:
            nedele = pondeli - datetime.timedelta(days=1)
        den = nedele.day
        den = str(den)
        den = den.zfill(2)
        mesic = nedele.month
        mesic = str(mesic)
        mesic = mesic.zfill(2)
        rok = nedele.year


    if '.' in fujdatum or ':' in fujdatum:
        if '.' in fujdatum:
            den = fujdatum.split('.',1)[0]
            den = den.zfill(2)

        # osetreni kvuli jednocifernym hodinam bez nuly        
        cas = fujdatum.split('v ',1)[1]
        hodiny = cas.split(':',1)[0]
        hodiny = hodiny.zfill(2)
        minuty = cas.split(':',1)[1]
        cas = hodiny + ':' + minuty

        wpdatum =  str(rok) + '-' + str(mesic) + '-' + str(den) + ' ' + str(cas) + ':00'

    elif 'Před' in fujdatum:
        minut = fujdatum.split('Před ',1)[1]
        minut = minut.split(' minutami',1)[0]
        minut = int(minut)
        sys.stdout.write('minut: ' + str(minut))
        pred = dneska - datetime.timedelta(minutes = minut)
        den = str(pred.day)
        den = den.zfill(2)
        mesic = str(pred.month)
        mesic = mesic.zfill(2)
        rok = str(pred.year)
        hodina = str(pred.hour)
        hodina = hodina.zfill(2)
        minuta = str(pred.minute)
        minuta = minuta.zfill(2)
        vterina = str(pred.second)
        vterina = vterina.zfill(2)
        cas = str(pred.ctime)
        wpdatum =  str(rok) + '-' + str(mesic) + '-' + str(den) + ' ' + hodina + ':' + minuta + ':' + vterina

    if debug:
        sys.stdout.write('datum prevedene: ' + wpdatum + '\n')

    return wpdatum

def minus_hodina(wpdatum):

    gmtdatum = datetime.datetime.strptime(wpdatum, '%Y-%m-%d %H:%M:%S')
    gmtdatum = gmtdatum - datetime.timedelta(hours = 1)
    gmtdatum = datetime.datetime.strftime(gmtdatum, '%Y-%m-%d %H:%M:%S')

    return gmtdatum

def gmtdate2pubdate(gmtdatum):
    # 		<pubDate>Tue, 15 Sep 2015 20:04:03 +0000</pubDate>
    pubdatum = datetime.datetime.strptime(gmtdatum, '%Y-%m-%d %H:%M:%S')
    pubdatum = datetime.datetime.strftime(pubdatum, '%a, %d %b %Y %H:%M:%S')
    pubdatum = pubdatum + ' +0000'

    return pubdatum

##############################
# progressbar
##############################

def opakuj_znak(znak,pocet):
        return (znak * ((pocet/len(znak))+1))[:pocet]

def progressbar(done,total):

        totalpct = float(total) / 100
        if done == 0:
                donepct = 0
        else:
                donepct = float(done) / totalpct
                donepct = round(donepct)
                donepct = int(donepct)

        zbyva = 100 - donepct

        hotovo = donepct

        bar = opakuj_znak(u'\u2588',hotovo) + opakuj_znak(u'\u2591',zbyva)

        sys.stdout.write("\r [" + str(done) + "/" + str(total) +"] |" + bar + "| " + str(donepct) + "%")
	sys.stdout.flush()

##############################
# ocistit_url - zbavi url v komentari nezadouciho nofollow
##############################

def ocistit_url(web_url):
    if 'nofollow' in web_url:
        ocistena_url = web_url.split('" rel="nofollow',1)[0]
    else:
        ocistena_url = web_url

    return ocistena_url

##############################
# stahni_obrazek
##############################

def stahni_obrazek(url_ke_stazeni,export_mode,debug,prepis_obrazku):

    vstupni_url = url_ke_stazeni

    url_obrazku = ''
    server = ''
    spravna_url = ''
    jmeno_souboru = ''
    jmeno_souboru_p1 = ''
    jmeno_souboru_p2 = ''
    blog_cz_hosting = False

    url_blog = url_ke_stazeni.split('.cz/',1)[0]
    url_blog = url_blog + '.cz/'

    # pokud url obrazku obsahuje vyrazy "bcache" nebo "imageproxy", 
    # je nahran na galerie.cz a je chranen proti externimu nacteni/odkazovani

    # pokud je toto detekovano, je chranena url odrbana o ochranne prvky
    if 'bcache' in vstupni_url or 'imageproxy' in vstupni_url:
	if debug:
            sys.stdout.write('obrazek je hostovan na blogu.cz\n')
	blog_cz_hosting = True
	if '%7E' in vstupni_url:
           url_obrazku = vstupni_url.split('cz%7E',1)[1]
           server = vstupni_url.split('%7E',1)[1]
           server = server.split('%7E',1)[0]
	if '~' in vstupni_url:
           url_obrazku = vstupni_url.split('cz~',1)[1]
           server = vstupni_url.split('~',1)[1]
           server = server.split('~',1)[0]

        server = server.replace('/','.')

        spravna_url = 'http://' + server + url_obrazku
	if debug:
            sys.stdout.write('spravna url po zruseni ochrany: ' + spravna_url + '\n')
    else:
        # pokud vyrazy testovane vyse detekovany nejsou,
        spravna_url = vstupni_url           # je zjistena url rovnou povazovana za pouzitelnou

    # samotne stahovani neprovadime u varianty exportu, kdy ponechavame puvodni url obrazku
    if export_mode != 3:
        jmeno_souboru = url_ke_stazeni.rsplit('/',1)[1]
        jmeno_souboru = 'obrazky/' + jmeno_souboru
	if debug:
            sys.stdout.write('lokalni cesta: ' + jmeno_souboru + '\n')

    # zjistena url je vlozena do soupisu obrazku 
    if prepis_obrazku == 2 and blog_cz_hosting:
        soupis = open('temp/soupis_obrazku.txt', "a")
        soupis.write(spravna_url + '\n')
        soupis.close()
    elif prepis_obrazku == 1:
        soupis = open('temp/soupis_obrazku.txt', "a")
        soupis.write(spravna_url + '\n')
        soupis.close()
 
    '''  
    # STAHOVANI OBRAZKU - zatim nedoreseno
    if not os.path.isfile(jmeno_souboru):

            req = urllib2.Request(spravna_url)
            req.add_header('Referer', vstupni_url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:10.0) Gecko/20100101 Firefox/10.0')
            response = urllib2.urlopen(req)
            do_souboru = response.read()

            sys.stdout.write('zapisuji...'
            soubor_zapis = open(jmeno_souboru, "w+")

            soubor_zapis.write(do_souboru)
            soubor_zapis.close()
            sys.stdout.write('zapsano'
            sys.stdout.write('zacatek sleepu 4s'
            time.sleep(10)
            sys.stdout.write('konec sleepu 4s'
        else:
            sys.stdout.write('         soubor ' + jmeno_souboru + ' jiz existuje'
    '''
    #return jmeno_souboru # jen filename
    return spravna_url # i s adresou


##############################
# stahni_html - stahne ze zadane url html soubor
##############################

def stahni_html(url_ke_stazeni,clanek):

    jmeno_souboru = ''
    jmeno_souboru_p1 = ''
    jmeno_souboru_p2 = ''
    url_blog = url_ke_stazeni.split('.cz/',1)[0]
    url_blog = url_blog + '.cz/'

    req = urllib2.Request(url_ke_stazeni)
    req.add_header('Referer', url_blog)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:10.0) Gecko/20100101 Firefox/10.0')
    response = urllib2.urlopen(req)
    do_souboru = response.read()

    if clanek:
        jmeno_souboru_p1 = url_ke_stazeni.rsplit('/',2)[1]
        jmeno_souboru_p2 = url_ke_stazeni.rsplit('/',1)[1]
        jmeno_souboru = jmeno_souboru_p1 + '-' + jmeno_souboru_p2
    else:
        jmeno_souboru = url_ke_stazeni.rsplit('/',1)[1]

    jmeno_souboru = 'temp/' + jmeno_souboru

    soubor_zapis = open(jmeno_souboru, "w+")

    soubor_zapis.write(do_souboru)
    soubor_zapis.close()
    time.sleep(1)
    return jmeno_souboru


##############################
# exportovat_rubriky  
##############################

def exportovat_rubriky(url_blog,vystupni_soubor,debug):

    status_fail = ' [\033[91mFAIL\033[0m] '
    status_ok = ' [\033[92m OK \033[0m] '
    status_warn= ' [\033[93mWARN\033[0m] '

    url_rubriky = url_blog + '/rubriky'

    cislo_rubriky = 0

    cislo_radku = 0
    radek_rubrika = 0
    rubrika_url = {}
    rubrika_nazev = {}

    konec_rubrik = False

    nazev_blogu = ''

    aktualni_timestamp = datetime.datetime.now()
    export_pubdate = datetime.datetime.strftime(aktualni_timestamp, '%a, %d %b %Y %H:%M:%S')
    export_pubdate = export_pubdate + ' +0000'
    export_created = datetime.datetime.strftime(aktualni_timestamp, '%Y-%m-%d %H:%M:%S')




    if os.path.isfile('temp/rubriky'):
        sys.stdout.write(status_warn + 'soubor temp/rubriky již existuje, pokračuji s daty z něho\n')
    else:
        stahni_html(url_rubriky,False)
        sys.stdout.write(status_ok + 'soubor s definicemi rubrik úspešně stažen\n')

    # a ted to zapiseme do xmlka
    wpxml = open(vystupni_soubor, "w+")
    rubriky_txt = open('temp/rubriky.txt', "w+")


    with open('temp/rubriky', 'r') as k:
        for line in k:
            cislo_radku += 1
            
            # autor blogu
            if "<meta name=\"author\"" in line:
              autor_blogu = line.split('content=',1)[1]
              autor_blogu = autor_blogu.split('"',2)[1]
              autor_blogu = autor_blogu.replace('"','')


            # nazev blogu
            if "<title>" in line:
                nazev_blogu = line.split('|',1)[1]
                nazev_blogu = nazev_blogu.split('</title>',1)[0]
                nazev_blogu = nazev_blogu.rstrip()
                nazev_blogu = nazev_blogu.strip()
		
                wpxml.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
		wpxml.write('<!-- generator="Blogcz2WP ver.' + verze + '" created="' + export_created  + '" -->\n')
                wpxml.write('<!-- Blogcz2WP: blog.cz to Wordpress export tool, made by Martin Rybensky 2017-2019  -->\n')
                wpxml.write('<!-- Project homepage: https://github.com/MartinRybensky/blogcz2wp  -->\n')
                wpxml.write(' <rss version="2.0"\n')
                wpxml.write('    xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"\n')
                wpxml.write('    xmlns:content="http://purl.org/rss/1.0/modules/content/"\n')
                wpxml.write('    xmlns:wfw="http://wellformedweb.org/CommentAPI/"\n')
                wpxml.write('    xmlns:dc="http://purl.org/dc/elements/1.1/"\n')
                wpxml.write('    xmlns:wp="http://wordpress.org/export/1.2/"\n')
                wpxml.write('>\n')
                wpxml.write(' <channel>\n')
                wpxml.write('   <title>' + nazev_blogu + '</title>\n')
                wpxml.write('   <link>' + url_blog + '</link>\n')
                wpxml.write('   <description>' + nazev_blogu + '</description>\n')
                wpxml.write('   <pubDate>' + export_pubdate + '</pubDate>\n')
                wpxml.write('   <language>cs-CZ</language>\n')
                wpxml.write('   <wp:wxr_version>1.2</wp:wxr_version>\n')
                wpxml.write('   <wp:base_site_url>' + url_blog + '</wp:base_site_url>\n')
                wpxml.write('   <wp:base_blog_url>' + url_blog + '</wp:base_blog_url>\n')
                wpxml.write('\n')
                wpxml.write('   <wp:author>\n')
                wpxml.write('     <wp:author_id>1</wp:author_id>\n')
                wpxml.write('     <wp:author_login><![CDATA[' + autor_blogu + ']]></wp:author_login>\n')
                wpxml.write('     <wp:author_email><![CDATA[]]></wp:author_email>\n')
                wpxml.write('     <wp:author_display_name><![CDATA[' + autor_blogu + ']]></wp:author_display_name>\n')
                wpxml.write('     <wp:author_first_name><![CDATA[]]></wp:author_first_name>\n')
                wpxml.write('     <wp:author_last_name><![CDATA[]]></wp:author_last_name>\n')
                wpxml.write('   </wp:author>\n')
                wpxml.write('\n')


            # jednotlive rubriky
            if 'AdTrackCategoryBottom' in line:
                konec_rubrik = True

            if '<li id=' in line and not konec_rubrik:
                cislo_rubriky += 1
                radek_rubrika = cislo_radku + 1
            if cislo_radku == radek_rubrika:
                rubrika_url[cislo_rubriky] = line.split('href="/rubrika/',1)[1]
                rubrika_url[cislo_rubriky] = rubrika_url[cislo_rubriky].split('"',1)[0]

                rubrika_nazev[cislo_rubriky] = line.split('title="',1)[1]
                rubrika_nazev[cislo_rubriky] = rubrika_nazev[cislo_rubriky].split('">',1)[0]

                wpxml.write('   <wp:category>\n')
                wpxml.write('       <wp:term_id>' + str(cislo_rubriky) + '</wp:term_id>\n')
                wpxml.write('       <wp:category_nicename>' + rubrika_url[cislo_rubriky] + '</wp:category_nicename>\n')
                wpxml.write('       <wp:category_parent><![CDATA[]]></wp:category_parent>\n')
                wpxml.write('       <wp:term_slug><![CDATA[' + rubrika_url[cislo_rubriky] + ']]></wp:term_slug>\n')
                wpxml.write('       <wp:cat_name><![CDATA[' + rubrika_nazev[cislo_rubriky] + ']]></wp:cat_name>\n')
                wpxml.write('   </wp:category>\n')

                rubriky_txt.write(url_blog + '/rubrika/' + rubrika_url[cislo_rubriky] + '\n')
		if debug:
                    sys.stdout.write(' ' + str(cislo_rubriky) + ': ' + rubrika_nazev[cislo_rubriky] + '\n')


    rubriky_txt.close()
    wpxml.close()

##############################
# exportovat_archiv
##############################

def exportovat_archiv(url_blog,debug):
    url_archiv = url_blog + '/archiv'

    status_fail = ' [\033[91mFAIL\033[0m] '
    status_ok = ' [\033[92m OK \033[0m] '
    status_warn= ' [\033[93mWARN\033[0m] '


    cislo_radku = 0
    radek_odkaz = 0
    radek_nazev = 0
    radek_pocet = 0
    zaznam = 0
    archiv_url = {}
    archiv_nazev = {}
    archiv_pocet = {}


    konec_archivu = False


    if os.path.isfile('temp/archiv'):
        sys.stdout.write(status_warn + 'soubor temp/archiv již existuje, pokračuji s daty z něho\n')
    else:
        stahni_html(url_archiv,False)
        sys.stdout.write(status_ok + 'soubor s archivem úspesně stažen\n')

    # a ted to zapiseme do txt
    archiv_txt = open('temp/archiv.txt', "w+")


    with open('temp/archiv', 'r') as k:
        for line in k:
            cislo_radku += 1

            # jednotlive rubriky
            if '<div id="pageBottom">' in line:
                konec_archivu = True
            if '<li>' in line and not konec_archivu:
                zaznam += 1
                radek_odkaz = cislo_radku + 1
                radek_nazev = cislo_radku + 2
                radek_pocet = cislo_radku + 3
            if cislo_radku == radek_odkaz:
		if debug:
			sys.stdout.write('exportovat_archiv, zpracovavany radek: '+str(cislo_radku) + '\n')
                archiv_url[zaznam] = line.split('<a href="/',1)[1]
                archiv_url[zaznam] = archiv_url[zaznam].split('">',1)[0]
            if cislo_radku == radek_nazev:
                archiv_nazev[zaznam] = line.split('</a>',1)[0]
                archiv_nazev[zaznam] = archiv_nazev[zaznam].strip()
                archiv_nazev[zaznam] = archiv_nazev[zaznam].rstrip()
            if cislo_radku == radek_pocet:
                archiv_pocet[zaznam] = line.split('(',1)[1]
                archiv_pocet[zaznam] = archiv_pocet[zaznam].split(')',1)[0]
                archiv_pocet[zaznam] = int(archiv_pocet[zaznam])
	    	if debug:
                	sys.stdout.write(archiv_nazev[zaznam] + ', záznamů: ' + str(archiv_pocet[zaznam]) + '\n')
                archiv_txt.write(url_blog + '/' + archiv_url[zaznam] + '\n')
		
	    if '<div id="menuInner">' in line:
	    	break

    pocet_celkem = sum(archiv_pocet.values())
    sys.stdout.write(' [info] celkový počet článků v archivu (dle deklarovaných počtů v závorkách): ' +  str(pocet_celkem) + '\n')
    
    archiv_txt.close()

    return pocet_celkem

##############################
# soupis_clanku
##############################

def soupis_clanku(url_blog,debug):

    status_fail = ' [\033[91mFAIL\033[0m] '
    status_ok = ' [\033[92m OK \033[0m] '
    status_warn= ' [\033[93mWARN\033[0m] '

    cislo_radku = 0
    radek_odkaz = 0
    radek_zacatek = 0
    posledni_stranka = 0
    odkaz_cislo = 0
    strankovani = False
    konec_vypisu = False
    vypis_excerpt = False


    # zapis ziskanych url clanku
    if os.path.isfile('temp/soupis_clanku.txt'):
        sys.stdout.write(status_warn + 'soubor temp/soupis_clanku.txt již existuje, pokračuji s daty z něho\n')
	with open('temp/soupis_clanku.txt', 'r') as s:
	    for radek in s:
		if url_blog not in radek:
		   sys.stdout.write(status_fail + 'neodpovídající lokální data, soupis_clanku.txt obsahuje odkazy na jiný blog!\n        Program zavolán ve špatném adresáři nebo na špatnou URL?\n')
		   sys.exit(1)
    else:
        seznam_txt = open('temp/soupis_clanku.txt', 'w+')

	sys.stdout.write(' [info] pořizuji soupis článků:\n')

        # nacteni radku s url rubrik
        with open('temp/archiv.txt', 'r') as f:
            for radek in f:
                radek = radek.strip()
                nactena_url = radek.rstrip()

                stahni_html(nactena_url,False)
                soubor_rubrika = nactena_url.rsplit('/',1)[1]

                konec_vypisu = False

                with open('temp/' + soubor_rubrika, 'r') as o:
                    for linka in o:
                        if '<div class="articleText">' in linka:
                            vypis_excerpt = True

                with open('temp/' + soubor_rubrika, 'r') as p:
                    for line in p:
                        cislo_radku += 1
                        odkaz = ''

                        # sebere odkazy na clanky na prvni/jedine strance vypisu rubriky
                        if 'AdTrackCategoryBottom' in line or '<div class="paginator2">' in line:
                            konec_vypisu = True

                        # clanky jako seznam odkazu v rubrice
                        ############################################################
                        elif '<li>' in line and not konec_vypisu and not vypis_excerpt:
                            radek_odkaz = cislo_radku + 1
                        elif radek_odkaz == cislo_radku and not konec_vypisu and not vypis_excerpt:
                            odkaz = line.split('<a href="',1)[1]
                            odkaz = odkaz.split('"',1)[0]
                            odkaz = odkaz.strip()
                            odkaz = odkaz.rstrip()
			    odkaz_cislo = odkaz_cislo + 1
			    #if debug:
                            sys.stdout.write('\r [' + str(odkaz_cislo).zfill(4) + '] ' + url_blog + odkaz + '                                               ')
			    sys.stdout.flush()
                            seznam_txt.write(url_blog + odkaz + '\n')
                        # clanky jako excerpty
                        ###############################################################
                        elif '<div id="mainInner">' in line:
                            radek_zacatek = cislo_radku + 1
                        elif '<h3>' in line and not konec_vypisu and cislo_radku > radek_zacatek:
                            odkaz = line.split('<a href="',1)[1]
                            odkaz = odkaz.split('"',1)[0]
                            odkaz = odkaz.strip()
                            odkaz = odkaz.rstrip()
 			    #if debug:
			    odkaz_cislo = odkaz_cislo + 1
                            sys.stdout.write('\r [' + str(odkaz_cislo).zfill(4) + '] ' + url_blog + odkaz + '                                               ')
			    sys.stdout.flush()
                            seznam_txt.write(url_blog + odkaz + '\n')



                        # pokud je v rubrice hodne clanku a strankuje se    
                        elif 'paginatorLongButton' in line and 'Poslední stránka' in line:
                            strankovani = True
                            posledni_stranka = line.rsplit('" title="Poslední stránka"',1)[0]
                            posledni_stranka = posledni_stranka.rsplit('"',1)[1]
                            posledni_stranka = posledni_stranka.rsplit('/',1)[1]
			    if debug:
                                sys.stdout.write('posledni stránka katogorie: ' + posledni_stranka + '\n')

                            for_posledni = int(posledni_stranka)
                            for_posledni = for_posledni + 1

                            for y in range (2, for_posledni):
                                strankovana_rubrika = url_blog + '/' + soubor_rubrika + '/' + str(y)
                                sys.stdout.write(strankovana_rubrika + '\n')
                                stahni_html(strankovana_rubrika,False)
                                os.rename('temp/'+str(y), 'temp/'+soubor_rubrika+'-'+str(y)+'.txt')
                                nove_jmeno = 'temp/'+soubor_rubrika+'-'+str(y)+'.txt'

                                konec_vypisu = False
                                vypis_excerpt = False

                                with open(nove_jmeno, 'r') as q:
                                    for linkaa in q:
                                        if '<div class="articleText">' in linkaa:
                                            vypis_excerpt = True


                                with open(nove_jmeno, 'r') as r:
                                    for line in r:
                                        cislo_radku += 1
                                        odkaz = ''
                                        if 'AdTrackCategoryBottom' in line or '<div class="paginator2">' in line:
                                            konec_vypisu = True

                                        if '<div class="articleText">' in line:
                                            vypis_excerpt = True

                                        # sebere odkazy na clanky na prvni/jedine strance vypisu rubriky

                                        elif '<li>' in line and not konec_vypisu and not vypis_excerpt:
                                            radek_odkaz = cislo_radku + 1
                                        elif radek_odkaz == cislo_radku and not konec_vypisu and not vypis_excerpt:
                                            odkaz = line.split('<a href="',1)[1]
                                            odkaz = odkaz.split('"',1)[0]
                                            odkaz = odkaz.strip()
                                            odkaz = odkaz.rstrip()
                                            sys.stdout.write(url_blog + odkaz)
                                            seznam_txt.write(url_blog + odkaz + '\n')
                                        # clanky jako excerpty
                                        elif '<div id="mainInner">' in line:
                                            radek_zacatek = cislo_radku + 1
                                        elif '<h3>' in line and not konec_vypisu and cislo_radku > radek_zacatek:
                                            odkaz = line.split('<a href="',1)[1]
                                            odkaz = odkaz.split('"',1)[0]
                                            odkaz = odkaz.strip()
                                            odkaz = odkaz.rstrip()
                                            sys.stdout.write(url_blog + odkaz)
                                            seznam_txt.write(url_blog + odkaz + '\n')


        seznam_txt.close()




##############################
# zpracovat_komentare
##############################

def zpracovat_komentare(vstupni_soubor,vystupni_soubor,debug):

    # definice promennych
    komentarovy_soubor = vstupni_soubor
    soubor_komentare = ''
    strankovane_komentare = False
    zpracovano = False
    od_jednicky = False

    with open(vstupni_soubor, 'rU') as c:
       for lajnc in c:
            if 'discussPrevious' in lajnc:
                strankovane_komentare = True
                if debug:
                    sys.stdout.write('discussPrevious nalezen (strankovany vypis komentaru detekovan)\n')

    with open(vstupni_soubor, 'rU') as d:
       for lajnd in d:
            if 'commentNr" id="ref1"' in lajnd:
                od_jednicky = True
                if debug:
                    sys.stdout.write('commentNr" id="ref1" nalezen (vypis komentaru od 1. detekovan)\n')

    with open(vstupni_soubor, 'rU') as e:
       for lajn in e:

            if strankovane_komentare and not od_jednicky and 'discussPrevious' in lajn:
		if debug:
                    sys.stdout.write('strankovane komentare u clanku vyse')
                url_komentaru = lajn.split('discussPrevious" href="',1)[1]
                url_komentaru = url_komentaru.split('" title="Zobrazit',1)[0]

                url_komentaru = url_blog + url_komentaru
                cislo_radku_komentare = 0
                stahni_html(url_komentaru,False)

                soubor_komentare = url_komentaru.rsplit('/',1)[1]
                url_noindex = url_komentaru.rsplit('/',1)[0]
		if debug:
                    sys.stdout.write('stranek komentaru: ' + soubor_komentare + ' + zbytek\n')
                soubor_komentare = int(soubor_komentare)
                soubor_komentare_range = soubor_komentare + 1
                for w in range(1, soubor_komentare_range):
                    kom_url = url_noindex + '/' + str(w)
                    stahni_html(kom_url,False)
                    komentarovy_soubor = 'temp/' + str(w)
                    if soubor_komentare == 1:
                        index_pole = int(0)
                    else:
                        index_pole = w - 1
                        index_pole = str(index_pole) + '00'
                        index_pole = int(index_pole)
                    if debug:
		        sys.stdout.write('zpracovavam soubor:' + komentarovy_soubor + ', pocatecni index: ' + str(index_pole) + '\n')
                    zapis_komentare(komentarovy_soubor,vystupni_soubor,index_pole,debug)

                    # aby se uz neprovadely radky nize
                    zpracovano = True

                index_pole = str(index_pole)
                index_pole = str(soubor_komentare) + '00'
                index_pole = int(index_pole)
		if debug:
                    sys.stdout.write('zpracovavam zbytek z clanku, pocatecni index: ' + str(index_pole) + '\n')
                zapis_komentare(vstupni_soubor,vystupni_soubor,index_pole,debug)




    if not zpracovano:
        index_pole = int(0)
        # nestrankovane komentare / zbytek komentaru prebyvajicich ze strankovanych
        komentarovy_soubor = vstupni_soubor
        if debug:
            sys.stdout.write('komentare zpracovavany ze souboru: ' + komentarovy_soubor + '\n')
        zapis_komentare(komentarovy_soubor,vystupni_soubor,index_pole,debug)

def zapis_komentare(komentarovy_soubor,vystupni_soubor,index_pole,debug):

    # definice promennych
    pocet_komentaru = 0

    cislo_radku_komentare = 0
    nasledujici_radek_komentare = 0
    kom_jmeno = {}
    kom_web = {}
    kom_datum =  {}
    kom_email = {}
    kom_text = {}

    kom_jmeno[0] = ''
    kom_text[0] = ''
    kom_email[0] = ''
    kom_web[0] = ''

    with open(komentarovy_soubor, 'rU') as b:
        for line in b:
            cislo_radku_komentare += 1

            if '<a class="commentNr" id="ref' in line:
                radek_s_komentarem = cislo_radku_komentare + 1
                pocet_komentaru = line.split('<a class="commentNr" id="ref',1)[1]
                pocet_komentaru = pocet_komentaru.split('" name=',1)[0]
                pocet_komentaru = int(pocet_komentaru)
		if debug:
		    sys.stdout.write('pocet komentaru: ' + str(pocet_komentaru) + '\n')
                kom_jmeno[pocet_komentaru] = line.split('<strong>',1)[1]
                kom_jmeno[pocet_komentaru] = kom_jmeno[pocet_komentaru].split('</strong>',1)[0]

                # mail + web
                if 'mailto:' in line and 'title="Web"' in line:
                    kom_email[pocet_komentaru] = line.split('mailto:',1)[1]
                    kom_email[pocet_komentaru] = kom_email[pocet_komentaru].split('">E-mail',1)[0]
                    kom_email[pocet_komentaru] = kom_email[pocet_komentaru].replace(' (V) ','@')

                    kom_web[pocet_komentaru] = line.split('E-mail</a> | <a href="',1)[1]
                    kom_web[pocet_komentaru] = kom_web[pocet_komentaru].split('" title="Web">',1)[0]
                    kom_web[pocet_komentaru] = ocistit_url(kom_web[pocet_komentaru])

                    kom_datum[pocet_komentaru] = line.split('Web</a> | ',1)[1]
                    kom_datum[pocet_komentaru] = kom_datum[pocet_komentaru].split(' | <a',1)[0]
                # jen web
                elif 'title="Web"' in line and 'mailto:' not in line:
                    kom_web[pocet_komentaru] = line.split('</strong> | <a href="',1)[1]
                    kom_web[pocet_komentaru] = kom_web[pocet_komentaru].split('" title="Web">',1)[0]
                    kom_web[pocet_komentaru] = ocistit_url(kom_web[pocet_komentaru])

                    kom_datum[pocet_komentaru] = line.split('Web</a> | ',1)[1]
                    kom_datum[pocet_komentaru] = kom_datum[pocet_komentaru].split(' | <a',1)[0]
                # jen mail
                elif 'title="Web"'not in line and 'mailto:' in line:
                    kom_email[pocet_komentaru] = line.split('mailto:',1)[1]
                    kom_email[pocet_komentaru] = kom_email[pocet_komentaru].split('">E-mail',1)[0]
                    kom_email[pocet_komentaru] = kom_email[pocet_komentaru].replace(' (V) ','@')

                    kom_datum[pocet_komentaru] = line.split('E-mail</a> | ',1)[1]
                    kom_datum[pocet_komentaru] = kom_datum[pocet_komentaru].split(' | <a',1)[0]
                # ani jedno
                elif 'title="Web"' not in line and 'mailto:' not in line:
                    kom_datum[pocet_komentaru] = line.split('</strong> | ',1)[1]
                    kom_datum[pocet_komentaru] = kom_datum[pocet_komentaru].split(' | <a',1)[0]
            # text komentare
            elif '<div class="commentText"><p>' in line and cislo_radku_komentare == radek_s_komentarem:
                if debug:
                    sys.stdout.write('cislo_radku_komentare: ' + str(cislo_radku_komentare) + ' ; radek_s_komentarem: ' + str(radek_s_komentarem) + '\n')
                kom_text[pocet_komentaru] = line.split('<p>',1)[1]
                kom_text[pocet_komentaru] = kom_text[pocet_komentaru].split('</p></div></div>',1)[0]
                kom_text[pocet_komentaru] = kom_text[pocet_komentaru].strip()
                kom_text[pocet_komentaru] = kom_text[pocet_komentaru].rstrip()

		if '</p></div></div>' not in line:
                   nasledujici_radek_komentare = radek_s_komentarem + 1
		else:
                   nasledujici_radek_komentare = 0

	    elif cislo_radku_komentare == nasledujici_radek_komentare and 'commentHeader' not in line:
                if debug:
                    sys.stdout.write('Detekován víceřádkový komentář. nasledujici_radek_komentare: ' + str(nasledujici_radek_komentare) + '\n')
                zbytek_komentare = line.strip()
                zbytek_komentare = zbytek_komentare.rstrip()
                kom_text[pocet_komentaru] += zbytek_komentare
                kom_text[pocet_komentaru] = kom_text[pocet_komentaru].split('</p></div></div>',1)[0]
                kom_text[pocet_komentaru] = kom_text[pocet_komentaru].strip()
                kom_text[pocet_komentaru] = kom_text[pocet_komentaru].rstrip()

		if '</p></div></div>' not in line:
                   nasledujici_radek_komentare = nasledujici_radek_komentare + 1
		else:
                   nasledujici_radek_komentare = 0
                

    for y, elem in enumerate(kom_jmeno):

        z = y + index_pole

        try:
            test_mail = kom_email[z]
        except:
            kom_email[z] = ''
        try:
            test_web = kom_web[z]
        except:
            kom_web[z] = ''
        try:
            test_datum = kom_datum[z]
        except:
            kom_datum[z] = ''
        try:
            test_text = kom_text[z]
        except:
            kom_text[z] = ''
	#-------debug, pod vyřešení odstranit -->
	if debug:
	    sys.stdout.write('proměnná z: ' + str(z) + '\n')

	if komentarovy_soubor == 'temp/1510-transformace-rijen-2015' and z == 204:
	   sys.stdout.write('JE TO ON!!\n')
	   break
		
	if komentarovy_soubor == 'temp/1409-aktualni-energie-bovis-xi' and z == 208:
	   sys.stdout.write('JE TO ON!!\n')
	   break
 
	#-----------
        if z > index_pole:
            if debug:
                sys.stdout.write('komentar: ' + str(z) + '. ' + kom_jmeno[z] + ' | ')
            wpxml = open(vystupni_soubor, 'a')
            wpxml.write('       <wp:comment>\n')
            wpxml.write('           <wp:comment_id>' + str(z) + '</wp:comment_id>\n')
            wpxml.write('           <wp:comment_author><![CDATA[' + kom_jmeno[z] + ']]></wp:comment_author>\n')
            wpxml.write('           <wp:comment_author_email><![CDATA[' + kom_email[z] +']]></wp:comment_author_email>\n')
            wpxml.write('           <wp:comment_author_url>' + kom_web[z] + '</wp:comment_author_url>\n')
            wpxml.write('           <wp:comment_author_IP>127.0.0.1</wp:comment_author_IP>\n')
            wpxml.write('           <wp:comment_date>' + prevoddata(kom_datum[z],debug) + '</wp:comment_date>\n')
            wpxml.write('           <wp:comment_date_gmt>' + minus_hodina(prevoddata(kom_datum[z],debug)) + '</wp:comment_date_gmt>\n')
            wpxml.write('           <wp:comment_content><![CDATA[' + kom_text[z] + ']]></wp:comment_content>\n')
            wpxml.write('           <wp:comment_approved>1</wp:comment_approved>\n')
            wpxml.write('           <wp:comment_type></wp:comment_type>\n')
            wpxml.write('           <wp:comment_parent>0</wp:comment_parent>\n')
            wpxml.write('           <wp:comment_user_id>0</wp:comment_user_id>\n')
            wpxml.write('       </wp:comment>\n')
            wpxml.close()


##############################
# exportovat_clanek 
##############################

def exportovat_clanek(url_blog,vstupni_soubor,vystupni_soubor,idclanku,debug,export_mode,novy_blog,img_dir,prepis_odkazu,prepis_obrazku):
    titulek_clanku = ''
    rubrika_url = ''
    rubrika = ''
    autor = ''
    datum_extrakt = ''
    text_clanku = ''
    url_clanku = ''
    url_komentaru = ''
    id_clanku = idclanku
    cislo_radku = 0
    od_zacatku = 0
    clanek_zacatek = 0
    radek_clanek = 0
    radek_datum = 0
    zapsano_radku = 0

    status_fail = ' [\033[91mFAIL\033[0m] '
    status_ok = ' [\033[92m OK \033[0m] '
    status_warn= ' [\033[93mWARN\033[0m] '

    vstupni_soubor = vstupni_soubor.strip()
    vstupni_soubor = vstupni_soubor.rstrip()
    vstupni_soubor = 'temp/'+vstupni_soubor

    obrazek = ''

    with open(vstupni_soubor, 'rU') as k:
        for line in k:
            cislo_radku += 1
            od_zacatku = cislo_radku - clanek_zacatek

	    #if debug:
	    #   sys.stdout.write(str(cislo_radku) + '\n')

            if '<meta property="og:url"' in line:
		if debug:
		   sys.stdout.write('meta property detekovano na radku: ' + str(cislo_radku) + '\n')
                url_clanku = line.split('blog.cz/',1)[1]
                url_clanku = url_clanku.split('/',1)[1]
                url_clanku = url_clanku.split('" />',1)[0]
            # cislo radku, kde zacina clanek
            elif '<div class="article">' in line:
                clanek_zacatek = cislo_radku
		if debug:
 		   sys.stdout.write('zacatek sekce <div class="article"> detekovan na radku: ' + str(cislo_radku) + '\n')
            # titulek clanku    
            elif "<title>" in line:
		if debug:
		   sys.stdout.write("<title> detekováno na radku: " + str(cislo_radku) + '\n')
                titulek_clanku = line.split('|',1)[0]
                titulek_clanku = titulek_clanku.split('<title>',1)[1]
                titulek_clanku = titulek_clanku.rstrip()
            # nazev blogu
                nazev_blogu = line.split('|',1)[1]
                nazev_blogu = nazev_blogu.split('</title>',1)[0]
                nazev_blogu = nazev_blogu.rstrip()
                nazev_blogu = nazev_blogu.strip()
            # url rubriky, ve ktere byl clanek publikovan
            elif '/rubrika' in line and od_zacatku < 5 and od_zacatku > 0:
                rubrika_url = line.split('<a href="/rubrika/',1)[1]
                rubrika_url = rubrika_url.split('"',1)[0]
		if debug:
		   sys.stdout.write('url rubriky, ve ktere byl clanek publikovan: ' + rubrika_url + '\n')
            # slovni nazev rubriky
            elif 'title="Rubrika:' in line and od_zacatku < 7 and od_zacatku > 0:
                rubrika = line.split('title="Rubrika: ',1)[1]
                rubrika = rubrika.split('">',1)[0]
		if debug:
		   sys.stdout.write('nazev rubriky, ve ktere byl clanek publikovan: ' + rubrika + '\n')
            # autor clanku
            elif '|&nbsp;' in line and ':' in line and od_zacatku < 3 and od_zacatku > 0:
                autor = line.split('|&nbsp;',1)[1]
                autor = autor.rstrip()
		if debug:
		   sys.stdout.write('autor clanku: ' + autor + '\n') 
	    # datum publikovani
                datum_extrakt = line.split('|&nbsp;',1)[0]
                datum_extrakt = datum_extrakt.rstrip()
                datum_extrakt = datum_extrakt.strip()
            elif '|&nbsp;' in line and 'Před' in line and od_zacatku < 3 and od_zacatku > 0:
		if debug:
		   sys.stdout.write('datum varianta 1\n')
                autor = line.split('|&nbsp;',1)[1]
                autor = autor.rstrip()
	    elif '</h2>' in line and od_zacatku < 2 and od_zacatku > 0 and datum_extrakt == "":
		if debug:
		   sys.stdout.write('datum varianta 2\n')
		radek_datum = cislo_radku + 1
	    elif cislo_radku is radek_datum and datum_extrakt == "":
		if debug:
		   sys.stdout.write('datum varianta 3\n')
		datum_extrakt = line.rstrip()
		datum_extrakt = datum_extrakt.strip()
		sys.stdout.write(datum_extrakt)
            # ulozime si cislo radku, za kterym zacina samotny clanek + 1, kde zacina doopravdy
            elif '<div class="articleText">' in line:
                radek_clanek = cislo_radku + 1
		if debug:
		   sys.stdout.write('cislo radku, kde je text clanku: ' + str(radek_clanek) + '\n')
            # tady uz samotny text..    
            elif cislo_radku == radek_clanek:
		if debug:
		   sys.stdout.write('prave je zpracovavan radek s textem clanku\n')
                text_clanku = line.rsplit('</div>',1)[0]
                text_clanku = text_clanku.strip()
                text_clanku = text_clanku.rstrip()
		if debug:
		   sys.stdout.write('text_clanku: ' + text_clanku + '\n')
               # vykosteni a stazeni obrazku
                if '<img' in line:
		    if debug:
		       sys.stdout.write('v clanku byly nalezeny obrazky\n')
                    xx = '<img'
                    yy = 0
                    konec = False

                    if not konec:
                        posledni = ''
                        for xx in line:
                            yy += 1
			    if debug:
			       sys.stdout.write(str(yy) +'.<img> \n')
                            try:
                                obrazek = line.split('<img',1)[1]
                                obrazek = obrazek.split('src="',1)[1]
                                obrazek = obrazek.split('"',1)[0]

                                jmeno_souboru = obrazek.rsplit('/',1)[1]
                                soubor_obrazek = 'obrazky/' + jmeno_souboru
                                if obrazek == obrazek:
                                    jmeno_souboru = obrazek.rsplit('/',1)[1]

                                    if export_mode == 4:
                                        stahni_obrazek(obrazek,export_mode,debug,prepis_obrazku)
					novy_blog_img = novy_blog.split('.',1)[0]
					novy_blog_img = novy_blog_img + '.files.wordpress.com'
					
                                        nova_url = novy_blog_img + '/' + tento_rok + '/' + tento_mesic.zfill(2) + '/' + jmeno_souboru
                                    if export_mode == 3:
                                        prepis_obrazku = 1
                                        nova_url = stahni_obrazek(obrazek,export_mode,debug,prepis_obrazku)
                                    if export_mode == 2:
                                        stahni_obrazek(obrazek,export_mode,debug,prepis_obrazku)
                                        nova_url = 'wp-content/uploads/' + jmeno_souboru
                                    if export_mode == 1:
                                        stahni_obrazek(obrazek,export_mode,debug,prepis_obrazku)
                                        nova_url = img_dir + '/' +  jmeno_souboru

                                    if debug:
                                        sys.stdout.write('stara url: ' + obrazek + '\n')
                                        sys.stdout.write('nova url: ' + nova_url + '\n')
				    
                                    # rewrite pouze adres obrázků hostovaných na blog.cz
                                    if 'jxs.cz' in obrazek and prepis_obrazku == 2:
                                        text_clanku = text_clanku.replace(obrazek, nova_url)
				    elif prepis_obrazku == 1: # přepsat cesty všech obrázků
					text_clanku = text_clanku.replace(obrazek, nova_url)
				    

                                    line = line.split(obrazek,1)[1]
                                    posledni = obrazek


                                else:
                                    if debug:
                                        sys.stdout.write('obrázek již stažen a zpracován\n')
                            except:
                               break 

		#------- rewrite odkazů na interní články (na stejném blogu, jako je ten exportovaný) -----------------
		odkaz = ''
		odkaz_novy = ''

                if url_blog in text_clanku:
                    if debug:
                       sys.stdout.write('v článku byl nalezen odkaz na interní článek\n')
		    tt = '<a href="'
                    pp = 0
                    konec_odkazu = False

		    ke_zpracovani = text_clanku

                    if not konec_odkazu:
                        posledni_odkaz = '' 
                        for tt in ke_zpracovani:
                            pp += 1 
                            try:
				odkaz = ke_zpracovani.split('<a',1)[1]
                                odkaz = odkaz.split('href="',1)[1]
                                odkaz = odkaz.split('"',1)[0]
				if posledni_odkaz == odkaz:
				   if debug:
				      sys.stdout.write('tento odkaz byl poslední, konec cyklu \n')
				   break
				if debug:
				   sys.stdout.write(str(pp) + ': ' + odkaz + '\n')
				
				# přepisovat odkazy jen ty, co původně vedly na stejný blog jako právě exportovaný
				# a zároveň pouze pokud je aktivní režim přepisu odkazů
				if url_blog in odkaz and prepis_odkazu == 2:
                                    odkaz_novy = odkaz.rsplit('/',1)[1]
				    text_clanku = text_clanku.replace(odkaz, odkaz_novy)
				    if debug:
			                sys.stdout.write('odkaz novy: ' + odkaz_novy + '\n')

				posledni_odkaz = odkaz
				
				# odzriznout jiz zpracovanou cast
				ke_zpracovani = ke_zpracovani.split(odkaz,1)[1]
			    except:
				break
		else:
		    if debug:
			sys.stdout.write('nebyl nalezen žádný interní odkaz k přepsání\n')

    wpdatum = prevoddata(datum_extrakt,debug)
    gmtdatum = minus_hodina(wpdatum)
    pubdatum = gmtdate2pubdate(gmtdatum)

    if autor == "":
        if debug:
    	    sys.stdout.write('\n' + status_warn + 'U článku "' + titulek_clanku + '" se nepodařilo extrahovat jméno autora\n')
        autor = "neznámý autor"

    elif wpdatum == "":
	sys.stdout.write('\n' + status_fail + 'U článku "' + titulek_clanku + '" se nepodařilo extrahovat datum publikování\n')
	sys.exit(1)

    elif text_clanku == "":
    	sys.stdout.write('\n' + status_fail + 'Nepodařilo se extrahovat text článku "' + titulek_clanku + '"\n')
    	sys.exit(1)

    wpxml = open(vystupni_soubor, "a")

    wpxml.write('   <item>\n')
    wpxml.write('       <title>' + titulek_clanku + '</title>\n')
    wpxml.write('       <link>' + novy_blog + '/' + url_clanku + '/</link>\n')
    wpxml.write('       <pubDate>' + pubdatum + '</pubDate>\n')
    wpxml.write('       <dc:creator><![CDATA[' + autor + ']]></dc:creator>\n')
    wpxml.write('       <guid isPermaLink="false">' + novy_blog + '/?p=' + str(id_clanku) + '</guid>\n')
    wpxml.write('       <description></description>\n')
    wpxml.write('       <content:encoded><![CDATA[' + text_clanku + ']]></content:encoded>\n')
    wpxml.write('       <excerpt:encoded><![CDATA[]]></excerpt:encoded>\n')
    wpxml.write('       <wp:post_id>' + str(id_clanku) + '</wp:post_id>\n')
    wpxml.write('       <category domain="category" nicename="' + rubrika_url + '"><![CDATA[' + rubrika + ']]></category>\n')
    wpxml.write('       <wp:post_date>' + wpdatum + '</wp:post_date>\n')
    wpxml.write('       <wp:post_date_gmt>' + gmtdatum + '</wp:post_date_gmt>\n')
    wpxml.write('       <wp:comment_status>open</wp:comment_status>\n')
    wpxml.write('       <wp:ping_status>open</wp:ping_status>\n')
    wpxml.write('       <wp:post_name>' + url_clanku + '</wp:post_name>\n')
    wpxml.write('       <wp:status>publish</wp:status>\n')
    wpxml.write('       <wp:post_parent>0</wp:post_parent>\n')
    wpxml.write('       <wp:menu_order>0</wp:menu_order>\n')
    wpxml.write('       <wp:post_type>post</wp:post_type>\n')
    wpxml.write('       <wp:post_password></wp:post_password>\n')
    wpxml.write('       <wp:is_sticky>0</wp:is_sticky>\n')
    wpxml.write('       <wp:postmeta>\n')
    wpxml.write('           <wp:meta_key>_edit_last</wp:meta_key>\n')
    wpxml.write('           <wp:meta_value><![CDATA[1]]></wp:meta_value>\n')
    wpxml.write('       </wp:postmeta>\n')
    wpxml.close()

    zpracovat_komentare(vstupni_soubor,vystupni_soubor,debug)

    wpxml = open(vystupni_soubor, "a")
    wpxml.write('   </item>\n\n\n')
    wpxml.close()

    zapsano_radku = num_lines = sum(1 for line in open(vystupni_soubor))

    # csv
    wpcsv = open('temp/odkazy.csv', "a")
    wpcsv.write(novy_blog + '/' + url_clanku + ';' + url_clanku + '/\n')
    wpcsv.close()



    return zapsano_radku


##########################################################################################
#
# SAMOTNY PROGRAM
#

# statusy v konzoli
status_fail = ' [\033[91mFAIL\033[0m] '
status_ok = ' [\033[92m OK \033[0m] '
status_warn= ' [\033[93mWARN\033[0m] '

try:
    url_blog = sys.argv[1]
except:
    sys.stdout.write(status_fail + 'Jako parametr je třeba zadat adresu převáděného blogu\n')
    sys.exit(1)

if 'blog.cz' not in url_blog:
    sys.stdout.write(status_fail + 'Adresa převáděného blogu musí být ve tvaru nazevblogu.blog.cz\n')
    sys.exit(1)

# pokud byla url blogu zadana bez "http://", doplnime
if 'http://' not in url_blog:
    url_blog = 'http://' + url_blog

# orizneme vsechno za .cz
url_blog = url_blog.split('.cz',1)[0]
url_blog = url_blog + '.cz'

# zapnout/vypnout debug mode parametrem
try:
    if sys.argv[2] == 'debug':
        debug = True
except:
    debug = False



# inicializace promennych
cislo_radku = 0
clanek_soubor = ''
clanek_soubor_p1 = ''
clanek_soubor_p2 = ''
pocet_dle_blogu = 0
pocet_dle_souboru = 0

export_mode = 0
export_mode_vstup = ''
prepis_odkazu = 0
prepis_obrazku = 0

novy_blog = ''
img_dir = ''

sys.stdout.write('\n')
sys.stdout.write('1 - vlastní wordpress nebo hosting obrázků: stáhnout obrázky, cesty změnit na absolutní\n')
sys.stdout.write('2 - vlastní wordpress: stáhnout obrázky, cesty změnit na relativní do wp-content/uploads\n')
sys.stdout.write('3 - blogspot.com: obrázky nestahovat, ponechat absolutní cesty na jejich puvodní umístění\n')
sys.stdout.write('4 - wordpress.com: stáhnout obrázky, cesty změnit na nové umistaní na wp.com\n')

while True:
    export_mode_vstup = raw_input("Zvolte režim exportu (1-4): ")
    if export_mode_vstup == '1':
        export_mode = 1
        break
    elif export_mode_vstup == '2':
        export_mode = 2
        break
    elif export_mode_vstup == '3':
        export_mode = 3
        break
    elif export_mode_vstup == '4':
        export_mode = 4
        break

sys.stdout.write('\nVybrali jste: ' + str(export_mode) + '\n\n')

# --- input adresy nového blogu na vlastním Wordpressu + input url k adresáři s obrázky
if export_mode == 1:
    sys.stdout.write('Zadejte doménu, na které bude běžet nový blog.\nZadávejte ve tvaru s http/https, např. http://mojedomena.cz nebo https://mujblog.cz\n')
    while True:
        novy_blog = raw_input("Adresa: ")
        if novy_blog != '':
            break
    sys.stdout.write('Zadej URL adresáře s obrázky, cesta může být absolutní i relativní - např. http://mojedomena.cz/obrazky/fotky, img/obrazky nebo wp-content/uploads/stare\n')
    
    while True:
        img_dir = raw_input("Adresa: ")
	if img_dir != '':
            break

# --- input adresy cílového blogu na wordpress.com
if export_mode == 4:
    sys.stdout.write('Zadejte adresu nového blogu na wordpress.com.\nZadávejte ve tvaru bez http/https, např. mujblog.wordpress.com\n')
    while True:
        novy_blog = raw_input("Adresa: ")
        if novy_blog != '':
            novy_blog = 'https://' + novy_blog
            break

if export_mode == 3:
	novy_blog = url_blog

# --- výběr režimu nakládání s interními odkazy
if export_mode != 3:

    sys.stdout.write('Režim nakládání s interními odkazy směrujícími na články na exportovaném blogu:\n')
    sys.stdout.write('1 - ponechat v původní podobě, např. <a href="' + url_blog + '/1902/nejaky-pekny-clanek">\n') 
    sys.stdout.write('2 - přepsat na novou doménu s konvencí Permalink: post name, např. <a href=' + novy_blog + '/nejaky-pekny-clanek">\n')
    while True:
        prepis_odkazu_input = raw_input("Zvolte režim (1-2):\n")
	if prepis_odkazu_input == "1":
            prepis_odkazu = 1
	    break
 	elif prepis_odkazu_input == "2":
	    prepis_odkazu = 2
            break

# --- výběr režimu nakládání s adresami obrázků
if export_mode != 3:

    sys.stdout.write('Režim nakládání s adresami obrázků linkovaných v článcích:\n')
    sys.stdout.write('1 - přepsat všechny cesty na nové umístění, stáhnout všechny obrázky\n') 
    sys.stdout.write('2 - přepsat pouze cesty obrázků hostovaných na blog.cz a stáhnout pouze ty\n')
    while True:
        prepis_obrazku_input = raw_input("Zvolte režim (1-2):\n")
	if prepis_obrazku_input == "1":
            prepis_obrazku = 1
	    break
 	elif prepis_obrazku_input == "2":
	    prepis_obrazku = 2
            break
         



vystupni_soubor = url_blog.split('http://',1)[1]
vystupni_soubor = vystupni_soubor + '.xml'

# zalozime pracovni adresar temp
if not os.path.exists('temp'):
        os.makedirs('temp')

# zalozime obrazkovy adresar
if not os.path.exists('obrazky'):
    os.makedirs('obrazky')
    # zalozime soupis
    soupis_obrazku = open('temp/soupis_obrazku.txt', "w+")
    soupis_obrazku.close()


sys.stdout.write('        URL exportovaného blogu: ' + url_blog + '\n')
sys.stdout.write('        URL nového blogu: ' + novy_blog + '\n')
sys.stdout.write('        URL adresáře s obrázky: ' + img_dir + '\n\n')

sys.stdout.write('        Pracovní adresář: ' + 'temp\n')
sys.stdout.write('        Jméno XML souboru s exportem: ' + vystupni_soubor + '\n\n')



#sys.stdout.write('        Nalezené rubriky k exportu:\n')
exportovat_rubriky(url_blog,vystupni_soubor,debug)

#sys.stdout.write('        Nalezene články v archivu:\n')
pocet_dle_blogu = exportovat_archiv(url_blog,debug)

#sys.stdout.write('        Nalezené články:\n')
soupis_clanku(url_blog,debug)


# porovnavame pocet radku s odkazy na clanky s cislem spocitanym z poctu clanku v archivu
pocet_dle_souboru = num_lines = sum(1 for line in open('temp/soupis_clanku.txt'))

# pokud program nebezi v debug modu, pri nesouhlasu poctu nalezenych clanku oproti archivu se ukonci
if pocet_dle_souboru != pocet_dle_blogu:
    sys.stdout.write(status_fail + 'Počet článků nesouhlasí! V archivu deklarováno / nalezeno: ' + str(pocet_dle_blogu) + ' / ' + str(pocet_dle_souboru) + '\n')
    if not debug:
        sys.exit(1)
else:
    sys.stdout.write('\n' + status_ok + 'Počet nalezených článků se shoduje s deklarovanými počty v archivu\n')
    sys.stdout.write(status_ok + 'Celkový počet článků ke stažení: ' + str(pocet_dle_souboru) + '\n')
    sys.stdout.write(' [info] stahuji články, zpracovávám jejich obsah a zapisuji jej do XML:\n')


# zapsat do XMLka clanky
with open('temp/soupis_clanku.txt', 'rU') as m:
    for zaznam in m:
        cislo_radku += 1
        zaznam = zaznam.rstrip('\r\n')
        clanek_soubor = zaznam.split('blog.cz/',1)[1]
        clanek_soubor_p1 = clanek_soubor.split('/',1)[0]
        clanek_soubor_p2 = clanek_soubor.split('/',1)[1]
        clanek_soubor = clanek_soubor_p1 + '-' + clanek_soubor_p2
        clanek_soubor = clanek_soubor.strip()
        clanek_soubor = clanek_soubor.rstrip('\r\n')
        clanek_soubor_test = 'temp/' + clanek_soubor
	
        if os.path.isfile(clanek_soubor_test):
	    if debug:
               sys.stdout.write("\n\n [" + str(cislo_radku) + '/' + str(pocet_dle_souboru) + '] soubor již existuje, zapisuji do xml: ' + clanek_soubor + '\n')
	    else:
               progressbar(cislo_radku,pocet_dle_souboru)
        else:
            stahni_html(zaznam,True)
	    if debug:
               sys.stdout.write("\n\n [" + str(cislo_radku) + '/' + str(pocet_dle_souboru) +  '] soubor stažen, zapisuji do xml: ' + clanek_soubor + '\n')
            else:
		progressbar(cislo_radku,pocet_dle_souboru)



        exportovat_clanek(url_blog,clanek_soubor,vystupni_soubor,cislo_radku,debug,export_mode,novy_blog,img_dir,prepis_odkazu,prepis_obrazku)

wpxml = open(vystupni_soubor, "a")
wpxml.write(' <generator>https://wordpress.org/?v=4.8.1</generator>')
wpxml.write('</channel>\n')
wpxml.write('</rss>\n')
wpxml.close()

os.rename("temp/soupis_obrazku.txt", "obrazky/soupis_obrazku.txt")

sys.stdout.write('\n' + status_ok + 'Hotovo! Výsledek uložen do ' + vystupni_soubor + '\n')
sys.exit(0)
