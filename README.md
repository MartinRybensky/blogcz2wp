# blogcz2wp

Blogcz2WP je nástroj umožňující export obsahu blogu běžícího na doméně blog.cz a následný import do redakčního systému Wordpress.
Výstupem je soubor XML ve formátu WXR (Wordpress Extended RSS) určený pro Wordpress Importer.

Blogcz2WP umí:
* stáhnout obsah blogu na doméně blog.cz, tzn. články, autory, kategorie a komentáře
* zachovat u článků a komentářů jejich metadata (čas zveřejnění, autor, e-mail, www autora, atd.)
* stáhnout obrázky v článcích, v exportovaných článcích modifikovat cesty k obrázkům tak, aby se načítaly z nového umístění
* přepsat interní odkazy v článcích na jiné články na stejném blogu na novou doménu podle konvence PermaLink: Post Name

Není vyžadováno žádné heslo ani jiné přístupové údaje, skript pracuje s volně dostupnými stránkami, nepřistupuje k žádným chráněným zdrojům, nehackuje blog.cz ani jeho databázi.
Export se nijak nedotkne stávajícího blogu, ten zůstává beze změny. Pro správnou funkci je pouze nutné mít rozhraní blogu nastaveno na český jazyk.




Více o projektu naleznete zde:
http://blog.veruce.cz/migrace-z-blog-cz-na-wordpress/

## Použití:
```
./blog2wp.py jmeno-vaseho-blogu.blog.cz
```

## Upozornění 
__Autor programu nenese odpovědnost za neautorizované použití ve smyslu exportu cizího blogu bez souhlasu jeho autora. 
Uživatel se zavazuje stahovat pouze autorský obsah, jehož je vlastníkem nebo od vlastníka obdržel explicitní souhlas.
Program Blogcz2WP je poskytován zdarma bez jakýchkoliv záruk a nároku na cokoliv.__

