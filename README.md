# Psycho webová aplikace
## Architektura webu
## Databáze
K uchovávání uživatelů (account management), seznam kurzů, videa jednotlivých kurzů, objednávky, počet zařízení pro jednotlivé
uživatele  

## PHP backend
- [ ] Laravel - zjistit jestli bude fungovat na Forpsi nebo na jakém hostingu to půjde  

### Správa uživatelů
- propojení s tabulkou "uživatelé" v SQL  
- PHP má funkce pro hashování hesel  
- algorytmus BCRYPT pomocí password_hash()  
- po přihlášení server generuje uživatelskou session (JWT token, nebo PHP session)  

### Kontrola zařízení uživatele
Z důvodu zamezení přihlašování z tisíce zařízení  
- aplikace zjistí identifikátor zařízení -> cookie s uloženým tokenem (po předešlém přihlášení), při registraci se vytvoří nový token)  
- pokud token neextistuje a uživatel má v SQL méně než 3 zařízení -> uloží se do SQL do tabulky "zařízení" a nastaví se jako cookie v prohlížeči  
	- generování tokenu pomocí PHP funkce bin2hex(random_bytes(16)) pro random 128 bitový token
- pokud token neexistuje, ale v SQL má uživatel více jak 3 zařízení -> aplikace přihlášení odmítne    

Tato logika bude implementována v rámci Auth middleware (auth.php). Při generování tokenu je možné použít náhodný GUID (Globally unique identiffier) nebo kombinovat informace
 (user agent, rozlišení apod.). Je důležité, aby odstranění cookies nebo změna prohlížeče bylo vyhodnoceno jako nové zařízení.  

### Správa kurzů a obsahu
- bude potřeba neustále kontrolovat přístup a oprávnění uživatelů  
- k servírování souborů po ověření přístup je možné použít Apache modul XSendFile  
- je také varianta videa nahrát na YouTube, nastavit je jako privátní a videa otevírat přes odkaz (ulehčení serveru)  
- kontroly lze také kontrolovat pomocí middleware nebo gate/policy (např. **Laravel**)  

### Správa nákupů (objednávky a platby)
- jakmile uživatel vybere kurz a klikne na objednat, zavolá se funkce, která vytvoří novou Objednávku, zapíše do SQL a zobrazí se údaje k platbě + se pošlou na email  
- [ ] Jde generovat QR kód k platbě i v php? Pokud ano, bude i QR  
- objednávka je nyní ve stavu "neuhrazeno" dokud uživatel platbu přes bankovní převod neuhradí  
- po uhrazení se změní stav objednávky v SQL na "uhrazeno" a uživatel dostane přístup ke kurzu (také přes SQL)  
- uživateli přijde na email potvrzení o uhrazení, shrnutí objednávky a ještě bychom udělali PDF fakturu  
- [ ] Jak udělat PDF fakturu?    
Máme tři varianty jak kontrolovat přijaté platby:  
1. Manuálně - po příchozí platbě by "admin" přepnul v databázi stav objednávky na "uhrazeno"  
2. Poloautomaticky (Česká spořitelna, mBank) - stáhnout denní výpis v ABO formátu, nahrát do aplikace -> appka potom zkontroluje podle VS jestli platba už přišla nebo ne  
3. Automaticky (Fio, AirBank, Raiffeisen, ČSOB) - přes bankovní API    

### Správa zařízení a omezení přístupu
- uložení identifikátorů (ID/token) a jejich kontrolu při každém přihlášení nebo přístupu ke kurzu  
- je možné také hlídat počet aktuálních session, aby nebylo možné mít více uživatelů přihlášených najednou  
- [ ] Doporučuje se implementovat stránku, kde uživatel uvidí všechna svá přihlášená zařízení -> zase ale aby toho nezneužívali...  
- buď by si teda správu dělali uživatelé sami (mazat zařízení, vidět je), nebo by je mohli jenom vidět a kdyby potřebovali nějaké zařízení smazat, kontaktovali by admina    

## Frontend struktura
Implementováno klasicky pomocí HTML, CSS, JavaScriptu.  
Struktura webu:  
- **Domovská stránka**  
	- uvítání + obecné informace o čem projekt je  
	- výpis všech kurzů -> úvodní fotka, název, popis, cena, možnost dát do košíku/rovnou koupit  
- **Detail kurzu**  
	- název + podrobný popis kurzu  
	- sylabus kurzu, seznam všech lekcí  
	- cena + tlačítko pro zakoupení  
	- pokud uživatel má kurz zakoupen, objeví se tlačítko vstoupit do kurzu  
- **Vstoupení do kurzu**  
	- budeme mít nějakou konkrétní posloupnost videí - tlačítko na přehrát poslední/kde jsme skončili/pokračovat v kurzu  
	- seznam všech videí (kdyby uživatel chtěl něco přeskočit nebo se podívat na něco jiného)  
	- u každého videa bude název, možná krátký popis, úvodní fotka/grafika, délka videa  
	- pokud bude video na serveru, tak se přehraje normálně přes <video> + odkaz by měl obsahovat svoji chráněnou url (video/stream/{video_id})  
- **Uživatelský profil**  
	- zde uživatel uvidí své údaje + zakoupené kurzy  
	- možná i ta tabulka registrovaných zařízení  
- **Admin sekce**  
	- kdybychom chtěli nějakou admin sekci pro přehlednou správu uživatelů    

### Frontend technologie
- AJAX požadavky pro některé akce - nereloadne se celá stránka, ale pouze část (lepší optimalizace paměti a výkonu)  
- pro lepší přehrávač videí můžeme integrovat JS knihovnu Video.js pro jednotný vzhled napříč prohlížeči + podporu adaptivního streamování (HLS - HTTP Live Streaming)    

## Bezpečnost
- HTTPS stoprocentně  
- bezpečné ukládání hesel - hashování pomocí password_hash()  
	- při ověřování hesla použít funkci password_verify()  
- ochrana proti nabourání SQL natabáze - nepsat raw SQL dotazy  
- omezit pokusy pro přihlášení (např. 5) - potom vyžadovat vyplnění CAPTCHA (Completely automated public turing test to tell computers and humans apart)  
- ošetření vstupů a XSS - před vkládáním školivých JS kódů od hackerů  
- bezpečnost před možností stažení videa  
- logování veškeré aktivity na stránce do SQL (přihlášení, registrace, zásahy admina, vytvoření objednávky apod.) -> user_id, date_time  
- pravidelně zálohovat SQL  
- zajistit uživatelské oprávnění, neustále kontrolovat + dbát na to, aby nešly parametry měnit v url  
  
**PŘED SPUŠTĚNÍM APLIKACE OTESTOVAT VEŠKEROU BEZPEČNOST**