#!/usr/bin/python
# -*- coding: utf-8 -*-

#  blog2wp.py
#
#
# 2018-09-18
#
# Martin Rybensky
#

import sys, os, urllib2, datetime, time, urlparse

tento_rok = str(datetime.datetime.now().year)
tento_mesic = str(datetime.datetime.now().month)

##########################################################################################
# DEFINICE FUNKCI


##############################
# prevoddata - funkce prevadejici posrane tvary datumu z blog.cz 
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
        print 'prevoddata na vstupu: ' + fujdatum

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
        print 'minut: ' + str(minut)
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
        print 'prevoddata na vystupu: ' + wpdatum

    return wpdatum


##############################
#
# ocistit_url - zbavi url v komentari nezadouciho nofollow
#
##############################

def ocistit_url(web_url):
    if 'nofollow' in web_url:
        ocistena_url = web_url.split('" rel="nofollow',1)[0]
    else:
        ocistena_url = web_url

    return ocistena_url

##############################
#
# stahni_obrazek
#
##############################

def stahni_obrazek(url_ke_stazeni,export_mode):
    # debug
    #print '--! zavolana funkce stahni_obrazek'
    vstupni_url = url_ke_stazeni

    url_obrazku = ''
    server = ''
    spravna_url = ''
    jmeno_souboru = ''
    jmeno_souboru_p1 = ''
    jmeno_souboru_p2 = ''

    url_blog = url_ke_stazeni.split('.cz/',1)[0]
    url_blog = url_blog + '.cz/'

    # pokud url obrazku obsahuje vyrazy "bcache" nebo "imageproxy", 
    # je nahran na galerie.cz a je chranen proti externimu nacteni/odkazovani

    # pokud je toto detekovano, je chranena url odrbana o ochranne prvky
    if 'bcache' in vstupni_url or 'imageproxy' in vstupni_url:
        #print 'obrazek je hostovan na blogu.cz'
        url_obrazku = vstupni_url.split('cz~',1)[1]
        server = vstupni_url.split('~',1)[1]
        server = server.split('~',1)[0]
        server = server.replace('/','.')
        spravna_url = 'http://' + server + url_obrazku
        print 'spravna url po zruseni ochrany: ' + spravna_url
    else:
        #print 'obrazek je hostovan externe' # pokud vyrazy testovane vyse detekovany nejsou,
        spravna_url = vstupni_url           # je zjistena url rovnou povazovana za pouzitelnou

    # samotne stahovani neprovadime u varianty exportu, kdy ponechavame puvodni url obrazku
    if export_mode != 3:
        jmeno_souboru = url_ke_stazeni.rsplit('/',1)[1]
        jmeno_souboru = 'obrazky/' + jmeno_souboru
        #print 'lokalni cesta: ' + jmeno_souboru

        # zjistena url je vlozena do soupisu obrazku 
        soupis = open('temp/soupis_obrazku.txt', "a")
        soupis.write(spravna_url + '\n')
        soupis.close()

        '''
        if not os.path.isfile(jmeno_souboru):

            req = urllib2.Request(spravna_url)
            req.add_header('Referer', vstupni_url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:10.0) Gecko/20100101 Firefox/10.0')
            response = urllib2.urlopen(req)
            do_souboru = response.read()

            print 'zapisuji...'
            soubor_zapis = open(jmeno_souboru, "w+")

            soubor_zapis.write(do_souboru)
            soubor_zapis.close()
            print 'zapsano'
            print 'zacatek sleepu 4s'
            time.sleep(10)
            print 'konec sleepu 4s'
        else:
            print '         soubor ' + jmeno_souboru + ' jiz existuje'
        '''
    #return jmeno_souboru # jen filename
    return spravna_url # i s adresou


