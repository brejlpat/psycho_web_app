# Psycho webová aplikace
## Architektura webu
## Databáze
K uchovávání uživatelů (account management), seznam kurzů, videa jednotlivých kurzů, objednávky, počet zařízení pro jednotlivé
uživatele  
## PHP backend
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
Tato logika bude implementována v rámci Auth middleware (auth.php). Při generování tokenu je možné použít náhodný GUID (??) nebo kombinovat informace
 (user agent, rozlišení apod.). Je důležité, aby odstranění cookies nebo změna prohlížeče bylo vyhodnoceno jako nové zařízení.  
### Správa kurzů a obsahu
