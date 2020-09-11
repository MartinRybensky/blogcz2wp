# blogcz2wp
```diff
- Provoz serveru blog.cz byl ukončen, blogy na něm hostované již nejsou dostupné.

- Skriptem blogcz2wp již nelze žádný blog stáhnout a zazálohovat, program jako takový již tedy pozbyl smysl své existence. 
```
Od vzniku první verze programu v srpnu 2017 bylo až do srpna 2020 během těchto tří let jen mnou zazálohováno na žádost jejich autorů přes 150 blogů. Mnoho dalších pak bez mé pomoci uživateli samostatně, jejich počet mi však není znám. Tak jako tak, s odstupem hodnotím celý projekt jako úspěšný a mám radost z každého blogu, který byl pomocí skriptu blogcz2wp zachráněn.

Děkuji všem, kteří mi jej hlášením chyb a poskytnutím námětů na rozšíření či vylepšení pomohli rozvíjet. Speciální dík patří uživateli @korbeljak, který kód převedl do formátu kompatibilního s Python3.

## původní README (již neaktuální)

Blogcz2WP je nástroj umožňující export obsahu blogu běžícího na doméně blog.cz a následný import do redakčního systému Wordpress.
Výstupem je soubor XML ve formátu WXR (Wordpress Extended RSS) určený pro Wordpress Importer.

Blogcz2WP umí:
* stáhnout obsah blogu na doméně blog.cz, tzn. články, autory, kategorie a komentáře
* zachovat u článků a komentářů jejich metadata (čas zveřejnění, autor, e-mail, www autora, atd.)
* vyhledat obrázky v článcích a pořídit jejich soupis, v exportovaných článcích modifikovat cesty k obrázkům tak, aby se načítaly z nového umístění
* přepsat interní odkazy v článcích na jiné články na stejném blogu na novou doménu podle konvence PermaLink: Post Name
* rozdělit výstupní data do více XML souborů po 5 MB (kvůli limitům upload_max_filesize/post_max_size a blogspot konvertoru) 

Není vyžadováno žádné heslo ani jiné přístupové údaje, skript pracuje s volně dostupnými stránkami, nepřistupuje k žádným chráněným zdrojům, nehackuje blog.cz ani jeho databázi.
Export se nijak nedotkne stávajícího blogu, ten zůstává beze změny. Pro správnou funkci je pouze nutné mít rozhraní blogu nastaveno na český jazyk.


Více o projektu naleznete zde:
http://blog.veruce.cz/migrace-z-blog-cz-na-wordpress/

## Závislosti:
Python 2.7 nebo Python 3

requests  (pip install requests)

## Použití (Linux):
```
./blog2wp.py jmeno-vaseho-blogu.blog.cz
```

## Použití (Windows):
Vyžaduje mít nainstalován Python 2.7 pro Windows: https://www.python.org/ftp/python/2.7.18/python-2.7.18.msi
```
C:\python27\python.exe -m pip install requests

C:\python27\python.exe blog2wp.py jmeno-vaseho-blogu.blog.cz
```
## Obrázky
Soupis obrázků je pořízen do souboru obrazky/soupis_obrazku.txt, obrázky nejsou skriptem stahovány za jeho běhu. K jejich následnému stažení použijte svůj oblíbený download manager, třeba wget:
```
wget -i soupis_obrazku.txt -nc
```
# Blogspot.com / Blogger.com
Výsledné XML vygenerované programem je určeno pro Wordpress, před importem do blogu na blogspot.com je nutné provést konverzi pomocí této webové aplikace:
https://wordpress-to-blogger-converter.appspot.com/

## Upozornění 
__Autor programu nenese odpovědnost za neautorizované použití ve smyslu exportu cizího blogu bez souhlasu jeho autora. 
Uživatel se zavazuje stahovat pouze autorský obsah, jehož je vlastníkem nebo od vlastníka obdržel explicitní souhlas.
Program Blogcz2WP je poskytován zdarma bez jakýchkoliv záruk a nároku na cokoliv.__