##############################
#
# stahni_html - stahne ze zadane url html soubor
#
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
#
# exportovat_rubriky  
#
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

    if os.path.isfile('temp/rubriky'):
        print status_warn + 'soubor temp/soupis_clanku.txt již existuje, pokračuji s daty z něho'
    else:
        stahni_html(url_rubriky,False)
        print status_ok + 'soubor s definicemi rubrik úspešně stažen'

    # a ted to zapiseme do xmlka
    wpxml = open(vystupni_soubor, "w+")
    rubriky_txt = open('temp/rubriky.txt', "w+")


    with open('temp/rubriky', 'r') as k:
        for line in k:
            cislo_radku += 1

            # nazev blogu
            if "<title>" in line:
                nazev_blogu = line.split('|',1)[1]
                nazev_blogu = nazev_blogu.split('</title>',1)[0]
                nazev_blogu = nazev_blogu.rstrip()
                nazev_blogu = nazev_blogu.strip()

                wpxml.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
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
                wpxml.write('   <pubDate>Thu, 03 Aug 2017 20:18:27 +0000</pubDate>\n')
                wpxml.write('   <language>cs-CZ</language>\n')
                wpxml.write('   <wp:wxr_version>1.2</wp:wxr_version>\n')
                wpxml.write('   <wp:base_site_url>' + url_blog + '</wp:base_site_url>\n')
                wpxml.write('   <wp:base_blog_url>' + url_blog + '</wp:base_blog_url>\n')
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
                print str(cislo_rubriky) + ': ' + rubrika_nazev[cislo_rubriky]


    # soubor rubriky je jiz vytezen, smazat
    # os.remove('temp/rubriky')


    rubriky_txt.close()
    wpxml.close()
##############################
#
# exportovat_archiv
#
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
        print status_warn + 'soubor temp/archiv již existuje, pokračuji s daty z něho'
    else:
        stahni_html(url_archiv,False)
        print status_ok + 'soubor s definicemi rubrik úspesně stažen'

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
			print 'exportovat_archiv, zpracovavany radek: '+str(cislo_radku)
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

                print archiv_nazev[zaznam] + ', záznamů: ' + str(archiv_pocet[zaznam])
                archiv_txt.write(url_blog + '/' + archiv_url[zaznam] + '\n')
		
	    if '<div id="menuInner">' in line:
	    	break

    # soubor rubriky je jiz vytezen, smazat
    # os.remove('temp/archiv')
    pocet_celkem = sum(archiv_pocet.values())
    print 'celkový počet článků v archivu (dle deklarovaných počtů v závorkách): ' +  str(pocet_celkem)
    
    archiv_txt.close()

    return pocet_celkem

##############################
#
# soupis_clanku
#
##############################

def soupis_clanku(url_blog,debug):

    status_fail = ' [\033[91mFAIL\033[0m] '
    status_ok = ' [\033[92m OK \033[0m] '
    status_warn= ' [\033[93mWARN\033[0m] '

    cislo_radku = 0
    radek_odkaz = 0
    radek_zacatek = 0
    posledni_stranka = 0
    strankovani = False
    konec_vypisu = False
    vypis_excerpt = False


    # zapis ziskanych url clanku
    if os.path.isfile('temp/soupis_clanku.txt'):
        print status_warn + 'soubor temp/soupis_clanku.txt jiz existuje, pokracuji s daty z neho'
    else:
        seznam_txt = open('temp/soupis_clanku.txt', 'w+')

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
                            print url_blog + odkaz
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
                            print url_blog + odkaz
                            seznam_txt.write(url_blog + odkaz + '\n')



                        # pokud je v rubrice hodne clanku a strankuje se    
                        elif 'paginatorLongButton' in line and 'Poslední stránka' in line:
                            strankovani = True
                            posledni_stranka = line.rsplit('" title="Poslední stránka"',1)[0]
                            posledni_stranka = posledni_stranka.rsplit('"',1)[1]
                            posledni_stranka = posledni_stranka.rsplit('/',1)[1]
                            print 'posledni stránka katogorie: ' + posledni_stranka

                            for_posledni = int(posledni_stranka)
                            for_posledni = for_posledni + 1

                            for y in range (2, for_posledni):
                                strankovana_rubrika = url_blog + '/' + soubor_rubrika + '/' + str(y)
                                print strankovana_rubrika
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
                                            print url_blog + odkaz
                                            seznam_txt.write(url_blog + odkaz + '\n')
                                        # clanky jako excerpty
                                        elif '<div id="mainInner">' in line:
                                            radek_zacatek = cislo_radku + 1
                                        elif '<h3>' in line and not konec_vypisu and cislo_radku > radek_zacatek:
                                            odkaz = line.split('<a href="',1)[1]
                                            odkaz = odkaz.split('"',1)[0]
                                            odkaz = odkaz.strip()
                                            odkaz = odkaz.rstrip()
                                            print url_blog + odkaz
                                            seznam_txt.write(url_blog + odkaz + '\n')


        seznam_txt.close()




