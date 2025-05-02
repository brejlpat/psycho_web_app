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
Máme tři varianty jak kontrolovat přijaté platby:  
1. Manuálně - po příchozí platbě by "admin" přepnul v databázi stav objednávky na "uhrazeno"  
2. Poloautomaticky (Česká spořitelna, mBank) - stáhnout denní výpis v ABO formátu, nahrát do aplikace -> appka potom zkontroluje podle VS jestli platba už přišla nebo ne  
3. Automaticky (Fio, AirBank, Raiffeisen, ČSOB) - přes bankovní API    
