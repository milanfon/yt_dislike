# Stahování disliků z YouTube - milafon

Tento skript slouží jako možnost zobrazit divákům počet disliků u YouTube videí. Vyžaduje implementaci ze strany tvůrce. Tato dokumentace popisuje detailně veškeré náležitosti potřebné k jeho spuštění. 

## Spuštění programu

Pro získání spustitelného programu naklonujte nebo stáhněte **kořenovou** složku tohoto projektu. Hlavní program se nalézá v souboru `dislike.py`. 

Základními požadavky pro jeho spuštění jsou:
- Instalace Python 3
- Knihovny `requests`, `json`, `sqlite3` a `urllib`

_Další požadavky_ pro spuštění jsou sepsány dále.

### Prerekvizity

#### Získání klíčů - Google Cloud

V první řadě si musíme na platformě [Google Cloud](https://console.cloud.google.com/) obstarat následující klíče, které jsou potřeba pro chod programu. 
- API klíč pro YouTube API
- Veřejný klíč klienta
- Privátní klíč klienta

##### Založení projektu

Před tím než můžeme získat klíče k API, musíme si na platformě Google Cloud vytvořit **nový projekt**. To provedeme _klinutím_ na _seznam projektů_ vedle loga platformy. 

![Seznam projektů](/dokumentace/pic/projects.png)

Následovně v dialogovém okně můžeme vytvořit nový projekt kliknutím na tlačítko "nový projekt". 

![Vyskakovací okno projektů](/dokumentace/pic/cloud_console_projekty.png)

To nás přivede na stránku, ve které můžeme zadat jeho název a klinout na tlačítko "vytvořit".

![Vytvoření nového projektu](/dokumentace/pic/new_project.png)

##### Přidání YouTube API do projektu

Pro tento krok nalezneme ve vyhledávání na platformě _Google Cloud_ položku `YouTube Data API v3`. U té poté klikneme na tlačítko _enable_ pro přidání tohoto API do našeho projektu. 

![Přidání API do projektu](/dokumentace/pic/cloud_console_api_add.png)

##### Klíče

V navigaci _Google Cloud_ se dostaneme do sekce _Credentials_, ve které se nalázejí právě klíče. 

![Navigace Google Cloud](/dokumentace/pic/cloud_console_api_nav.png)

Tam máme na vrchu stránky možnost přidat jak nový _API klíč_ tak _OAuth client ID_, z čehož obojí budeme potřebovat. Pro vytvoření API klíče stačí pouze kliknutí a zobrazí se nám nový _API klíč_.

![API klíč](/dokumentace/pic/api_key.png)

Vytvoření _OAuth client ID_ pro autorizaci však již vyžaduje určitou interakci. V první řadě musíme zvolit druh aplikace. Zde doporučuji kategorii _Desktop app_. 

![Vytvoření klíče klienta](/dokumentace/pic/create_oauth.png)

Poté stačí jen dát tomuto klíči název a klinout na tlačítko _vytvořit_. Poté se nám zobrazí okno, ve kterém nalzeneme jak **Veřejný klíč klienta - Client ID**, tak **privátní klíč klienta - Client Secret**. Obě hodnoty si zkopírujte, protože je budeme potřebovat později.

![Client ID](/dokumentace/pic/oauth_credentials.png)

##### Přidání testovacího uživatele

Protože pracujeme s **API YouTube**, musíme náš účet spojený s **YouTube kanálem**, ke kterému chceme přistupovat, přidat mezi _testovací uživatele_ projektu. Do této sekce se opět dostaneme pomocí postraní navigace v rámci _Google Cloud_ kliknutím na položku _OAuth consent screen_. Zde pod kategorií _Test users_ kliknutím na tlačítko _Add users_ přidáme zvolený účet.

![Přidání testovacího uživatele](/dokumentace/pic/test_users.png)

### Konfigurace aplikace

Po splnění všech prerekvizit můžeme do hlavního souboru programu `dislike.py` vložit získané klíče k patřičným konstantám. 

```python
API_KEY = "AIzaHJiT856h0qfR54..."
CLIENT_ID = "8345674-nmrtkdj..."
CLIENT_SECRET = "HKPFDR-dsgr..."
```

### Přidání sledovaných videí