##############################
#
# zpracovat_komentare
#
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
                    print 'discussPrevious nalezen (strankovany vypis komentaru detekovan)'

    with open(vstupni_soubor, 'rU') as d:
       for lajnd in d:
            if 'commentNr" id="ref1"' in lajnd:
                od_jednicky = True
                if debug:
                    print 'commentNr" id="ref1" nalezen (vypis komentaru od 1. detekovan)'

    with open(vstupni_soubor, 'rU') as e:
       for lajn in e:

            if strankovane_komentare and not od_jednicky and 'discussPrevious' in lajn:
                print 'strankovane komentare u clanku vyse'
                url_komentaru = lajn.split('discussPrevious" href="',1)[1]
                url_komentaru = url_komentaru.split('" title="Zobrazit',1)[0]

                url_komentaru = url_blog + url_komentaru
                cislo_radku_komentare = 0
                stahni_html(url_komentaru,False)

                soubor_komentare = url_komentaru.rsplit('/',1)[1]
                url_noindex = url_komentaru.rsplit('/',1)[0]

                print 'stranek komentaru: ' + soubor_komentare + ' + zbytek'
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
                    print 'zpracovavam soubor:' + komentarovy_soubor + ', pocatecni index: ' + str(index_pole)
                    zapis_komentare(komentarovy_soubor,vystupni_soubor,index_pole,debug)

                    # aby se uz neprovadely radky nize
                    zpracovano = True

                index_pole = str(index_pole)
                index_pole = str(soubor_komentare) + '00'
                index_pole = int(index_pole)
                print 'zpracovavam zbytek z clanku, pocatecni index: ' + str(index_pole)
                zapis_komentare(vstupni_soubor,vystupni_soubor,index_pole,debug)




    if not zpracovano:
        index_pole = int(0)
        # nestrankovane komentare / zbytek komentaru prebyvajicich ze strankovanych
        komentarovy_soubor = vstupni_soubor
        if debug:
            print 'komentare zpracovavany ze souboru: ' + komentarovy_soubor
        zapis_komentare(komentarovy_soubor,vystupni_soubor,index_pole,debug)

def zapis_komentare(komentarovy_soubor,vystupni_soubor,index_pole,debug):

    # definice promennych
    pocet_komentaru = 0

    cislo_radku_komentare = 0
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
                kom_text[pocet_komentaru] = line.split('<p>',1)[1]
                kom_text[pocet_komentaru] = kom_text[pocet_komentaru].split('</p></div></div>',1)[0]
                kom_text[pocet_komentaru] = kom_text[pocet_komentaru].strip()
                kom_text[pocet_komentaru] = kom_text[pocet_komentaru].rstrip()

    if debug:
        print kom_jmeno
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

        if z > index_pole:
            if debug:
                print 'index: ' + str(z) + '. ' + kom_jmeno[z] + ', zapisuji'
            wpxml = open(vystupni_soubor, 'a')
            wpxml.write('       <wp:comment>\n')
            wpxml.write('           <wp:comment_id>' + str(z) + '</wp:comment_id>\n')
            wpxml.write('           <wp:comment_author><![CDATA[' + kom_jmeno[z] + ']]></wp:comment_author>\n')
            wpxml.write('           <wp:comment_author_email><![CDATA[' + kom_email[z] +']]></wp:comment_author_email>\n')
            wpxml.write('           <wp:comment_author_url>' + kom_web[z] + '</wp:comment_author_url>\n')
            wpxml.write('           <wp:comment_author_IP>127.0.0.1</wp:comment_author_IP>\n')
            wpxml.write('           <wp:comment_date>' + prevoddata(kom_datum[z],debug) + '</wp:comment_date>\n')
            wpxml.write('           <wp:comment_date_gmt>0000-00-00 00:00:00</wp:comment_date_gmt>\n')
            wpxml.write('           <wp:comment_content><![CDATA[' + kom_text[z] + ']]></wp:comment_content>\n')
            wpxml.write('           <wp:comment_approved>1</wp:comment_approved>\n')
            wpxml.write('           <wp:comment_type></wp:comment_type>\n')
            wpxml.write('           <wp:comment_parent>0</wp:comment_parent>\n')
            wpxml.write('           <wp:comment_user_id>0</wp:comment_user_id>\n')
            wpxml.write('       </wp:comment>\n')
            wpxml.close()


##############################
#
# exportovat_clanek - 
#
##############################


def exportovat_clanek(vstupni_soubor,vystupni_soubor,idclanku,debug,export_mode,novy_blog):
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

    #now = datetime.datetime.now()
    #aktualni_rok = now.year

    vstupni_soubor = vstupni_soubor.strip()
    vstupni_soubor = vstupni_soubor.rstrip()
    vstupni_soubor = 'temp/'+vstupni_soubor

    obrazek = ''

    with open(vstupni_soubor, 'rU') as k:
        for line in k:
            cislo_radku += 1
            od_zacatku = cislo_radku - clanek_zacatek

            if '<meta property="og:url"' in line:
                url_clanku = line.split('blog.cz/',1)[1]
                url_clanku = url_clanku.split('/',1)[1]
                url_clanku = url_clanku.split('" />',1)[0]
            # cislo radku, kde zacina clanek
            elif '<div class="article">' in line:
                clanek_zacatek = cislo_radku
            # titulek clanku    
            elif "<title>" in line:
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
            # slovni nazev rubriky
            elif 'title="Rubrika:' in line and od_zacatku < 7 and od_zacatku > 0:
                rubrika = line.split('title="Rubrika: ',1)[1]
                rubrika = rubrika.split('">',1)[0]
            # autor clanku
            elif '|&nbsp;' in line and ':' in line and od_zacatku < 3 and od_zacatku > 0:
                autor = line.split('|&nbsp;',1)[1]
                autor = autor.rstrip()
	    # datum publikovani
                datum_extrakt = line.split('|&nbsp;',1)[0]
                datum_extrakt = datum_extrakt.rstrip()
                datum_extrakt = datum_extrakt.strip()
            elif '|&nbsp;' in line and 'Před' in line and od_zacatku < 3 and od_zacatku > 0:
                autor = line.split('|&nbsp;',1)[1]
                autor = autor.rstrip()
	    elif '</h2>' in line and od_zacatku < 2 and od_zacatku > 0 and datum_extrakt == "":
		radek_datum = cislo_radku + 1
	    elif cislo_radku is radek_datum and datum_extrakt == "":
		datum_extrakt = line.rstrip()
		datum_extrakt = datum_extrakt.strip()
		print datum_extrakt
            # ulozime si cislo radku, za kterym zacina samotny clanek + 1, kde zacina doopravdy
            elif '<div class="articleText">' in line:
                radek_clanek = cislo_radku + 1
            # tady uz samotny text..    
            elif cislo_radku is radek_clanek:
                text_clanku = line.rsplit('</div>',1)[0]
                text_clanku = text_clanku.strip()
                text_clanku = text_clanku.rstrip()

               # vykosteni a stazeni obrazku
                if '<img' in line:
                    xx = '<img'
                    yy = 0
                    konec = False

                    if not konec:
                        posledni = ''
                        for xx in line:
                            yy += 1

                            try:
                                obrazek = line.split('<img',1)[1]
                                obrazek = obrazek.split('src="',1)[1]
                                obrazek = obrazek.split('"',1)[0]

                                jmeno_souboru = obrazek.rsplit('/',1)[1]
                                soubor_obrazek = 'obrazky/' + jmeno_souboru
                                if obrazek == obrazek:
                                    if debug:
                                        print 'podminka prosla..'
                                    jmeno_souboru = obrazek.rsplit('/',1)[1]

                                    if export_mode == 4:
                                        stahni_obrazek(obrazek,export_mode)
                                        nova_url = novy_blog + '/' + tento_rok + '/' + tento_mesic.zfill(2) + '/' + jmeno_souboru
                                    if export_mode == 3:
                                        nova_url = stahni_obrazek(obrazek,export_mode)
                                    if export_mode == 2:
                                        stahni_obrazek(obrazek,export_mode)
                                        nova_url = 'wp-content/uploads/' + jmeno_souboru
                                    if export_mode == 1:
                                        stahni_obrazek(obrazek,export_mode)
                                        nova_url = novy_blog + '/' + jmeno_souboru

                                    if debug:
                                        print 'stara url: ' + obrazek
                                        print 'nova url: ' + obrazek ## TADY KVULI DEBUGU NECHAVAME STAROU ADRESU NA BLOG.CZ

                                    text_clanku = text_clanku.replace(obrazek, nova_url)
                                    if debug:
                                        print 'pred zavolanim stahni'
                                        stahni_obrazek(obrazek,export_mode)
                                    if debug:
                                        print 'stahni_obrazek(' + obrazek + ')    --  doopravdy nestahuje, neprovokujeme'
                                    if debug:
                                        print 'po zavolani stahni'

                                    line = line.split(obrazek,1)[1]
                                    posledni = obrazek
                                    if debug:
                                        print 'posledni: ' + posledni
                                        print 'konec deje za podminkou'
                                else:
                                    if debug:
                                        print 'obrazek jiz stazen a zpracovan'
                                        #konec = True

                            except:
                                #print 'konec, protoze nelze iniciovat pole po splitu'
                                #konec = True
                                aha = 'haha'

    wpdatum = prevoddata(datum_extrakt,debug)

    if autor == "":
	print status_fail + 'U článku "' + titulek_clanku + '" se nepodařilo extrahovat jméno autora'
	sys.exit(0)
    elif wpdatum == "":
	print status_fail + 'U článku "' + titulek_clanku + '" se nepodařilo extrahovat datum publikování'
	sys.exit(0)
    elif text_clanku == "":
	print status_fail + 'Nepodařilo se extrahovat text článku "' + titulek_clanku + '"'
	sys.exit(0)

    wpxml = open(vystupni_soubor, "a")

    wpxml.write('   <item>\n')
    wpxml.write('       <title>' + titulek_clanku + '</title>\n')
    wpxml.write('       <link>' + url_blog + '/' + rubrika_url + '/' + url_clanku + '/</link>\n')
    wpxml.write('       <pubDate></pubDate>\n')
    wpxml.write('       <dc:creator><![CDATA[' + autor + ']]></dc:creator>\n')
    wpxml.write('       <guid isPermaLink="false">' + url_blog + '/?p=' + str(id_clanku) + '</guid>\n')
    wpxml.write('       <description></description>\n')
    wpxml.write('       <content:encoded><![CDATA[' + text_clanku + ']]></content:encoded>\n')
    wpxml.write('       <excerpt:encoded><![CDATA[]]></excerpt:encoded>\n')
    wpxml.write('       <wp:post_id>' + str(id_clanku) + '</wp:post_id>\n')
    wpxml.write('       <category domain="category" nicename="' + rubrika_url + '"><![CDATA[' + rubrika + ']]></category>\n')
    wpxml.write('       <wp:post_date>' + wpdatum + '</wp:post_date>\n')
    wpxml.write('       <wp:post_date_gmt>0000-00-00 00:00:00</wp:post_date_gmt>\n')
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
    wpxml.write('   </item>\n')
    wpxml.close()

    zapsano_radku = num_lines = sum(1 for line in open(vystupni_soubor))

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
    print status_fail + 'Jako parametr je třeba zadat adresu převáděného blogu'
    sys.exit(1)

if 'blog.cz' not in url_blog:
    print status_fail + 'Adresa převáděného blogu musí být ve tvaru nazevblogu.blog.cz'
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
domena = 'blogcz.veruce.cz'
cislo_radku = 0
clanek_soubor = ''
clanek_soubor_p1 = ''
clanek_soubor_p2 = ''
pocet_dle_blogu = 0
pocet_dle_souboru = 0

export_mode = 0
export_mode_vstup = ''

novy_blog = ''

print '\n'
print '1 - vlastni wordpress nebo hosting obrazku: stahnout obrazky, cesty zmenit na absolutni'
print '2 - vlastni wordpress: stahnout obrazky, cesty zmenit na relativni do wp-content/uploads'
print '3 - blogspot.com: obrazky nestahovat, ponechat absolutni cesty na jejich puvodni umisteni'
print '4 - wordpress.com: stahnout obrazky, cesty zmenit na nove umistani na wp.com\n'

while True:
    export_mode_vstup = raw_input("Zvolte rezim exportu (1-4): ")
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

print "Vybrali jste: ", export_mode

if export_mode == 1:
    print 'Zadejte kompletni adresu adresare, ve kterem se budou nachazet obrazky.\nZadavejte ve tvaru s http/https, napr. http://mojedomena.cz/obrazky/fotky nebo http://mujblog.cz/wp-content/upload\n'
    while True:
        novy_blog = raw_input("Adresa: ")
        if novy_blog != '':
            break
if export_mode == 4:
    print 'Zadejte adresu noveho blogu na wordpress.com.\nZadavejte ve tvaru bez http/https, napr. mujblog.wordpress.com\n'
    while True:
        novy_blog = raw_input("Adresa: ")
        if novy_blog != '':
            novy_blog = 'https://' + novy_blog
            break




print 'Adresa noveho blogu je nasledujici: ' + novy_blog



vystupni_soubor = url_blog.split('http://',1)[1]
vystupni_soubor = vystupni_soubor + '.xml'

# zalozime pracovni adresar
if not os.path.exists('temp'):
        os.makedirs('temp')

if export_mode != 3:
    # zalozime obrazkovy adresar
    if not os.path.exists('obrazky'):
        os.makedirs('obrazky')
    # zalozime soupis
    soupis_obrazku = open('temp/soupis_obrazku.txt', "w+")
    soupis_obrazku.close()


print '        URL exportovaného blogu: ' + url_blog
print '        Pracovní adresář: ' + 'temp'
print '        Jméno XML souboru s exportem: ' + vystupni_soubor + '\n'



print '        Nalezené rubriky k exportu:'
exportovat_rubriky(url_blog,vystupni_soubor,debug)

print '        Nalezene články v archivu:'
pocet_dle_blogu = exportovat_archiv(url_blog,debug)

print '        Nalezené články:'
soupis_clanku(url_blog,debug)


# porovnavame pocet radku s odkazy na clanky s cislem spocitanym z poctu clanku v archivu
pocet_dle_souboru = num_lines = sum(1 for line in open('temp/soupis_clanku.txt'))

# pokud program nebezi v debug modu, pri nesouhlasu poctu nalezenych clanku oproti archivu se ukonci
if pocet_dle_souboru != pocet_dle_blogu and not debug:
    print status_fail + 'Počet článků nesouhlasí! V archivu deklarováno / nalezeno: ' + str(pocet_dle_blogu) + ' / ' + str(pocet_dle_souboru) + '\n'
    sys.exit(0)
else:
    print status_ok + 'Počet nalezených článků se shoduje s deklarovanými počty v archivu'
    print status_ok + 'Celkový počet článků ke stažení: ' + str(pocet_dle_souboru)

# debug

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
            print str(cislo_radku) + '. soubor jiz existuje, zapisuji do xml: ' + clanek_soubor
        else:
            stahni_html(zaznam,True)
            print str(cislo_radku) + '.soubor stazen, zapisuji do xml: ' + clanek_soubor



        exportovat_clanek(clanek_soubor,vystupni_soubor,cislo_radku,debug,export_mode,novy_blog)

wpxml = open(vystupni_soubor, "a")
wpxml.write(' <generator>https://wordpress.org/?v=4.8.1</generator>')
wpxml.write('</channel>\n')
wpxml.write('</rss>\n')
wpxml.close()



print status_ok + 'Hotovo! Vysledek ulozen do ' + vystupni_soubor ; '\n'
sys.exit(0)
